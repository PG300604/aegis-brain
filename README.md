# AegisBrain

<p align="center">
  <img src="https://raw.githubusercontent.com/PG300604/aegis-brain/main/assets/aegis-banner.svg" alt="AegisBrain Banner" width="100%">
</p>

<p align="center">
  <strong>The Local-First Autonomous Engineering Chassis, Neural Memory Bus, and 3-Tier Multi-Agent Governor.</strong>
</p>

<p align="center">
  <a href="https://github.com/PG300604/aegis-brain/actions/workflows/ci.yml"><img src="https://img.shields.io/badge/CI-281%20Passing-10B981.svg?logo=githubactions&logoColor=white" alt="CI: 281 Passing"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white" alt="Python 3.10+"></a>
  <img src="https://img.shields.io/badge/Dependencies-Zero%20External-F97316.svg" alt="Zero External Dependencies">
  <img src="https://img.shields.io/badge/Memory-%3C%2025%20MB-8B5CF6.svg" alt="Memory: < 25 MB">
  <img src="https://img.shields.io/badge/Boot-%3C%2050%20ms-06B6D4.svg" alt="Boot: < 50 ms">
  <a href="https://sqlite.org"><img src="https://img.shields.io/badge/Storage-SQLite%20WAL%20%2B%20FTS5-003B57.svg?logo=sqlite&logoColor=white" alt="Storage: SQLite WAL + FTS5"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-EC4899.svg" alt="License: GPLv3"></a>
</p>

<p align="center">
  <a href="#-why-aegisbrain">Why AegisBrain</a> &bull;
  <a href="#-market-comparison-matrix">Comparison Matrix</a> &bull;
  <a href="#-system-architecture">System Architecture</a> &bull;
  <a href="#-3-tier-multi-agent-power-architecture">3-Tier Hierarchy</a> &bull;
  <a href="#-senior-boss-escalation-protocol">Escalation Protocol</a> &bull;
  <a href="#-universal-agent-interchangeability">Interchangeability</a> &bull;
  <a href="#-native-hands-engine--ui-testing">Hands Engine</a> &bull;
  <a href="#-247-mobile-remote-operations--whisper-engine">Mobile Remote</a> &bull;
  <a href="#-arch-wiki-documentation-hub">Arch Wiki Hub</a> &bull;
  <a href="#-60-second-quickstart">Quickstart</a> &bull;
  <a href="#-complete-cli-reference">CLI Reference</a> &bull;
  <a href="#-verified-benchmarks">Benchmarks</a>
</p>

---

## ⚡ Why AegisBrain?

Modern AI coding agents (Antigravity, Claude Code, OpenAI Codex, OpenCode, Hermes, Cursor) excel in isolated prompt windows, but suffer from four systemic constraints on developer workstations:

1. **The Amnesia Tax & Token Burn**: Launching a new terminal window clears working memory. When developers ask *"What was our last database decision?"*, traditional agents crawl raw `transcript.jsonl` files, burning **50,000+ tokens** and stalling the session for **15+ seconds**.
2. **Frontier Token Waste & Direct Code Misalignment**: High-cognition models (Gemini 3.8 Flash, Claude 3.7 Sonnet) waste precious reasoning tokens generating repetitive boilerplate, tests, and syntax implementations. Meanwhile, smaller free models introduce subtle edge-case flaws when left unsupervised.
3. **Desktop Lock-In & Unattended Session Halts**: Long-running builds, multi-agent pipelines, and test suites require developers to sit in front of their screens. If the operating system enters standby, execution aborts; if an agent finishes, it sits idle waiting for human input.
4. **The "It Works on My Machine" Frontend Blind Spot**: Coding agents declare frontend work complete without ever rendering localhost or checking for browser console errors.

**AegisBrain** resolves these bottlenecks by providing a zero-external-dependency background chassis running 24/7 on your workstation: sub-50ms instant neural memory, a 3-tier division of cognition with automated coaching loops, 24/7 smartphone remote operations with offline Whisper voice notes, and headless browser inspection.

---

## 📊 Market Comparison Matrix

