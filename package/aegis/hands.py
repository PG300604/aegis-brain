"""Aegis Hands Engine - Web Application & UI Automation/Inspection.

Provides AI agents the physical ability to touch, inspect, click, and verify
web applications, dashboards, and local developer servers (http://localhost:...).

Supported capabilities:
- Playwright Headless Automation: full DOM access, console error inspection, screenshots.
- Graceful Zero-Dependency Fallback: pure standard library HTTP + HTMLParser ('lightweight_dom')
  when Playwright is not installed.
- UI Journeys: sequence execution (click, fill, wait, navigate, scroll).
- Markdown Report Formatter: structured page health, interactive elements audit, and console errors.
"""

from __future__ import annotations

import html
import logging
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AegisBrainHands/1.0"
SCREENSHOT_DIR = Path(".aegis/screenshots")


@dataclass
class HandsInspectionResult:
    """Inspection outcome of a target web application or URL."""

    url: str
    status_code: int
    title: str
    interactive_elements: List[Dict[str, Any]] = field(default_factory=list)
    console_errors: List[str] = field(default_factory=list)
    screenshot_path: Optional[str] = None
    is_live: bool = False
    driver_used: str = "lightweight_dom"
    latency_ms: float = 0.0

    @property
    def elements(self) -> List[Dict[str, Any]]:
        """Convenience alias for interactive_elements."""
        return self.interactive_elements

    @property
    def driver(self) -> str:
        """Convenience alias for driver_used."""
        return self.driver_used

    @property
    def success(self) -> bool:
        """Convenience alias for is_live."""
        return self.is_live

    def to_dict(self) -> Dict[str, Any]:
        """Serialize inspection result to dictionary."""
        data = asdict(self)
        # Ensure convenience aliases are also in serialized dict for downstream AI agents
        data["elements"] = self.interactive_elements
        data["driver"] = self.driver_used
        data["success"] = self.is_live
        return data


