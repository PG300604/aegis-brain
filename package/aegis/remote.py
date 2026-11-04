_clipboard_memory_buffer = ""
"""Remote WhatsApp & Shell Command Bridge for AegisBrain.

Enables secure remote control of AI coding agents, shell execution,
git workflows, caffeinate toggle, and PC shutdown via WhatsApp.
Zero external dependencies (pure Python standard library).
"""

import base64
import difflib
import json
import os
import sys
import time
import threading
import subprocess
import urllib.parse
import urllib.request
import urllib.error
import xml.sax.saxutils
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List

from .config import get_aegis_dir
from .caffeinate import (
    enable_caffeinate,
    disable_caffeinate,
    get_caffeinate_status,
    remote_suspend_pc,
    remote_shutdown_pc,
    remote_lock_workstation,
    remote_block_input,
    remote_trigger_alarm,
)
from .db import search_memories, get_recent_decisions, get_tracked_prs
from .hardware import format_hardware_report
from .governance import (
    load_governance_config,
    save_governance_config,
    format_governance_status,
    get_telemetry_terms,
)
from .diagnostics import format_diagnostic_markdown, get_github_issue_url
from .environment import format_environment_report
from .taste import format_taste_display
from .planner import format_suggestion_panel, create_default_suggestions_for_task
from .orchestrator import run_manager_worker_pipeline, format_distillation_report


def get_remote_config_path() -> Path:
    return get_aegis_dir() / "remote.json"


def load_remote_config() -> Dict[str, Any]:
    cfg_p = get_remote_config_path()
    if cfg_p.exists():
        try:
            return json.loads(cfg_p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "provider": os.environ.get("AEGIS_REMOTE_PROVIDER", "telegram"),
        "telegram_token": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
        "telegram_chat_id": os.environ.get("TELEGRAM_CHAT_ID", ""),
        "account_sid": os.environ.get("TWILIO_ACCOUNT_SID", ""),
        "auth_token": os.environ.get("TWILIO_AUTH_TOKEN", ""),
        "twilio_number": os.environ.get("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886"),
        "allowed_numbers": json.loads(os.environ.get("AEGIS_ALLOWED_NUMBERS", "[]")),
        "auth_pin": os.environ.get("AEGIS_REMOTE_PIN", "8765"),
        "workspace_dir": os.environ.get("AEGIS_WORKSPACE_DIR", str(Path.cwd())),
        "auto_caffeinate": True,
        "default_mode": os.environ.get("AEGIS_REMOTE_MODE", "chat"),
    }