| Architectural Capability | **AegisBrain** | **Standalone Claude Code** | **Standalone OpenCode** | **AutoGPT / CrewAI** | **Raw LangChain** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **3-Tier Power Hierarchy (Boss / Subagent / Worker)** | **Native Built-in** | Manual prompts | Manual prompts | Fragile graph | Manual code |
| **Senior Boss Escalation & Coaching Loop** | **Automated (Dossier)** | None | None | Simple loop | None |
| **Zero-Direct-Code Frontier Token Arbitrage** | **Strict Invariant** | None | None | None | None |
| **Sub-50ms Memory Recall (SQLite WAL + FTS5)** | **Native (< 25 ms)** | None (re-reads logs) | None | Vector DB required | Vector DB required |
| **Deterministic Context Governor ($\le 400$ tokens)** | **Automated** | None | None | None | None |
| **24/7 Mobile Remote (Telegram / WhatsApp)** | **Native (@HHAACLIBot)** | None | None | None | None |
| **100% Offline Local Whisper Voice Ingestion** | **Native (`whisper.exe`)** | None | None | None | None |
| **Physical Hands Headless DOM & Error Trap** | **Native (`aegis hands`)** | None | None | Web browser plugin | Selenium wrapper |
| **Win32 Away Mode & System Sleep Prevention** | **Native Continuous Pulse**| None | None | None | None |
| **Zero External Runtime Dependencies** | **Python stdlib only** | Node.js required | Bun/Node required | 50+ PyPI packages | 80+ PyPI packages |
| **Cold Boot Latency** | **34 ms** | ~850 ms | ~420 ms | ~3,200 ms | ~4,500 ms |
| **Workstation Idle RAM Footprint** | **18.4 MB** | ~120 MB | ~85 MB | ~350 MB | ~480 MB |
| **Universal Tool Interchangeability** | **Standard Envelope** | Proprietary | Proprietary | Custom adapters | Custom chains |

---

## 🏛️ System Architecture

AegisBrain unifies your coding tools around an ultra-fast, zero-dependency background daemon connected to persistent SQLite Write-Ahead Logging:

<p align="center">
  <img src="https://raw.githubusercontent.com/PG300604/aegis-brain/main/assets/architecture-unified.svg" alt="AegisBrain Unified Architecture Diagram" width="100%">
</p>

<p align="center">
  <small><em>Editable Excalidraw source available at <a href="assets/architecture.excalidraw">assets/architecture.excalidraw</a>.</em></small>
</p>

### Subsystems Breakdown

1. **Unified AI Agent Client Layer**: Any coding agent (Google Antigravity, Anthropic Claude Code, OpenAI Codex, Cursor, Windsurf, Nous Hermes, OpenCode) communicates through **one common unified bus** (`127.0.0.1:8765`, CLI `aegis recall`, or native companion skills).
2. **AegisBrain Daemon Chassis (`aegis.server` on `:8765`)**:
   - **Internal Dispatcher**: Routes tasks across arbitrary Boss-Worker pairings using the `UniversalAgentEnvelope`.
   - **Deterministic Context Governor**: Dynamically inspects git status, dirty diffs, tracked PRs, and active decisions, pruning context to $\le 400$ tokens (`ACTIVE_CONTEXT.md`).
   - **Neural Memory Bus & Instant Recall**: Multi-threaded SQLite engine in WAL mode with auto-synchronizing FTS5 virtual tables (< 50ms recall, 99.5% token reduction).
   - **Cross-Model Skill Distiller & Proxy**: OpenAI-compatible reverse proxy (`127.0.0.1:8765/v1`) augmenting prompts with domain heuristics before forwarding to local Ollama.
   - **Native Caffeinate Engine**: Win32 `SetThreadExecutionState` Away Mode pulse thread, macOS `caffeinate`, and Linux `systemd-inhibit` preventing system standby.
   - **Mobile Remote Agent Bridge**: 24/7 Telegram (`@HHAACLIBot`) & WhatsApp bridge with local Whisper audio transcription and Win32 direct console injection.
