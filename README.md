# AegisBrain

<p align="center">
  <img src="assets/aegis-banner.svg" alt="AegisBrain Banner" width="100%">
</p>

<p align="center">
  <strong>Local neural memory bus and context governor for AI coding agents.</strong><br>
  Eliminates agent amnesia across terminal sessions, guarantees zero disk trace in private stealth mode, and distills 500+ skills into local Ollama models with a ≤ 400-token boot budget.
</p>

<p align="center">
  <a href="https://github.com/PG300604/aegis-brain/actions/workflows/ci.yml"><img src="https://github.com/PG300604/aegis-brain/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://sqlite.org"><img src="https://img.shields.io/badge/Storage-SQLite%20WAL%20%2B%20FTS5-003B57.svg?logo=sqlite&logoColor=white" alt="Storage"></a>
  <img src="https://img.shields.io/badge/RAM-%3C%2025%20MB-10B981.svg" alt="Memory">
  <img src="https://img.shields.io/badge/Boot-%3C%2050%20ms-38BDF8.svg" alt="Boot">
  <img src="https://img.shields.io/badge/Dependencies-Zero%20External-F97316.svg" alt="Zero Dependencies">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-6366F1.svg" alt="License: GPLv3"></a>
</p>

---

## Terminal Proof

```text
$ python package/install.py
[1/3] Initializing local neural memory bus...
[2/3] Setting up zero-elevation background autostart...
      Configured Windows User Startup VBScript runner.
[3/3] Registering global 'aegis' CLI command...
      Created Windows shim: ~/.local/bin/aegis.cmd
AegisBrain successfully installed.

$ aegis status
=== AegisBrain Status ===
Daemon:        RUNNING (http://127.0.0.1:8765)
Autostart:     ENABLED (starts on login/wake)
Mode:          PUBLIC
Database:      C:\Users\priya\.aegis-brain\brain.db (Exists)
Decisions:     6 recorded
Tracked PRs:   1 (spring-projects/spring-ai#7308)
Active Alerts: 0

$ aegis search "cardinality"
Found 1 matches for 'cardinality':
[1] [ARCHITECTURE] GenAI Observation Cardinality Protection
    Decision:  Low-cardinality protection: attributes omitted when empty to avoid metric explosion.
    Rationale: Aligns with OpenTelemetry semantic conventions for Micrometer/Spring AI.
```

---

## Motivation

Modern AI coding agents excel in isolated prompt windows, but suffer from two systemic constraints on developer workstations:

1. **The Amnesia Tax**: Launching a new terminal session or switching agents (Antigravity, Hermes, OpenCode, Aider) wipes working context. Developers repeatedly feed active branch states, ongoing pull requests, and architectural decisions back into prompts—burning tokens and introducing inconsistent assumptions.
2. **The Local Model Skill Gap**: Frontier cloud models benefit from vast, modular skill libraries. Local models running via Ollama (`qwen2.5-coder`, `deepseek-coder`, `llama3`) execute without domain constraints or architecture guardrails.

AegisBrain resolves both problems through a local, zero-overhead background daemon:
- **Zero External Dependencies**: Operates strictly on Python standard library modules (`sqlite3`, `http.server`, `urllib`, `argparse`).
- **Deterministic Budget**: Injects a structured markdown workspace summary bounded at $\le 400$ tokens to preserve prompt cache hits.
- **Dual-Mode Privacy**: Ephemeral stealth mode (`aegis mode private`) ensures zero bytes of prompt data or decision logs reach the disk.
- **Sub-Millisecond Search**: Indexed through SQLite WAL mode and FTS5 full-text virtual tables with synchronized triggers.

---

## Architecture

```mermaid
flowchart TD
    subgraph Clients["Agent Clients & Terminal Sessions"]
        A["Antigravity CLI"]
        B["Hermes Agent"]
        C["OpenCode / Aider"]
        D["Local IDEs & Scripts"]
    end

    subgraph Daemon["AegisBrain Daemon (127.0.0.1:8765)"]
        direction TB
        E["Threading HTTP Server"]
        F["Context Governor<br/><i>≤ 400 Token Budget</i>"]
        G["Memory Bus<br/><i>SQLite WAL + FTS5</i>"]
        H["Skill Distiller<br/><i>Semantic Rule Proxy</i>"]
        M["Media Bridge<br/><i>OpenHiggsfield Dispatch</i>"]
    end

    subgraph Targets["Execution & Storage Targets"]
        I["ACTIVE_CONTEXT.md"]
        J["brain.db (Local Disk)"]
        K["Local Ollama Runtime<br/><i>127.0.0.1:11434</i>"]
        L["OpenHiggsfield Studio / Models<br/><i>Flux 2, Seedance, Kling, Wan</i>"]
    end

    Clients --> E
    E --> F
    E --> G
    E --> H
    E --> M
    F --> I
    G -.->|"Public Mode"| J
    H --> K
    M --> L
```

---

## Quickstart

### 1. Installation

```bash
git clone https://github.com/PG300604/aegis-brain.git
cd aegis-brain
python package/install.py
```

The installer initializes `~/.aegis-brain/brain.db`, establishes zero-elevation autostart (Windows `shell:startup` VBScript, Linux `systemd`, or macOS `LaunchAgent`), and registers the global `aegis` CLI shim.

### 2. Verify System State

```bash
aegis status
```

### 3. Automatic Shell Hook