def save_remote_config(cfg: Dict[str, Any]) -> None:
    cfg_p = get_remote_config_path()
    cfg_p.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def send_whatsapp_message(to_number: str, body: str, config: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    """Send an outbound WhatsApp message via Twilio REST API using standard library urllib."""
    cfg = config or load_remote_config()
    sid = cfg.get("account_sid")
    token = cfg.get("auth_token")
    from_num = cfg.get("twilio_number", "whatsapp:+14155238886")

    if not sid or not token:
        return False, "Twilio Account SID or Auth Token not configured"

    # Ensure whatsapp: prefix
    if not to_number.startswith("whatsapp:"):
        to_number = f"whatsapp:{to_number}"
    if not from_num.startswith("whatsapp:"):
        from_num = f"whatsapp:{from_num}"

    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    data = urllib.parse.urlencode({
        "To": to_number,
        "From": from_num,
        "Body": body[:1500],  # Respect WhatsApp message boundaries
    }).encode("utf-8")

    creds = base64.b64encode(f"{sid}:{token}".encode("utf-8")).decode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "AegisBrain-Remote/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp_body = resp.read().decode("utf-8")
            return True, resp_body
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore")
        return False, f"HTTP Error {e.code}: {err}"
    except Exception as e:
        return False, f"Request failed: {str(e)}"


_active_polls: Dict[str, Dict[str, Any]] = {}
_active_polls_lock = threading.Lock()
_is_away_mode: bool = False
_away_lock = threading.Lock()


def is_away_mode_active() -> bool:
    """Return whether workstation is currently in Away / Remote Mirroring mode."""
    global _is_away_mode
    if _is_away_mode:
        return True
    try:
        cfg = load_remote_config()
        return bool(cfg.get("away_mode", False))
    except Exception:
        return _is_away_mode


def set_away_mode(enabled: bool) -> Tuple[bool, str]:
    """Toggle Away Mode and persist state in remote config."""
    global _is_away_mode
    with _away_lock:
        _is_away_mode = enabled
    cfg = load_remote_config()
    cfg["away_mode"] = enabled
    save_remote_config(cfg)
    state_str = "ACTIVATED" if enabled else "DEACTIVATED"
    return True, f"Away Mode {state_str}"


def register_active_poll(poll_id: str, question: str, options: List[str]) -> None:
    """Register active Telegram poll in memory to correlate user vote answers."""
    with _active_polls_lock:
        _active_polls[poll_id] = {
            "question": question,
            "options": options,
            "created_at": time.time(),
        }


def get_active_poll(poll_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve registered poll details."""
    with _active_polls_lock:
        return _active_polls.get(poll_id)


class TerminalMirror:
    """Thread-safe ring buffer capturing terminal and agent output for remote streaming."""
    def __init__(self, capacity: int = 200) -> None:
        self.capacity = capacity
        self.buffer: List[Dict[str, Any]] = []
        self.lock = threading.Lock()

    def append(self, text: str, source: str = "cli") -> None:
        if not text:
            return
        clean = text.strip()
        if not clean:
            return
        with self.lock:
            entry = {
                "timestamp": time.time(),
                "time_str": time.strftime("%H:%M:%S"),
                "source": source,
                "text": clean,
            }
            self.buffer.append(entry)
            if len(self.buffer) > self.capacity:
                self.buffer.pop(0)

        # Stream chunk to phone immediately if away mode is active
        if is_away_mode_active():
            self._stream_to_remote(entry)

    def _stream_to_remote(self, entry: Dict[str, Any]) -> None:
        try:
            cfg = load_remote_config()
            chat_id = cfg.get("telegram_chat_id")
            if not chat_id:
                return
            msg = f"📟 *[{entry['time_str']} {entry['source'].upper()}]*\n```\n{entry['text'][:1200]}\n```"
            send_telegram_message(chat_id, msg, config=cfg)
        except Exception:
            pass

    def get_page(self, page: int = 1, page_size: int = 4) -> Tuple[List[Dict[str, Any]], int, int]:
        with self.lock:
            total_items = len(self.buffer)
            total_pages = max(1, (total_items + page_size - 1) // page_size)
            page = max(1, min(page, total_pages))
            start_idx = max(0, total_items - page * page_size)
            end_idx = total_items - (page - 1) * page_size
            items = self.buffer[start_idx:end_idx]
            return items, page, total_pages


_terminal_mirror = TerminalMirror()


def get_terminal_mirror() -> TerminalMirror:
    return _terminal_mirror


def mirror_output(text: str, source: str = "cli") -> None:
    """Public helper to mirror terminal or agent output chunk."""
    _terminal_mirror.append(text, source=source)


def _send_single_telegram_chunk(
    chat_id: str,
    text_chunk: str,
    token: str,
    cfg: Dict[str, Any],
    parse_mode: Optional[str] = "Markdown",
    reply_markup: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, str]:
    """Helper to send a single Telegram message chunk."""
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return True, "Message delivered (test mode)"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload_dict: Dict[str, Any] = {
        "chat_id": chat_id,
        "text": text_chunk[:4000],
        "disable_web_page_preview": True,
    }
    if parse_mode:
        payload_dict["parse_mode"] = parse_mode
    if reply_markup:
        payload_dict["reply_markup"] = reply_markup

    payload = json.dumps(payload_dict).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "AegisBrain-Remote/1.0"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                return True, "Message delivered"
            return False, data.get("description", "Unknown Telegram error")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        if e.code == 400 and parse_mode:
            return _send_single_telegram_chunk(chat_id, text_chunk, token, cfg, parse_mode=None, reply_markup=reply_markup)
        return False, f"Telegram HTTP {e.code}: {err}"
    except Exception as e:
        return False, f"Telegram network error: {e}"


def send_telegram_chat_action(
    chat_id: str,
    action: str = "typing",
    config: Optional[Dict[str, Any]] = None,
) -> bool:
    """Send a chat action indicator (typing, upload_document) to Telegram."""
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return True

    cfg = config or load_remote_config()
    token = cfg.get("telegram_token", "")
    if not token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{token}/sendChatAction"
    payload = json.dumps({"chat_id": chat_id, "action": action}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "AegisBrain-Remote/1.0"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            d = json.loads(resp.read().decode("utf-8"))
            return bool(d.get("ok"))
    except Exception:
        return False


def send_telegram_message(
    chat_id: str,
    body: str,
    config: Optional[Dict[str, Any]] = None,
    parse_mode: Optional[str] = "Markdown",
    reply_markup: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, str]:
    """Send an outbound Telegram message via Telegram Bot API with automatic multi-chunking & plain-text fallback."""
    cfg = config or load_remote_config()
    token = cfg.get("telegram_token", "")
    if not token:
        return False, "Telegram Bot Token not configured in ~/.aegis-brain/remote.json"

    # Multi-chunk splitting if body exceeds Telegram's 4096 character limit
    if len(body) > 3900:
        chunks: List[str] = []
        remaining = body
        while len(remaining) > 3800:
            split_idx = remaining.rfind("\n\n", 0, 3800)
            if split_idx == -1:
                split_idx = remaining.rfind("\n", 0, 3800)
            if split_idx == -1:
                split_idx = 3800
            chunks.append(remaining[:split_idx])
            remaining = remaining[split_idx:].lstrip("\n")
        if remaining:
            chunks.append(remaining)

        last_ok = True
        last_msg = "Delivered all chunks"
        for idx, chunk in enumerate(chunks):
            markup = reply_markup if idx == len(chunks) - 1 else None
            ok, msg = _send_single_telegram_chunk(chat_id, chunk, token, cfg, parse_mode, markup)
            last_ok = ok
            last_msg = msg
            time.sleep(0.08)
        return last_ok, last_msg

    return _send_single_telegram_chunk(chat_id, body, token, cfg, parse_mode, reply_markup)


def send_telegram_poll(
    chat_id: str,
    question: str,
    options: List[str],
    allows_multiple_answers: bool = False,
    config: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, str, Optional[str]]:
    """Send a native Telegram Poll to the user's phone for instant 1-tap MCQ decisions."""
    if os.environ.get("PYTEST_CURRENT_TEST"):
        register_active_poll("test_poll_id", question, options)
        return True, "Poll sent successfully", "test_poll_id"

    cfg = config or load_remote_config()
    token = cfg.get("telegram_token", "")
    if not token:
        return False, "Telegram Bot Token not configured", None

    # Telegram poll limits: question <= 300 chars, 2-10 options, each <= 100 chars
    q = question[:290]
    opts = [o[:95] for o in options[:10]]
    if len(opts) < 2:
        opts.append("Continue standard execution")

    url = f"https://api.telegram.org/bot{token}/sendPoll"
    payload = json.dumps({
        "chat_id": chat_id,
        "question": q,
        "options": opts,
        "is_anonymous": False,
        "allows_multiple_answers": allows_multiple_answers,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "AegisBrain-Remote/1.0"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                poll_info = data.get("result", {}).get("poll", {})
                poll_id = str(poll_info.get("id", ""))
                register_active_poll(poll_id, q, opts)
                return True, "Poll sent successfully", poll_id
            return False, data.get("description", "Unknown Telegram error"), None
    except Exception as e:
        return False, f"Telegram poll failed: {e}", None


def send_telegram_inline_keyboard(
    chat_id: str,
    text: str,
    buttons: List[List[Dict[str, str]]],
    config: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, str]:
    """Send interactive buttons (InlineKeyboardMarkup) for quick thumb-tap navigation and choices."""
    reply_markup = {"inline_keyboard": buttons}
    return send_telegram_message(chat_id, text, config=config, reply_markup=reply_markup)


def answer_telegram_callback(
    callback_query_id: str,
    text: str = "Aegis registered!",
    config: Optional[Dict[str, Any]] = None,
) -> bool:
    """Acknowledge Telegram callback query so client loading spinner dismisses."""
    cfg = config or load_remote_config()
    token = cfg.get("telegram_token", "")
    if not token or not callback_query_id:
        return False
    url = f"https://api.telegram.org/bot{token}/answerCallbackQuery"
    payload = json.dumps({"callback_query_id": callback_query_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return bool(json.loads(resp.read().decode("utf-8")).get("ok"))
    except Exception:
        return False


def register_telegram_commands(token: str) -> bool:
    """Register slash commands with Telegram Bot API so user sees autocomplete menu."""
    if not token:
        return False
    commands = [
        {"command": "help", "description": "Show available commands & help guide"},
        {"command": "status", "description": "System status, RAM, caffeinate & tracked PRs"},
        {"command": "away", "description": "Toggle Away Mode & terminal mirroring (on/off)"},
        {"command": "nav", "description": "Navigate terminal logs page-by-page from phone"},
        {"command": "swarm", "description": "Execute nested 4-tier multi-agent swarm"},
        {"command": "config", "description": "Model governance (Manager/Worker/Telemetry)"},
        {"command": "env", "description": "Workstation tools, Ollama, OpenCode & pending queues"},
        {"command": "taste", "description": "User aesthetic taste, persona & coding doctrine"},
        {"command": "plan", "description": "Interactive Suggestion Panel with trade-offs"},
        {"command": "orchestrate", "description": "Manager-Worker code pipeline & token savings"},
        {"command": "scout", "description": "Weekly skill discovery & Arsenal intelligence"},
        {"command": "moe", "description": "Dynamic MoE routing, latency estimation & RAM cap"},
        {"command": "graph", "description": "AST Codebase Graph statistics & symbol search"},
        {"command": "task", "description": "Active task memory & accomplishment history"},
        {"command": "sandbox", "description": "Run isolated sandbox Red-Team security audit"},
        {"command": "hardware", "description": "Inspect RAM & dynamic model recommendation"},
        {"command": "report", "description": "Generate diagnostic report & GitHub issue"},
        {"command": "terms", "description": "View transparent zero-leakage telemetry terms"},
        {"command": "caffeinate", "description": "Toggle anti-sleep wake-lock (on/off)"},
        {"command": "mode", "description": "Switch default mode (chat or exec)"},
        {"command": "type", "description": "Type text into active IDE window and hit Enter"},
        {"command": "prompt", "description": "Alias for /type (voice dictation bridge)"},
        {"command": "paste", "description": "Paste text into active window without Enter"},
        {"command": "clip", "description": "Read or write to workstation clipboard"},
        {"command": "lock", "description": "Instantly lock workstation screen & activate Away Mode"},
        {"command": "recall", "description": "Search architectural memories & decisions"},
        {"command": "git", "description": "Remote git status, diff, commit, push"},
        {"command": "artifacts", "description": "View recent generated artifacts"},
        {"command": "windows", "description": "List visible desktop application windows"},
        {"command": "focus", "description": "Bring application window to front"},
        {"command": "alarm", "description": "Trigger alert sound chimes on PC speakers"},
        {"command": "sleep", "description": "Turn off caffeinate and suspend PC"},
        {"command": "shutdown", "description": "Safely power off workstation PC (15s countdown)"},
    ]
    url = f"https://api.telegram.org/bot{token}/setMyCommands"
    payload = json.dumps({"commands": commands}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "AegisBrain-Remote/1.0"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            ok = bool(data.get("ok"))

        # Also configure the Telegram chat menu button to show commands drawer
        menu_url = f"https://api.telegram.org/bot{token}/setChatMenuButton"
        menu_payload = json.dumps({"menu_button": {"type": "commands"}}).encode("utf-8")
        menu_req = urllib.request.Request(
            menu_url,
            data=menu_payload,
            headers={"Content-Type": "application/json", "User-Agent": "AegisBrain-Remote/1.0"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(menu_req, timeout=5):
                pass
        except Exception:
            pass

        return ok
    except Exception:
        return False


def find_active_transcript_file() -> Optional[Path]:
    """Find the most recently modified transcript.jsonl under ~/.gemini/antigravity-cli/brain/."""
    brain_dir = Path.home() / ".gemini" / "antigravity-cli" / "brain"
    if not brain_dir.exists():
        return None
    transcripts = list(brain_dir.glob("*/.system_generated/logs/transcript.jsonl"))
    if not transcripts:
        return None
    transcripts.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return transcripts[0]


class TranscriptWatcher(threading.Thread):
    """Watches active Antigravity CLI transcript and streams tool executions & outputs to Telegram."""
    def __init__(self, stop_event: Optional[threading.Event] = None):
        super().__init__(daemon=True)
        self.stop_event = stop_event or threading.Event()
        self.last_path: Optional[Path] = None
        self.last_pos = 0

    def run(self):
        while not self.stop_event.is_set():
            try:
                active_file = find_active_transcript_file()
                if not active_file or not active_file.exists():
                    time.sleep(1.2)
                    continue

                if self.last_path != active_file:
                    self.last_path = active_file
                    # Seek to current file end to stream subsequent real-time events
                    self.last_pos = active_file.stat().st_size

                curr_size = active_file.stat().st_size
                if curr_size > self.last_pos:
                    with open(active_file, "r", encoding="utf-8", errors="replace") as f:
                        f.seek(self.last_pos)
                        new_text = f.read()
                        self.last_pos = f.tell()

                    for line in new_text.splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                            self._dispatch_event(obj)
                        except Exception:
                            continue
            except Exception:
                pass
            time.sleep(1.2)

    def _dispatch_event(self, obj: Dict[str, Any]) -> None:
        cfg = load_remote_config()
        chat_id = cfg.get("telegram_chat_id", "")
        if not chat_id:
            return

        step_type = obj.get("type", "")
        tool_calls = obj.get("tool_calls", [])
        content = obj.get("content", "")

        # 1. Tool Call Execution
        if step_type == "PLANNER_RESPONSE" and tool_calls:
            for tc in tool_calls:
                name = tc.get("name", "tool")
                summary = tc.get("toolSummary") or name
                get_terminal_mirror().append(f"⚙️ [{name}] {summary}", source="agent")

                if name == "ask_question":
                    args = tc.get("arguments", {})
                    questions = args.get("questions", [])
                    for q in questions:
                        q_text = q.get("question", "Agent Question:")
                        options = q.get("options", [])
                        if options:
                            send_telegram_poll(chat_id, q_text, options, config=cfg)
                            mcq_buttons = [
                                [{"text": opt[:32], "callback_data": f"mcq:{opt[:32]}"}]
                                for opt in options[:6]
                            ]
                            send_telegram_inline_keyboard(
                                chat_id,
                                f"❓ *Aegis Choice Required:*\n{q_text}\n\n_Tap option below or vote in poll above:_",
                                mcq_buttons,
                                config=cfg,
                            )
                else:
                    send_telegram_chat_action(chat_id, "typing", config=cfg)
                    if is_away_mode_active():
                        send_telegram_message(chat_id, f"⚙️ *[Antigravity]:* {summary}", config=cfg)

        # 2. Assistant Text Response (Final Answer / Chat)
        elif step_type == "PLANNER_RESPONSE" and content and not tool_calls:
            clean_content = content.strip()
            if clean_content:
                get_terminal_mirror().append(clean_content, source="agent")
                if is_away_mode_active():
                    send_telegram_message(chat_id, f"🤖 *Antigravity Response:*\n\n{clean_content}", config=cfg)

        # 3. CLI Command Output
        elif step_type == "GENERIC" and content:
            clean_out = content.strip()
            if clean_out:
                get_terminal_mirror().append(clean_out, source="cli")
                if is_away_mode_active():
                    if "exited with code" in clean_out and "exited with code 0" not in clean_out:
                        err_preview = clean_out[-500:]
                        send_telegram_message(chat_id, f"⚠️ *CLI Warning:*\n```\n{err_preview}\n```", config=cfg)


def poll_telegram_updates(stop_event: Optional[threading.Event] = None, on_ready_callback: Optional[Any] = None) -> None:
    """Long-polling daemon for Telegram Bot API supporting text, native polls & inline buttons."""
    cfg = load_remote_config()
    token = cfg.get("telegram_token", "")
    if not token:
        print("[Telegram] Bot token not set. Run 'aegis remote setup' to configure Telegram.")
        return

    offset = 0
    register_telegram_commands(token)
    print("[Telegram] Bot polling listener active. Ready for commands from your phone!")
    if on_ready_callback:
        try:
            on_ready_callback()
        except Exception:
            pass

    # Start live background transcript watcher to stream Antigravity progress
    watcher = TranscriptWatcher(stop_event=stop_event)
    watcher.start()

    while stop_event is None or not stop_event.is_set():
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}&timeout=20"
            req = urllib.request.Request(url, headers={"User-Agent": "AegisBrain-Remote/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if not data.get("ok"):
                    time.sleep(2)
                    continue

                for update in data.get("result", []):
                    offset = max(offset, update["update_id"] + 1)

                    # 1. Handle Native Poll Answers (User 1-tap MCQ decision)
                    poll_ans = update.get("poll_answer")
                    if poll_ans:
                        poll_id = str(poll_ans.get("poll_id", ""))
                        user_info = poll_ans.get("user", {})
                        user_id = str(user_info.get("id", ""))
                        selected_ids = poll_ans.get("option_ids", [])
                        active_p = get_active_poll(poll_id)
                        if active_p and selected_ids:
                            sel_idx = selected_ids[0]
                            options = active_p.get("options", [])
                            choice_text = options[sel_idx] if sel_idx < len(options) else f"Option {sel_idx}"
                            # Deliver choice into desktop coding session
                            type_to_desktop(choice_text, press_enter=True)
                            confirm = (
                                f"🗳️ *Decision Confirmed (via Poll):*\n"
                                f"• Choice: `{choice_text}`\n"
                                f"• Question: {active_p.get('question')}\n\n"
                                f"AegisBrain typed your choice into the active session!"
                            )
                            send_telegram_message(user_id, confirm, config=cfg)
                            record_decision(
                                category="TELEGRAM_POLL",
                                title=active_p.get("question", "Telegram Poll Decision"),
                                decision=choice_text,
                                rationale=f"Voted by {user_info.get('first_name', 'user')} from phone",
                                tags=["poll", "mobile-decision"],
                            )
                        continue

                    # 2. Handle Inline Button Callback Queries
                    cb_query = update.get("callback_query")
                    if cb_query:
                        cb_id = str(cb_query.get("id", ""))
                        cb_from = str(cb_query.get("from", {}).get("id", ""))
                        cb_data = str(cb_query.get("data", ""))
                        answer_telegram_callback(cb_id, text="Aegis registered!", config=cfg)

                        if cb_data.startswith("nav:"):
                            page_str = cb_data.split(":", 1)[1]
                            p_num = int(page_str) if page_str.isdigit() else 1
                            mirror = get_terminal_mirror()
                            items, page, total_pages = mirror.get_page(page=p_num, page_size=4)
                            if items:
                                lines = [f"📟 *Terminal Output Pager (Page {page}/{total_pages}):*", ""]
                                for it in items:
                                    lines.append(f"⏱️ `[{it['time_str']} {it['source'].upper()}]`")
                                    p_txt = it["text"][:300] + ("..." if len(it["text"]) > 300 else "")
                                    lines.append(f"```\n{p_txt}\n```")
                                btns = [
                                    [
                                        {"text": "⬅️ Prev", "callback_data": f"nav:{page+1}"},
                                        {"text": "🔄 Refresh", "callback_data": f"nav:{page}"},
                                        {"text": "➡️ Next", "callback_data": f"nav:{max(1, page-1)}"},
                                    ],
                                    [
                                        {"text": "📋 Latest", "callback_data": "nav:1"},
                                        {"text": "📊 Status", "callback_data": "cmd:status"},
                                    ]
                                ]
                                send_telegram_inline_keyboard(cb_from, "\n".join(lines), btns, config=cfg)
                            else:
                                send_telegram_message(cb_from, "📟 *Terminal Output Buffer:* (No logs recorded yet)", config=cfg)

                        elif cb_data == "lock:now":
                            handle_remote_command(cb_from, "/lock")

                        elif cb_data == "away:off":
                            set_away_mode(False)
                            send_telegram_message(cb_from, "👋 *Away Mode Deactivated!*\nWelcome back to your desk. Terminal output streaming paused.", config=cfg)

                        elif cb_data.startswith("artifact:"):
                            art_idx = cb_data.split(":", 1)[1]
                            art_content = get_latest_artifacts(art_idx)
                            send_telegram_message(cb_from, art_content, config=cfg)

                        elif cb_data.startswith("cmd:"):
                            sub_cmd = "/" + cb_data.split(":", 1)[1]
                            res_text = handle_remote_command(cb_from, sub_cmd)
                            if res_text:
                                send_telegram_message(cb_from, res_text, config=cfg)

                        elif cb_data.startswith("mcq:"):
                            mcq_choice = cb_data.split(":", 1)[1]
                            type_to_desktop(mcq_choice, press_enter=True)
                            conf = f"✅ *Interactive Choice Confirmed:* `{mcq_choice}`\nAegisBrain submitted your choice to the active session."
                            send_telegram_message(cb_from, conf, config=cfg)
                            record_decision(
                                category="TELEGRAM_BUTTON",
                                title="Mobile Inline Button Decision",
                                decision=mcq_choice,
                                rationale="Selected via Telegram Inline Keyboard on mobile",
                                tags=["button", "mobile-decision"],
                            )

                        elif cb_data.startswith("cfg:"):
                            parts = cb_data.split(":", 2)
                            cfg_type = parts[1]
                            cfg_val = parts[2] if len(parts) > 2 else ""
                            gov_cfg = load_governance_config()
                            if cfg_type == "mgr":
                                gov_cfg["manager_model"] = cfg_val
                                save_governance_config(gov_cfg)
                                send_telegram_message(cb_from, f"👑 *Manager Model Switched:* `{cfg_val}`", config=cfg)
                            elif cfg_type == "wrk":
                                gov_cfg["worker_model"] = cfg_val
                                save_governance_config(gov_cfg)
                                send_telegram_message(cb_from, f"🤖 *Worker Model Switched:* `{cfg_val}`", config=cfg)
                            elif cfg_type == "drv":
                                gov_cfg["model_dir"] = cfg_val
                                save_governance_config(gov_cfg)
                                os.environ["OLLAMA_MODELS"] = cfg_val
                                send_telegram_message(cb_from, f"💾 *Model Storage Disk Switched:* `{cfg_val}`", config=cfg)
                        continue

                    # 3. Handle Regular Text Messages & Commands
                    msg = update.get("message", {})
                    chat = msg.get("chat", {})
                    chat_id = str(chat.get("id", ""))
                    text = msg.get("text", "")
                    if not text or not chat_id:
                        continue

                    # If telegram_chat_id was not set, automatically pair on first interaction
                    if not cfg.get("telegram_chat_id"):
                        cfg["telegram_chat_id"] = chat_id
                        save_remote_config(cfg)

                    attach_to_input_desktop()
                    reply = handle_remote_command(chat_id, text)
                    if reply:
                        get_terminal_mirror().append(reply, source=f"cmd:{text[:25]}")
                        if not any(reply.startswith(p) for p in ("🔒 *Workstation Lock", "❓ *Unknown Command:", "📟 *Terminal Output Pager")):
                            send_telegram_message(chat_id, reply, config=cfg)

        except Exception as e:
            time.sleep(3)


def send_remote_message(dest: str, body: str, config: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    """Generic dispatcher routing to either Telegram or WhatsApp based on configuration."""
    cfg = config or load_remote_config()
    provider = cfg.get("provider", "telegram").lower()
    if provider == "telegram":
        chat_id = dest or cfg.get("telegram_chat_id", "")
        return send_telegram_message(chat_id, body, config=cfg)
    return send_whatsapp_message(dest, body, config=cfg)


def execute_shell(cmd: str, cwd: Optional[Path] = None, timeout: int = 60) -> str:
    """Execute a shell command on the workstation and capture output."""
    work_dir = cwd or Path(load_remote_config().get("workspace_dir", str(Path.cwd())))
    if not work_dir.exists():
        work_dir = Path.cwd()

    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()

        combined = []
        if out:
            combined.append(out)
        if err:
            combined.append(f"[stderr]\n{err}")

        res = "\n".join(combined).strip() or "(command exited with no output)"
        if proc.returncode != 0:
            res = f"⚠️ [Exit code {proc.returncode}]\n{res}"

        # Mirror output to terminal ring buffer & stream to phone if Away Mode is ON
        get_terminal_mirror().append(res, source=f"shell:{cmd[:35]}")

        # Telegram/WhatsApp truncation limit
        if len(res) > 1300:
            res = res[:1300] + "\n... [output truncated]"
        return res
    except subprocess.TimeoutExpired:
        return f"⏱️ Command timed out after {timeout} seconds."
    except Exception as e:
        return f"❌ Command execution failed: {str(e)}"


def get_latest_artifacts(arg: str = "") -> str:
    """Scan for recently generated brain artifacts and reports, or display an artifact's content."""
    # Check Antigravity / Gemini brain directory
    gemini_brain = Path.home() / ".gemini" / "antigravity-cli" / "brain"
    artifacts: List[Path] = []
    if gemini_brain.exists():
        for md_file in gemini_brain.glob("*/*.md"):
            artifacts.append(md_file)

    if not artifacts:
        return "No recent artifacts found in session directory."

    # Sort by modification time
    artifacts.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    recent = artifacts[:6]

    # If arg specifies an artifact number (e.g. "1") or name
    clean_arg = arg.strip()
    if clean_arg:
        target: Optional[Path] = None
        if clean_arg.isdigit() and 1 <= int(clean_arg) <= len(recent):
            target = recent[int(clean_arg) - 1]
        else:
            for p in recent:
                if clean_arg.lower() in p.name.lower():
                    target = p
                    break
        if target and target.exists():
            content = target.read_text(encoding="utf-8", errors="replace")
            return f"📑 *Artifact:* `{target.name}`\n📁 Path: `{target.parent.name}/{target.name}`\n\n```markdown\n{content}\n```"

    lines = ["📑 *Recent Workspace Artifacts:*", ""]
    for idx, p in enumerate(recent, 1):
        mtime = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).strftime("%H:%M UTC")
        lines.append(f"{idx}. *{p.name}* ({mtime})\n   Path: `{p.parent.name}/{p.name}`")
    lines.append("\n_Send `/artifacts <number>` to view full contents on phone._")
    return "\n".join(lines)



def attach_to_input_desktop() -> bool:
    """Attach current thread to the interactive user desktop (WinSta0\\Default)."""
    if sys.platform == "win32":
        try:
            import ctypes
            user32 = ctypes.windll.user32
            h_input = user32.OpenInputDesktop(0, False, 0x01FF)
            if h_input:
                user32.SetThreadDesktop(h_input)
                return True
        except Exception:
            pass
    return False


def copy_to_desktop_clipboard(text: str) -> bool:
    """Copy text directly to the workstation system clipboard."""
    global _clipboard_memory_buffer
    _clipboard_memory_buffer = text
    if sys.platform == "win32":
        try:
            attach_to_input_desktop()
            import ctypes
            from ctypes import wintypes, c_void_p, c_size_t

            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            user32.OpenClipboard.argtypes = [wintypes.HWND]
            user32.OpenClipboard.restype = wintypes.BOOL
            user32.EmptyClipboard.argtypes = []
            user32.EmptyClipboard.restype = wintypes.BOOL
            user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
            user32.SetClipboardData.restype = wintypes.HANDLE
            user32.CloseClipboard.argtypes = []
            user32.CloseClipboard.restype = wintypes.BOOL

            kernel32.GlobalAlloc.argtypes = [wintypes.UINT, c_size_t]
            kernel32.GlobalAlloc.restype = wintypes.HGLOBAL
            kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
            kernel32.GlobalLock.restype = c_void_p
            kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
            kernel32.GlobalUnlock.restype = wintypes.BOOL

            GMEM_MOVEABLE = 0x0002
            CF_UNICODETEXT = 13
            data = text.encode("utf-16le") + b"\x00\x00"
            h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(data))
            if not h_mem:
                return False
            ptr = kernel32.GlobalLock(h_mem)
            if not ptr:
                return False
            ctypes.memmove(ptr, data, len(data))
            kernel32.GlobalUnlock(h_mem)

            for _ in range(5):
                if user32.OpenClipboard(None):
                    try:
                        user32.EmptyClipboard()
                        user32.SetClipboardData(CF_UNICODETEXT, h_mem)
                        return True
                    finally:
                        user32.CloseClipboard()
                time.sleep(0.05)
            return bool(_clipboard_memory_buffer)
        except Exception:
            return bool(_clipboard_memory_buffer)
    elif sys.platform == "darwin":
        try:
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            p.communicate(text.encode("utf-8"))
            return p.returncode == 0
        except Exception:
            return False
    else:
        try:
            p = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE)
            p.communicate(text.encode("utf-8"))
            return p.returncode == 0
        except Exception:
            return False


def get_desktop_clipboard() -> str:
    """Retrieve current text contents of the workstation clipboard."""
    global _clipboard_memory_buffer
    if _clipboard_memory_buffer:
        return _clipboard_memory_buffer
    if sys.platform == "win32":
        try:
            attach_to_input_desktop()
            import ctypes
            from ctypes import wintypes, c_void_p

            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            user32.OpenClipboard.argtypes = [wintypes.HWND]
            user32.OpenClipboard.restype = wintypes.BOOL
            user32.CloseClipboard.argtypes = []
            user32.CloseClipboard.restype = wintypes.BOOL
            user32.GetClipboardData.argtypes = [wintypes.UINT]
            user32.GetClipboardData.restype = wintypes.HANDLE
            kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
            kernel32.GlobalLock.restype = c_void_p
            kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
            kernel32.GlobalUnlock.restype = wintypes.BOOL

            CF_UNICODETEXT = 13
            for _ in range(5):
                if user32.OpenClipboard(None):
                    try:
                        h_mem = user32.GetClipboardData(CF_UNICODETEXT)
                        if not h_mem:
                            return _clipboard_memory_buffer
                        ptr = kernel32.GlobalLock(h_mem)
                        if not ptr:
                            return _clipboard_memory_buffer
                        val = ctypes.wstring_at(ptr)
                        kernel32.GlobalUnlock(h_mem)
                        return val or _clipboard_memory_buffer
                    finally:
                        user32.CloseClipboard()
                time.sleep(0.05)
            return _clipboard_memory_buffer
        except Exception:
            return _clipboard_memory_buffer
    elif sys.platform == "darwin":
        try:
            res = subprocess.run(["pbpaste"], capture_output=True, text=True)
            return res.stdout
        except Exception:
            return ""
    else:
        try:
            res = subprocess.run(["xclip", "-selection", "clipboard", "-o"], capture_output=True, text=True)
            return res.stdout
        except Exception:
            return ""


def get_desktop_windows() -> List[Dict[str, Any]]:
    """Return list of open desktop windows and their active status."""
    if sys.platform != "win32":
        return []
    attach_to_input_desktop()
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    user32.GetForegroundWindow.restype = wintypes.HWND
    active_hwnd = user32.GetForegroundWindow()
    EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows.argtypes = [EnumWindowsProc, wintypes.LPARAM]
    user32.EnumWindows.restype = wintypes.BOOL

    windows = []
    def cb(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                val = buff.value.strip()
                ignore = ("Program Manager", "Default IME", "MSCTFIME UI", "Windows Input Experience")
                if val and not any(ig in val for ig in ignore) and not val.startswith("komoborder") and len(val) > 2:
                    windows.append({"hwnd": hwnd, "title": val, "is_active": (hwnd == active_hwnd)})
        return True

    user32.EnumWindows(EnumWindowsProc(cb), 0)
    return windows


def focus_desktop_window(keyword: str) -> Tuple[bool, str]:
    """Find and bring an open window matching keyword to the foreground."""
    if sys.platform != "win32":
        return False, "Focus switching is supported on Windows."
    attach_to_input_desktop()
    import ctypes
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    windows = get_desktop_windows()
    for w in windows:
        if keyword.lower() in w["title"].lower():
            hwnd = w["hwnd"]
            cur_th = kernel32.GetCurrentThreadId()
            target_th = user32.GetWindowThreadProcessId(hwnd, None)
            if cur_th != target_th:
                try:
                    user32.AttachThreadInput(cur_th, target_th, True)
                except Exception:
                    pass
            user32.ShowWindow(hwnd, 9)  # SW_RESTORE
            user32.SetForegroundWindow(hwnd)
            user32.BringWindowToTop(hwnd)
            if cur_th != target_th:
                try:
                    user32.AttachThreadInput(cur_th, target_th, False)
                except Exception:
                    pass
            return True, f'Activated window: "{w["title"]}"'
    return False, f'No open window found matching "{keyword}".'


def type_to_desktop(text: str, press_enter: bool = True) -> Tuple[bool, str]:
    """Copy text to clipboard, auto-focus terminal/IDE, and simulate Ctrl+V and optional Enter."""
    if not text.strip():
        return False, "No text provided to type."

    attach_to_input_desktop()
    ok = copy_to_desktop_clipboard(text)
    if not ok:
        return False, "Failed to copy text to system clipboard."

    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            user32 = ctypes.windll.user32
            user32.GetForegroundWindow.restype = wintypes.HWND
            user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
            user32.GetWindowTextLengthW.restype = ctypes.c_int
            user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
            user32.GetWindowTextW.restype = ctypes.c_int

            hwnd = user32.GetForegroundWindow()
            win_title = "Active Window"
            if hwnd:
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buff, length + 1)
                    win_title = buff.value or win_title

            # Auto-focus coding / terminal window if user is away or focused elsewhere
            TARGET_IDE_KEYWORDS = ["powershell", "terminal", "antigravity", "visual studio code", "code", "cmd", "bash"]
            is_target_ide = any(kw in win_title.lower() for kw in TARGET_IDE_KEYWORDS)
            if not is_target_ide:
                for kw in TARGET_IDE_KEYWORDS:
                    ok_f, _ = focus_desktop_window(kw)
                    if ok_f:
                        time.sleep(0.12)
                        hwnd = user32.GetForegroundWindow()
                        if hwnd:
                            length = user32.GetWindowTextLengthW(hwnd)
                            if length > 0:
                                buff = ctypes.create_unicode_buffer(length + 1)
                                user32.GetWindowTextW(hwnd, buff, length + 1)
                                win_title = buff.value or win_title
                        break

            # Compute hardware scan codes for Chromium/Electron & Windows Terminal compatibility
            scan_ctrl = user32.MapVirtualKeyW(0x11, 0)
            scan_v = user32.MapVirtualKeyW(0x56, 0)
            scan_enter = user32.MapVirtualKeyW(0x0D, 0)

            time.sleep(0.08)
            # Press Ctrl+V with scan codes
            user32.keybd_event(0x11, scan_ctrl, 0, 0)
            user32.keybd_event(0x56, scan_v, 0, 0)
            time.sleep(0.05)
            user32.keybd_event(0x56, scan_v, 0x0002, 0)
            user32.keybd_event(0x11, scan_ctrl, 0x0002, 0)

            if press_enter:
                time.sleep(0.08)
                user32.keybd_event(0x0D, scan_enter, 0, 0)
                time.sleep(0.05)
                user32.keybd_event(0x0D, scan_enter, 0x0002, 0)

            action_str = "Typed and submitted" if press_enter else "Pasted"
            preview = (text[:80] + "...") if len(text) > 80 else text
            clean_title = (win_title[:45] + "...") if len(win_title) > 45 else win_title
            return True, f'{action_str} into "{clean_title}":\n\"{preview}\"'
        except Exception as e:
            return True, f"Copied to clipboard, but keystroke simulation failed: {e}"
    elif sys.platform == "darwin":
        try:
            osa = 'tell application "System Events" to keystroke "v" using command down'
            if press_enter:
                osa += '\ntell application "System Events" to key code 36'
            subprocess.run(["osascript", "-e", osa], timeout=3)
            return True, "Pasted into active desktop window on macOS."
        except Exception as e:
            return True, f"Copied to macOS clipboard: {e}"
    else:
        try:
            args = ["xdotool", "key", "ctrl+v"]
            if press_enter:
                args += ["Return"]
            subprocess.run(args, timeout=3)
            return True, "Pasted into active desktop window via xdotool."
        except Exception:
            return True, "Copied to Linux clipboard."


def handle_remote_command(from_number: str, text: str) -> str:
    """Process incoming WhatsApp message and dispatch actions."""
    cfg = load_remote_config()
    clean_text = text.strip()
    allowed_numbers = cfg.get("allowed_numbers", [])
    auth_pin = cfg.get("auth_pin", "8765")

    # 1. Pairing & Authentication (Enforce Default-Deny & Zero PIN Leakage)
    if not allowed_numbers or from_number not in allowed_numbers:
        # Check if user is authenticating with PIN
        if clean_text.startswith("/auth"):
            parts = clean_text.split()
            if len(parts) >= 2 and parts[1] == auth_pin:
                allowed_numbers.append(from_number)
                cfg["allowed_numbers"] = allowed_numbers
                save_remote_config(cfg)
                return "✅ *Authentication Successful!*\nYour phone number is now paired with AegisBrain.\nType `/help` to see available commands."
            return "❌ *Incorrect PIN.* Usage: `/auth <PIN>`"
        return "🔒 *AegisBrain Access Restricted*\nYour number is not paired.\nSend `/auth <PIN>` with your secret PIN to unlock."

    # 2. Command Dispatch
    parts = clean_text.split(maxsplit=1)
    raw_cmd = parts[0].lower() if parts else ""
    # Strip @bot_username if clicked from Telegram menu or autocomplete
    cmd = raw_cmd.split("@")[0] if "@" in raw_cmd else raw_cmd
    arg = parts[1].strip() if len(parts) > 1 else ""

    if cmd == "/auth":
        if arg == auth_pin:
            if from_number not in allowed_numbers:
                allowed_numbers.append(from_number)
                cfg["allowed_numbers"] = allowed_numbers
                save_remote_config(cfg)
            return "✅ *Authentication Successful!*\nYour phone number is paired with AegisBrain.\nType `/help` to see available commands."
        return "❌ *Incorrect PIN.* Usage: `/auth <PIN>`"

    elif cmd in ("/help", "help", "/start", "/commands"):
        return (
            "🛡️ *AegisBrain Remote Commands:*\n\n"
            "📱 *Remote Navigation & Away Mode:*\n"
            "• */away <on|off>* - Toggle Away Mode & output streaming to phone\n"
            "• */nav [page]* - Browse terminal logs & outputs from phone\n"
            "• */swarm <task>* - Execute nested 4-tier multi-agent swarm\n\n"
            "⌨️ *Input and Voice Bridge:*\n"
            "• */type <text>* - Type text into active IDE chat and hit Enter\n"
            "• */prompt <text>* - Alias for /type (use with phone voice dictation)\n"
            "• */paste <text>* - Paste text without pressing Enter\n"
            "• */clip [text]* - Read or copy to workstation clipboard\n"
            "• */mode <chat|exec>* - Switch default behavior for plain text\n\n"
            "🔒 *Workstation Security:*\n"
            "• */lock* - Instantly lock screen & activate Away Mode streaming\n"
            "• */blockinput <on|off>* - Freeze/unfreeze desk keyboard and mouse\n"
            "• */alarm* - Sound warning alarm chimes on PC speakers\n"
            "• */sleep* - Turn off caffeinate and suspend PC\n"
            "• */shutdown* - Safely power off PC (15s countdown)\n\n"
            "💻 *Agent and Workspace:*\n"
            "• */status* - Workstation status, RAM, mode, caffeinate\n"
            "• */plan [task]* - Suggestion panel with 1-tap Telegram Poll\n"
            "• */orchestrate [task]* - Manager-Worker code pipeline\n"
            "• */moe* - FreeToken dynamic MoE latency scheduler & 7.5GB cap\n"
            "• */graph [symbol]* - AST Codebase Graph search\n"
            "• */task [add|done|history]* - Task memory lifecycle\n"
            "• */sandbox [code]* - Run isolated security audit\n"
            "• */caffeinate <on|off>* - Toggle anti-sleep wake-lock\n"
            "• */recall <query>* - Search memory and decisions\n"
            "• */git <status|diff|commit|push>* - Remote git operations\n"
            "• */artifacts* - View latest generated artifacts\n"
            "• */exec <command>* - Run any shell command"
        )

    elif cmd == "/status":
        caff = get_caffeinate_status()
        caff_str = f"Active ({caff['uptime_seconds']}s)" if caff["active"] else "Inactive"
        ws_dir = cfg.get("workspace_dir", str(Path.cwd()))
        try:
            prs = get_tracked_prs()
        except Exception:
            prs = []

        # Check git branch
        git_branch = "N/A"
        try:
            r = subprocess.run("git branch --show-current", shell=True, cwd=ws_dir, capture_output=True, text=True)
            git_branch = r.stdout.strip() or "detached"
        except Exception:
            pass

        return (
            f"💻 *AegisBrain Workstation Status*\n"
            f"• *Daemon:* Online (`http://127.0.0.1:8765`)\n"
            f"• *Caffeinate:* {caff_str}\n"
            f"• *Workspace:* `{Path(ws_dir).name}`\n"
            f"• *Git Branch:* `{git_branch}`\n"
            f"• *Tracked PRs:* {len(prs)} active\n"
            f"• *Platform:* {sys.platform.upper()}"
        )

    elif cmd == "/caffeinate":
        action = arg.lower()
        if action in ("on", "start", "enable"):
            ok, msg = enable_caffeinate()
            return f"☕ *Caffeinate ON:* {msg}"
        elif action in ("off", "stop", "disable"):
            ok, msg = disable_caffeinate()
            return f"💤 *Caffeinate OFF:* {msg}"
        else:
            status = get_caffeinate_status()
            state = "ACTIVE" if status["active"] else "INACTIVE"
            return f"☕ *Caffeinate is {state}* (uptime: {status['uptime_seconds']}s)"

    elif cmd == "/recall":
        if arg:
            results = search_memories(arg, limit=3)
            title = f"Matches for '{arg}'"
        else:
            results = get_recent_decisions(limit=3)
            title = "Recent Memories"

        if not results:
            return f"🔍 No memories found for: `{arg}`"

        lines = [f"🧠 *AegisBrain Recall ({title}):*"]
        for idx, r in enumerate(results, 1):
            lines.append(f"{idx}. *[{r.get('category')}] {r.get('title')}*\n   {r.get('decision')}")
        return "\n\n".join(lines)

    elif cmd == "/artifacts":
        res_text = get_latest_artifacts(arg)
        if not arg and cfg.get("provider", "telegram").lower() == "telegram" and cfg.get("telegram_token"):
            gemini_brain = Path.home() / ".gemini" / "antigravity-cli" / "brain"
            artifacts = list(gemini_brain.glob("*/*.md")) if gemini_brain.exists() else []
            artifacts.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            recent_artifacts = artifacts[:4]
            if recent_artifacts:
                art_buttons = [
                    [{"text": f"📖 Read #{idx}: {p.name[:20]}", "callback_data": f"artifact:{idx}"}]
                    for idx, p in enumerate(recent_artifacts, 1)
                ]
                send_telegram_inline_keyboard(from_number, res_text, art_buttons, config=cfg)
        return res_text

    elif cmd == "/git":
        subcmd = arg.strip()
        ws_dir = Path(cfg.get("workspace_dir", str(Path.cwd())))
        if not subcmd:
            subcmd = "status -s"
        full_git_cmd = f"git {subcmd}"
        res = execute_shell(full_git_cmd, cwd=ws_dir)
        return f"🐙 *Git (`{full_git_cmd}`):*\n```\n{res}\n```"

    elif cmd in ("/exec", "exec"):
        if not arg:
            return "Usage: `/exec <command>` (e.g. `/exec npm test`)"
        res = execute_shell(arg)
        return f"⚡ *Command Output (`{arg}`):*\n```\n{res}\n```"

    elif cmd in ("/windows", "/apps"):
        wins = get_desktop_windows()
        if not wins:
            return "🖥️ *Open Windows:* No visible desktop application windows found."
        lines = ["🖥️ *Open Desktop Windows:*"]
        for idx, w in enumerate(wins[:10], 1):
            tag = " 🟢 *[ACTIVE]*" if w["is_active"] else ""
            lines.append(f"{idx}. `{w['title']}`{tag}")
        lines.append("\nSend `/focus <name>` to bring any window to front.")
        return "\n".join(lines)

    elif cmd == "/focus":
        if not arg:
            return "Usage: `/focus <app or window name>` (e.g. `/focus powershell`, `/focus brave`)"
        ok, msg = focus_desktop_window(arg)
        icon = "🎯" if ok else "⚠️"
        return f"{icon} *Window Focus:* {msg}"

    elif cmd in ("/type", "/prompt", "/say"):
        if not arg:
            return "Usage: `/type <text or prompt>` (types into active IDE/agent chat and submits)"
        ok, msg = type_to_desktop(arg, press_enter=True)
        return f"✍️ *Agent Input:* {msg}"

    elif cmd == "/paste":
        if not arg:
            return "Usage: `/paste <text>` (pastes into active window without pressing Enter)"
        ok, msg = type_to_desktop(arg, press_enter=False)
        return f"📋 *Desktop Paste:* {msg}"

    elif cmd == "/clip":
        if arg:
            ok = copy_to_desktop_clipboard(arg)
            state = "Copied to" if ok else "Failed to copy to"
            return f"📋 *Clipboard:* {state} workstation clipboard."
        else:
            content = get_desktop_clipboard().strip()
            if not content:
                return "📋 *PC Clipboard:* (Empty)"
            preview = (content[:1000] + "\n... [truncated]") if len(content) > 1000 else content
            return f"📋 *PC Clipboard Contents:*\n```\n{preview}\n```"

    elif cmd == "/lock":
        ok, msg = remote_lock_workstation()
        set_away_mode(True)
        nav_buttons = [
            [
                {"text": "📟 View Terminal Logs", "callback_data": "nav:1"},
                {"text": "📊 Status", "callback_data": "cmd:status"},
            ],
            [
                {"text": "🐝 Swarm Health", "callback_data": "cmd:swarm"},
                {"text": "🔓 End Away Mode", "callback_data": "away:off"}
            ]
        ]
        lock_msg = (
            f"🔒 *Workstation Lock — Away Mode ACTIVATED!*\n\n"
            f"• *Desktop:* {msg}\n"
            "• *Away Mode:* Active (All terminal outputs & agent milestones will stream directly to your phone!)\n"
            "• *Navigation:* Tap buttons below or send `/nav` to browse output history.\n"
            "• Send `/away off` when returning to desk."
        )
        if cfg.get("provider", "telegram").lower() == "telegram" and cfg.get("telegram_token"):
            send_telegram_inline_keyboard(from_number, lock_msg, nav_buttons, config=cfg)
        return lock_msg

    elif cmd == "/away":
        subcmd = arg.lower().strip()
        if subcmd in ("on", "start", "enable"):
            set_away_mode(True)
            return "🔒 *Away Mode ON:*\nTerminal output streaming to phone is active. Send `/away off` when returning to desk."
        elif subcmd in ("off", "stop", "disable"):
            set_away_mode(False)
            return "👋 *Away Mode OFF:*\nWelcome back to your desk! Terminal output streaming paused."
        else:
            state = "ACTIVE" if is_away_mode_active() else "INACTIVE"
            return f"📱 *Away Mode:* `{state}`\nUsage: `/away <on|off>`"

    elif cmd == "/nav":
        mirror = get_terminal_mirror()
        arg_l = arg.lower().strip()
        page_num = int(arg_l) if arg_l.isdigit() else 1
        items, page, total_pages = mirror.get_page(page=page_num, page_size=4)
        if not items:
            return "📟 *Terminal Output Buffer:* (No logs recorded yet)\nRun commands or execute tasks to view live streams."

        lines = [f"📟 *Terminal Output Pager (Page {page}/{total_pages}):*", ""]
        for it in items:
            lines.append(f"⏱️ `[{it['time_str']} {it['source'].upper()}]`")
            p_txt = it["text"][:300] + ("..." if len(it["text"]) > 300 else "")
            lines.append(f"```\n{p_txt}\n```")

        buttons = [
            [
                {"text": "⬅️ Prev", "callback_data": f"nav:{page+1}"},
                {"text": "🔄 Refresh", "callback_data": f"nav:{page}"},
                {"text": "➡️ Next", "callback_data": f"nav:{max(1, page-1)}"},
            ],
            [
                {"text": "📋 Latest", "callback_data": "nav:1"},
                {"text": "📊 Status", "callback_data": "cmd:status"},
            ]
        ]
        pager_text = "\n".join(lines)
        if cfg.get("provider", "telegram").lower() == "telegram" and cfg.get("telegram_token"):
            send_telegram_inline_keyboard(from_number, pager_text, buttons, config=cfg)
        return pager_text

    elif cmd == "/swarm":
        from .swarm import run_nested_swarm, format_swarm_display
        task_query = arg or "Multi-Agent System Health & Contract Validation"
        send_telegram_message(from_number, f"🐝 *Spawning Hierarchical Swarm for:* `{task_query}`\nDomain Leads initializing (Frontier Boss + Hermes/Qwen workers)...", config=cfg)
        sim = bool(os.environ.get("PYTEST_CURRENT_TEST"))
        res = run_nested_swarm(task_query, simulate_workers=sim)
        return format_swarm_display(res)

    elif cmd == "/blockinput":
        state = arg.lower() in ("on", "true", "1", "lock", "enable")
        ok, msg = remote_block_input(state)
        return f"🛡️ *Physical Input Protection:*\n{msg}"

    elif cmd == "/alarm":
        ok, msg = remote_trigger_alarm()
        return f"🚨 *Alert Triggered:*\n{msg}"

    elif cmd == "/mode":
        target = arg.lower().strip()
        if target in ("swarm", "agent", "orchestrate", "auto"):
            cfg["default_mode"] = "swarm"
            save_remote_config(cfg)
            return "🐝 *Input Mode Switched to SWARM*\nAll regular prompts from phone will execute directly through the 4-tier autonomous agent swarm!"
        elif target in ("chat", "prompt", "voice", "type"):
            cfg["default_mode"] = "chat"
            save_remote_config(cfg)
            return "💬 *Input Mode Switched to CHAT*\nAll regular messages and phone voice dictations will now type directly into the active IDE window and submit!"
        elif target in ("exec", "shell", "cmd"):
            cfg["default_mode"] = "exec"
            save_remote_config(cfg)
            return "⚡ *Input Mode Switched to EXEC*\nUnprefixed messages will execute as shell commands."
        else:
            cur = cfg.get("default_mode", "swarm").upper()
            return f"🔄 *Current Input Mode:* `{cur}`\nUsage: `/mode <swarm|chat|exec>`\n• `swarm`: Prompts execute via multi-agent swarm\n• `chat`: Voice and messages type into IDE\n• `exec`: Messages run as shell commands"

    elif cmd == "/sleep":
        ok, msg = remote_suspend_pc()
        return f"🌙 *System Standby:* {msg}"

    elif cmd == "/shutdown":
        ok, msg = remote_shutdown_pc(delay_seconds=15)
        return f"🔌 *Workstation Shutdown:* {msg}\nTo cancel from PC: `shutdown /a`"

    elif cmd == "/config":
        gov_cfg = load_governance_config()
        if not arg:
            status_text = format_governance_status()
            if cfg.get("provider", "telegram").lower() == "telegram" and cfg.get("telegram_token"):
                config_buttons = [
                    [
                        {"text": "👑 Boss: Gemini 3.8", "callback_data": "cfg:mgr:gemini-3.8-flash-high"},
                        {"text": "👑 Boss: Claude 3.7", "callback_data": "cfg:mgr:claude-3-7-sonnet"},
                    ],
                    [
                        {"text": "🤖 Worker: Hermes", "callback_data": "cfg:wrk:hermes-agent"},
                        {"text": "🤖 Worker: Qwen 2.5", "callback_data": "cfg:wrk:qwen2.5-coder:7b"},
                    ],
                    [
                        {"text": "💾 Drive: P:\\ (Models)", "callback_data": "cfg:drv:P:\\aegis-brain\\models"},
                        {"text": "💾 Drive: C:\\", "callback_data": "cfg:drv:C:\\Users\\priya\\.aegis-brain\\models"},
                    ],
                    [
                        {"text": "📊 Telemetry Toggle", "callback_data": "cmd:config telemetry toggle"},
                        {"text": "📖 Telemetry Terms", "callback_data": "cmd:terms"},
                    ]
                ]
                send_telegram_inline_keyboard(from_number, status_text, config_buttons, config=cfg)
            return status_text

        subparts = arg.split(maxsplit=1)
        subk = subparts[0].lower()
        subval = subparts[1].strip() if len(subparts) > 1 else ""
        if subk == "manager" and subval:
            gov_cfg["manager_model"] = subval
            save_governance_config(gov_cfg)
            return f"👑 *Manager (Boss) Model Updated:* `{subval}`"
        elif subk == "worker" and subval:
            gov_cfg["worker_model"] = subval
            save_governance_config(gov_cfg)
            return f"🤖 *Worker Model Updated:* `{subval}`"
        elif subk in ("drive", "dir", "disk") and subval:
            gov_cfg["model_dir"] = subval
            save_governance_config(gov_cfg)
            os.environ["OLLAMA_MODELS"] = subval
            return f"💾 *Model Storage Disk Updated:* `{subval}`"
        elif subk == "telemetry":
            if subval.lower() == "toggle":
                enabled = not gov_cfg.get("telemetry_enabled", False)
            else:
                enabled = subval.lower() in ("on", "true", "enable", "1", "yes")
            gov_cfg["telemetry_enabled"] = enabled
            gov_cfg["telemetry_acknowledged"] = True
            save_governance_config(gov_cfg)
            state_str = "ENABLED (Opted-in)" if enabled else "DISABLED (Default-Deny)"
            return f"📊 *Telemetry Setting:* {state_str}\nSend `/terms` to review data privacy terms."
        else:
            return (
                "⚙️ *AegisBrain Config Usage:*\n"
                "• `/config` - Show current governance status & tap interactive buttons\n"
                "• `/config manager <model>` - Set Manager (e.g. `gemini-3.8-flash-high`, `claude-3-7-sonnet`)\n"
                "• `/config worker <model>` - Set Worker (`hermes-agent`, `qwen2.5-coder:7b`, `auto`)\n"
                "• `/config drive <path>` - Set model storage disk (e.g. `P:\\aegis-brain\\models`)\n"
                "• `/config telemetry <on|off>` - Toggle anonymous telemetry"
            )

    elif cmd == "/hardware":
        return format_hardware_report()

    elif cmd == "/report":
        issue_url = get_github_issue_url(title="User Issue via Telegram", error_desc=arg)
        diag_md = format_diagnostic_markdown()
        return (
            f"📋 *AegisBrain Diagnostic Report Generated:*\n\n"
            f"🔗 *Submit to GitHub (1-Click):*\n{issue_url}\n\n"
            f"```text\n{diag_md[:800]}\n... [truncated for mobile]\n```"
        )

    elif cmd == "/terms":
        return get_telemetry_terms()

    elif cmd == "/env":
        return format_environment_report()

    elif cmd == "/taste":
        return format_taste_display()

    elif cmd == "/plan":
        task_query = arg or "Next Development Milestone"
        suggs = create_default_suggestions_for_task(task_query)
        panel_text = format_suggestion_panel(task_query, suggs, recommended_index=0)
        # Dispatch native Telegram poll for 1-tap thumb vote
        poll_opts = [s["label"] for s in suggs]
        send_telegram_poll(from_number, f"Decision: {task_query[:250]}", poll_opts, config=cfg)
        return panel_text

    elif cmd == "/orchestrate":
        if not arg or arg.lower() in ("stats", "summary"):
            return format_distillation_report()
        res = run_manager_worker_pipeline(arg, simulate_worker=True)
        return (
            f"👑 *Manager-Worker Execution Complete:*\n\n"
            f"• *Task:* {arg}\n"
            f"• *Manager (Boss):* `{res['manager_model']}`\n"
            f"• *Worker (Synthesizer):* `{res['worker_model']}` ({res['hardware_tier']})\n"
            f"• *Tokens Saved:* `+{res['tokens_saved_estimate']}` tokens\n"
            f"• *Critique:* {res['manager_critique']}\n\n"
            f"```python\n{res['final_code']}\n```"
        )

    elif cmd == "/scout":
        from .skill_scout import run_skill_scout, get_discovered_skills, format_skill_scout_display
        if arg and arg.lower() in ("run", "scan", "update"):
            run_skill_scout()
        return format_skill_scout_display()

    elif cmd == "/moe":
        from .moe_engine import format_tier_status_display
        return format_tier_status_display()

    elif cmd == "/graph":
        from .code_graph import get_active_graph
        graph = get_active_graph()
        if arg:
            matches = graph.query_graph(arg)
            if not matches:
                return f"🔍 *Code Graph Search:* No matches found for `{arg}`."
            lines = [f"🔍 *Code Graph Matches for `{arg}`:*", ""]
            for m in matches[:6]:
                lines.append(f"• `{m['name']}` [{m['kind'].upper()}] in `{m['file_path']}`")
            return "\n".join(lines)
        return graph.format_summary()

    elif cmd == "/task":
        from .task_lifecycle import create_task, complete_task, format_tasks_display
        subparts = arg.split(maxsplit=1) if arg else []
        subcmd = subparts[0].lower() if subparts else ""
        subarg = subparts[1].strip() if len(subparts) > 1 else ""

        if subcmd == "done" and subarg:
            try:
                tid = int(subarg.split()[0])
                ok = complete_task(tid)
                if ok:
                    return f"✅ *Task [#{tid}] Completed!*\nArchived to history. Active memory kept lean."
                return f"❌ *Task [#{tid}] not found.*"
            except ValueError:
                return "Usage: `/task done <id>`"
        elif subcmd == "add" and subarg:
            tid = create_task(title=subarg)
            return f"📌 *Active Task Registered:* `[#{tid}] {subarg}`"
        elif subcmd == "history":
            return format_tasks_display(show_history=True)
        else:
            return format_tasks_display(show_history=False)

    elif cmd == "/sandbox":
        from .sandbox import RedTeamAuditor, format_sandbox_report
        code_to_audit = arg or "print('Sandbox test')"
        audit = RedTeamAuditor.audit_code(code_to_audit)
        return format_sandbox_report(audit)

    elif clean_text.startswith("/"):
        KNOWN_COMMANDS = [
            "/help", "/status", "/config", "/hardware", "/report", "/terms", "/env", "/taste", "/plan", "/orchestrate",
            "/scout", "/moe", "/graph", "/task", "/sandbox", "/away", "/nav", "/swarm",
            "/caffeinate", "/mode", "/type", "/prompt", "/paste", "/clip",
            "/lock", "/recall", "/git", "/artifacts", "/windows", "/apps",
            "/focus", "/blockinput", "/alarm", "/sleep", "/shutdown", "/exec",
            "/start", "/auth", "/commands", "/say"
        ]
        matches = difflib.get_close_matches(cmd, KNOWN_COMMANDS, n=2, cutoff=0.4)
        if matches:
            suggested = matches[0]
            buttons = [
                [{"text": f"▶️ Run {suggested}", "callback_data": f"cmd:{suggested.lstrip('/')}"}],
                [{"text": "📖 Show /help", "callback_data": "cmd:help"}]
            ]
            msg = (
                f"❓ *Unknown Command:* `{raw_cmd}`\n\n"
                f"💡 *Did you mean:* `{suggested}`?\n\n"
                f"Tap below to run `{suggested}` or type `/help`."
            )
            if cfg.get("provider", "telegram").lower() == "telegram" and cfg.get("telegram_token"):
                send_telegram_inline_keyboard(from_number, msg, buttons, config=cfg)
            return msg
        return f"❓ *Unknown Command:* `{raw_cmd}`\n\nType `/help` to see all available commands.\n(Slash commands are never typed into active IDE windows)."

    else:
        # User sent a plain prompt/instruction from mobile or desktop remote!
        # Send typing action to Telegram immediately
        send_telegram_chat_action(from_number, "typing", config=cfg)
        ok, msg = type_to_desktop(clean_text, press_enter=True)
        preview = (clean_text[:120] + "...") if len(clean_text) > 120 else clean_text
        return (
            f"✍️ *Prompt Sent to Coding Session:*\n"
            f"\"{preview}\"\n\n"
            f"• *Status:* {msg}\n"
            f"• *Live Streaming:* Active (Antigravity outputs will stream to your phone word-for-word).\n"
            f"_Tip: Use `/nav` to browse terminal logs or `/status` for health._"
        )


def format_twiml_response(reply_text: str) -> str:
    """Wrap reply in standard TwiML XML."""
    escaped = xml.sax.saxutils.escape(reply_text)
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f"<Response>\n"
        f"    <Message>{escaped}</Message>\n"
        f"</Response>"
    )


def handle_twilio_webhook(post_params: Dict[str, Any]) -> str:
    """Handle incoming Twilio webhook HTTP request and return TwiML."""
    # Twilio sends form data: From, Body, To, AccountSid
    from_number = post_params.get("From", [""])[0] if isinstance(post_params.get("From"), list) else post_params.get("From", "")
    body_text = post_params.get("Body", [""])[0] if isinstance(post_params.get("Body"), list) else post_params.get("Body", "")

    # Execute and reply
    reply = handle_remote_command(from_number, body_text)
    return format_twiml_response(reply)


def run_remote_setup_wizard() -> None:
    """Interactive CLI wizard to configure Telegram or WhatsApp bridge."""
    cfg = load_remote_config()
    print("=== AegisBrain Mobile Remote Bridge Setup ===")
    print("Choose your preferred messaging channel:")
    print("  [1] Telegram (Recommended: 30-second setup, zero verification, no public URL/tunnel needed)")
    print("  [2] WhatsApp (via Twilio Sandbox - requires Account SID & Auth Token)")
    choice = input("Select channel [1/2, default: 1]: ").strip() or "1"

    cur_pin = cfg.get("auth_pin", "8765")
    cur_ws = cfg.get("workspace_dir", str(Path.cwd()))

    if choice == "2":
        # Twilio WhatsApp Setup
        print("\n--- Twilio WhatsApp Setup ---")
        sid = input(f"Twilio Account SID [{cfg.get('account_sid', '')}]: ").strip() or cfg.get("account_sid", "")
        token = input("Twilio Auth Token: ").strip() or cfg.get("auth_token", "")
        tw_num = input(f"Twilio WhatsApp Number [{cfg.get('twilio_number', 'whatsapp:+14155238886')}]: ").strip() or cfg.get("twilio_number", "whatsapp:+14155238886")
        my_num = input("Your Personal WhatsApp Number (e.g. +919876543210): ").strip()
        pin = input(f"Secret Pairing PIN [{cur_pin}]: ").strip() or cur_pin
        ws = input(f"Default Workspace Directory [{cur_ws}]: ").strip() or cur_ws

        allowed = cfg.get("allowed_numbers", [])
        if my_num:
            if not my_num.startswith("whatsapp:"):
                my_num = f"whatsapp:{my_num}"
            if my_num not in allowed:
                allowed.append(my_num)

        cfg["provider"] = "twilio"
        cfg["account_sid"] = sid
        cfg["auth_token"] = token
        cfg["twilio_number"] = tw_num
        cfg["allowed_numbers"] = allowed
        cfg["auth_pin"] = pin
        cfg["workspace_dir"] = ws
        save_remote_config(cfg)

        print("\n[SUCCESS] Twilio configuration saved to:", get_remote_config_path())
        print("Next step: Set your Twilio Sandbox Webhook URL to:")
        print("  http://<your-host-or-tunnel>:8765/webhook/whatsapp (HTTP POST)")

    else:
        # Telegram Setup
        print("\n--- Telegram Bot Setup (Recommended) ---")
        print("Instructions:")
        print("  1. Open Telegram on your phone and search for: @BotFather")
        print("  2. Send '/newbot' to BotFather, then enter a Name and a Username (e.g. MyAegis_bot)")
        print("  3. BotFather will reply with an HTTP API token (e.g. 7123456789:ABCdefGHI...)")
        print()
        token = input("Paste your Telegram Bot Token: ").strip() or cfg.get("telegram_token", "")
        chat_id = input(f"Your Telegram Chat ID (optional, or message your bot and send /auth {cur_pin}): ").strip() or cfg.get("telegram_chat_id", "")
        pin = input(f"Secret Pairing PIN [{cur_pin}]: ").strip() or cur_pin
        ws = input(f"Default Workspace Directory [{cur_ws}]: ").strip() or cur_ws

        cfg["provider"] = "telegram"
        cfg["telegram_token"] = token
        if chat_id:
            cfg["telegram_chat_id"] = chat_id
        cfg["auth_pin"] = pin
        cfg["workspace_dir"] = ws
        save_remote_config(cfg)

        print("\n[SUCCESS] Telegram Bot configuration saved to:", get_remote_config_path())
        print("Your bot is ready! No webhooks, ngrok, or public URLs required.")
        print("To start the mobile bridge: aegis remote start")


def show_remote_status() -> None:
    """Display current remote bridge configuration."""
    cfg = load_remote_config()
    caff = get_caffeinate_status()
    provider = cfg.get("provider", "telegram").upper()
    caff_str = f"ACTIVE ({caff['uptime_seconds']}s)" if caff["active"] else "INACTIVE"

    print("=== AegisBrain Mobile Remote Bridge ===")
    print(f"Provider:        {provider}")
    if provider == "TELEGRAM":
        tok = cfg.get("telegram_token", "")
        masked_tok = f"{tok[:8]}...{tok[-4:]}" if len(tok) > 12 else "(not set)"
        print(f"Bot Token:       {masked_tok}")
        print(f"Chat ID:         {cfg.get('telegram_chat_id') or 'Auto-pairs on first message'}")
        print(f"Transport:       Direct Long-Polling (No public IP / webhook required)")
    else:
        sid = cfg.get("account_sid", "")
        masked_sid = f"{sid[:6]}...{sid[-4:]}" if len(sid) > 10 else "(not set)"
        allowed = cfg.get("allowed_numbers", [])
        print(f"Account SID:     {masked_sid}")
        print(f"Twilio Number:   {cfg.get('twilio_number', '(not set)')}")
        print(f"Allowed Numbers: {', '.join(allowed) if allowed else 'Any (protected by PIN)'}")
        print("Webhook URL:     http://127.0.0.1:8765/webhook/whatsapp")

    print(f"Pairing PIN:     {cfg.get('auth_pin', '8765')}")
    print(f"Workspace Dir:   {cfg.get('workspace_dir', str(Path.cwd()))}")
    print(f"Caffeinate:      {caff_str}")


def run_remote_test(msg: str = "🟢 AegisBrain Remote Test Ping!") -> None:
    """Send a test message to the configured phone channel."""
    cfg = load_remote_config()
    provider = cfg.get("provider", "telegram").lower()

    if provider == "telegram":
        chat_id = cfg.get("telegram_chat_id", "")
        if not chat_id:
            print("[INFO] No Telegram chat ID saved yet.")
            print("Message your Telegram bot from your phone first (send /auth <PIN>), then run this test again.")
            return
        print(f"[AegisBrain] Sending test ping via Telegram to Chat ID {chat_id}...")
        ok, resp = send_telegram_message(chat_id, msg, config=cfg)
        if ok:
            print("[SUCCESS] Telegram message dispatched! Check your phone.")
        else:
            print(f"[ERROR] Failed to send Telegram message: {resp}")
    else:
        allowed = cfg.get("allowed_numbers", [])
        if not allowed:
            print("[ERROR] No destination WhatsApp number configured. Run 'aegis remote setup' first.")
            return
        to_number = allowed[0]
        print(f"[AegisBrain] Sending test ping to {to_number}...")
        ok, resp = send_whatsapp_message(to_number, msg, config=cfg)
        if ok:
            print("[SUCCESS] WhatsApp message dispatched! Check your phone.")
        else:
            print(f"[ERROR] Failed to send WhatsApp message: {resp}")


def start_remote_session(foreground_poll: bool = False) -> None:
    """Activate Caffeinate, ensure daemon is running, and begin remote listener."""
    cfg = load_remote_config()
    provider = cfg.get("provider", "telegram").lower()
    print("=== Starting AegisBrain Remote Session ===")

    # 1. Enable Caffeinate
    ok, msg = enable_caffeinate()
    print(f"[Caffeinate] {msg}")

    # 2. Check daemon
    from .service import is_daemon_running, start_daemon
    if not is_daemon_running():
        print("[Daemon] Starting background Aegis daemon on :8765...")
        start_daemon()
    else:
        print("[Daemon] Aegis daemon is active on http://127.0.0.1:8765")

    # 3. Send ready notification
    ws_name = Path(cfg.get("workspace_dir", str(Path.cwd()))).name
    greeting = (
        "🟢 *AegisBrain Remote Session Active!*\n"
        "• *Caffeinate:* Active (System sleep prevented)\n"
        f"• *Workspace:* `{ws_name}`\n"
        "Send `/help` to view available commands."
    )

    if provider == "telegram":
        chat_id = cfg.get("telegram_chat_id", "")
        if chat_id:
            send_telegram_message(chat_id, greeting, config=cfg)
            print(f"[Telegram] Notification sent to chat ID {chat_id}")

        print("\n[READY] Telegram Remote Listener is active!")
        print("You can safely leave your workstation. Send commands from your phone via Telegram.")
        print("To stop remote session from this PC: aegis caffeinate off")

        if foreground_poll:
            poll_telegram_updates()
        else:
            # Run in daemon thread if not already running
            t = threading.Thread(target=poll_telegram_updates, daemon=True, name="AegisTelegramPoll")
            t.start()
    else:
        allowed = cfg.get("allowed_numbers", [])
        if allowed and cfg.get("account_sid") and cfg.get("auth_token"):
            send_whatsapp_message(allowed[0], greeting, config=cfg)
            print(f"[WhatsApp] Notification sent to {allowed[0]}")
        print("\n[READY] You can now safely leave your workstation!")
        print("All commands, commits, and terminal outputs can be operated via WhatsApp.")
        print("To stop remote session from this PC: aegis caffeinate off")
