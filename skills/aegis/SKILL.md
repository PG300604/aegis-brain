---
name: aegis
description: "Universal local neural memory bus, snapshot restore points, 4-stage quality gates pipeline, lightweight web browser, and live transparent agent orchestrator for Antigravity, Claude Code, Codex, Cursor, Windsurf, and OpenCode."
tools: [claude-code, codex, gemini-cli, antigravity, hermes, cursor, opencode, aider]
category: memory
risk: safe
tags: [agent-memory, snapshot-restore, quality-gates, gitguardian, unslop, lightweight-browser, fts5, sqlite, prompt-caching, open-higgsfield, instant-recall, caffeinate, remote-whatsapp]
---

# AegisBrain Universal Controller Skill

AegisBrain provides deterministic workspace memory, automated snapshot restore points, 4-stage post-processing quality gates, lightweight browser research, active context compiling ($\le 400$ tokens), wake-lock caffeinate, WhatsApp remote agent bridge, and skill proxying for all major autonomous AI coding agents:
- **Google Antigravity CLI**
- **Anthropic Claude Code**
- **OpenAI Codex CLI**
- **Nous Research Hermes Agent**
- **Cursor / Windsurf / Continue / Cline**
- **OpenCode CLI & Aider**

## Slash Commands & CLI Reference

Whenever invoked via `/aegis` or asked to operate in an AegisBrain-managed workspace:

| Command | Action | Output / Behavior |
|---|---|---|
| `/aegis recall [q]` | **Instant memory recall** | Sub-second recall of recent tasks, workflows, or FTS5 keyword match |
| `/aegis search <q>` | Query memory bus | Sub-millisecond SQLite FTS5 search across architectural records |
| `/aegis briefing` (or `hi`) | **Greeting & Offline Sync** | Greet user, check tracked PR reviews/alerts, and steer next actions |
| `/aegis optimize <task>` | **Proactive Arsenal Skills** | Recommend and activate highest-scoring Arsenal skills and web search vectors |
| `/aegis snapshot [create/list]` | **Restore Point Safety** | Captures snapshot of agent configs, prompts, and rules before mutations |
| `/aegis restore [id]` | **Rollback System** | Reverts agent configs, prompts, and rules back to previous restore point |
| `/aegis browse <url>` | **Lightweight Browser** | Distills web pages into token-efficient, ad-free Markdown (< 1,500 tokens) |
| `/aegis research <q>` | **Deep Research & Scout** | Explores web + scrapes matching Arsenal skills for domain gaps |
| `/aegis align <task>` | **Concept Education & Grill-Me**| Archify architectural blueprints, curated video links & Matt Pocock interview |
| `/aegis pipeline <target>` | **4-Stage Quality Gates** | Unslop/TurnItOut -> Security Audit -> GitGuardian Secrets -> Sandbox Test |
| `/aegis dashboard [--open/--tui]` | **Web GUI & Benchmarks** | Dark-mode Web GUI on `http://127.0.0.1:8765/dashboard` or ANSI terminal TUI |
| `/aegis feedback <comment>` | **Continuous Evolution** | Persists user critique, ratings, and suggestions to drive future model evolution |
| `/aegis ceo <idea>` | **YC CEO Stress-Test** | Evaluates hair-on-fire pain, inflection, moat, fatal failure modes & 24h MVP |
| `/aegis challenge <target>` | **Anti-Sycophancy Audit** | Devil's advocate audit: flags false passes, NTFS path bugs, unverified claims |
| `/aegis mistakes [recall/list]`| **Mistake Ledger & Traps** | Pre-flight error recall preventing repeat mistakes across workspaces |
| `/aegis caffeinate [on/off]` | Anti-sleep wake-lock | Prevents PC sleep during long agent workflows (`--display` optional) |
| `/aegis remote start` | WhatsApp remote session | Activates Caffeinate, ensures daemon runs, and pings WhatsApp/Telegram |
| `/aegis bootstrap` | Compile workspace context | Generates `~/.aegis-brain/ACTIVE_CONTEXT.md` ($\le 400$ tokens) |
| `/aegis status` | Inspect system health | Daemon state, autostart runner, Caffeinate state, tracked PRs, recorded decisions |
| `/aegis decision` | Record technical decision | Persists decision, rationale, and tags to SQLite WAL index |
| `/aegis mode [public/private]`| Ephemeral stealth mode | `private` = zero-disk logging; `public` = persistent WAL storage |
| `/aegis graph --query <q>` | AST Code Graph | Locates symbols, callers, and dependencies via AST without file dumping |