Add this single hook to your shell configuration (`$PROFILE` in PowerShell, or `~/.bashrc` in Bash/Zsh) so every opened terminal automatically compiles the latest workspace context:

```powershell
# PowerShell ($PROFILE)
python -m aegis.cli bootstrap > $null
```

```bash
# Bash / Zsh
python3 -m aegis.cli bootstrap > /dev/null 2>&1
```

---

## Workflows

### Memory Search

Search across all recorded architectural decisions, past technical solutions, and workspace notes instantly:

```bash
aegis search "FTS5 WAL mode"
```

### Record an Architectural Decision

```bash
aegis decision \
  --category "DATABASE" \
  --title "SQLite FTS5 Storage Engine" \
  --desc "Use SQLite WAL mode and FTS5 triggers for local search" \
  --rationale "Guarantees zero pip dependencies and sub-millisecond retrieval" \
  --tags database sqlite fts5 performance
```

### Context Bootstrapping

Compile an ultra-compact ($\le 400$ tokens) markdown snapshot of your current workspace for any agent:

```bash
aegis bootstrap
```

This writes `~/.aegis-brain/ACTIVE_CONTEXT.md` with active git branch status, modified files, recent commits, and tracked pull requests.

### Private Stealth Mode

When handling sensitive or proprietary client codebases:

```bash
# Activate zero-disk stealth mode
aegis mode private

# Re-enable persistent memory
aegis mode public
```

In private mode, all writes to `sessions`, `decisions`, and `tracked_prs` are completely bypassed in memory. No queries or tokens touch the disk.

### Background Watchdog & PR Sweep

Silently monitor tracked pull requests (e.g. Spring AI PR #7308) and local git repositories:

```bash
aegis poll
```

### Routing Local Models Through the Skill Proxy

Start the daemon and point any OpenAI-compatible client, agent CLI, or SDK to the Aegis proxy:

```bash
aegis start
```

```text
Base URL: http://127.0.0.1:8765/v1
```

AegisBrain intercepts prompts, fetches relevant workspace decisions and skill vectors (e.g., Karpathy simplicity, TypeScript patterns, or SQL optimization heuristics), injects them into the system prompt, and forwards the augmented request to your local Ollama server (`http://127.0.0.1:11434/v1`).

### AI Media Generation (OpenHiggsfield Bridge)

Dispatch image and video generation requests to [OpenHiggsfield](https://github.com/wide-trace/open-higgsfield) models (Flux 2, Seedance 2.5, Kling 3, Wan 2.6) directly from the command line while cataloging prompts, seeds, and asset metadata in the local memory bus:

```bash
aegis media --model flux-2 --prompt "Minimalist vector emblem for developer tools" --ratio 16:9
```

---

## Benchmarks

All measurements executed on Python 3.14 on Windows 11 / AMD & Intel host platforms.

| Metric | AegisBrain | Chroma / LanceDB (PyPI) | Redis / Memcached |
|---|---|---|---|
| **External Dependencies** | **0 (Python stdlib only)** | 15–35 packages | C daemon / Docker |
| **RAM Footprint** | **< 25 MB** | 180–350 MB | 50–120 MB |
| **Cold Boot Time** | **< 50 ms** | 1,200–2,800 ms | Service dependent |
| **Context Token Budget** | **≤ 400 tokens** | Unbounded | Unbounded |
| **Zero-Disk Stealth Mode** | **Native (`private`)** | Requires reconfig | In-memory only |
| **Test Suite Runtime** | **1.25s (8/8 passing)** | 8.5–18.0s | N/A |

---

## Documentation

Exhaustive references are maintained in the [`docs/`](docs/) directory:

| Document | Focus |
|---|---|
| [**Architecture Specification**](docs/ARCHITECTURE.md) | SQLite WAL mode, FTS5 virtual tables, sync triggers, and Context Governor internals. |
| [**CLI Command Reference**](docs/CLI_REFERENCE.md) | Exhaustive command manual with syntax, options, and output examples. |
| [**Zero-Elevation Autostart**](docs/AUTORUN_AND_STARTUP.md) | Windows VBScript background launcher, Linux systemd, and macOS LaunchAgents. |
| [**Local Model Skill Distillation**](docs/LOCAL_MODEL_DISTILLATION.md) | Skill compression matrix, prompt caching heuristics, and Ollama proxy routing. |
| [**Contributing Guide**](CONTRIBUTING.md) | Development setup, zero-dependency philosophy, and test execution. |
| [**Security Policy**](SECURITY.md) | Stealth mode specifications and responsible vulnerability disclosure. |

---

## Testing

Run the zero-dependency test suite via Python's standard library:

```bash
cd package
python -m unittest tests/test_aegis.py
```

```text
........
----------------------------------------------------------------------
Ran 8 tests in 1.257s

OK
```

All 8 tests execute in $< 1.5\text{ seconds}$ across Ubuntu, Windows, and macOS on every pull request.

---

## License

Copyright © 2026 **Priyanshu Ghosh** ([@PG300604](https://github.com/PG300604)).

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. See the [`LICENSE`](LICENSE) file for complete details.

Under GPLv3:
- Anyone may inspect, run, modify, and contribute to this open-source software.
- Any derivative work, distribution, or modifications **must remain free and open source under the same GPLv3 license**, preventing proprietary lock-in or unauthorized closed-source reproduction.
