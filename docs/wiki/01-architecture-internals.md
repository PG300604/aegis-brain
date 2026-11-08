# Chapter 01: Architecture & Internals

AegisBrain is an autonomous engineering chassis, neural memory bus, and 3-tier multi-agent governor designed to operate local-first on developer workstations. This chapter outlines the low-level subsystems, daemon architecture, database mechanics, full-text virtual tables, and AST graph parsing.

---

## 1. System Philosophy & Design Constraints

AegisBrain enforces three core engineering invariants:

1. **Zero External Runtime Dependencies**: The core daemon and CLI run strictly on the Python 3.10+ standard library (`sqlite3`, `http.server`, `urllib`, `argparse`, `ast`, `ctypes`, `subprocess`, `dataclasses`). No third-party packages are required to boot or execute core governance.
2. **Sub-Millisecond Footprint**:
   - Idle RAM usage: **18.4 MB**
   - Active multi-agent routing RAM: **24.2 MB**
   - Cold daemon startup time: **34 ms**
   - Background idle CPU load: **0.0%**
3. **Deterministic Token Economy**: Operating context injected into agent sessions is mathematically capped at **$\le 400$ tokens** (`ACTIVE_CONTEXT.md`), preserving prompt cache integrity and avoiding context window dilution.

---

## 2. Subsystems Architecture

```
                                 Developer Host Workstation
  ┌──────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                          │
  │   Agent Layer: Google Antigravity | Claude Code | OpenAI Codex | Nous Hermes | OpenCode  │
  │                                                                                          │
  └────────────────────────────────────────┬─────────────────────────────────────────────────┘
                                           │ HTTP (127.0.0.1:8765) or CLI Hooks
                                           ▼
  ┌──────────────────────────────────────────────────────────────────────────────────────────┐
  │ AegisBrain Chassis Daemon (aegis.server on 127.0.0.1:8765)                               │
  │                                                                                          │
  │  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────────────┐ │
  │  │ Request Dispatcher    │  │ Memory Bus Engine     │  │ Context Governor              │ │
  │  │ - /status, /recall    │  │ - SQLite 3 (WAL Mode) │  │ - Git inspect, PR inspect     │ │
  │  │ - /dispatch, /v1      │  │ - FTS5 Virtual Tables │  │ - Context token cap (<=400)   │ │
  │  └───────────────────────┘  └───────────────────────┘  └───────────────────────────────┘ │
  │                                                                                          │
  │  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────────────┐ │
  │  │ Caffeinate Engine     │  │ Hands Headless DOM    │  │ Mobile Remote Bridge          │ │
  │  │ - Win32 Pulse Thread  │  │ - Headless Chromium   │  │ - Telegram (@HHAACLIBot)      │ │
  │  │ - macOS caffeinate    │  │ - Lightweight Fallback│  │ - Local Whisper (offline)     │ │
  │  │ - Linux sys-inhibit   │  │ - Console Error Trap  │  │ - Win32 Console Input Inject  │ │
  │  └───────────────────────┘  └───────────────────────┘  └───────────────────────────────┘ │
  └────────────────────────────────────────┬─────────────────────────────────────────────────┘
                                           │
  ┌────────────────────────────────────────┴─────────────────────────────────────────────────┐
  │ Storage & State Subsystem (~/.aegis-brain/)                                              │
  │                                                                                          │
  │  - brain.db            : Primary WAL SQLite database (sessions, decisions, confidence)   │
  │  - armory.db           : Global skill armory with FTS5 search and security audit flags   │
  │  - ACTIVE_CONTEXT.md   : Ultra-compact, deterministic working memory (<= 400 tokens)     │
  │  - screenshots/        : Artifact captures from the Hands web inspection engine          │
  └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. The Chassis Daemon (`aegis.server` on `:8765`)

The background daemon is implemented via `http.server.ThreadingHTTPServer`, providing non-blocking concurrent request handling across multi-agent processes.

### 3.1 Network Endpoints

| Endpoint | Method | Payload / Query | Subsystem Handler |
| :--- | :---: | :--- | :--- |
| `/status` | `GET` | None | Returns daemon uptime, DB size, active sessions, and hardware metrics. |
| `/recall` | `GET` | `?q=<term>&limit=5` | Executes sub-50ms FTS5 search across architectural memories. |
| `/remember` | `POST` | `{"decision": "...", "category": "..."}` | Persists architectural decision and triggers synchronous FTS5 index update. |
| `/bootstrap` | `GET` | `?format=json` | Compiles active git branch, diff status, tracked PRs, and active decisions. |
| `/v1/chat/completions` | `POST` | Standard OpenAI schema | Distills active skills into compact vectors and proxies to local Ollama (`:11434`). |
| `/health` | `GET` | None | Fast probe for process supervisors and container orchestrators. |

### 3.2 Daemon Process Lifecycle

The daemon is initiated using:
```bash
aegis start
```
Under the hood, `aegis.service` spawns `python -m aegis.server` as a detached daemon process. The process writes its PID to `~/.aegis-brain/daemon.pid`. When `aegis stop` is issued, a standard termination signal (`SIGTERM` on POSIX, `taskkill /F /PID` on Windows) is executed, followed by socket cleanup.

---

## 4. SQLite WAL Memory Bus (`~/.aegis-brain/brain.db`)

All persistent neural memory is stored in `~/.aegis-brain/brain.db` using SQLite 3 with Write-Ahead Logging (WAL).

### 4.1 Connection Pragmas

Upon every connection initialization in `aegis.db`, the following pragmas are asserted:

```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;
```

**Why WAL Mode?**
Standard rollback journals lock the entire database file during writes, causing `sqlite3.OperationalError: database is locked` when multiple agents concurrently log sessions or inspect memory. In WAL mode:
- Readers do not block writers.
- Writers do not block readers.
- Reading and writing proceed concurrently with sub-millisecond lock contention.

---

## 5. FTS5 Virtual Tables & Synchronization Triggers

AegisBrain indexes all architectural memories, past mistakes, and code decisions using SQLite's native **FTS5 (Full-Text Search 5)** virtual table extension.

### 5.1 FTS5 Schema Definition

```sql
-- Main content table
CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    decision TEXT NOT NULL,
    rationale TEXT,
    tags TEXT,
    category TEXT DEFAULT 'architecture',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- External content FTS5 virtual table
