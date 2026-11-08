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


_HOST_CAPABILITIES_CACHE: Optional[Dict[str, Any]] = None


def detect_host_platform() -> Dict[str, Any]:
    """Detect host OS, shell, and package manager across Windows, macOS, and Linux."""
    # OS detection
    if sys.platform == "win32":
        os_name = "windows"
    elif sys.platform == "darwin":
        os_name = "macos"
    else:
        os_name = "linux"

    # Shell detection
    shell_env = os.environ.get("SHELL", "")
    if shell_env and any(s in shell_env.lower() for s in ("bash", "zsh", "fish", "sh")):
        shell = os.path.basename(shell_env).lower()
    elif os_name == "windows":
        if "PSModulePath" in os.environ or "POWERSHELL_DISTRIBUTION_CHANNEL" in os.environ or shutil.which("powershell"):
            shell = "powershell"
        else:
            shell = "cmd"
    else:
        shell = os.path.basename(shell_env) if shell_env else "bash"

    # Package manager detection
    pkg_manager = "unknown"
    if os_name == "windows":
        for pm in ("winget", "choco", "scoop"):
            if shutil.which(pm):
                pkg_manager = pm
                break
    elif os_name == "macos":
        if shutil.which("brew"):
            pkg_manager = "brew"
    else:  # linux
        for pm in ("brew", "apt", "pacman", "dnf"):
            if shutil.which(pm):
                pkg_manager = pm
                break

    return {
        "os": os_name,
        "shell": shell,
        "pkg_manager": pkg_manager,
    }


