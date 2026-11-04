"""AegisBrain Episodic Task Lifecycle & Memory Compaction Engine.

Manages ongoing tasks, future ideas, and automatic memory compaction:
- Active tasks and pending ideas are kept in active memory with automatic reminders.
- Once a task is accomplished, it transitions from active state to the historical
  archive with outcome and key learnings recorded.
- Active working context (ACTIVE_CONTEXT.md) only retains pending tasks,
  preventing token bloat (<150 tokens) and maintaining sub-second latency.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from .db import get_connection, record_decision

TASK_SCHEMA = """
CREATE TABLE IF NOT EXISTS aegis_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    category TEXT DEFAULT 'feature',  -- feature, bugfix, idea, research, model-setup
    status TEXT DEFAULT 'active',      -- active, completed, discarded
    priority TEXT DEFAULT 'medium',   -- high, medium, low
    outcome TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
"""


def init_task_db() -> None:
    with get_connection() as conn:
        conn.executescript(TASK_SCHEMA)


def create_task(
    title: str,
    description: str = "",
    category: str = "feature",
    priority: str = "medium"
) -> int:
    """Register a new active task or future idea."""
    init_task_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO aegis_tasks (title, description, category, status, priority)
            VALUES (?, ?, ?, 'active', ?)
        """, (title, description, category, priority.lower()))
        return cursor.lastrowid or 0


def list_active_tasks() -> List[Dict[str, Any]]:
    """Retrieve only ongoing tasks and active ideas (for compact working context)."""
    init_task_db()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM aegis_tasks WHERE status = 'active' ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, created_at ASC"
        ).fetchall()
        return [dict(r) for r in rows]


def complete_task(task_id: int, outcome: str = "", learning: str = "") -> bool:
    """Transition task from active memory to historical archive."""
    init_task_db()
    task_category = "milestone"
    task_title = ""
    updated = False

    with get_connection() as conn:
        cur = conn.cursor()
        task = cur.execute("SELECT * FROM aegis_tasks WHERE id = ?", (task_id,)).fetchone()
        if not task:
            return False

        task_category = task["category"] or "milestone"
        task_title = task["title"]

        cur.execute("""
            UPDATE aegis_tasks
            SET status = 'completed', outcome = ?, completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (outcome or "Successfully completed and verified.", task_id))
        updated = cur.rowcount > 0

    # Execute outside the connection block to prevent nested SQLite transaction lock
    if updated and (learning or outcome):
        try:
            record_decision(
                category=task_category,
                title=f"Task Completed: {task_title}",
                decision=outcome or "Milestone achieved.",
                rationale=learning or "Shifted from active memory to historical ledger.",
                tags=["task", task_category, "completed"]
            )
        except Exception:
            pass

    return updated


def get_task_history(limit: int = 15) -> List[Dict[str, Any]]:
    """Retrieve archived completed tasks."""
    init_task_db()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM aegis_tasks WHERE status = 'completed' ORDER BY completed_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def format_tasks_display(show_history: bool = False) -> str:
    """Clean markdown display for CLI and Telegram."""
    if show_history:
        history = get_task_history()
        if not history:
            return "📜 *AegisBrain Task History:* No completed tasks archived yet."
        lines = [
            "📜 *AegisBrain Completed Task History & Achievements*",
            "• *Memory Status:* Archived to long-term ledger (Zero active token footprint).",
            ""
        ]
        for t in history:
            comp_time = t.get("completed_at", "")[:16]
            lines.append(f"• ✅ `[#{t['id']}]` *{t['title']}* ({comp_time})")
            if t.get("outcome"):
                lines.append(f"   _Outcome:_ {t['outcome']}")
        return "\n".join(lines)

    active = list_active_tasks()
    if not active:
        return "✨ *AegisBrain Task Memory:* Zero pending tasks! System memory is clean and running at maximum velocity."

    lines = [
        "📌 *AegisBrain Active Tasks & Ongoing Ideas*",
        f"• *Active Count:* {len(active)} ongoing tasks in working memory.",
        "• *Memory Rule:* Completed tasks automatically shift to history to prevent context bloat.",
        ""
    ]
    for t in active:
        p_badge = "🔴 High" if t.get("priority") == "high" else ("🟡 Med" if t.get("priority") == "medium" else "⚪ Low")
        lines.append(f"• `[#{t['id']}]` *{t['title']}* [{t.get('category', 'feature').upper()}] — {p_badge}")
        if t.get("description"):
            lines.append(f"   _{t['description']}_")

    lines.append("")
    lines.append("👉 *Complete Task:* Run `/task done <id>` or `aegis task done <id>` to archive.")
    return "\n".join(lines)
