# AegisBrain 🧠⚡

> **A zero-dependency, local neural memory bus and agent orchestrator for developer workstations.**  
> Eliminates agent amnesia across CLIs (Antigravity, Hermes, Claude Code, OpenCode, Aider), guarantees zero disk trace in private stealth mode, and distills 500+ skills into local Ollama models with a $< 400$-token instant boot budget.

[![CI](https://github.com/PG300604/aegis-brain/actions/workflows/ci.yml/badge.svg)](https://github.com/PG300604/aegis-brain/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Storage](https://img.shields.io/badge/Storage-SQLite%20WAL%20%2B%20FTS5-003B57.svg?logo=sqlite&logoColor=white)](https://sqlite.org)
[![Memory](https://img.shields.io/badge/RAM-%3C%2025%20MB-brightgreen.svg)](#benchmarks)
[![Boot Time](https://img.shields.io/badge/Boot-%3C%2050%20ms-success.svg)](#benchmarks)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20External-orange.svg)](#architecture)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

---

## ⚡ The Problem: Agent Amnesia & The Local Skill Gap

Modern AI coding agents excel in isolated prompt windows, but suffer from two major architectural flaws on developer machines:

1. **Terminal Amnesia**: Every time you launch a new terminal, switch virtual machines, or start a new chat session in Antigravity or Hermes, the agent forgets previous context. Developers spend precious minutes and thousands of prompt tokens repeatedly feeding workspace status, ongoing PRs, and architectural decisions.
2. **The Local Model Skill Gap**: Flagship cloud models have access to hundreds of modular skills, prompts, and linters. Local open-source models (e.g. `qwen2.5-coder`, `deepseek-coder`, `llama3` running via Ollama) run naked without domain knowledge or constraints, leading to inconsistent code style and hallucinated abstractions.

---

## 💡 The Solution: AegisBrain

**AegisBrain** is a lightweight, zero-UI background neural daemon that runs locally on your machine:

- **🧠 Unified Neural Memory Bus**: Automatically indexes architectural decisions, session summaries, and project knowledge using SQLite WAL mode and sub-millisecond FTS5 full-text search.
- **⚡ Deterministic Context Governor**: Synthesizes active workspace state, Git diffs, commits, and tracked pull requests into an ultra-compact `ACTIVE_CONTEXT.md` ($\le 400$ tokens) injected into every session.
- **🛡️ Dual Mode Operation (Public vs. Private Stealth)**:
  - `PUBLIC`: Full persistence in SQLite WAL with sub-millisecond FTS5 search.
  - `PRIVATE`: Zero-disk ephemeral stealth mode. No queries, sessions, or tokens touch the disk.
- **🔄 Cross-Model Skill Distillation**: Distills 500+ skills into semantic constraint matrices and injects them seamlessly via an OpenAI-compatible proxy (`http://127.0.0.1:8765/v1`) in front of your local Ollama server.
- **🐕 Proactive Background Watchdog**: Silently sweeps tracked GitHub PRs (e.g., Spring AI PR #7308) and local Git repositories, notifying you of review comments, triage labels, and CI status the moment you open your terminal.
- **🪶 Zero External Dependencies**: Powered entirely by Python's standard library (`sqlite3`, `http.server`, `urllib`, `argparse`). Uses $< 25\text{ MB}$ of RAM and boots in $< 50\text{ ms}$.

---

## 🏛️ System Architecture

```
                       ┌──────────────────────────────────────────────┐
                       │            Developer Workstation             │
                       └──────────────────────┬───────────────────────┘
                                              │
         ┌─────────────────────────┬──────────┴──────────┬────────────────────────┐
         │                         │                     │                        │
  Antigravity CLI             Hermes Agent          OpenCode CLI             Local Ollama
(Claude / Gemini)          (Thinking / Fallback)   (Coding Agents)       (Qwen / DeepSeek 7B)
         │                         │                     │                        │
         └─────────────────────────┼─────────────────────┼────────────────────────┘
                                   ▼
                       ┌───────────────────────┐
                       │   AegisBrain Daemon   │  (127.0.0.1:8765)
                       │  ThreadingHTTPServer  │
                       └───────────┬───────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│ Context Governor │      │ Memory Bus (WAL) │      │ Skill Distiller  │
│ - ACTIVE_CONTEXT │      │ - SQLite + FTS5  │      │ - Dynamic Rules  │
│ - Git Inspection │      │ - Dual Mode      │      │ - Proxy /v1      │
└──────────────────┘      └──────────────────┘      └──────────────────┘
```

---

## 📂 Repository Structure

The repository is organized into distinct, focused packages for clean navigation:

```
aegis-brain/
├── package/                       # Core installable Python package
│   ├── aegis/                     # Daemon, database, governor, proxy, watchdog
│   │   ├── __init__.py
│   │   ├── cli.py                 # Multi-command CLI entry point
│   │   ├── config.py              # Environment configuration & path resolution
│   │   ├── db.py                  # SQLite WAL + FTS5 full-text engine
│   │   ├── distiller.py           # Skill distillation & prompt augmentation
│   │   ├── governor.py            # Active workspace context compiler
│   │   ├── hooks.py               # Session boot & bootstrap hooks
│   │   ├── proxy.py               # OpenAI-compatible Ollama proxy
│   │   ├── server.py              # Multi-threaded background HTTP server
│   │   ├── service.py             # OS-level autostart (Windows VBS / systemd / launchd)
│   │   └── watchdog.py            # GitHub PR and local repository poller
│   ├── tests/                     # Standard library test suite
│   │   └── test_aegis.py
│   ├── install.py                 # 1-Click cross-platform installer script
│   └── pyproject.toml             # Build configuration (Python >= 3.10)
│
├── skills/                        # AI coding agent skills
│   └── aegis/
│       └── SKILL.md               # Companion skill for Antigravity, Hermes & Claude Code
│
├── docs/                          # Deep-dive architectural documentation
│   ├── ARCHITECTURE.md            # Topology, SQLite schema & FTS5 triggers
│   ├── CLI_REFERENCE.md           # Exhaustive CLI command reference
│   ├── AUTORUN_AND_STARTUP.md     # Zero-elevation boot & wake configuration
│   └── LOCAL_MODEL_DISTILLATION.md# Skill vectors & Ollama integration guide
│
├── .github/                       # GitHub workflows & issue/PR templates
│   ├── workflows/ci.yml           # Cross-platform matrix CI (Ubuntu, Windows, macOS)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
│
├── CODE_OF_CONDUCT.md             # Contributor Covenant 2.1
├── CONTRIBUTING.md                # Contribution guidelines & test procedures
├── SECURITY.md                    # Private stealth mode guarantees & vulnerability reporting
├── LICENSE                        # GNU General Public License v3 (GPLv3)
└── README.md
```

---

## 🚀 Quick Start

### 1. 1-Click Installation
Clone the repository and run the automated installer:

```bash
git clone https://github.com/PG300604/aegis-brain.git
cd aegis-brain
python package/install.py
```

The installer will:
1. Initialize your local SQLite WAL database at `~/.aegis-brain/brain.db`.
2. Configure **zero-elevation background autostart** on system boot and wake.
3. Install the global `aegis` CLI shim in your user binary path (`~/.local/bin/`).

---

### 2. Check Daemon & System Status
```bash
aegis status
```
```text
=== AegisBrain Status ===
Daemon:        RUNNING (http://127.0.0.1:8765)
Autostart:     ENABLED (starts on login/wake)
Mode:          PUBLIC
Database:      C:\Users\username\.aegis-brain\brain.db (Exists)
Decisions:     5 recorded
Tracked PRs:   1
  - spring-projects/spring-ai#7308: Add missing GenAI request attributes to observations [open]
Active Alerts: 0
```

---

### 3. Sub-Millisecond Knowledge Search (SQLite FTS5)
Search through all your recorded architectural decisions, past project solutions, and codebase conventions instantly:

```bash
aegis search "cardinality"
```

---

### 4. Record an Architectural Decision
```bash
aegis decision "Use SQLite FTS5 for local neural index" \
  --context "Need sub-millisecond search without external vector DB dependencies" \
  --rationale "FTS5 with WAL mode provides instant full-text search with zero pip dependencies" \
  --tags "database,fts5,sqlite,performance"
```

---

### 5. Generate Instant Agent Bootstrap Context
Compile an ultra-compact ($\le 400$ token) markdown snapshot of your current workspace:

```bash
aegis bootstrap
```
This generates `~/.aegis-brain/ACTIVE_CONTEXT.md` containing active branch status, modified files, recent commits, and open pull requests.

---

### 6. Toggle Private Stealth Mode
When working with confidential client repositories or proprietary code:

```bash
# Enable stealth mode (zero disk logging)
aegis mode private

# Re-enable persistent memory
aegis mode public
```

---

### 7. Background Autostart Control
You have full control over background startup at all times:

```bash
# Enable zero-elevation autostart on system boot/wake
aegis autostart on

# Disable autostart and remove background runner
aegis autostart off

# Start or stop the daemon manually
aegis start
aegis stop
```

---

## 🤖 Hooking into Agents & Local LLMs

### Automatic Terminal / CLI Session Hook
Add this line to your shell profile (`$PROFILE` in PowerShell or `~/.bashrc` in Linux/macOS) so every terminal window automatically syncs the latest context:

```powershell
# PowerShell ($PROFILE)
python -m aegis.cli bootstrap > $null
```
```bash
# Bash (~/.bashrc) / Zsh (~/.zshrc)
python3 -m aegis.cli bootstrap > /dev/null 2>&1
```

### Route Local Ollama Models Through Aegis Skill Proxy
Start the Aegis daemon:
```bash
aegis start
```

Point any OpenAI-compatible client, agent CLI (Hermes, OpenCode, Aider), or SDK to the Aegis proxy:
```text
Base URL: http://127.0.0.1:8765/v1
```

AegisBrain intercepts incoming prompts, retrieves active workspace context and matching skill vectors (e.g. Karpathy simplicity, TypeScript patterns, or SQL optimizations), appends them to the system prompt, and forwards the augmented request to your local Ollama server (`http://127.0.0.1:11434/v1`).

---

## 📖 Documentation Hub

Explore deep dives on internal components and workflows in the [`docs/`](docs/) directory:

| Document | Description |
|---|---|
| [**Architecture Deep Dive**](docs/ARCHITECTURE.md) | System topology, SQLite WAL mode, FTS5 triggers, and Context Governor internals |
| [**CLI Command Reference**](docs/CLI_REFERENCE.md) | Exhaustive command manual with syntax, options, and output examples |
| [**Zero-Elevation Autostart**](docs/AUTORUN_AND_STARTUP.md) | Windows VBScript background launcher, Linux systemd, and macOS LaunchAgents |
| [**Local Model Skill Distillation**](docs/LOCAL_MODEL_DISTILLATION.md) | Skill compression matrix, prompt caching heuristics, and Ollama proxy routing |
| [**Contributing Guide**](CONTRIBUTING.md) | Development setup, zero-dependency philosophy, and testing instructions |
| [**Security Policy**](SECURITY.md) | Private stealth mode specifications and vulnerability disclosure protocol |

---

## 🧪 Testing

AegisBrain maintains strict zero-dependency test coverage using the standard library `unittest` runner:

```bash
cd package
python -m unittest tests/test_aegis.py
```
```text
.......
----------------------------------------------------------------------
Ran 7 tests in 1.224s

OK
```

All 7 test suites run in $< 1.5\text{ seconds}$ across Windows, Ubuntu, and macOS on every pull request.

---

## 📊 Benchmarks

| Metric | AegisBrain | Chroma / LanceDB (PyPI) | Redis / Memcached |
|---|---|---|---|
| **External Dependencies** | **0 (Python stdlib)** | 15–35 packages | C daemon / Docker |
| **RAM Footprint** | **$< 25\text{ MB}$** | 180–350 MB | 50–120 MB |
| **Cold Boot Time** | **$< 50\text{ ms}$** | 1,200–2,800 ms | Service dependent |
| **Context Token Budget** | **$\le 400$ tokens** | Unbounded | Unbounded |
| **Zero-Disk Stealth Mode** | **Native (`private`)** | Requires reconfig | In-memory only |

---

## 📄 License & Attribution

Copyright © 2026 **Priyanshu Ghosh** ([@PG300604](https://github.com/PG300604)).

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. See the [`LICENSE`](LICENSE) file for complete details.

Under GPLv3:
- Anyone may inspect, run, modify, and contribute to this open-source software.
- Any derivative work, distribution, or modifications **must remain free and open source under the same GPLv3 license**, preventing proprietary lock-in or unauthorized closed-source reproduction.
