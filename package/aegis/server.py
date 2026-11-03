import json
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from socketserver import ThreadingMixIn
from typing import Any, Dict
from .config import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    get_aegis_dir,
    get_current_mode,
    set_current_mode,
)

# Under pythonw.exe, stdout/stderr are None. Redirect to daemon.log (line-buffered)
if sys.stdout is None or sys.stderr is None:
    try:
        log_f = open(get_aegis_dir() / "daemon.log", "a", encoding="utf-8", buffering=1)
        if sys.stdout is None:
            sys.stdout = log_f
        if sys.stderr is None:
            sys.stderr = log_f
    except Exception:
        pass
from .db import (
    get_active_alerts,
    get_recent_decisions,
    get_tracked_prs,
    init_db,
    record_decision,
    record_session,
    search_memories,
    track_pr,
)
from .governor import generate_active_context
from .proxy import forward_chat_completion
from .watchdog import WatchdogRunner, sweep_tracked_prs
from .caffeinate import (
    enable_caffeinate,
    disable_caffeinate,
    get_caffeinate_status,
    remote_suspend_pc,
    remote_shutdown_pc,
)
from .remote import handle_twilio_webhook


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class AegisRequestHandler(BaseHTTPRequestHandler):
    """Zero-dependency HTTP API for Aegis Brain."""

    def _send_json(self, status_code: int, data: Any) -> None:
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def _send_text(self, status_code: int, text: str) -> None:
        payload = text.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/markdown; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def _send_xml(self, status_code: int, xml_text: str) -> None:
        payload = xml_text.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/xml; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def _read_json_body(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        params = urllib.parse.parse_qs(parsed.query)

        if path == "" or path == "/health":
            self._send_json(200, {
                "status": "ok",
                "service": "aegis-brain",
                "mode": get_current_mode(),
                "version": "0.1.0",
            })
        elif path == "/bootstrap":
            workspace_param = params.get("workspace", [None])[0]
            ws_path = Path(workspace_param) if workspace_param else None
            context_md = generate_active_context(ws_path)
            self._send_text(200, context_md)
        elif path == "/search":
            query = params.get("q", [""])[0]
            limit = int(params.get("limit", [10])[0])
            results = search_memories(query, limit=limit)
            self._send_json(200, {"query": query, "count": len(results), "results": results})
        elif path == "/decisions":
            limit = int(params.get("limit", [10])[0])
            category = params.get("category", [None])[0]
            decisions = get_recent_decisions(limit=limit, category=category)
            self._send_json(200, decisions)
        elif path == "/tracked_prs":
            prs = get_tracked_prs()
            self._send_json(200, prs)
        elif path == "/alerts":
            alerts = get_active_alerts()
            self._send_json(200, alerts)
        elif path == "/caffeinate":
            self._send_json(200, get_caffeinate_status())
        else:
            self._send_json(404, {"error": "Not Found", "path": self.path})

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        content_type = self.headers.get("Content-Type", "")

        body: Dict[str, Any] = {}
        form_params: Dict[str, Any] = {}

        length = int(self.headers.get("Content-Length", 0))
        raw_bytes = self.rfile.read(length) if length > 0 else b""

        if "application/x-www-form-urlencoded" in content_type:
            raw_text = raw_bytes.decode("utf-8", errors="ignore")
            form_params = urllib.parse.parse_qs(raw_text)
        elif raw_bytes:
            try:
                body = json.loads(raw_bytes.decode("utf-8", errors="ignore"))
            except Exception as e:
                self._send_json(400, {"error": f"Invalid JSON payload: {str(e)}"})
                return

        if path in ("/webhook/twilio", "/webhook/whatsapp"):
            post_data = form_params if form_params else body
            twiml = handle_twilio_webhook(post_data)
            self._send_xml(200, twiml)
            return
        elif path == "/caffeinate":
            action = body.get("action", "status")
            if action in ("on", "enable"):
                ok, msg = enable_caffeinate(keep_display=body.get("keep_display", False))
                self._send_json(200, {"active": True, "message": msg})
            elif action in ("off", "disable"):
                ok, msg = disable_caffeinate()
                self._send_json(200, {"active": False, "message": msg})
            else:
                self._send_json(200, get_caffeinate_status())
            return
        elif path == "/power/sleep":
            ok, msg = remote_suspend_pc()
            self._send_json(200, {"status": "sleep_initiated" if ok else "error", "message": msg})
            return
        elif path == "/power/shutdown":
            delay = int(body.get("delay", 15))
            ok, msg = remote_shutdown_pc(delay_seconds=delay)
            self._send_json(200, {"status": "shutdown_scheduled" if ok else "error", "message": msg})
            return

        if path == "/decision":
            row_id = record_decision(
                category=body.get("category", "GENERAL"),
                title=body.get("title", "Untitled Decision"),
                decision=body.get("decision", ""),
                rationale=body.get("rationale", ""),
                tags=body.get("tags"),
                session_id=body.get("session_id"),
            )
            self._send_json(201, {"status": "recorded", "id": row_id})
        elif path == "/session":
            success = record_session(
                session_id=body.get("id", "default"),
                agent_name=body.get("agent_name", "unknown"),
                workspace_path=body.get("workspace_path", str(Path.cwd())),
                summary=body.get("summary", ""),
            )
            self._send_json(200, {"status": "recorded" if success else "bypassed_private_mode"})
        elif path == "/mode":
            new_mode = body.get("mode")
            if not new_mode:
                self._send_json(400, {"error": "Missing 'mode' field"})
                return
            try:
                active_mode = set_current_mode(new_mode)
                self._send_json(200, {"status": "ok", "mode": active_mode})
            except ValueError as ve:
                self._send_json(400, {"error": str(ve)})
        elif path == "/tracked_prs":
            track_pr(
                repo=body["repo"],
                pr_number=int(body["pr_number"]),
                title=body["title"],
                status=body.get("status", "open"),
                labels=body.get("labels"),
                ci_status=body.get("ci_status", "pending"),
            )
            self._send_json(200, {"status": "tracked"})
        elif path == "/watchdog/poll":
            alerts = sweep_tracked_prs()
            self._send_json(200, {"status": "polled", "new_alerts": alerts})
        elif path == "/v1/chat/completions":
            status_code, resp_payload = forward_chat_completion(body)
            self._send_json(status_code, resp_payload)
        elif path == "/shutdown":
            self._send_json(200, {"status": "shutting_down", "service": "aegis-brain"})
            import time
            def _kill():
                time.sleep(0.2)
                self.server.shutdown()
            import threading
            threading.Thread(target=_kill, daemon=True).start()
        else:
            self._send_json(404, {"error": "Not Found", "path": self.path})

    def log_message(self, format: str, *args: Any) -> None:
        # Suppress noisy standard HTTP access logs
        return


def create_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    init_db()
    server = ThreadingHTTPServer((host, port), AegisRequestHandler)
    return server


def run_daemon(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, watchdog_interval: int = 300) -> None:
    init_db()
    watchdog = WatchdogRunner(interval_seconds=watchdog_interval)
    watchdog.start()

    server = create_server(host, port)
    print(f"[AegisBrain] Neural memory daemon running on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        watchdog.stop()
        server.server_close()
        print("[AegisBrain] Daemon shut down cleanly.")


if __name__ == "__main__":
    run_daemon()
