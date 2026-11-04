"""Environment & Software Dependency Inspector for AegisBrain.

Inspects workstation tools (Ollama, OpenCode, Hermes, Winget, uv, GPU VRAM)
and handles software requirements. If administrative access or user interaction is
needed while the user is away, it safely queues the obligation in SQLite and alerts
via Telegram, reminding the user in the next interactive session.
"""

import os
import sys
import shutil
import sqlite3
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

from .config import get_db_path, get_aegis_dir
from .hardware import get_hardware_status


def init_environment_table() -> None:
    """Create pending_installations table if it does not exist."""
    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pending_installations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_name TEXT NOT NULL,
                installer TEXT NOT NULL,
                reason TEXT NOT NULL,
                requires_admin INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def check_tool(cmd: str, version_args: Optional[List[str]] = None) -> Dict[str, Any]:
    """Check if an executable exists on the system PATH and query its version."""
    path = shutil.which(cmd)
    if not path:
        return {"status": "MISSING", "path": None, "version": None}

    args = version_args or ["--version"]
    try:
        # Use shell=True on Windows for .cmd or .bat scripts (e.g. npm globals like opencode.cmd)
        r = subprocess.run(
            [cmd] + args,
            shell=(sys.platform == "win32"),
            capture_output=True,
            text=True,
            timeout=5,
        )
        lines = (r.stdout or r.stderr or "").strip().splitlines()
        ver = lines[0] if lines else "Installed"
        return {"status": "INSTALLED", "path": path, "version": ver}
    except Exception as e:
        return {"status": "INSTALLED", "path": path, "version": f"Installed ({e})"}


def get_gpu_vram() -> Optional[Dict[str, Any]]:
    """Inspect NVIDIA GPU VRAM if nvidia-smi is available."""
    if not shutil.which("nvidia-smi"):
        return None
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if r.returncode == 0 and r.stdout.strip():
            parts = [p.strip() for p in r.stdout.strip().split(",")]
            if len(parts) >= 3:
                return {
                    "name": parts[0],
                    "total_mb": int(parts[1]),
                    "free_mb": int(parts[2]),
                }
    except Exception:
        pass
    return None


def get_ollama_status() -> Dict[str, Any]:
    """Inspect local Ollama installation, daemon reachability, and downloaded models."""
    path = shutil.which("ollama")
    if not path:
        return {"installed": False, "running": False, "models": []}

    # Check if daemon is responding
    running = False
    models: List[str] = []
    try:
        import urllib.request
        import json
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags", headers={"User-Agent": "AegisBrain/1.0"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            if resp.status == 200:
                running = True
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", [])]
    except Exception:
        pass

    return {
        "installed": True,
        "path": path,
        "running": running,
        "models": models,
    }


def get_pending_installations() -> List[Dict[str, Any]]:
    """Instant sub-millisecond query for pending setup obligations."""
    init_environment_table()
    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM pending_installations WHERE status = 'pending'")
        return [dict(r) for r in cursor.fetchall()]


def scan_environment() -> Dict[str, Any]:
    """Comprehensive scan of workstation tools, model runtimes, and GPU."""
    init_environment_table()
    hw = get_hardware_status()
    gpu = get_gpu_vram()
    ollama_info = get_ollama_status()

    tools = {
        "ollama": check_tool("ollama", ["--version"]),
        "opencode": check_tool("opencode", ["--version"]),
        "hermes": check_tool("hermes", ["--version"]),
        "winget": check_tool("winget", ["--version"]),
        "uv": check_tool("uv", ["--version"]),
        "git": check_tool("git", ["--version"]),
    }

    # Query pending installations from SQLite
    db_p = get_db_path()
    pending: List[Dict[str, Any]] = []
    with sqlite3.connect(db_p) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM pending_installations WHERE status = 'pending'")
        pending = [dict(r) for r in cursor.fetchall()]

    return {
        "hardware": hw,
        "gpu": gpu,
        "ollama": ollama_info,
        "tools": tools,
        "pending_installations": pending,
    }


def queue_pending_installation(package_name: str, installer: str, reason: str, requires_admin: bool = False) -> int:
    """Queue a required software tool into memory if administrative access or user interaction is needed."""
    init_environment_table()
    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        cursor = conn.execute(
            """
            INSERT INTO pending_installations (package_name, installer, reason, requires_admin, status)
            VALUES (?, ?, ?, ?, 'pending')
            """,
            (package_name, installer, reason, 1 if requires_admin else 0),
        )
        conn.commit()
        row_id = cursor.lastrowid or 0

    # Notify via Telegram if configured
    try:
        from .remote import send_remote_message, load_remote_config
        cfg = load_remote_config()
        chat_id = cfg.get("telegram_chat_id", "")
        if chat_id:
            admin_tag = "🔐 (Requires Administrator Access)" if requires_admin else "📦 (Standard Install)"
            body = (
                f"⚠️ *AegisBrain Environment Notice:*\n\n"
                f"Tool `{package_name}` {admin_tag} is needed for:\n_{reason}_\n\n"
                f"AegisBrain has preserved this requirement in memory. Run `aegis env --install {package_name}` when at your desk."
            )
            send_remote_message(chat_id, body, config=cfg)
    except Exception:
        pass

    return row_id


def resolve_pending_installation(install_id: int) -> bool:
    """Mark a queued installation as completed."""
    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        cursor = conn.execute("UPDATE pending_installations SET status = 'completed' WHERE id = ?", (install_id,))
        conn.commit()
        return cursor.rowcount > 0


def format_environment_report() -> str:
    """Format structured report of installed tools, runtimes, and pending queues."""
    env = scan_environment()
    hw = env["hardware"]
    gpu = env["gpu"]
    ollama = env["ollama"]
    tools = env["tools"]
    pending = env["pending_installations"]

    lines = [
        "🛠️ *AegisBrain Workstation Environment Profile*",
        f"• *RAM:* {hw['total_ram_gb']} GB total ({hw['avail_ram_gb']} GB available for multitasking)",
    ]

    if gpu:
        lines.append(f"• *GPU:* `{gpu['name']}` ({gpu['free_mb']} MB free / {gpu['total_mb']} MB VRAM)")
    else:
        lines.append("• *GPU:* Integrated / CPU-only inference")

    lines.append("")
    lines.append("📦 *Installed Agent & Model Runtimes:*")
    for t_name, t_info in tools.items():
        icon = "✅" if t_info["status"] == "INSTALLED" else "❌"
        ver = f"(`{t_info['version']}`)" if t_info["version"] else ""
        lines.append(f"• {icon} *{t_name}*: {t_info['status']} {ver}")

    lines.append("")
    lines.append("🦙 *Ollama Status:*")
    lines.append(f"• *Daemon:* {'🟢 Online (http://127.0.0.1:11434)' if ollama['running'] else '🔴 Offline (Run `ollama serve`)'}")
    if ollama["models"]:
        lines.append(f"• *Pulled Models:* {', '.join([f'`{m}`' for m in ollama['models']])}")
    else:
        lines.append("• *Pulled Models:* (None currently pulled. Aegis recommends: `ollama pull qwen2.5-coder:7b`)")

    if pending:
        lines.append("")
        lines.append(f"⏳ *Pending Setup Tasks ({len(pending)} queued):*")
        for p in pending:
            admin_icon = "🔐 Admin" if p["requires_admin"] else "📦 User"
            lines.append(f"• *[{admin_icon}] {p['package_name']}* ({p['installer']}): {p['reason']}")
        lines.append("💡 *Tip:* Run `aegis env --install <name>` when ready.")

    return "\n".join(lines)
