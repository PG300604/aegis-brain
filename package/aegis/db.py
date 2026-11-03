import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, Generator, List, Optional
from .config import get_current_mode, get_db_path

SCHEMA = """
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    agent_name TEXT NOT NULL,
    workspace_path TEXT NOT NULL,
    mode TEXT DEFAULT 'public',
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    decision TEXT NOT NULL,
    rationale TEXT,
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
    title,
    decision,
    rationale,
    tags,
    content='decisions',
    content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS decisions_ai AFTER INSERT ON decisions BEGIN
  INSERT INTO memory_fts(rowid, title, decision, rationale, tags)
  VALUES (new.id, new.title, new.decision, new.rationale, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS decisions_ad AFTER DELETE ON decisions BEGIN
  INSERT INTO memory_fts(memory_fts, rowid, title, decision, rationale, tags)
  VALUES('delete', old.id, old.title, old.decision, old.rationale, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS decisions_au AFTER UPDATE ON decisions BEGIN
  INSERT INTO memory_fts(memory_fts, rowid, title, decision, rationale, tags)
  VALUES('delete', old.id, old.title, old.decision, old.rationale, old.tags);
  INSERT INTO memory_fts(rowid, title, decision, rationale, tags)
  VALUES (new.id, new.title, new.decision, new.rationale, new.tags);
END;

CREATE TABLE IF NOT EXISTS tracked_prs (
    repo TEXT NOT NULL,
    pr_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    labels TEXT,
    ci_status TEXT,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (repo, pr_number)
);

CREATE TABLE IF NOT EXISTS proactive_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    message TEXT NOT NULL,
    acknowledged INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(str(get_db_path()), timeout=10.0)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """Initialize database tables and triggers."""
    with get_connection() as conn:
        conn.executescript(SCHEMA)


def record_session(session_id: str, agent_name: str, workspace_path: str, summary: str = "") -> bool:
    """Record or update a session. Bypassed if in private mode."""
    if get_current_mode() == "private":
        return False

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO sessions (id, agent_name, workspace_path, mode, summary, updated_at)
            VALUES (?, ?, ?, 'public', ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                summary = excluded.summary,
                updated_at = CURRENT_TIMESTAMP
        """, (session_id, agent_name, workspace_path, summary))
    return True


def record_decision(
    category: str,
    title: str,
    decision: str,
    rationale: str = "",
    tags: Optional[List[str]] = None,
    session_id: Optional[str] = None,
) -> Optional[int]:
    """Record an architectural or operational decision. Bypassed in private mode."""
    if get_current_mode() == "private":
        return None

    tag_str = json.dumps(tags or [])
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO decisions (session_id, category, title, decision, rationale, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session_id, category, title, decision, rationale, tag_str))
        return cursor.lastrowid


def track_pr(
    repo: str,
    pr_number: int,
    title: str,
    status: str,
    labels: Optional[List[str]] = None,
    ci_status: str = "pending",
) -> None:
    """Record or update tracked PR status. Bypassed in private mode."""
    if get_current_mode() == "private":
        return

    label_str = json.dumps(labels or [])
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO tracked_prs (repo, pr_number, title, status, labels, ci_status, last_checked)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(repo, pr_number) DO UPDATE SET
                title = excluded.title,
                status = excluded.status,
                labels = excluded.labels,
                ci_status = excluded.ci_status,
                last_checked = CURRENT_TIMESTAMP
        """, (repo, pr_number, title, status, label_str, ci_status))


def get_tracked_prs(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve tracked PRs."""
    query = "SELECT * FROM tracked_prs"
    params = []
    if status:
        query += " WHERE status = ?"
        params.append(status)
    query += " ORDER BY last_checked DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        result = []
        for r in rows:
            item = dict(r)
            if item.get("labels"):
                try:
                    item["labels"] = json.loads(item["labels"])
                except Exception:
                    pass
            result.append(item)
        return result


def get_recent_decisions(limit: int = 10, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve recent decisions."""
    query = "SELECT * FROM decisions"
    params = []
    if category:
        query += " WHERE category = ?"
        params.append(category)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        result = []
        for r in rows:
            item = dict(r)
            if item.get("tags"):
                try:
                    item["tags"] = json.loads(item["tags"])
                except Exception:
                    pass
            result.append(item)
        return result


def search_memories(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Sub-millisecond keyword search across decisions using SQLite FTS5."""
    clean_query = "".join(c if (c.isalnum() or c.isspace()) else " " for c in query).strip()
    if not clean_query:
        return []

    # Tokenize words for FTS prefix matching: "Sub second" -> "Sub* second*"
    tokens = clean_query.split()
    fts_match = " ".join(f"{t}*" for t in tokens)

    with get_connection() as conn:
        try:
            rows = conn.execute("""
                SELECT d.*, rank
                FROM memory_fts f
                JOIN decisions d ON f.rowid = d.id
                WHERE memory_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (fts_match, limit)).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            # Fallback to simple LIKE search if FTS query fails
            rows = conn.execute("""
                SELECT * FROM decisions
                WHERE title LIKE ? OR decision LIKE ? OR rationale LIKE ?
                ORDER BY created_at DESC LIMIT ?
            """, (f"%{clean_query}%", f"%{clean_query}%", f"%{clean_query}%", limit)).fetchall()
            return [dict(r) for r in rows]


def add_alert(category: str, message: str) -> None:
    if get_current_mode() == "private":
        return
    with get_connection() as conn:
        conn.execute("INSERT INTO proactive_alerts (category, message) VALUES (?, ?)", (category, message))


def get_active_alerts() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM proactive_alerts WHERE acknowledged = 0 ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]