def init_host_capabilities_table() -> None:
    """Create host_capabilities table in SQLite brain.db if not exists."""
    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS host_capabilities (
                id INTEGER PRIMARY KEY DEFAULT 1,
                os TEXT NOT NULL,
                shell TEXT NOT NULL,
                pkg_manager TEXT NOT NULL,
                has_ffmpeg INTEGER DEFAULT 0,
                has_whisper INTEGER DEFAULT 0,
                has_ollama INTEGER DEFAULT 0,
                has_hermes INTEGER DEFAULT 0,
                has_tiling INTEGER DEFAULT 0,
                has_vim INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def save_host_capabilities(doctor_results: Dict[str, Any]) -> None:
    """Save doctor evaluation results to host_capabilities table and update memory cache."""
    global _HOST_CAPABILITIES_CACHE
    init_host_capabilities_table()

    platform_info = doctor_results.get("platform", {})
    if not platform_info:
        platform_info = detect_host_platform()

    tiers = doctor_results.get("tiers", {})
    sensory = tiers.get("sensory_accelerators", {}).get("items", doctor_results.get("sensory_accelerators", {}))
    workers = tiers.get("token_arbitrage_workers", {}).get("items", doctor_results.get("token_arbitrage_workers", {}))
    modifiers = tiers.get("workstation_modifiers", {}).get("items", doctor_results.get("workstation_modifiers", {}))

    has_ffmpeg = 1 if sensory.get("ffmpeg", {}).get("status") == "INSTALLED" else 0
    has_whisper = 1 if sensory.get("whisper", {}).get("status") == "INSTALLED" else 0
    has_ollama = 1 if workers.get("ollama", {}).get("status") == "INSTALLED" else 0
    has_hermes = 1 if workers.get("hermes", {}).get("status") == "INSTALLED" else 0
    has_tiling = 1 if modifiers.get("komorebi", {}).get("status") == "INSTALLED" else 0
    has_vim = 1 if modifiers.get("vim", {}).get("status") == "INSTALLED" else 0

    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        conn.execute("""
            INSERT INTO host_capabilities (
                id, os, shell, pkg_manager,
                has_ffmpeg, has_whisper, has_ollama, has_hermes, has_tiling, has_vim, updated_at
            ) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                os = excluded.os,
                shell = excluded.shell,
                pkg_manager = excluded.pkg_manager,
                has_ffmpeg = excluded.has_ffmpeg,
                has_whisper = excluded.has_whisper,
                has_ollama = excluded.has_ollama,
                has_hermes = excluded.has_hermes,
                has_tiling = excluded.has_tiling,
                has_vim = excluded.has_vim,
                updated_at = CURRENT_TIMESTAMP
        """, (
            platform_info.get("os", "unknown"),
            platform_info.get("shell", "unknown"),
            platform_info.get("pkg_manager", "unknown"),
            has_ffmpeg, has_whisper, has_ollama, has_hermes, has_tiling, has_vim
        ))
        conn.commit()

    _HOST_CAPABILITIES_CACHE = {
        "os": platform_info.get("os", "unknown"),
        "shell": platform_info.get("shell", "unknown"),
        "pkg_manager": platform_info.get("pkg_manager", "unknown"),
        "has_ffmpeg": bool(has_ffmpeg),
        "has_whisper": bool(has_whisper),
        "has_ollama": bool(has_ollama),
        "has_hermes": bool(has_hermes),
        "has_tiling": bool(has_tiling),
        "has_vim": bool(has_vim),
        "standard_desktop_mode": (not bool(has_tiling) or not bool(has_vim)),
        "updated_at": "CURRENT_TIMESTAMP",
    }


def get_host_capabilities() -> Dict[str, Any]:
    """Retrieve host capabilities with sub-1ms in-memory cache lookup."""
    global _HOST_CAPABILITIES_CACHE
    if _HOST_CAPABILITIES_CACHE is not None:
        return _HOST_CAPABILITIES_CACHE

    init_host_capabilities_table()
    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM host_capabilities WHERE id = 1").fetchone()

    if row is None:
        results = run_doctor()
        save_host_capabilities(results)
        return _HOST_CAPABILITIES_CACHE or {}

    has_t = bool(row["has_tiling"])
    has_v = bool(row["has_vim"])
    _HOST_CAPABILITIES_CACHE = {
        "os": row["os"],
        "shell": row["shell"],
        "pkg_manager": row["pkg_manager"],
        "has_ffmpeg": bool(row["has_ffmpeg"]),
        "has_whisper": bool(row["has_whisper"]),
        "has_ollama": bool(row["has_ollama"]),
        "has_hermes": bool(row["has_hermes"]),
        "has_tiling": has_t,
        "has_vim": has_v,
        "standard_desktop_mode": (not has_t or not has_v),
        "updated_at": str(row["updated_at"]) if "updated_at" in row.keys() else "",
    }
    return _HOST_CAPABILITIES_CACHE


def _extract_version_string(cmd_name: str, version_args: Optional[List[str]] = None) -> str:
    """Safely extract version string from an executable."""
    args = version_args or ["--version"]
    try:
        r = subprocess.run(
            [cmd_name] + args,
            shell=(sys.platform == "win32"),
            capture_output=True,
            text=True,
            timeout=5,
        )
        lines = (r.stdout or r.stderr or "").strip().splitlines()
        return lines[0] if lines else "Installed"
    except Exception:
        return "Installed"


def run_doctor() -> Dict[str, Any]:
    """Evaluate 4 host capability tiers and return comprehensive diagnostic scorecard."""
    plat = detect_host_platform()
    os_name = plat["os"]
    pkg_mgr = plat["pkg_manager"]

    # Package manager command prefix
    if pkg_mgr == "winget":
        pm_install = "winget install -e --id"
    elif pkg_mgr == "choco":
        pm_install = "choco install -y"
    elif pkg_mgr == "scoop":
        pm_install = "scoop install"
    elif pkg_mgr == "brew":
        pm_install = "brew install"
    elif pkg_mgr == "apt":
        pm_install = "sudo apt install -y"
    elif pkg_mgr == "pacman":
        pm_install = "sudo pacman -S --noconfirm"
    elif pkg_mgr == "dnf":
        pm_install = "sudo dnf install -y"
    else:
        pm_install = f"{pkg_mgr} install"

    # 1. Core Essentials (Mandatory for AegisBrain)
    core_items: Dict[str, Any] = {}

    # Python >= 3.10
    py_ok = sys.version_info >= (3, 10)
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_install = "winget install Python.Python.3.12" if os_name == "windows" else ("brew install python" if os_name == "macos" else "sudo apt install -y python3")
    core_items["python"] = {
        "status": "INSTALLED" if py_ok else "MISSING_CORE",
        "version": py_ver,
        "path": sys.executable,
        "impact": "Required runtime to execute AegisBrain neural memory and daemon.",
        "install_cmd": py_install,
    }

    # Git
    git_p = shutil.which("git")
    git_install = "winget install --id Git.Git -e --source winget" if os_name == "windows" else f"{pm_install} git"
    core_items["git"] = {
        "status": "INSTALLED" if git_p else "MISSING_CORE",
        "version": _extract_version_string("git") if git_p else "N/A",
        "path": git_p,
        "impact": "Required for tracking repository states, diffing, and git operations.",
        "install_cmd": git_install,
    }

    # SQLite3
    try:
        import sqlite3 as _sq
        sql_ver = getattr(_sq, "sqlite_version", "3.x")
        sql_ok = True
    except ImportError:
        sql_ver = "N/A"
        sql_ok = False
    sql_install = "winget install SQLite.SQLite" if os_name == "windows" else f"{pm_install} sqlite3"
    core_items["sqlite3"] = {
        "status": "INSTALLED" if sql_ok else "MISSING_CORE",
        "version": sql_ver,
        "path": "builtin",
        "impact": "Required for brain.db neural memory, FTS5 search, and task state.",
        "install_cmd": sql_install,
    }

    # 2. Sensory Perception Accelerators (Eyes & Ears)
    sensory_items: Dict[str, Any] = {}

    # FFmpeg
    ffmpeg_p = shutil.which("ffmpeg")
    ffmpeg_install = "winget install Gyan.FFmpeg" if os_name == "windows" else f"{pm_install} ffmpeg"
    sensory_items["ffmpeg"] = {
        "status": "INSTALLED" if ffmpeg_p else "MISSING_OPTIONAL",
        "version": _extract_version_string("ffmpeg", ["-version"]) if ffmpeg_p else "N/A",
        "path": ffmpeg_p,
        "impact": "Required for audio extraction, video slicing, and visual frame analysis.",
        "install_cmd": ffmpeg_install,
    }

    # Whisper
    whisper_p = shutil.which("whisper") or shutil.which("whisper.exe")
    sensory_items["whisper"] = {
        "status": "INSTALLED" if whisper_p else "MISSING_OPTIONAL",
        "version": _extract_version_string("whisper") if whisper_p else "N/A",
        "path": whisper_p,
        "impact": "Required for local zero-cloud speech-to-text and voice transcription.",
        "install_cmd": "pip install openai-whisper",
    }

    # 3. Token Arbitrage Workers (Zero-cost local execution)
    worker_items: Dict[str, Any] = {}

    # Ollama
    ollama_p = shutil.which("ollama")
    ollama_install = "winget install Ollama.Ollama" if os_name == "windows" else ("brew install ollama" if os_name == "macos" else "curl -fsSL https://ollama.com/install.sh | sh")
    worker_items["ollama"] = {
        "status": "INSTALLED" if ollama_p else "MISSING_OPTIONAL",
        "version": _extract_version_string("ollama") if ollama_p else "N/A",
        "path": ollama_p,
        "impact": "Provides zero-cost local MoE inference and 7B/14B Q4 worker offloading.",
        "install_cmd": ollama_install,
    }

    # Hermes
    hermes_p = shutil.which("hermes") or shutil.which("hermes.exe")
    worker_items["hermes"] = {
        "status": "INSTALLED" if hermes_p else "MISSING_OPTIONAL",
        "version": _extract_version_string("hermes") if hermes_p else "N/A",
        "path": hermes_p,
        "impact": "CLI execution worker engine for autonomous task drafting and tool dispatch.",
        "install_cmd": "pip install hermes-agent",
    }

    # OpenCode
    opencode_p = shutil.which("opencode") or shutil.which("opencode.cmd") or shutil.which("opencode.ps1")
    worker_items["opencode"] = {
        "status": "INSTALLED" if opencode_p else "MISSING_OPTIONAL",
        "version": _extract_version_string("opencode") if opencode_p else "N/A",
        "path": opencode_p,
        "impact": "Alternative local code generation and editing worker CLI.",
        "install_cmd": "npm install -g opencode-ai",
    }

    # uv
    uv_p = shutil.which("uv")
    uv_install = "winget install astral-sh.uv" if os_name == "windows" else ("brew install uv" if os_name == "macos" else "curl -LsSf https://astral.sh/uv/install.sh | sh")
    worker_items["uv"] = {
        "status": "INSTALLED" if uv_p else "MISSING_OPTIONAL",
        "version": _extract_version_string("uv") if uv_p else "N/A",
        "path": uv_p,
        "impact": "Ultra-fast Python package and virtualenv manager for scratch environments.",
        "install_cmd": uv_install,
    }

    # 4. Workstation & Terminal Modifiers (Strictly Optional)
    modifier_items: Dict[str, Any] = {}

    # Komorebi
    komorebi_p = shutil.which("komorebi") or shutil.which("komorebic")
    komo_install = "winget install LGUG2Z.komorebi" if os_name == "windows" else "echo 'komorebi is windows-only'"
    modifier_items["komorebi"] = {
        "status": "INSTALLED" if komorebi_p else "MISSING_OPTIONAL",
        "version": _extract_version_string("komorebic" if shutil.which("komorebic") else "komorebi") if komorebi_p else "N/A",
        "path": komorebi_p,
        "impact": "Required for automated window tiling and modal desktop layout.",
        "install_cmd": komo_install,
    }

    # Vim / Neovim
    vim_bin = "nvim" if shutil.which("nvim") else "vim"
    vim_p = shutil.which(vim_bin)
    vim_install = "winget install vim.vim" if os_name == "windows" else f"{pm_install} vim"
    modifier_items["vim"] = {
        "status": "INSTALLED" if vim_p else "MISSING_OPTIONAL",
        "version": _extract_version_string(vim_bin) if vim_p else "N/A",
        "path": vim_p,
        "impact": "Required for modal terminal editing and keyboard-driven workflows.",
        "install_cmd": vim_install,
    }

    # Aggregate summaries
    all_tiers = {
        "core_essentials": {
            "name": "Core Essentials",
            "mandatory": True,
            "items": core_items,
        },
        "sensory_accelerators": {
            "name": "Sensory Perception Accelerators",
            "mandatory": False,
            "items": sensory_items,
        },
        "token_arbitrage_workers": {
            "name": "Token Arbitrage Workers",
            "mandatory": False,
            "items": worker_items,
        },
        "workstation_modifiers": {
            "name": "Workstation & Terminal Modifiers",
            "mandatory": False,
            "items": modifier_items,
        },
    }

    total_count = len(core_items) + len(sensory_items) + len(worker_items) + len(modifier_items)
    installed_count = sum(1 for items in (core_items, sensory_items, worker_items, modifier_items) for it in items.values() if it["status"] == "INSTALLED")
    missing_core = sum(1 for it in core_items.values() if it["status"] == "MISSING_CORE")
    missing_optional = sum(1 for items in (sensory_items, worker_items, modifier_items) for it in items.values() if it["status"] == "MISSING_OPTIONAL")
    has_tiling = modifier_items["komorebi"]["status"] == "INSTALLED"
    has_vim = modifier_items["vim"]["status"] == "INSTALLED"

    return {
        "platform": plat,
        "tiers": all_tiers,
        "core_essentials": core_items,
        "sensory_accelerators": sensory_items,
        "token_arbitrage_workers": worker_items,
        "workstation_modifiers": modifier_items,
        "summary": {
            "total_items": total_count,
            "installed": installed_count,
            "missing_core": missing_core,
            "missing_optional": missing_optional,
            "healthy": missing_core == 0,
            "standard_desktop_mode": (not has_tiling or not has_vim),
        },
    }


def format_doctor_report(doctor_results: Dict[str, Any], show_fix: bool = False) -> str:
    """Format structured doctor report as a clean markdown scorecard."""
    plat = doctor_results.get("platform", {})
    summary = doctor_results.get("summary", {})

    lines = [
        "# 🩺 AegisBrain Doctor & Host Capabilities Scorecard",
        "",
        f"- **OS:** `{plat.get('os', 'unknown')}`",
        f"- **Shell:** `{plat.get('shell', 'unknown')}`",
        f"- **Package Manager:** `{plat.get('pkg_manager', 'unknown')}`",
        f"- **Operational Mode:** `{'Standard Desktop Mode' if summary.get('standard_desktop_mode', True) else 'Modal Tiling Mode'}`",
        "",
    ]

    tier_order = [
        ("core_essentials", "Core Essentials (Mandatory)", "🔴"),
        ("sensory_accelerators", "Sensory Perception Accelerators", "🟡"),
        ("token_arbitrage_workers", "Token Arbitrage Workers", "🟢"),
        ("workstation_modifiers", "Workstation & Terminal Modifiers", "🔵"),
    ]

    missing_actions = []

    for key, title, emoji in tier_order:
        items = doctor_results.get(key, {})
        lines.append(f"### {emoji} {title}")
        for tool_name, info in items.items():
            status = info.get("status", "UNKNOWN")
            ver = info.get("version", "N/A")
            impact = info.get("impact", "")
            cmd = info.get("install_cmd", "")

            if status == "INSTALLED":
                icon = "✅"
                ver_display = f" (`{ver}`)" if ver and ver != "N/A" else ""
                lines.append(f"- {icon} **{tool_name}**{ver_display} — {impact}")
            elif status == "MISSING_CORE":
                icon = "❌"
                lines.append(f"- {icon} **{tool_name}** [MISSING CORE] — {impact}")
                if show_fix and cmd:
                    lines.append(f"  - Fix: `{cmd}`")
                missing_actions.append((tool_name, cmd, impact, True))
            else:
                icon = "⚠️"
                lines.append(f"- {icon} **{tool_name}** [MISSING OPTIONAL] — {impact}")
                if show_fix and cmd:
                    lines.append(f"  - Fix: `{cmd}`")
                missing_actions.append((tool_name, cmd, impact, False))
        lines.append("")

    lines.append("## 🚀 Recommended Next Actions")
    if not missing_actions:
        lines.append("- All core and optional workstation tools are installed and ready.")
        lines.append("- AegisBrain host capabilities are synchronized in `brain.db`.")
    else:
        for idx, (t_name, t_cmd, t_impact, is_core) in enumerate(missing_actions, 1):
            severity_tag = "CRITICAL" if is_core else "OPTIONAL"
            lines.append(f"{idx}. **[{severity_tag}] Install {t_name}**")
            lines.append(f"   Command: `{t_cmd}`")
            lines.append(f"   Impact: {t_impact}")

    return "\n".join(lines)


def install_tool(tool_name: str) -> bool:
    """Install a missing tool using detected platform package manager."""
    doc = run_doctor()
    t_clean = tool_name.strip().lower()

    # Search tiers
    target_cmd: Optional[str] = None
    for tier_key in ("core_essentials", "sensory_accelerators", "token_arbitrage_workers", "workstation_modifiers"):
        items = doc.get(tier_key, {})
        for name, info in items.items():
            if name.lower() == t_clean:
                target_cmd = info.get("install_cmd")
                break
        if target_cmd:
            break

    if not target_cmd or target_cmd.startswith("echo"):
        return False

    try:
        r = subprocess.run(
            target_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if r.returncode == 0:
            global _HOST_CAPABILITIES_CACHE
            _HOST_CAPABILITIES_CACHE = None
            save_host_capabilities(run_doctor())
            return True
        return False
    except Exception:
        return False