class LightweightDOMParser(HTMLParser):
    """Zero-dependency HTML parser for extracting interactive elements from raw HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.elements: List[Dict[str, Any]] = []
        self._current_elem: Optional[Dict[str, Any]] = None
        self._in_title: bool = False
        self.title: str = ""
        self._text_buffer: str = ""

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        attrs_dict = {k: (v if v is not None else "") for k, v in attrs}
        tag_lower = tag.lower()

        if tag_lower == "title":
            self._in_title = True
            self.title = ""
            return

        if tag_lower not in ("button", "a", "input", "select", "textarea"):
            return

        selector = self._synthesize_selector(tag_lower, attrs_dict)
        elem_type = "link" if tag_lower == "a" else tag_lower

        element: Dict[str, Any] = {
            "type": elem_type,
            "tag": tag_lower,
            "selector": selector,
            "attributes": attrs_dict,
            "text": attrs_dict.get("placeholder") or attrs_dict.get("value") or "",
        }

        if tag_lower in ("button", "a", "textarea", "select"):
            self._current_elem = element
            self._text_buffer = ""

        self.elements.append(element)

    def handle_endtag(self, tag: str) -> None:
        tag_lower = tag.lower()

        if tag_lower == "title":
            self._in_title = False
            return

        if self._current_elem and tag_lower in ("button", "a", "textarea", "select"):
            extracted_text = html.unescape(self._text_buffer.strip())
            if extracted_text:
                self._current_elem["text"] = extracted_text
            self._current_elem = None
            self._text_buffer = ""

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        elif self._current_elem:
            self._text_buffer += data

    def _synthesize_selector(self, tag: str, attrs: Dict[str, str]) -> str:
        """Synthesize a robust, clean CSS selector for an element."""
        if "id" in attrs and attrs["id"].strip():
            return f"#{attrs['id'].strip()}"
        elif "name" in attrs and attrs["name"].strip():
            return f"{tag}[name='{attrs['name'].strip()}']"
        elif "class" in attrs and attrs["class"].strip():
            classes = attrs["class"].strip().split()
            if classes:
                return f"{tag}." + ".".join(classes)
        elif tag == "a" and "href" in attrs and attrs["href"].strip():
            return f"a[href='{attrs['href'].strip()}']"
        return tag

    def get_elements(self) -> List[Dict[str, Any]]:
        return self.elements

    def get_title(self) -> str:
        return self.title.strip()


def inspect_web_target(
    url: str,
    capture_screenshot: bool = True,
    timeout_sec: float = 5.0,
) -> HandsInspectionResult:
    """Inspect a web target URL, capturing live status, DOM elements, and errors.

    Attempts full browser inspection via Playwright if available, or seamlessly
    falls back to standard-library HTTP + HTMLParser.
    """
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    start_time = time.perf_counter()

    try:
        from playwright.sync_api import sync_playwright  # type: ignore

        return _inspect_with_playwright(url, capture_screenshot, timeout_sec, start_time)
    except (ImportError, Exception):
        return _inspect_with_lightweight_dom(url, timeout_sec, start_time)


def _inspect_with_playwright(
    url: str,
    capture_screenshot: bool,
    timeout_sec: float,
    start_time: float,
) -> HandsInspectionResult:
    """Perform browser-level inspection via Playwright."""
    from playwright.sync_api import sync_playwright  # type: ignore

    console_errors: List[str] = []
    screenshot_path: Optional[str] = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            def handle_console(msg: Any) -> None:
                if msg.type == "error":
                    console_errors.append(msg.text)

            page.on("console", handle_console)
            page.on("pageerror", lambda err: console_errors.append(str(err)))

            response = page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=int(timeout_sec * 1000),
            )
            status_code = response.status if response else 200
            title = page.title() or ""

            elements = page.evaluate(
                """() => {
                    const nodes = document.querySelectorAll('button, a[href], input, select, textarea');
                    const results = [];
                    for (const node of nodes) {
                        const tag = node.tagName.toLowerCase();
                        let type = tag;
                        if (tag === 'a') type = 'link';

                        let selector = tag;
                        if (node.id) {
                            selector = '#' + node.id;
                        } else if (node.name) {
                            selector = tag + '[name="' + node.name + '"]';
                        } else if (node.className && typeof node.className === 'string') {
                            const cls = node.className.trim().split(/\\s+/);
                            if (cls.length > 0 && cls[0]) {
                                selector = tag + '.' + cls.join('.');
                            }
                        } else if (tag === 'a' && node.getAttribute('href')) {
                            selector = 'a[href="' + node.getAttribute('href') + '"]';
                        }

                        const attrs = {};
                        for (const a of node.attributes) {
                            attrs[a.name] = a.value;
                        }

                        const text = (node.innerText || node.value || node.placeholder || '').trim();

                        results.push({
                            type: type,
                            tag: tag,
                            selector: selector,
                            attributes: attrs,
                            text: text.slice(0, 100)
                        });
                    }
                    return results.slice(0, 100);
                }"""
            )

            if capture_screenshot:
                SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
                sanitized_url = re.sub(r"[^a-zA-Z0-9_-]", "_", url)
                filename = f"hands_{int(time.time())}_{sanitized_url[:40]}.png"
                target_path = SCREENSHOT_DIR / filename
                page.screenshot(path=str(target_path))
                screenshot_path = str(target_path)

            browser.close()

        latency_ms = (time.perf_counter() - start_time) * 1000
        is_live = 200 <= status_code < 400

        return HandsInspectionResult(
            url=url,
            status_code=status_code,
            title=title,
            interactive_elements=elements,
            console_errors=console_errors,
            screenshot_path=screenshot_path,
            is_live=is_live,
            driver_used="playwright",
            latency_ms=latency_ms,
        )

    except Exception as e:
        logger.warning("Playwright inspection encountered error for %s: %s; falling back to lightweight DOM", url, e)
        return _inspect_with_lightweight_dom(url, timeout_sec, start_time)


def _inspect_with_lightweight_dom(
    url: str,
    timeout_sec: float,
    start_time: float,
) -> HandsInspectionResult:
    """Perform lightweight HTTP + HTMLParser inspection using pure standard library."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            status_code = resp.getcode()
            raw_bytes = resp.read(512 * 1024)  # Read up to 512KB
            charset = "utf-8"
            content_type = resp.headers.get("Content-Type", "")
            if "charset=" in content_type:
                charset = content_type.split("charset=")[-1].split(";")[0].strip()

            try:
                body = raw_bytes.decode(charset, errors="replace")
            except Exception:
                body = raw_bytes.decode("utf-8", errors="replace")

            parser = LightweightDOMParser()
            parser.feed(body)

            latency_ms = (time.perf_counter() - start_time) * 1000
            is_live = 200 <= status_code < 400

            return HandsInspectionResult(
                url=url,
                status_code=status_code,
                title=parser.get_title() or url,
                interactive_elements=parser.get_elements(),
                console_errors=[],
                screenshot_path=None,
                is_live=is_live,
                driver_used="lightweight_dom",
                latency_ms=latency_ms,
            )

    except urllib.error.HTTPError as e:
        latency_ms = (time.perf_counter() - start_time) * 1000
        elements: List[Dict[str, Any]] = []
        title = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
            parser = LightweightDOMParser()
            parser.feed(body)
            elements = parser.get_elements()
            title = parser.get_title()
        except Exception:
            pass

        return HandsInspectionResult(
            url=url,
            status_code=e.code,
            title=title or f"HTTP Error {e.code}",
            interactive_elements=elements,
            console_errors=[f"HTTP Error {e.code}: {e.reason}"],
            screenshot_path=None,
            is_live=(e.code < 500),
            driver_used="lightweight_dom",
            latency_ms=latency_ms,
        )

    except urllib.error.URLError as e:
        latency_ms = (time.perf_counter() - start_time) * 1000
        return HandsInspectionResult(
            url=url,
            status_code=0,
            title="",
            interactive_elements=[],
            console_errors=[f"URL Error: {e.reason}"],
            screenshot_path=None,
            is_live=False,
            driver_used="lightweight_dom",
            latency_ms=latency_ms,
        )

    except TimeoutError:
        latency_ms = (time.perf_counter() - start_time) * 1000
        return HandsInspectionResult(
            url=url,
            status_code=0,
            title="",
            interactive_elements=[],
            console_errors=[f"Connection timeout after {timeout_sec}s"],
            screenshot_path=None,
            is_live=False,
            driver_used="lightweight_dom",
            latency_ms=latency_ms,
        )

    except Exception as e:
        latency_ms = (time.perf_counter() - start_time) * 1000
        return HandsInspectionResult(
            url=url,
            status_code=0,
            title="",
            interactive_elements=[],
            console_errors=[str(e)],
            screenshot_path=None,
            is_live=False,
            driver_used="lightweight_dom",
            latency_ms=latency_ms,
        )


