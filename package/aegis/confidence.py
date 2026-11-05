"""AegisBrain Agent Confidence Scoring & Learning Curve Tracker.

Tracks each agent's output quality over time:
- success_rate: % of outputs accepted by manager without revision
- avg_revision_rounds: how many correction cycles needed
- learning_curve: improving / stable / degrading
- last_n_scores: rolling window of quality scores (1-10)
"""

from __future__ import annotations
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
from .config import get_db_path


def init_confidence_table() -> None:
    db = get_db_path()
    with sqlite3.connect(db) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_confidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                task_type TEXT DEFAULT 'general',
                score INTEGER CHECK(score BETWEEN 1 AND 10),
                accepted BOOLEAN DEFAULT 1,
                revision_rounds INTEGER DEFAULT 0,
                task_description TEXT,
                initial_errors INTEGER DEFAULT 0,
                final_errors INTEGER DEFAULT 0,
                improvement_delta INTEGER DEFAULT 0,
                teaching_notes TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        # Safe migration if table existed previously without error tracking columns
        c = conn.cursor()
        c.execute("PRAGMA table_info(agent_confidence)")
        cols = {row[1] for row in c.fetchall()}
        for col_name, col_type in [
            ("initial_errors", "INTEGER DEFAULT 0"),
            ("final_errors", "INTEGER DEFAULT 0"),
            ("improvement_delta", "INTEGER DEFAULT 0"),
            ("teaching_notes", "TEXT DEFAULT ''"),
        ]:
            if col_name not in cols:
                conn.execute(f"ALTER TABLE agent_confidence ADD COLUMN {col_name} {col_type}")