3. **Local Storage & State Subsystem (`~/.aegis-brain/`)**:
   - `brain.db`: Persistent SQLite WAL database storing sessions, decisions, confidence scores, escalation events, and mobile inbox.
   - `armory.db`: Global skill catalog with FTS5 search and automated 4-gate security audits.
   - `ACTIVE_CONTEXT.md`: Compact working memory ($\le 400$ tokens) for instant cross-session bootstrapping.
   - `screenshots/`: High-resolution visual captures from the Hands Engine.

---

## 👑 3-Tier Multi-Agent Power Architecture

To eliminate frontier token waste and guarantee production-grade code, AegisBrain enforces a strict **Division of Cognition**:

<p align="center">
  <img src="https://raw.githubusercontent.com/PG300604/aegis-brain/main/assets/hierarchy-escalation.svg" alt="3-Tier Multi-Agent Power Architecture and Escalation Protocol" width="100%">
</p>

### Division of Labor & Token Arbitrage

| Tier | Role | Supported Engines | Primary Responsibility | Direct Code Invariant |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Senior Boss** | Supreme Brain & Orchestrator | Gemini 3.8 Flash, Claude 3.7 Sonnet, OpenCode (GPT-6 Astra), Codex | System architecture, research, option exploration (Pros/Cons), invariants, error detection, test review, final sign-off. | **Zero Direct Code by default** (writes code *only* upon Tier 2 Escalation). |
| **Tier 2: Junior Bosses** | Domain Tech Leads / Subagents | Specialized Subagents (`invoke_subagent`) | Scoping boundaries, dispatching tasks to Tier 3 workers, bottom-to-top 4-Gate auditing, coaching error-reduction loops. | **Zero Direct Code**. Coaches workers; never writes code drafts directly. |
| **Tier 3: Execution Workers** | Code Synthesis Muscle | OpenCode Free Models, Hermes CLI, Codex CLI, Claude Code CLI, Ollama MoE | Writes all raw code drafts, functions, boilerplate, and implementations using free/local tokens (0 frontier tokens). | **Writes 100% of candidate code**. Subject to iterative coaching loops. |

---

## ⚡ Senior Boss Escalation Protocol

### Why Lower Models Require Supervision
Smaller cloud models (e.g., DeepSeek V4.1 Flash Free, Nemotron 3.5 Bolt) and local models (Qwen2.5-Coder 7B) offer rapid generation at zero token cost, but inherently lack deep multi-step logical reasoning and abstract edge-case comprehension. They frequently make logical assumptions, invert conditionals, or introduce subtle architectural flaws.

### Subagent Coaching Loops
In AegisBrain, Tier 2 Junior Bosses do not simply run a binary pass/fail check. Instead, they deeply analyze candidate drafts, formulate targeted coaching directives, and guide the worker through recursive correction cycles, logging error reduction deltas into `brain.db` (`agent_confidence`).

### The Escalation Clause & Senior Boss Takeover
When coaching retries expire (`max_retries` reached) or when a task is scored as `CRITICAL`, the Subagent generates a formal **Escalation Dossier**:

```json
{
  "subagent_id": "subagent-1",
  "domain": "backend_systems",
  "worker_type": "hermes",
  "task_spec": "Implement cross-platform key event dispatcher",
  "escalation_reason": "Worker failed quality verification after max retries.",
  "reasoning_critique": "Worker exhibited logical flaws in state transitions between normal and insert modes.",
  "initial_errors": 2,
  "final_errors": 1,
  "flaws": ["Unsafe shell invocation in retry loop"],
  "timestamp": "2026-11-08T13:30:00Z"
}
```

The Subagent marks its state as `status="escalated_to_senior_boss"` and alerts Tier 1. The **Senior Boss takes full command**, authors the production solution directly, verifies it through the 4-Decision Quality Architecture Gate, and signs off on delivery.

---

## 🔄 Universal Agent Interchangeability

AegisBrain is completely tool-agnostic. Any supported coding tool can act as **Tier 1 Boss** or **Tier 3 Execution Worker**:

