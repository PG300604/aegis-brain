_clipboard_memory_buffer = ""
"""Remote WhatsApp & Shell Command Bridge for AegisBrain.

Enables secure remote control of AI coding agents, shell execution,
git workflows, caffeinate toggle, and PC shutdown via WhatsApp.
Zero external dependencies (pure Python standard library).
"""

import base64
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


def send_telegram_message(chat_id: str, body: str, config: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    """Send an outbound Telegram message via Telegram Bot API using standard library urllib."""
    cfg = config or load_remote_config()
    token = cfg.get("telegram_token", "")
    if not token:
        return False, "Telegram Bot Token not configured in ~/.aegis-brain/remote.json"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": body[:4000],
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
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
                return True, "Message delivered"
            return False, data.get("description", "Unknown Telegram error")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        return False, f"Telegram HTTP {e.code}: {err}"
    except Exception as e:
        return False, f"Telegram network error: {e}"


def poll_telegram_updates(stop_event: Optional[threading.Event] = None, on_ready_callback: Optional[Any] = None) -> None:
    """Long-polling daemon for Telegram Bot API. Requires zero public IP, tunnel, or webhook!"""
    cfg = load_remote_config()
    token = cfg.get("telegram_token", "")
    if not token:
        print("[Telegram] Bot token not set. Run 'aegis remote setup' to configure Telegram.")
        return

    offset = 0
    print("[Telegram] Bot polling listener active. Ready for commands from your phone!")
    if on_ready_callback:
        try:
            on_ready_callback()
        except Exception:
            pass

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

        # WhatsApp truncation limit
        if len(res) > 1300:
            res = res[:1300] + "\n... [output truncated]"
        return res
    except subprocess.TimeoutExpired:
        return f"⏱️ Command timed out after {timeout} seconds."
    except Exception as e:
        return f"❌ Command execution failed: {str(e)}"


def get_latest_artifacts() -> str:
    """Scan for recently generated brain artifacts and reports."""
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
    recent = artifacts[:4]

    lines = ["📑 *Recent Workspace Artifacts:*"]
    for idx, p in enumerate(recent, 1):
        mtime = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).strftime("%H:%M UTC")
        lines.append(f"{idx}. *{p.name}* ({mtime})\n   Path: `{p.parent.name}/{p.name}`")
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
    windows = get_desktop_windows()
    for w in windows:
        if keyword.lower() in w["title"].lower():
            hwnd = w["hwnd"]
            user32.ShowWindow(hwnd, 9)  # SW_RESTORE
            user32.SetForegroundWindow(hwnd)
            return True, f'Activated window: "{w["title"]}"'
    return False, f'No open window found matching "{keyword}".'


def type_to_desktop(text: str, press_enter: bool = True) -> Tuple[bool, str]:
    """Copy text to clipboard and simulate Ctrl+V and optional Enter into the active desktop window."""
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
    cmd = parts[0].lower() if parts else ""
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
            "⌨️ *Input and Voice Bridge:*\n"
            "• */type <text>* - Type text into active IDE chat and hit Enter\n"
            "• */prompt <text>* - Alias for /type (use with phone voice dictation)\n"
            "• */paste <text>* - Paste text without pressing Enter\n"
            "• */clip [text]* - Read or copy to workstation clipboard\n"
            "• */mode <chat|exec>* - Switch default behavior for plain text\n\n"
            "🔒 *Workstation Security:*\n"
            "• */lock* - Instantly lock screen (agents and caffeinate keep running!)\n"
            "• */blockinput <on|off>* - Freeze/unfreeze desk keyboard and mouse\n"
            "• */alarm* - Sound warning alarm chimes on PC speakers\n"
            "• */sleep* - Turn off caffeinate and suspend PC\n"
            "• */shutdown* - Safely power off PC (15s countdown)\n\n"
            "💻 *Agent and Workspace:*\n"
            "• */status* - Workstation status, RAM, mode, caffeinate\n"
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
        return get_latest_artifacts()

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
        return f"🔒 *Workstation Lock:*\n{msg}\nCaffeinate and background AI tasks remain 100% active."

    elif cmd == "/blockinput":
        state = arg.lower() in ("on", "true", "1", "lock", "enable")
        ok, msg = remote_block_input(state)
        return f"🛡️ *Physical Input Protection:*\n{msg}"

    elif cmd == "/alarm":
        ok, msg = remote_trigger_alarm()
        return f"🚨 *Alert Triggered:*\n{msg}"

    elif cmd == "/mode":
        target = arg.lower().strip()
        if target in ("chat", "prompt", "voice", "type"):
            cfg["default_mode"] = "chat"
            save_remote_config(cfg)
            return "💬 *Input Mode Switched to CHAT*\nAll regular messages and phone voice dictations will now type directly into the active IDE window and submit!"
        elif target in ("exec", "shell", "cmd"):
            cfg["default_mode"] = "exec"
            save_remote_config(cfg)
            return "⚡ *Input Mode Switched to EXEC*\nUnprefixed messages will execute as shell commands."
        else:
            cur = cfg.get("default_mode", "exec").upper()
            return f"🔄 *Current Input Mode:* `{cur}`\nUsage: `/mode <chat|exec>`\n• `chat`: Voice and messages type into IDE\n• `exec`: Messages run as shell commands"

    elif cmd == "/sleep":
        ok, msg = remote_suspend_pc()
        return f"🌙 *System Standby:* {msg}"

    elif cmd == "/shutdown":
        ok, msg = remote_shutdown_pc(delay_seconds=15)
        return f"🔌 *Workstation Shutdown:* {msg}\nTo cancel from PC: `shutdown /a`"

    else:
        def_mode = cfg.get("default_mode", "exec").lower()
        if def_mode in ("chat", "prompt", "voice", "type"):
            ok, msg = type_to_desktop(clean_text, press_enter=True)
            return f"✍️ *Agent Input (Chat Mode):* {msg}"
        else:
            res = execute_shell(clean_text)
            return f"⚡ *Output (`{clean_text}`):*\n```\n{res}\n```"


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
