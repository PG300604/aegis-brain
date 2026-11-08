# Chapter 07: Hands Engine & UI Testing

This chapter describes the **Hands Engine** (`aegis.hands`) — AegisBrain's native headless web inspection, DOM extraction, browser console error trapping, and screenshot pipeline.

---

## 1. The Physical Hands Paradigm

A persistent limitation of AI coding agents is premature feature declaration: an agent finishes editing a React, Vue, or Svelte component and declares the task complete, unaware that the local development server failed to compile or the browser threw an unhandled React error boundary.

The **Hands Engine** equips agents with verifiable physical eyes and hands:
- **Validates Dev Servers**: Confirms that `http://localhost:<port>` is responding with HTTP 200.
- **Audits DOM Elements**: Extracts all interactive elements (buttons, inputs, links, forms) to verify they rendered.
- **Traps Browser Console Errors**: Detects runtime JavaScript errors, syntax exceptions, and broken network assets.
- **Captures Visual Proof**: Captures full-page screenshots to document UI state.

---

## 2. Architecture & Execution Modes

```
                       [ aegis hands <target_url> ]
                                    │
                                    ▼
                     Is Playwright Available?
                       /                 \
                     YES                  NO
                     /                     \
       ┌────────────────────────┐    ┌─────────────────────────────────┐
       │ Headless Chromium Mode │    │ Pure Standard Library Fallback  │
       │ - Playwright Runner    │    │ - LightweightDOMParser          │
       │ - Full JS Execution    │    │ - urllib.request + html.parser  │
       │ - Console Error Trap   │    │ - Static HTML element extract   │
       │ - Full Screenshot Capture│  │ - Zero dependencies required   │
       └────────────────────────┘    └─────────────────────────────────┘
```

---

## 3. Playwright Headless Inspection Mode

When Playwright is installed in the environment (`pip install playwright && playwright install chromium`), AegisBrain launches an automated headless browser session:

### 3.1 Console Error Trapping
The runner attaches event listeners to the browser page context:
```python
# Event trapping in aegis.hands
page.on("console", lambda msg: error_log.append(msg.text) if msg.type == "error" else None)
page.on("pageerror", lambda exc: exception_log.append(str(exc)))
```
Any uncaught exceptions, React hydration mismatches, or failed asset requests (`net::ERR_CONNECTION_REFUSED`) are captured into the inspection telemetry.

### 3.2 Visual Screenshot Capture
Screenshots are captured at high resolution and saved into `~/.aegis-brain/screenshots/`:
- Path format: `~/.aegis-brain/screenshots/screen_<timestamp>.png`
- File paths are returned in the JSON payload, allowing agents to embed them into visual audit artifacts.

---

## 4. Zero-Dependency Fallback (`LightweightDOMParser`)

If Playwright or browser binaries are not present on the workstation, AegisBrain executes an automatic fallback to `LightweightDOMParser` using Python's native `html.parser.HTMLParser` and `urllib.request`.

The parser extracts:
- Document `<title>`
- Headings (`<h1>` through `<h6>`)
- Forms, actions, and form methods
- Input elements (`type`, `name`, `id`, `placeholder`)
- Interactive buttons and links (`href`, text content)

This guarantees that web inspection never crashes or fails even in stripped-down CI environments or air-gapped workstations.

---

## 5. CI/CD Quality Gate Assertion (`--assert-clean`)

For automated pipelines, `aegis hands` provides the `--assert-clean` assertion flag:

```bash
aegis hands http://localhost:3000 --assert-clean
```

### 5.1 Exit Code Specification
- **Exit 0**: Server responded with HTTP 200, DOM parsed cleanly, and 0 console errors were detected.
- **Exit 1**: Target server unreachable, returned HTTP $\ge 400$, or unhandled browser console errors occurred.

This enables immediate inclusion into continuous integration workflows to catch broken frontends before merging PRs.

---

## 6. CLI Usage & Examples

```bash
# Basic inspection of local dev server
aegis hands http://localhost:5173

# Inspect and take a full-page screenshot
aegis hands http://localhost:3000 --screenshot

# CI/CD Quality Gate: fail build on any console error or HTTP failure
aegis hands http://localhost:3000 --assert-clean

# Output structured telemetry JSON for agent parsing
aegis hands http://localhost:8080 --json
```