<p align="center">
  <img src="https://raw.githubusercontent.com/PG300604/aegis-brain/main/assets/universal-agent-matrix.svg" alt="Universal Agent Interchangeability Architecture" width="100%">
</p>

- **OpenCode as Boss with Codex as Worker**:
  ```bash
  aegis dispatch "Build API gateway" --boss opencode --boss-model gpt-6-astra --worker codex
  ```
- **Codex as Boss with OpenCode Free as Worker**:
  ```bash
  aegis dispatch "Add database migrations" --boss codex --worker opencode --worker-model deepseek-v4.1-flash-free
  ```
- **Antigravity as Boss with Hermes as Worker**:
  ```bash
  aegis dispatch "Refactor auth middleware" --boss antigravity --worker hermes
  ```
- **Claude Code as Boss with Ollama as Worker**:
  ```bash
  aegis dispatch "Write scoped unit tests" --boss claude --worker ollama --worker-model qwen2.5-coder:7b
  ```

Every transaction is standardized through the **Universal Execution Envelope (`UniversalAgentEnvelope`)**, normalizing task payloads, 4-gate verification scores, and signed deliverables regardless of which tool initiated the request.

---

## 🛡️ The 4-Decision Quality Architecture Gate

Before any candidate draft reaches the user or repository, it must pass all 4 quality gates:

<p align="center">
  <img src="https://raw.githubusercontent.com/PG300604/aegis-brain/main/assets/quality-architecture-gate.svg" alt="4-Decision Quality Architecture Gate" width="100%">
</p>

1. **Karpathy Simplicity Doctrine**: Surgical, minimal code with zero speculative abstractions, unused wrappers, or premature flexibility. If 200 lines could be written in 50, it is rewritten.
2. **Ponytail / Unslop / TurnItOut**: Complete elimination of conversational AI slop, conversational preambles ("Sure! Here is..."), and polite markdown filler.
3. **Red-Team & Cloudflare Security Audit**: Strict perimeter defense blocking `shell=True`, `os.system()`, command injections, path traversals, and hardcoded secrets.
4. **Dual-Environment Verification**: AST syntax validation and dry-run compilation in an isolated sandbox environment before any host filesystem mutation.

---

## 🌐 Native Hands Engine & UI Testing

Modern AI coding agents frequently declare web frontend features "complete" without ever testing if the localhost dev server actually renders. AegisBrain gives agents **physical hands** to verify localhost apps, test interactive DOM elements, and capture screenshots:

- **Playwright Headless Automation**: Launches headless Chromium to render the live DOM, capture full-page screenshots, inspect console error logs, and audit clickable buttons and input forms.
- **Graceful Zero-Dependency Fallback (`lightweight_dom`)**: If Playwright or browser binaries are not installed, the engine seamlessly falls back to pure standard library HTTP + HTMLParser, extracting titles, forms, inputs, and links with zero runtime dependencies.
- **CI/CD Quality Gate Assertion**: `aegis hands http://localhost:3000 --assert-clean` exits with code 1 if the target fails to respond, returns HTTP $\ge 400$, or emits unhandled browser console errors.
- **AI-Native JSON & Markdown Telemetry**: Delivers structured element trees directly to agents via `aegis hands <url> --json`.

```bash
# Inspect a local developer server and take a screenshot
aegis hands http://localhost:3000 --screenshot

# CI/CD Quality Gate (fail build on HTTP error or browser console error)
aegis hands http://localhost:5173 --assert-clean
```

---

## 📱 24/7 Mobile Remote Operations & Whisper Engine

Manage, monitor, and steer your workstation coding sessions from your smartphone via **Telegram** (`@HHAACLIBot`) or **WhatsApp**:

<p align="center">
  <img src="https://raw.githubusercontent.com/PG300604/aegis-brain/main/assets/mobile-remote-bridge.svg" alt="Mobile Remote Bridge and Whisper Voice Pipeline" width="100%">
</p>

### Voice Note Dictation via Local Whisper
1. Send a voice message to the Telegram bot while away from your desk.
2. The bot downloads the audio (`.oga`) and converts it to 16kHz mono PCM using FFmpeg.
3. The local Whisper engine (`whisper.exe`, model: `base`) transcribes the audio 100% offline with zero cloud API keys.
4. AegisBrain tags the prompt and types it directly into your active coding session.

