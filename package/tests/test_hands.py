"""Unit tests for Aegis Hands Engine (Web Application Inspection & UI Automation)."""

from io import BytesIO
from unittest.mock import MagicMock, patch
import urllib.error

from aegis.hands import (
    HandsInspectionResult,
    LightweightDOMParser,
    execute_ui_journey,
    format_hands_report,
    inspect_web_target,
)


def test_lightweight_dom_parser_extraction():
    """Verify standard-library LightweightDOMParser correctly extracts DOM elements and title."""
    html_content = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>AegisBrain Mission Control</title>
      </head>
      <body>
        <header>
          <a href="/dashboard" id="logo-link">Dashboard</a>
          <a href="/settings" class="nav-item active">Settings</a>
        </header>
        <main>
          <h1>System Overview</h1>
          <form action="/deploy" method="POST">
            <input type="text" name="service_name" placeholder="Service Name" value="auth-api" />
            <select name="tier">
              <option value="t1">Tier 1 Frontier</option>
              <option value="t3">Tier 3 MoE</option>
            </select>
            <textarea name="description">Initial cluster deploy</textarea>
            <button id="deploy-btn" class="btn primary-action">Deploy Target</button>
          </form>
        </main>
      </body>
    </html>
    """
    parser = LightweightDOMParser()
    parser.feed(html_content)

    assert parser.get_title() == "AegisBrain Mission Control"
    elements = parser.get_elements()

    assert len(elements) == 6

    # Verify link with id
    link1 = elements[0]
    assert link1["type"] == "link"
    assert link1["selector"] == "#logo-link"
    assert link1["text"] == "Dashboard"

    # Verify link with class
    link2 = elements[1]
    assert link2["type"] == "link"
    assert link2["selector"] == "a.nav-item.active"
    assert link2["text"] == "Settings"

    # Verify input with name
    input_elem = elements[2]
    assert input_elem["type"] == "input"
    assert input_elem["selector"] == "input[name='service_name']"
    assert input_elem["attributes"]["value"] == "auth-api"

    # Verify select
    select_elem = elements[3]
    assert select_elem["type"] == "select"
    assert select_elem["selector"] == "select[name='tier']"

    # Verify textarea
    textarea_elem = elements[4]
    assert textarea_elem["type"] == "textarea"
    assert textarea_elem["selector"] == "textarea[name='description']"
    assert textarea_elem["text"] == "Initial cluster deploy"

    # Verify button with ID
    button_elem = elements[5]
    assert button_elem["type"] == "button"
    assert button_elem["selector"] == "#deploy-btn"
    assert button_elem["text"] == "Deploy Target"


def test_hands_inspection_result_serialization():
    """Verify HandsInspectionResult serialization and property aliases."""
    result = HandsInspectionResult(
        url="http://localhost:3000",
        status_code=200,
        title="Local Dev App",
        interactive_elements=[
            {"type": "button", "selector": "#btn-test", "text": "Run", "attributes": {"id": "btn-test"}}
        ],
        console_errors=[],
        screenshot_path=None,
        is_live=True,
        driver_used="lightweight_dom",
        latency_ms=12.5,
    )

    # Check property aliases
    assert result.elements == result.interactive_elements
    assert result.driver == "lightweight_dom"
    assert result.success is True

    # Check serialization
    d = result.to_dict()
    assert d["url"] == "http://localhost:3000"
    assert d["status_code"] == 200
    assert d["title"] == "Local Dev App"
    assert d["is_live"] is True
    assert d["driver_used"] == "lightweight_dom"
    assert len(d["interactive_elements"]) == 1
    assert d["elements"] == d["interactive_elements"]


def test_format_hands_report():
    """Verify clean Markdown formatting of inspection reports."""
    # Test clean report
    result = HandsInspectionResult(
        url="http://localhost:8080",
        status_code=200,
        title="Production Dashboard",
        interactive_elements=[
            {"type": "button", "selector": "#save", "text": "Save Changes", "attributes": {"id": "save"}},
            {"type": "link", "selector": "a[href='/logout']", "text": "Sign Out", "attributes": {"href": "/logout"}},
        ],
        console_errors=[],
        screenshot_path=".aegis/screenshots/hands_mock.png",
        is_live=True,
        driver_used="playwright",
        latency_ms=45.2,
    )

    report = format_hands_report(result)
    assert "# 🖐️ Aegis Hands: UI Inspection Report" in report
    assert "Production Dashboard" in report
    assert "Live & Reachable" in report
    assert "45.2 ms" in report
    assert "playwright" in report
    assert ".aegis/screenshots/hands_mock.png" in report
    assert "**Total Interactive Elements Found:** `2`" in report
    assert "Save Changes" in report
    assert "Sign Out" in report
    assert "0 console or network errors detected" in report

    # Test report with console errors
    error_result = HandsInspectionResult(
        url="http://localhost:8080/broken",
        status_code=500,
        title="Error 500",
        interactive_elements=[],
        console_errors=["Uncaught TypeError: Cannot read property 'map' of undefined", "Failed to load resource: 500"],
        screenshot_path=None,
        is_live=False,
        driver_used="lightweight_dom",
        latency_ms=8.1,
    )
    error_report = format_hands_report(error_result)
    assert "Unreachable / Error" in error_report
    assert "2 Error(s) Detected" in error_report
    assert "Uncaught TypeError" in error_report


def test_inspect_web_target_unreachable_url():
    """Verify error resilience when inspecting an unreachable target."""
    result = inspect_web_target("http://127.0.0.1:59123/unreachable", timeout_sec=0.5)
    assert result.is_live is False
    assert result.status_code == 0
    assert result.driver_used == "lightweight_dom"
    assert len(result.console_errors) > 0


def test_inspect_web_target_mock_http():
    """Verify inspect_web_target works seamlessly with mocked HTTP response."""
    mock_html = b"""
    <html>
      <head><title>Mocked Server</title></head>
      <body>
        <button id="ok-btn">OK</button>
      </body>
    </html>
    """
    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = mock_html
    mock_response.headers.get.return_value = "text/html; charset=utf-8"
    mock_response.__enter__.return_value = mock_response
    mock_response.__exit__.return_value = False

    with patch("urllib.request.urlopen", return_value=mock_response):
        result = inspect_web_target("http://example.local", capture_screenshot=False)
        assert result.is_live is True
        assert result.status_code == 200
        assert result.title == "Mocked Server"
        assert result.driver_used == "lightweight_dom"
        assert len(result.interactive_elements) == 1
        assert result.interactive_elements[0]["selector"] == "#ok-btn"
        assert result.interactive_elements[0]["text"] == "OK"


def test_inspect_web_target_mock_http_error():
    """Verify inspect_web_target handles HTTP errors gracefully."""
    err_body = b"<html><head><title>404 Not Found</title></head><body><h1>Not Found</h1></body></html>"
    http_error = urllib.error.HTTPError(
        url="http://example.local/not-found",
        code=404,
        msg="Not Found",
        hdrs={},
        fp=BytesIO(err_body),
    )

    with patch("urllib.request.urlopen", side_effect=http_error):
        result = inspect_web_target("http://example.local/not-found")
        assert result.status_code == 404
        assert result.is_live is True  # 404 is still a reachable server response
        assert "HTTP Error 404" in result.console_errors[0]
        assert result.title == "404 Not Found"


def test_execute_ui_journey_unsupported_when_no_playwright():
    """Verify execute_ui_journey returns graceful status when Playwright is absent."""
    with patch.dict("sys.modules", {"playwright": None, "playwright.sync_api": None}):
        actions = [
            {"action": "navigate", "url": "http://localhost:3000"},
            {"action": "click", "selector": "#login-btn"},
            {"action": "fill", "selector": "#username", "text": "admin"},
            {"action": "wait", "sec": 1.0},
        ]
        result = execute_ui_journey("http://localhost:3000", actions)
        assert result["status"] == "unsupported"
        assert result["passed_steps"] == 0
        assert result["total_steps"] == 4
        assert result["driver"] == "lightweight_dom"
        assert "Playwright is required" in result["errors"][0]


def test_cli_hands_command(monkeypatch, capsys):
    """Verify aegis hands CLI subcommand dispatches and outputs correctly."""
    from aegis.cli import main

    mock_html = b"<html><head><title>CLI Test Page</title></head><body><button id='cli-btn'>Test</button></body></html>"
    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = mock_html
    mock_response.headers.get.return_value = "text/html; charset=utf-8"
    mock_response.__enter__.return_value = mock_response
    mock_response.__exit__.return_value = False

    with patch("urllib.request.urlopen", return_value=mock_response):
        # 1. Test markdown output via alias 'test-ui'
        monkeypatch.setattr("sys.argv", ["aegis", "test-ui", "http://example.com"])
        main()
        captured = capsys.readouterr()
        assert "Aegis Hands: UI Inspection Report" in captured.out
        assert "CLI Test Page" in captured.out
        assert "#cli-btn" in captured.out

        # 2. Test json output via primary command 'hands'
        monkeypatch.setattr("sys.argv", ["aegis", "hands", "http://example.com", "--json"])
        main()
        captured_json = capsys.readouterr()
        import json
        parsed = json.loads(captured_json.out)
        assert parsed["url"] == "http://example.com"
        assert parsed["status_code"] == 200
        assert parsed["title"] == "CLI Test Page"
        assert parsed["driver_used"] == "lightweight_dom"