def execute_ui_journey(
    url: str,
    actions: List[Dict[str, Any]],
    timeout_sec: float = 10.0,
) -> Dict[str, Any]:
    """Execute a multi-step user journey against a web target.

    Supported action primitives:
    - {"action": "click", "selector": "#submit-btn"}
    - {"action": "fill", "selector": "input[name='q']", "text": "AegisBrain"}
    - {"action": "wait", "sec": 1.5}
    - {"action": "navigate", "url": "https://..."}
    - {"action": "scroll", "selector": "#footer"}

    Requires Playwright for true interaction; returns unsupported warning if unavailable.
    """
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except (ImportError, Exception):
        return {
            "status": "unsupported",
            "passed_steps": 0,
            "total_steps": len(actions),
            "driver": "lightweight_dom",
            "errors": [
                "Playwright is required for interactive UI journeys. "
                "Install via `pip install playwright && playwright install chromium`."
            ],
            "screenshot_path": None,
        }

    start_time = time.perf_counter()
    passed_steps = 0
    errors: List[str] = []
    screenshot_path: Optional[str] = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=int(timeout_sec * 1000))

            for i, step in enumerate(actions):
                action = step.get("action", "").lower()
                step_timeout = int(step.get("timeout_sec", 5.0) * 1000)

                try:
                    if action == "click":
                        selector = step.get("selector")
                        if not selector:
                            raise ValueError("Action 'click' requires 'selector'")
                        page.click(selector, timeout=step_timeout)

                    elif action in ("fill", "type"):
                        selector = step.get("selector")
                        text = step.get("text") or step.get("value") or ""
                        if not selector:
                            raise ValueError("Action 'fill' requires 'selector'")
                        page.fill(selector, str(text), timeout=step_timeout)

                    elif action == "wait":
                        wait_sec = float(step.get("sec") or step.get("seconds") or 1.0)
                        page.wait_for_timeout(int(wait_sec * 1000))

                    elif action == "navigate":
                        target_url = step.get("url")
                        if not target_url:
                            raise ValueError("Action 'navigate' requires 'url'")
                        page.goto(target_url, wait_until="domcontentloaded", timeout=int(timeout_sec * 1000))

                    elif action == "scroll":
                        selector = step.get("selector")
                        if selector:
                            page.locator(selector).scroll_into_view_if_needed()
                        else:
                            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

                    else:
                        raise ValueError(f"Unknown action type: {action}")

                    passed_steps += 1

                except Exception as e:
                    errors.append(f"Step {i+1} ({action}): {e}")
                    break

            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            screenshot_file = SCREENSHOT_DIR / f"journey_{int(time.time())}.png"
            page.screenshot(path=str(screenshot_file))
            screenshot_path = str(screenshot_file)

            browser.close()

        total_ms = (time.perf_counter() - start_time) * 1000
        return {
            "status": "success" if not errors else "failed",
            "passed_steps": passed_steps,
            "total_steps": len(actions),
            "driver": "playwright",
            "errors": errors,
            "screenshot_path": screenshot_path,
            "latency_ms": total_ms,
        }

    except Exception as e:
        return {
            "status": "failed",
            "passed_steps": passed_steps,
            "total_steps": len(actions),
            "driver": "playwright",
            "errors": errors + [str(e)],
            "screenshot_path": None,
            "latency_ms": (time.perf_counter() - start_time) * 1000,
        }