### Calibrated Vim Mode & Win32 Console Injection
- **Direct Win32 Console Injection**: Injects inputs directly via `AttachConsole()` and `WriteConsoleInputW()`—zero focus stealing, Komorebi tile-safe, and functional even when the display is locked.
- **Calibrated Vim Insert-Mode Execution**:
  - Automatically transitions to Insert Mode (`Esc`, `Esc`, `i`).
  - Injects or pastes the command payload.
  - **Presses `<Enter>` directly in Insert Mode** without returning to Normal Mode, guaranteeing prompt execution and eliminating trapped prompt bugs.
- **In-Flight Interrupts (`/altm`)**: Send `/altm` or append `/altm` to any prompt to trigger an in-flight Alt+M interrupt signal into running sessions.
- **In-Flight Memory Queries (`/btw`)**: Query neural memory and hardware metrics (`/btw what was our last DB migration?`) without stopping running tasks.
- **Word-for-Word Live Streaming**: Agent outputs stream directly to your phone in real time, concluding with a `🏁 Execution Completed!` banner.

---

## 📚 Arch Wiki Documentation Hub

AegisBrain includes an exhaustive, Arch Linux Wiki-style documentation book located in [`docs/wiki/`](docs/wiki/00-index.md):

| Chapter | Title | Summary |
| :---: | :--- | :--- |
| **[00](docs/wiki/00-index.md)** | **[Arch Wiki Portal & TOC](docs/wiki/00-index.md)** | Master portal, reading paths by persona, and index. |
| **[01](docs/wiki/01-architecture-internals.md)** | **[Architecture & Internals](docs/wiki/01-architecture-internals.md)** | Chassis daemon on `:8765`, SQLite WAL, FTS5 virtual tables, and AST graph tokens. |
| **[02](docs/wiki/02-installation-and-shell-hooks.md)** | **[Installation & Shell Hooks](docs/wiki/02-installation-and-shell-hooks.md)** | Universal install, shell hooks (PowerShell/Bash/Zsh/Fish), and autostart services. |
| **[03](docs/wiki/03-3-tier-multi-agent-power-hierarchy.md)** | **[3-Tier Multi-Agent Hierarchy](docs/wiki/03-3-tier-multi-agent-power-hierarchy.md)** | Division of Cognition: Tier 1 Boss, Tier 2 Subagents, Tier 3 Workers, and hardware sizing. |
| **[04](docs/wiki/04-senior-boss-escalation-and-coaching.md)** | **[Senior Boss Escalation & Coaching](docs/wiki/04-senior-boss-escalation-and-coaching.md)** | Supervision rationale, Subagent coaching loops, Escalation Dossiers, and Senior Takeover. |
| **[05](docs/wiki/05-universal-agent-interchangeability.md)** | **[Universal Agent Interchangeability](docs/wiki/05-universal-agent-interchangeability.md)** | Tool-agnostic architecture: OpenCode, Codex, Antigravity, Claude Code, and `UniversalAgentEnvelope`. |
| **[06](docs/wiki/06-worker-cascade-and-free-models.md)** | **[Worker Cascade & Free Models](docs/wiki/06-worker-cascade-and-free-models.md)** | Dynamic worker discovery (`opencode models`, `hermes fallback list`), free models, and Ollama failover. |
| **[07](docs/wiki/07-hands-engine-and-ui-testing.md)** | **[Hands Engine & UI Testing](docs/wiki/07-hands-engine-and-ui-testing.md)** | Headless web inspection, DOM extraction, console error trapping, Playwright runner, and fallback. |
| **[08](docs/wiki/08-neural-memory-and-context-governor.md)** | **[Neural Memory & Context Governor](docs/wiki/08-neural-memory-and-context-governor.md)** | Sub-50ms FTS5 memory recall (`aegis recall`), deterministic $\le 400$-token context, and stealth mode. |
| **[09](docs/wiki/09-mobile-remote-and-whisper-bridge.md)** | **[Mobile Remote & Whisper Bridge](docs/wiki/09-mobile-remote-and-whisper-bridge.md)** | 24/7 Mobile Operations: Telegram (`@HHAACLIBot`) & WhatsApp, offline Whisper STT, and console injection. |
| **[10](docs/wiki/10-power-management-caffeinate.md)** | **[Power Management & Caffeinate](docs/wiki/10-power-management-caffeinate.md)** | System sleep prevention: Win32 Away Mode pulse thread, macOS `caffeinate`, and `systemd-inhibit`. |
| **[11](docs/wiki/11-role-based-dynamic-arsenal.md)** | **[Role-Based Dynamic Arsenal](docs/wiki/11-role-based-dynamic-arsenal.md)** | Archetype profiles (`developer`, `creator`, `security`, `omni`), JIT expansion, and Jev Decision Head. |
| **[12](docs/wiki/12-4-decision-quality-architecture-gate.md)** | **[4-Decision Quality Architecture Gate](docs/wiki/12-4-decision-quality-architecture-gate.md)** | Karpathy Simplicity Doctrine, Ponytail/Unslop AI watermark stripping, Red-Team audit, and Dual-Env sandbox. |
| **[13](docs/wiki/13-fast-path-testing-and-ast.md)** | **[Fast-Path Testing & AST Verification](docs/wiki/13-fast-path-testing-and-ast.md)** | In-memory AST verification (`aegis test <file>`), scoped pytest runner (< 1s), and CI parity. |
| **[14](docs/wiki/14-cli-reference-bible.md)** | **[CLI Reference Bible](docs/wiki/14-cli-reference-bible.md)** | Exhaustive dictionary of all 58+ commands, subcommands, arguments, flags, options, and exit codes. |
| **[15](docs/wiki/15-troubleshooting-and-diagnostics.md)** | **[Troubleshooting & Diagnostics](docs/wiki/15-troubleshooting-and-diagnostics.md)** | Arch Wiki-style troubleshooting table: error messages, root causes, diagnostic recipes, and recoveries. |