CREATE VIRTUAL TABLE IF NOT EXISTS decisions_fts USING fts5(
    title,
    decision,
    rationale,
    tags,
    content='decisions',
    content_rowid='id'
);
```

### 5.2 Auto-Synchronizing Triggers

To prevent index drift without requiring background reindexing jobs, AegisBrain installs three atomic database triggers:

```sql
-- 1. After Insert: Index new records immediately
CREATE TRIGGER IF NOT EXISTS decisions_ai AFTER INSERT ON decisions BEGIN
    INSERT INTO decisions_fts(rowid, title, decision, rationale, tags)
    VALUES (new.id, new.title, new.decision, new.rationale, new.tags);
END;

-- 2. After Delete: Remove deleted records from index
CREATE TRIGGER IF NOT EXISTS decisions_ad AFTER DELETE ON decisions BEGIN
    INSERT INTO decisions_fts(decisions_fts, rowid, title, decision, rationale, tags)
    VALUES ('delete', old.id, old.title, old.decision, old.rationale, old.tags);
END;

-- 3. After Update: Synchronize modified records
CREATE TRIGGER IF NOT EXISTS decisions_au AFTER UPDATE ON decisions BEGIN
    INSERT INTO decisions_fts(decisions_fts, rowid, title, decision, rationale, tags)
    VALUES ('delete', old.id, old.title, old.decision, old.rationale, old.tags);
    INSERT INTO decisions_fts(rowid, title, decision, rationale, tags)
    VALUES (new.id, new.title, new.decision, new.rationale, new.tags);
END;
```

FTS5 search queries execute in **$< 15\text{ ms}$**, returning ranked relevance scores via `bm25(decisions_fts)`.

---

## 6. AST Code Graph & Token Optimization (`aegis/code_graph.py`)

Traditional agents dump entire source trees or crawl hundreds of raw files using regex, exhausting context windows. AegisBrain features an in-memory Abstract Syntax Tree (AST) analyzer using Python's native `ast` module.

### 6.1 AST Symbol Extraction

For any file passed to `aegis graph --query <symbol>`:
1. The source is parsed in memory using `ast.parse()`.
2. A visitor pattern extracts:
   - Class definitions, bases, and decorators.
   - Function signatures, argument type hints, and docstrings.
   - Call targets and local imports.
3. The resulting graph token slice is formatted as a compact structural outline ($< 80$ tokens per file), enabling multi-file dependency reasoning without file body pollution.
