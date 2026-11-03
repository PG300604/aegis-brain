# AegisBrain Architecture 🧠⚙️

AegisBrain is designed around three fundamental engineering principles:
1. **Zero External Dependencies**: Operates exclusively using the Python 3 standard library (`sqlite3`, `http.server`, `urllib`, `argparse`).
2. **Sub-Millisecond Footprint**: RAM consumption $< 25\text{ MB}$, sub-0.05s cold boot, zero CPU cycles when idle.
3. **Deterministic Token Economy**: Injects structured context under a strict $\le 400$-token budget to maximize prompt caching efficiency for flagship and local models alike.

---

## 🏛️ System Topology

```
                       ┌───────────────────────────────┐
                       │     Developer Host Machine    │
                       └───────────────┬───────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
 ┌──────────────┐              ┌──────────────┐              ┌────────────────┐
 │ Antigravity  │              │    Hermes    │              │  OpenCode CLI  │
 │  (Anthropic) │              │   (NousAI)   │              │ (Local Agents) │
 └──────┬───────┘              └──────┬───────┘              └───────┬────────┘
        │                             │                              │
        └─────────────────────────────┼──────────────────────────────┘
                                      ▼
                        ┌───────────────────────────┐
                        │    Aegis Daemon (:8765)   │
                        │   ThreadingHTTPServer     │
                        └─────────────┬─────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
┌──────────────────┐        ┌──────────────────┐          ┌───────────────────┐
│ Context Governor │        │    Memory Bus    │          │  Skill Distiller  │
│ - Git inspection │        │ - SQLite 3 (WAL) │          │ - Semantic matrix │
│ - Token budgeting│        │ - FTS5 Triggers  │          │ - Proxy /v1       │
│ - ACTIVE_CONTEXT │        │ - Dual Mode      │          │ - Ollama bridge   │
└──────────────────┘        └──────────────────┘          └───────────────────┘
```

---

## 1. Storage & Full-Text Engine (`aegis/db.py`)

- **WAL Mode (`PRAGMA journal_mode = WAL`)**: Allows concurrent multi-threaded reads while writes occur safely in the background without locking.
- **FTS5 External Content Virtual Table**: Full-text indexing is maintained across decisions, titles, rationales, and tags.
- **Auto-Sync Triggers**:
  - `decisions_ai`: Automatically indexes newly recorded architectural decisions.
  - `decisions_ad`: Removes deleted decisions from the index.
  - `decisions_au`: Updates modified decisions seamlessly.
- **Dual Mode (Public vs. Private)**:
  - When in `private` stealth mode, all writes to `sessions`, `decisions`, and `tracked_prs` are completely bypassed in memory. Zero bytes touch the disk.

---

## 2. Context Governor (`aegis/governor.py`)

Rather than dumping entire conversation histories or file trees, the Governor compiles a deterministic, compact summary containing:
1. **Current Workspace**: Active branch, git status (clean/dirty), and latest commit hash.
2. **Tracked PRs**: Active GitHub pull requests, labels, and CI status.
3. **Recent Decisions**: Up to 4 key architectural decisions and conventions.
4. **Active Alerts**: Proactive reminders from the background watchdog.

Target length is strictly constrained to **$\le 400$ tokens**, making it ideal for automatic injection on shell startup or system prompt prepending.

---

## 3. Skill Distiller & Reverse Proxy (`aegis/distiller.py`, `aegis/proxy.py`)

Smaller local models running via Ollama (e.g. Qwen 2.5 Coder 7B, DeepSeek Coder, Llama 3 8B) cannot parse hundreds of skill files without hallucinating or blowing up VRAM.

AegisBrain acts as an **OpenAI-compatible reverse proxy** on `http://127.0.0.1:8765/v1/chat/completions`:
1. It analyzes the incoming prompt to identify domain keywords (e.g. `spring`, `security`, `fastapi`).
2. It distills active skills into compact, actionable constraint vectors (<100 tokens).
3. It injects the active context + distilled skills into the `system` message.
4. It forwards the request to your local Ollama instance (`127.0.0.1:11434`) and records the session into SQLite.