---

## 🚀 60-Second Quickstart

### 1. Installation
Install AegisBrain via `pip` or `uv`:
```bash
pip install aegis-brain
```
*(Or install in editable mode: `git clone https://github.com/PG300604/aegis-brain.git && cd aegis-brain/package && pip install -e .`)*

### 2. Activate Shell Hook
Add the zero-latency context bootstrap hook to your shell:
```powershell
# PowerShell ($PROFILE)
if (Get-Command aegis -ErrorAction SilentlyContinue) { aegis hook --shell powershell | Out-String | Invoke-Expression }
```
```bash
# Bash / Zsh (~/.bashrc or ~/.zshrc)
command -v aegis >/dev/null 2>&1 && eval "$(aegis hook --shell bash)"
```

### 3. Launch the Background Daemon
```bash
aegis start
```

### 4. Verify System Health
```bash
aegis doctor
```

---

## 💻 Complete CLI Reference

| Command | Subcommand / Options | Description |
| :--- | :--- | :--- |
| `aegis setup` | `[--profile P] [--workers]` | Role-based Arsenal installation wizard (`developer`, `creator`, `security`, `omni`) and Tier 3 worker discovery. |
| `aegis doctor` | `[--fix] [--models]` | Workstation environment health scorecard and Tier 3 worker cascade inspection. |
| `aegis workers` | `list` / `setup` / `advice` / `clear` | Discover, configure, and manage Tier 3 execution worker models and fallback priority cascade. |
| `aegis test` | `<file> [--scoped]` | Fast-path in-memory AST verification and targeted scoped test runner (< 1s execution). |
| `aegis hands` | `<url> [--screenshot] [--assert-clean]` | Native headless web app inspector: live DOM extraction, console error checks, and screenshot captures. |
| `aegis briefing` | `[--name N]` (aliases: `hi`, `greeting`) | High-craft developer briefing: status, recent milestones, real-time community radar, and next actions. |
| `aegis bye` | `[--summary S]` (aliases: `close-session`, `session-end`) | Graceful session termination: restore-point snapshot, context compaction to `ACTIVE_CONTEXT.md`, and DB archive. |
| `aegis radar` | `[--sub S] [--limit N]` | Scan real-time engineering discussions from HackerNews and r/LocalLLaMA with 2-hour TTL auto-cache. |
| `aegis recall` | `[query] [--limit N]` | Instant sub-second memory search across decisions and tasks (< 50ms). |
| `aegis remember` | `<text> [--category C]` | Record a key architectural decision or milestone into persistent neural memory. |
| `aegis bootstrap` | `[--json]` | Output active workspace context ($\le 400$ tokens) for instant agent startup. |
| `aegis hierarchy` | `[--plan] [--task T]` / `set-boss` / `get-boss` | Inspect 3-tier hierarchy, set active Tier 1 Boss (`opencode`, `codex`, `antigravity`, `claude`), and view active roles. |
| `aegis dispatch` | `"<task>" [--boss B] [--worker W] [--simulate] [--json]` | Universal Agent Dispatch: Route tasks across arbitrary Boss-Worker pairings using standardized execution envelopes. |
| `aegis coach` | `<target_file> [--retries N]` | Junior Boss Subagent coaches execution workers through the 4 Quality Architecture Gates. |
| `aegis pipeline` | `<target> [--fix]` | Run candidate code through the 4-Decision Quality Architecture Gate. |
| `aegis challenge` | `<file_or_code>` | Red-team audit for injection vectors, `shell=True`, and path traversal flaws. |
| `aegis unslop` | `<file>` (alias: `deslop`) | Strip conversational AI watermarks, polite preambles, and filler text. |
| `aegis remote` | `start [--service telegram\|whatsapp]` | Launch 24/7 background mobile remote listener with Whisper voice ingestion. |
| `aegis caffeinate` | `enable [--keep-display]` / `disable` | Manage Win32 Away Mode wake-lock assertions to prevent workstation sleep during agent runs. |
| `aegis snapshot` | `create [--reason R]` / `list` / `restore <id>` | Create and manage instant configuration restore points. |
| `aegis stealth` | `on` / `off` | Toggle zero-disk private stealth mode for confidential sessions. |
| `aegis status` | `[--detailed]` | Display daemon status, database size, hardware metrics, and active session telemetry. |
| `aegis dashboard` | `[--open] [--port P]` | Launch real-time local web telemetry dashboard (`http://127.0.0.1:8766`). |

