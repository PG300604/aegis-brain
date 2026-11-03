import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from .config import DEFAULT_OPEN_SOURCE_ROOT, get_active_context_path, get_current_mode
from .db import get_active_alerts, get_recent_decisions, get_tracked_prs


def inspect_git_workspace(workspace_path: Optional[Path] = None) -> Dict[str, Any]:
    """Inspect current or specified git repository for branch, latest commit, and dirty status."""
    path = workspace_path or Path.cwd()
    info = {
        "path": str(path),
        "name": path.name,
        "is_git": False,
        "branch": "n/a",
        "last_commit": "n/a",
        "is_dirty": False,
    }

    try:
        # Check if inside git work tree
        is_git = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if is_git.returncode != 0 or "true" not in is_git.stdout:
            return info

        info["is_git"] = True

        # Current branch
        branch_res = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if branch_res.returncode == 0:
            info["branch"] = branch_res.stdout.strip()

        # Last commit
        log_res = subprocess.run(
            ["git", "-C", str(path), "log", "-1", "--oneline"],
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if log_res.returncode == 0:
            info["last_commit"] = log_res.stdout.strip()

        # Dirty status
        status_res = subprocess.run(
            ["git", "-C", str(path), "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if status_res.returncode == 0:
            info["is_dirty"] = bool(status_res.stdout.strip())

    except Exception:
        pass

    return info


def generate_active_context(workspace_path: Optional[Path] = None) -> str:
    """Compile a deterministic, token-budgeted (<= 400 tokens) active context summary."""
    mode = get_current_mode()
    path = workspace_path or Path.cwd()
    git_info = inspect_git_workspace(path)

    tracked_prs = get_tracked_prs()[:3]
    recent_decisions = get_recent_decisions(limit=4)
    alerts = get_active_alerts()[:3]

    lines: List[str] = []
    lines.append("# Aegis Brain Active Context")
    lines.append(f"**Mode**: `{mode.upper()}` | **Updated**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")

    if mode == "private":
        lines.append("> [!NOTE]")
        lines.append("> Private stealth mode active: zero disk logs, ephemeral execution.")

    lines.append("")
    lines.append(f"### Current Workspace: `{git_info['name']}`")
    if git_info["is_git"]:
        status_str = "dirty (uncommitted changes)" if git_info["is_dirty"] else "clean"
        lines.append(f"- **Branch**: `{git_info['branch']}` ({status_str})")
        lines.append(f"- **Latest Commit**: `{git_info['last_commit']}`")
    lines.append(f"- **Path**: `{git_info['path']}`")

    if tracked_prs:
        lines.append("")
        lines.append("### Active Tracked PRs")
        for pr in tracked_prs:
            labels_str = f" [{', '.join(pr['labels'])}]" if pr.get("labels") else ""
            lines.append(f"- **{pr['repo']}#{pr['pr_number']}** (`{pr['status']}`){labels_str}: {pr['title']} (CI: {pr.get('ci_status', 'pending')})")

    if recent_decisions:
        lines.append("")
        lines.append("### Key Decisions & Conventions")
        for d in recent_decisions:
            lines.append(f"- **[{d['category']}] {d['title']}**: {d['decision']}")

    if alerts:
        lines.append("")
        lines.append("### Proactive Alerts & Reminders")
        for a in alerts:
            lines.append(f"- [!IMPORTANT] **{a['category']}**: {a['message']}")

    context_str = "\n".join(lines) + "\n"

    # Write to file
    try:
        get_active_context_path().write_text(context_str, encoding="utf-8")
    except Exception:
        pass

    return context_str
