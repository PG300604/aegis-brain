"""Sanitized Diagnostic Bundler & Self-Healing Reporter for AegisBrain.

Gathers workstation specs, daemon state, memory headroom, and recent logs.
Strictly redacts tokens, credentials, and confidential paths before generating
a sanitized report or 1-click GitHub issue draft URL for developers.
"""

import os
import re
import sys
import platform
import urllib.parse
from pathlib import Path
from typing import Dict, Any, List

from .config import get_aegis_dir
from .hardware import get_hardware_status
from .governance import load_governance_config
from .service import is_daemon_running
from .db import get_tracked_prs


def sanitize_text(text: str) -> str:
    """Strip secrets, tokens, credentials, and private paths from diagnostic text."""
    if not text:
        return ""
    
    # Redact Telegram bot tokens (e.g. 123456789:ABCdef-ghIJK...)
    text = re.sub(r"\b\d{8,11}:[A-Za-z0-9_-]{32,}\b", "[REDACTED_TELEGRAM_TOKEN]", text)
    # Redact Twilio Account SIDs and Auth Tokens
    text = re.sub(r"\bAC[a-f0-9]{32}\b", "[REDACTED_TWILIO_SID]", text)
    text = re.sub(r"\b[a-f0-9]{32}\b", "[REDACTED_AUTH_TOKEN]", text)
    # Redact phone numbers
    text = re.sub(r"\b(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "[REDACTED_PHONE]", text)
    # Redact user directory path username
    home = str(Path.home())
    if home in text:
        text = text.replace(home, "~")
    
    return text


def collect_recent_logs(lines_count: int = 25) -> str:
    """Retrieve and sanitize recent log lines from daemon.log."""
    log_file = get_aegis_dir() / "daemon.log"
    if not log_file.exists():
        return "(no daemon logs found)"
    try:
        content = log_file.read_text(encoding="utf-8", errors="replace")
        lines = content.strip().splitlines()
        tail = lines[-lines_count:] if len(lines) > lines_count else lines
        return sanitize_text("\n".join(tail))
    except Exception as e:
        return f"(failed to read daemon log: {e})"


def generate_diagnostic_bundle() -> Dict[str, Any]:
    """Compile structured diagnostic information."""
    hw = get_hardware_status()
    gov = load_governance_config()
    daemon_ok = is_daemon_running()
    
    try:
        prs = get_tracked_prs()
    except Exception:
        prs = []

    return {
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "daemon_running": daemon_ok,
        "hardware": hw,
        "governance": {
            "manager_model": gov.get("manager_model"),
            "worker_model": gov.get("worker_model"),
            "worker_provider": gov.get("worker_provider"),
            "auto_ram_sizing": gov.get("auto_ram_sizing"),
            "self_healing": gov.get("self_healing"),
        },
        "tracked_prs_count": len(prs),
        "recent_logs": collect_recent_logs(20),
    }


def format_diagnostic_markdown() -> str:
    """Format sanitized diagnostic report in markdown."""
    diag = generate_diagnostic_bundle()
    hw = diag["hardware"]
    gov = diag["governance"]

    lines = [
        "## 🛡️ AegisBrain Diagnostic Report",
        "",
        "### 💻 System & Environment",
        f"- **OS / Platform:** `{diag['platform']}`",
        f"- **Python Version:** `{diag['python_version']}`",
        f"- **Daemon Status:** `{'ONLINE' if diag['daemon_running'] else 'OFFLINE'}`",
        f"- **Total RAM:** {hw['total_ram_gb']} GB (Available: {hw['avail_ram_gb']} GB, Load: {hw['load_percent']}%)",
        f"- **CPU Cores:** {hw['cpu_cores']}",
        "",
        "### 👑 Model Governance",
        f"- **Manager Model:** `{gov['manager_model']}`",
        f"- **Worker Model:** `{gov['worker_model']}` ({gov['worker_provider']})",
        f"- **Auto RAM Sizing:** `{gov['auto_ram_sizing']}`",
        f"- **Tracked PRs:** {diag['tracked_prs_count']} active",
        "",
        "### 📋 Recent Daemon Logs (Sanitized)",
        "```text",
        diag["recent_logs"],
        "```",
    ]
    return "\n".join(lines)


def get_github_issue_url(title: str = "Bug / Feedback Report", error_desc: str = "") -> str:
    """Generate a 1-click GitHub Issue draft URL with pre-filled markdown diagnostics."""
    base_url = "https://github.com/PriyanshuLathi/aegis-brain/issues/new"
    report_md = format_diagnostic_markdown()
    
    body = (
        f"### Description\n{error_desc or 'Describe the issue or unexpected behavior here.'}\n\n"
        f"### Diagnostic Bundle\n{report_md}\n"
    )
    
    params = {
        "title": f"[Issue] {title}",
        "body": body[:3500],  # URL length safe limit
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"