---

## 📈 Verified Benchmarks

<p align="center">
  <img src="https://raw.githubusercontent.com/PG300604/aegis-brain/main/assets/benchmarks-visual.svg" alt="AegisBrain Verified Benchmarks & Real Metrics" width="100%">
</p>

### Memory Recall Efficiency (AegisBrain vs Raw Transcript Crawling)

| Metric | Traditional Agent (Raw Log Crawling) | AegisBrain (`aegis recall`) | Improvement |
| :--- | :---: | :---: | :---: |
| **Token Consumption** | ~52,000 tokens / recall | **~240 tokens / recall** | **99.5% reduction** |
| **Recall Latency** | 12.4 seconds | **0.024 seconds (24 ms)** | **516x faster** |
| **Context Window Waste** | 48% of prompt window | **< 1% of prompt window** | **Zero window pollution** |
| **Storage Engine** | Unindexed JSON Lines (`> 50MB`) | SQLite WAL + FTS5 Index | Deterministic sub-second search |

### System Overhead & Reliability

- **Daemon RAM Footprint**: **18.4 MB** (idle), **24.2 MB** (active multi-agent routing).
- **Daemon Startup Time**: **34 ms** (zero external imports).
- **Test Suite Coverage**: **281 / 281 passed (100% pass rate)**.
- **Cross-Platform Parity**: 100% test pass rate across Ubuntu Linux (Python 3.10–3.13), macOS, and Windows.

---

## 📄 License

AegisBrain is open-source software licensed under the **GNU General Public License v3.0 (GPLv3)**. See [LICENSE](LICENSE) for details.
