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
    comments_count INTEGER DEFAULT 0,
    review_comments_count INTEGER DEFAULT 0,
    latest_review_state TEXT DEFAULT '',
    updated_at TEXT DEFAULT '',
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

CREATE TABLE IF NOT EXISTS telegram_inbox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    update_id INTEGER UNIQUE,
    chat_id TEXT,
    sender_username TEXT,
    sender_name TEXT,
    message_id INTEGER,
    text TEXT,
    extracted_urls TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    result_summary TEXT
);

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
    archetype TEXT DEFAULT 'developer',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS worker_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    display_name TEXT,
    priority INTEGER DEFAULT 1,
    is_primary INTEGER DEFAULT 0,
    is_free INTEGER DEFAULT 1,
    fallback_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tool_name, model_name)
);

CREATE TABLE IF NOT EXISTS active_agent_config (
    role TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    model TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    """Initialize database tables and triggers with safe migration support."""
    with get_connection() as conn:
        conn.executescript(SCHEMA)
        # Migrate existing tracked_prs schema if new columns are missing
        c = conn.cursor()
        c.execute("PRAGMA table_info(tracked_prs)")
        cols = {row["name"] for row in c.fetchall()}
        for col_name, col_type in [
            ("comments_count", "INTEGER DEFAULT 0"),
            ("review_comments_count", "INTEGER DEFAULT 0"),
            ("latest_review_state", "TEXT DEFAULT ''"),
            ("updated_at", "TEXT DEFAULT ''"),
        ]:
            if col_name not in cols:
                conn.execute(f"ALTER TABLE tracked_prs ADD COLUMN {col_name} {col_type}")

        # Migrate host_capabilities schema if archetype column is missing
        c.execute("PRAGMA table_info(host_capabilities)")
        hc_cols = {row["name"] for row in c.fetchall()}
        if "archetype" not in hc_cols and len(hc_cols) > 0:
            conn.execute("ALTER TABLE host_capabilities ADD COLUMN archetype TEXT DEFAULT 'developer'")


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
    comments_count: int = 0,
    review_comments_count: int = 0,
    latest_review_state: str = "",
    updated_at: str = "",
) -> None:
    """Record or update tracked PR status. Bypassed in private mode."""
    if get_current_mode() == "private":
        return

    label_str = json.dumps(labels or [])
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO tracked_prs (
                repo, pr_number, title, status, labels, ci_status,
                comments_count, review_comments_count, latest_review_state, updated_at,
                last_checked
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(repo, pr_number) DO UPDATE SET
                title = excluded.title,
                status = excluded.status,
                labels = excluded.labels,
                ci_status = excluded.ci_status,
                comments_count = excluded.comments_count,
                review_comments_count = excluded.review_comments_count,
                latest_review_state = excluded.latest_review_state,
                updated_at = excluded.updated_at,
                last_checked = CURRENT_TIMESTAMP
        """, (
            repo, pr_number, title, status, label_str, ci_status,
            comments_count, review_comments_count, latest_review_state, updated_at
        ))


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


def record_telegram_message(
    update_id: int,
    chat_id: str,
    text: str,
    sender_username: str = "",
    sender_name: str = "",
    message_id: int = 0,
    extracted_urls: str = "",
) -> int:
    """Store an incoming Telegram message into persistent inbox so no prompts are ever lost."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT OR IGNORE INTO telegram_inbox 
            (update_id, chat_id, sender_username, sender_name, message_id, text, extracted_urls, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
            """,
            (update_id, str(chat_id), sender_username, sender_name, message_id, text, extracted_urls),
        )
        if cur.lastrowid:
            return cur.lastrowid
        row = conn.execute("SELECT id FROM telegram_inbox WHERE update_id = ?", (update_id,)).fetchone()
        return row[0] if row else 0


def get_pending_telegram_messages(limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieve unhandled / pending messages from Telegram inbox."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM telegram_inbox WHERE status = 'pending' ORDER BY id ASC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]


def mark_telegram_message_processed(update_id: int, result_summary: str = "") -> None:
    """Mark a message as processed with an execution summary."""
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE telegram_inbox 
            SET status = 'processed', processed_at = CURRENT_TIMESTAMP, result_summary = ?
            WHERE update_id = ?
            """,
            (result_summary, update_id),
        )


def get_recent_telegram_messages(limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieve recent telegram messages for audit and replay."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM telegram_inbox ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]


def save_worker_model(
    tool_name: str = "",
    model_name: str = "",
    display_name: str = "",
    priority: int = 1,
    is_primary: bool = False,
    is_free: bool = True,
    fallback_order: int = 0,
    **kwargs: Any,
) -> int:
    """Save or update a confirmed worker model in persistent memory."""
    t_name = tool_name or str(kwargs.get("tool", ""))
    m_name = model_name or str(kwargs.get("model", ""))
    d_name = display_name or str(kwargs.get("name", m_name))
    is_prim = 1 if (is_primary or kwargs.get("primary", False)) else 0
    free_flag = 1 if (is_free or "free" in str(kwargs.get("cost_profile", "")).lower()) else 0

    if not t_name or not m_name:
        return 0

    init_db()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO worker_models 
            (tool_name, model_name, display_name, priority, is_primary, is_free, fallback_order)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(tool_name, model_name) DO UPDATE SET
                display_name = excluded.display_name,
                priority = excluded.priority,
                is_primary = excluded.is_primary,
                is_free = excluded.is_free,
                fallback_order = excluded.fallback_order
            """,
            (
                t_name,
                m_name,
                d_name,
                priority,
                is_prim,
                free_flag,
                fallback_order,
            ),
        )
        return cur.lastrowid or 0



def get_worker_models(tool_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve all confirmed worker models, optionally filtered by tool."""
    init_db()
    with get_connection() as conn:
        if tool_name:
            rows = conn.execute(
                """
                SELECT * FROM worker_models 
                WHERE tool_name = ? 
                ORDER BY priority ASC, fallback_order ASC, id ASC
                """,
                (tool_name,),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT * FROM worker_models 
                ORDER BY priority ASC, fallback_order ASC, id ASC
                """
            ).fetchall()
        return [dict(r) for r in rows]


def clear_worker_models(tool_name: Optional[str] = None) -> None:
    """Clear worker models from database."""
    init_db()
    with get_connection() as conn:
        if tool_name:
            conn.execute("DELETE FROM worker_models WHERE tool_name = ?", (tool_name,))
        else:
            conn.execute("DELETE FROM worker_models")


def get_worker_cascade() -> Dict[str, Any]:
    """Retrieve hierarchical worker model cascade organized by priority."""
    all_models = get_worker_models()
    p1 = [m for m in all_models if m.get("priority") == 1]
    p2 = [m for m in all_models if m.get("priority") == 2]
    p3 = [m for m in all_models if m.get("priority") == 3]

    primary_model = next((m for m in all_models if m.get("is_primary")), None)
    if not primary_model and p1:
        primary_model = p1[0]
    elif not primary_model and p2:
        primary_model = p2[0]

    return {
        "priority_1_opencode": p1,
        "priority_2_hermes": p2,
        "priority_3_ollama": p3,
        "all_models": all_models,
        "primary": primary_model,
        "total_count": len(all_models),
    }


def set_active_boss(name: str, model: Optional[str] = None) -> bool:
    """Persist active Tier 1 Boss agent and model configuration."""
    init_db()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO active_agent_config (role, name, model, updated_at)
            VALUES ('boss', ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(role) DO UPDATE SET
                name = excluded.name,
                model = excluded.model,
                updated_at = CURRENT_TIMESTAMP
            """,
            (name, model or ""),
        )
    return True


def get_active_boss() -> Dict[str, Any]:
    """Retrieve active Tier 1 Boss agent configuration (default: antigravity)."""
    init_db()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT name, model, updated_at FROM active_agent_config WHERE role = 'boss'"
        ).fetchone()
        if row:
            return {
                "name": row["name"],
                "model": row["model"] or None,
                "updated_at": row["updated_at"],
            }
        return {"name": "antigravity", "model": None, "updated_at": None}


def set_active_worker(name: str, model: Optional[str] = None) -> bool:
    """Persist active Tier 3 Worker agent and model configuration."""
    init_db()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO active_agent_config (role, name, model, updated_at)
            VALUES ('worker', ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(role) DO UPDATE SET
                name = excluded.name,
                model = excluded.model,
                updated_at = CURRENT_TIMESTAMP
            """,
            (name, model or ""),
        )
    return True


def get_active_worker() -> Dict[str, Any]:
    """Retrieve active Tier 3 Worker agent configuration (default: hermes)."""
    init_db()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT name, model, updated_at FROM active_agent_config WHERE role = 'worker'"
        ).fetchone()
        if row:
            return {
                "name": row["name"],
                "model": row["model"] or None,
                "updated_at": row["updated_at"],
            }
        return {"name": "hermes", "model": None, "updated_at": None}