---

## Autonomous Agent Operational Directives

### 1. Mandatory Restore Point Safety
- Before mutating major system configurations, rules, or system files, verify or create a restore point: `aegis snapshot create --reason "pre-change"`.
- If an agent configuration or prompt modification creates unwanted side-effects, rollback cleanly with: `aegis restore [snapshot_id]`.

### 2. Autonomous Ingestion & Lightweight Browser
- Assess required domain skills. If missing, query `aegis research "<query>"` to locate or scrape required skills.
- Use `aegis browse "<url>"` for dense, token-efficient extraction from GitHub, Stack Overflow, Reddit, and documentation without rendering bloat.

### 3. Interactive Alignment & Concept Education
- If the task is underspecified or exploring unfamiliar technologies, run `aegis align "<task>"`.
- Review the generated Archify architectural blueprint and educational video links.
- Answer Matt Pocock's 3-question diagnostic interview to lock deliverables, constraints, and error boundaries before writing code.

### 4. Manager-Worker Triage & Live Transparent Observer
- High-severity / confidential tasks are executed directly by the frontier Manager.
- Routine / boilerplate tasks can be drafted by local Workers, with strict Manager review.
- Companion Observer emits step-by-step progress micro-updates (`[Aegis Observer] 🔍 Step 1/5...`) so the user can steer or comment early.

### 5. Multi-Choice Aesthetic & Layout Dials
- For frontend/UI tasks, present the user with interactive layout & style options (UI-UX Pro Max, Impeccable, Taste, Modern, Cyberpunk, Neo-brutalism, Minimalist) before scaffolding components.

### 6. Mandatory 4-Stage Post-Processing Quality Gates
Every generated output must pass:
1. `turnitout` / `unslop` / `deslop`: Remove conversational watermarks ("Certainly!", "Here is the code:"), filler disclaimers, and redundant comments.
2. `Red-Team & Cloudflare security audit`: Block `shell=True`, unsanitized `eval`, path traversals, and destructive disk commands.
3. `GitGuardian Secret Scanner`: Scan for API keys, tokens, and credentials. **Never allow secrets into Git commits.**
4. `Dual-Environment Verification`: Execute in ephemeral sandbox first -> verify on local workstation second -> push to Git third.

### 7. AST Graph Token Optimization
- Use `aegis graph --query <symbol>` for sub-millisecond symbol and dependency retrieval.
- Fall back to conventional full-file reads only if AST indexing fails.

### 8. Zero-Prompt Autonomous Invocation Protocol
The user simply chats naturally. All AI CLI agents (Antigravity, Claude Code, Cursor, OpenCode, Hermes) MUST autonomously execute AegisBrain tools behind the scenes without waiting for explicit commands:
- **Session Start / Greeting**: On "hi", "hello", or new sessions, immediately run `aegis briefing` to sync offline PR reviews and active alerts.
- **Ideation & Concept Proposals**: Proactively run `aegis ceo "<idea>"` to evaluate PMF, inflection points, and failure modes.
- **Code & Test Review**: Proactively run `aegis challenge "<target>"` to eliminate false positives and check `aegis mistakes recall`.
- **Domain Auto-Optimization**: Run `aegis optimize "<task>"` to dynamically activate the best Arsenal skills and targeted web documentation vectors.
- **Safety Restore Point**: Run `aegis snapshot create --reason "pre-change"` before any major refactor or config change.
- **Quality Gates**: Pipe all candidate code through `aegis pipeline "<file>"` before presenting to the user.

### 9. Subagent & Local Model Token Arbitrage
- To prevent main conversation context bloat and save tokens, aggressively delegate parallel tasks (independent research, deep test execution, large document scans) to subagents (`invoke_subagent`).
- Delegate routine boilerplate to local models (Nous Hermes CLI, local Ollama) via `call_local_worker` while the Frontier Manager handles critical architectural reviews and security gating.