def format_hands_report(result: HandsInspectionResult) -> str:
    """Format a HandsInspectionResult into a clean markdown document."""
    status_icon = "🟢" if result.is_live else "🔴"
    driver_icon = "🎭" if result.driver_used == "playwright" else "📦"

    lines: List[str] = [
        "# 🖐️ Aegis Hands: UI Inspection Report",
        "",
        "## 🎯 Target Health",
        f"- **URL:** `{result.url}`",
        f"- **Status Code:** `{result.status_code}`",
        f"- **Live Status:** {status_icon} {'Live & Reachable' if result.is_live else 'Unreachable / Error'}",
        f"- **Latency:** `{result.latency_ms:.1f} ms`",
        f"- **Driver:** {driver_icon} `{result.driver_used}`",
    ]

    if result.screenshot_path:
        lines.append(f"- **Screenshot:** `{result.screenshot_path}`")

    lines.extend([
        "",
        f"## 📄 Page Title",
        f"> {result.title or '(No title extracted)'}",
        "",
        "## 🔘 Interactive Elements Summary",
    ])

    # Element counts by type
    counts: Dict[str, int] = {}
    for el in result.interactive_elements:
        t = el.get("type", "other")
        counts[t] = counts.get(t, 0) + 1

    lines.append(f"- **Total Interactive Elements Found:** `{len(result.interactive_elements)}`")
    for t, c in sorted(counts.items()):
        lines.append(f"  - `{t}`: {c}")

    if result.interactive_elements:
        lines.extend([
            "",
            "### 📋 Elements Overview",
            "| Type | Selector | Text / Label | Attributes |",
            "| :--- | :--- | :--- | :--- |",
        ])
        for el in result.interactive_elements[:25]:
            el_type = el.get("type", "")
            selector = el.get("selector", "")
            raw_text = el.get("text", "") or ""
            clean_text = raw_text.replace("\n", " ")[:40]
            attrs = el.get("attributes", {})
            attr_summary = ", ".join(f"{k}={v}" for k, v in list(attrs.items())[:3] if v)
            lines.append(f"| `{el_type}` | `{selector}` | {clean_text} | {attr_summary} |")

        if len(result.interactive_elements) > 25:
            remaining = len(result.interactive_elements) - 25
            lines.append(f"| *...* | *...* | *({remaining} more elements omitted)* | *...* |")

    lines.extend([
        "",
        "## ⚠️ Console & Network Audit",
    ])

    if result.console_errors:
        lines.append(f"🔴 **{len(result.console_errors)} Error(s) Detected:**")
        for err in result.console_errors:
            lines.append(f"- `{err}`")
    else:
        lines.append("🟢 **Clean:** 0 console or network errors detected.")

    lines.append("")
    return "\n".join(lines)
