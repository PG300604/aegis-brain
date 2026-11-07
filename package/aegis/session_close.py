"""AegisBrain Session Close & Compaction Protocol ('Bye' Protocol).

Automates graceful session termination:
1. Takes a complete restore-point snapshot of agent configurations and prompt files.
2. Compresses the working context (ACTIVE_CONTEXT.md) into token-efficient form.
3. Records the session summary, milestones, and architectural decisions into brain.db.
4. Prepares the system for exit via '/exit' and 'exit'.
"""

import time
from pathlib import Path
from typing import Any, Dict, Optional
from .snapshot import create_snapshot
from .db import record_session, record_decision, init_db
from .governor import generate_active_context


def close_session(
    agent_name: str = "antigravity",
    summary: str = "",
    workspace_path: Optional[Path] = None,
    archive_reason: str = "session_bye_archive",
) -> Dict[str, Any]:
    """Capture snapshot, compact context, and store session data in brain DB."""
    init_db()
    ts = int(time.time())
    session_id = f"session_{ts}"
    ws = workspace_path or Path.cwd()

    # 1. Take restore-point snapshot
    snap = create_snapshot(name="session_end_snapshot", reason=archive_reason)

    # 2. Record session in brain.db
    session_summary = summary or f"Session completed at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))}. Snapshot {snap['snapshot_id']} archived."
    record_session(
        session_id=session_id,
        agent_name=agent_name,
        workspace_path=str(ws),
        summary=session_summary,
    )

    # 3. If a specific summary was provided, also record as decision/milestone
    if summary:
        try:
            record_decision(
                category="SESSION",
                title=f"Session Summary ({time.strftime('%Y-%m-%d %H:%M', time.localtime(ts))})",
                decision=summary,
                rationale="Recorded via 'bye' session closing protocol.",
                tags=["session", "bye", "archive"],
                session_id=session_id,
            )
        except Exception:
            pass

    # 4. Compact and refresh ACTIVE_CONTEXT.md
    ctx = generate_active_context(ws)

    return {
        "session_id": session_id,
        "snapshot": snap,
        "workspace": str(ws),
        "context_bytes": len(ctx),
        "status": "archived",
    }


def format_session_close_display(result: Dict[str, Any]) -> str:
    """Format clean markdown / terminal display for session closure."""
    snap = result.get("snapshot", {})
    snap_id = snap.get("snapshot_id", "unknown")
    files_count = snap.get("file_count", 0)
    reason = snap.get("reason", "session_bye_archive")
    session_id = result.get("session_id", "unknown")

    divider = "─" * 72
    return f"""
{divider}
AegisBrain • Session Safely Closed & Archived
{divider}
• Snapshot ID:    {snap_id} ({files_count} files archived)
• Reason:         {reason}
• Neural DB:      Session {session_id} saved to brain.db
• Active Context: Compacted & synced to ACTIVE_CONTEXT.md

Ready for clean shutdown:
  1. Type '/exit' to exit Antigravity CLI.
  2. Type 'exit' to close terminal.
{divider}
""".strip()