def record_score(agent_name: str, score: int, accepted: bool = True,
                 revision_rounds: int = 0, task_type: str = "general",
                 task_description: str = "",
                 initial_errors: int = 0, final_errors: int = 0,
                 teaching_notes: str = "") -> int:
    init_confidence_table()
    db = get_db_path()
    delta = max(0, initial_errors - final_errors)
    with sqlite3.connect(db) as conn:
        cur = conn.execute(
            """INSERT INTO agent_confidence 
               (agent_name, task_type, score, accepted, revision_rounds, task_description, initial_errors, final_errors, improvement_delta, teaching_notes) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (agent_name, task_type, min(10, max(1, score)), accepted, revision_rounds, task_description, initial_errors, final_errors, delta, teaching_notes)
        )
        return cur.lastrowid


def record_agent_task_feedback(
    agent_name: str,
    task_type: str = "general",
    initial_errors: int = 0,
    final_errors: int = 0,
    task_description: str = "",
    teaching_notes: str = ""
) -> Dict[str, Any]:
    """Records worker trial, measures error reduction, and dynamically adjusts confidence.
    
    Example: Hermes committed 5 errors on first run. Subagent provided guidance/teaching.
    Hermes reruns and commits 3 errors (-2 errors). Confidence score increases.
    """
    init_confidence_table()
    delta = initial_errors - final_errors
    accepted = (final_errors == 0)
    rev_rounds = 1 if initial_errors > 0 else 0

    if final_errors == 0:
        base_score = 10
    else:
        # Score scaled: base 10 minus final errors, boosted by positive error reduction delta
        base_score = max(1, min(9, 10 - final_errors + max(0, delta)))

    record_id = record_score(
        agent_name=agent_name,
        score=base_score,
        accepted=accepted,
        revision_rounds=rev_rounds,
        task_type=task_type,
        task_description=task_description,
        initial_errors=initial_errors,
        final_errors=final_errors,
        teaching_notes=teaching_notes
    )

    conf = get_agent_confidence(agent_name)
    trajectory = "IMPROVING" if delta > 0 else "STABLE" if delta == 0 else "DEGRADING"

    return {
        "record_id": record_id,
        "agent": agent_name,
        "initial_errors": initial_errors,
        "final_errors": final_errors,
        "error_delta": delta,
        "awarded_score": base_score,
        "learning_trajectory": trajectory,
        "new_avg_score": conf["avg_score"],
        "learning_curve": conf["learning_curve"],
        "summary": (
            f"Agent `{agent_name}` errors {initial_errors} ➔ {final_errors} "
            f"({'reduced by ' + str(delta) if delta > 0 else 'unchanged'}). "
            f"Confidence: {conf['avg_score']}/10 ({conf['learning_curve']})."
        )
    }


def can_delegate_complex_task(agent_name: str, task_type: str = "general") -> Tuple[bool, float, str]:
    """Gating test: can this local worker be trusted with high-complexity subtasks?
    
    Requires avg_score >= 8.0 and non-degrading learning curve.
    """
    conf = get_agent_confidence(agent_name)
    avg = conf.get("avg_score", 0.0)
    curve = conf.get("learning_curve", "unknown")
    total = conf.get("total_tasks", 0)

    if total >= 2 and avg >= 8.0 and curve in ("improving", "stable", "insufficient_data"):
        return True, avg, f"Approved for complex delegation (Avg: {avg}/10, Curve: {curve})"
    elif total == 0:
        return False, 0.0, "Zero historical trials. Limit to routine or supervisor-guided tasks."
    else:
        return False, avg, f"Requires junior boss supervision (Avg: {avg}/10, Curve: {curve})"


def get_agent_confidence(agent_name: str, window: int = 20) -> Dict[str, Any]:
    init_confidence_table()
    db = get_db_path()
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT score, accepted, revision_rounds FROM agent_confidence WHERE agent_name = ? ORDER BY id DESC LIMIT ?",
            (agent_name, window)
        ).fetchall()

    if not rows:
        return {"agent": agent_name, "success_rate": 0.0, "avg_score": 0.0,
                "avg_revision_rounds": 0.0, "learning_curve": "unknown",
                "total_tasks": 0, "last_scores": []}

    scores = [r["score"] for r in rows]
    accepted_count = sum(1 for r in rows if r["accepted"])
    rev_rounds = [r["revision_rounds"] for r in rows]

    # Determine learning curve from score trend
    if len(scores) >= 6:
        first_half = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
        second_half = sum(scores[:len(scores)//2]) / (len(scores)//2)
        if second_half > first_half + 0.5:
            curve = "improving"
        elif second_half < first_half - 0.5:
            curve = "degrading"
        else:
            curve = "stable"
    else:
        curve = "insufficient_data"

    return {
        "agent": agent_name,
        "success_rate": round(accepted_count / len(rows) * 100, 1),
        "avg_score": round(sum(scores) / len(scores), 2),
        "avg_revision_rounds": round(sum(rev_rounds) / len(rev_rounds), 2),
        "learning_curve": curve,
        "total_tasks": len(rows),
        "last_scores": scores[:10],
    }


def get_all_agents_confidence() -> List[Dict[str, Any]]:
    init_confidence_table()
    db = get_db_path()
    with sqlite3.connect(db) as conn:
        agents = [r[0] for r in conn.execute("SELECT DISTINCT agent_name FROM agent_confidence").fetchall()]
    return [get_agent_confidence(a) for a in agents]


def format_confidence_report() -> str:
    agents = get_all_agents_confidence()
    if not agents:
        return "📊 No agent confidence data recorded yet. Run tasks to build scores."
    
    lines = ["📊 **Agent Confidence Scoreboard**\n"]
    for a in sorted(agents, key=lambda x: x["avg_score"], reverse=True):
        emoji = "📈" if a["learning_curve"] == "improving" else "📉" if a["learning_curve"] == "degrading" else "➡️"
        lines.append(f"**{a['agent']}** {emoji}")
        lines.append(f"  • Success Rate: {a['success_rate']}% | Avg Score: {a['avg_score']}/10")
        lines.append(f"  • Avg Revisions: {a['avg_revision_rounds']} | Curve: {a['learning_curve']}")
        lines.append(f"  • Last scores: {a['last_scores']}")
        lines.append("")
    return "\n".join(lines)


def recommend_agent(task_type: str = "general") -> str:
    """Recommend the best agent for a task type based on confidence scores."""
    init_confidence_table()
    db = get_db_path()
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT agent_name, AVG(score) as avg_s, COUNT(*) as cnt FROM agent_confidence WHERE task_type = ? GROUP BY agent_name HAVING cnt >= 3 ORDER BY avg_s DESC LIMIT 1",
            (task_type,)
        ).fetchall()
    if rows:
        return rows[0]["agent_name"]
    return "hermes"  # default fallback
