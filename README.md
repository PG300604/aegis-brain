# AegisBrain 🧠⚡

> **A local, zero-UI background neural memory bus and agent orchestrator for developer machines.**
> Eliminates agent amnesia across CLIs (Antigravity, Hermes, OpenCode, Aider) and distills 500+ skills into local Ollama models with $< 400$-token instant boot.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Storage](https://img.shields.io/badge/Storage-SQLite%20WAL%20%2B%20FTS5-green.svg)](https://sqlite.org)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20External-orange.svg)](#architecture)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## ⚡ Why AegisBrain?

1. **Zero Agent Amnesia**: Every time you launch a new terminal, CLI, or agent session, AegisBrain dynamically compiles an ultra-compact `ACTIVE_CONTEXT.md` ($\le 400$ tokens) of active workspaces, branch states, open pull requests, and architectural decisions.
2. **Cross-Model Skill Distillation**: Smaller local models (e.g., `qwen2.5-coder`, `deepseek-coder`, `llama3` running via Ollama) don't have access to massive 500+ skill libraries. AegisBrain distills skills into semantic constraint blocks and injects them seamlessly via an OpenAI-compatible proxy (`http://127.0.0.1:8765/v1`).
3. **Public vs. Private Stealth Modes**:
   - `PUBLIC`: Full persistence in SQLite WAL with sub-millisecond FTS5 search.
   - `PRIVATE`: Zero-disk ephemeral stealth mode. No sessions, memories, or tokens ever touch disk.
4. **Proactive PR & Workspace Watchdog**: Silently monitors your active GitHub pull requests (like Spring AI PR #7308) and local Git repositories in the background, surfacing triage labels, CI checks, and review comments upon session startup.
5. **Zero External Dependencies**: Powered entirely by the Python standard library (`sqlite3`, `http.server`, `urllib`, `argparse`). Boots in $< 0.05$ seconds and consumes $< 25\text{ MB}$ of RAM.

---

## 🏗️ Architecture

```
                               ┌──────────────────────────────────────────────┐
                               │                 Developer PC                 │
                               └──────────────────────┬───────────────────────┘
                                                      │
         ┌─────────────────────────┬──────────────────┴──────────────────┬────────────────────────┐
         │                         │                                     │                        │
  Antigravity CLI             Hermes Agent                           OpenCode CLI             Local Ollama
(Claude / Gemini)          (Thinking / Fallback)                    (Coding Agents)       (Qwen / DeepSeek 7B)
         │                         │                                     │                        │
         └─────────────────────────┼─────────────────────────────────────┼────────────────────────┘
                                   ▼
                       ┌───────────────────────┐
                       │  AegisBrain Daemon    │  (127.0.0.1:8765)
                       │  Zero-Dep HTTP Server │
                       └───────────┬───────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│ Governor & Boot  │      │ Memory Bus (WAL) │      │ Skill Distiller  │
│ - ACTIVE_CONTEXT │      │ - SQLite + FTS5  │      │ - Dynamic Rules  │
│ - Git Inspection │      │ - Dual Mode      │      │ - Proxy /v1      │
└──────────────────┘      └──────────────────┘      └──────────────────┘
```

---

## 🚀 Quick Start

### 1. Installation
Clone or place AegisBrain in your preferred development directory:
```bash
git clone https://github.com/your-username/aegis-brain.git P:/open-source/aegis-brain
cd P:/open-source/aegis-brain
```

### 2. Seed Initial Project Knowledge
```bash
python -m aegis.cli seed
```

### 3. Check System Status
```bash
python -m aegis.cli status
```
Output:
```text
=== AegisBrain Status ===
Mode:          PUBLIC
Database:      C:\Users\priya\.aegis-brain\brain.db (Exists)
Decisions:     3 recorded
Tracked PRs:   1
  - spring-projects/spring-ai#7308: Add missing GenAI request attributes to observations [open]
Active Alerts: 0
```

### 4. Sub-Millisecond Memory Search (SQLite FTS5)
```bash
python -m aegis.cli search "cardinality"
```

### 5. Generate Instant Agent Bootstrap Context
```bash
python -m aegis.cli bootstrap -w P:/open-source/spring-ai
```

### 6. Toggle Private Stealth Mode
```bash
python -m aegis.cli mode private
# To return to public recording:
python -m aegis.cli mode public
```

---

## 🤖 Hooking into Agents & Local LLMs

### Hook into Any CLI Session
Add this one-liner to your shell profile (`$PROFILE` in PowerShell or `~/.bashrc`):
```powershell
# Auto-sync active context on CLI launch
python -m aegis.cli bootstrap > $null
```

### Route Local Ollama Models Through Aegis Skill Proxy
Start the Aegis daemon:
```bash
python -m aegis.cli daemon --port 8765
```
Configure your agent CLI (Hermes, OpenCode, Aider) or application to point to:
```text
Base URL: http://127.0.0.1:8765/v1
```
AegisBrain intercepts every request, injects the active workspace context and relevant skill guardrails into the system prompt, and forwards it to your local Ollama runtime (`http://127.0.0.1:11434/v1`).

---

## 🧪 Testing

Run the zero-dependency test suite:
```bash
python -m unittest tests/test_aegis.py
```
```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.899s

OK
```

---

## 📄 License
MIT © 2026 Priyanshu Ghosh.
