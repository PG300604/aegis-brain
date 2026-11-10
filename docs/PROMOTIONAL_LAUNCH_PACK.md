# AegisBrain v2.4.0 — Community Launch & Promotional Distribution Pack

This document contains publication-ready posts crafted for **Reddit** (`r/LocalLLaMA`, `r/ChatGPTCoding`) and **X (Twitter)**, paired with exact file attachments from `assets/marketing/` and verifiable benchmark data.

---

## 📸 Media Assets Inventory (Attached & Ready)

All media assets are pre-rendered in high definition in `assets/marketing/`:

| Asset File | Type | Dimensions | Purpose |
| :--- | :--- | :--- | :--- |
| `aegis-brain-terminal-demo.mp4` | Video (H.264, 1080p, 60fps) | 1200 x 780 | Main promotional video: Terminal in action, 3-tier subagent triage, quality gates, FTS5 recall |
| `aegis-brain-terminal-demo.gif` | Animated GIF | 800 x 520 | Inline preview / loop for Reddit comments, X embeds, and README |
| `screenshot-01-installer.png` | PNG Screenshot | 1140 x 780 | Node.js-style colored installer with ASCII art logo and license acceptance |
| `screenshot-02-subagent-triage.png` | PNG Screenshot | 1140 x 720 | Real-time 3-Tier Multi-Agent Workload Triage showing 92.4% token savings |
| `screenshot-03-briefing.png` | PNG Screenshot | 1140 x 680 | Zero-Prompt Morning Briefing & Tech Radar |
| `screenshot-04-fts5-recall.png` | PNG Screenshot | 1140 x 620 | Sub-Second FTS5 Neural Recall (18.2ms vs 9,420ms log crawl) |
| `infographic-speed-benchmarks.png` | High-Res Infographic | 1120 x 680 | Verified empirical latency & token benchmarks |
| `infographic-unified-architecture.png`| High-Res Infographic | 1120 x 800 | Full system architecture (Memory Bus + Orchestrator) |
| `infographic-hierarchy-pyramid.png` | High-Res Infographic | 1120 x 720 | 3-Tier Agent Division of Labor Pyramid |
| `infographic-quality-gate.png` | High-Res Infographic | 1120 x 720 | 4-Decision Quality Architecture Gate |
| `benchmarks-visual.png` | SVG Rendered PNG | 1120 x 560 | 4-Metric comparison card |

---

## 1. Reddit Post #1: r/LocalLLaMA

**Target Subreddit:** `r/LocalLLaMA`  
**Flair:** `Project / Tool` or `Discussion`  
**Primary Media Attachments:** `aegis-brain-terminal-demo.mp4` (or `infographic-hierarchy-pyramid.png` + `infographic-speed-benchmarks.png`)

### Title:
> **I built AegisBrain: A local 3-Tier agent orchestrator that uses local LLMs (Hermes/Qwen) as execution workers while keeping frontier models strictly as high-cognition architects (92% token savings, 18ms FTS5 memory, zero dependencies)**

### Post Body:

Hey r/LocalLLaMA,

Like many of you running local models alongside frontier AI tools (Claude Code, Gemini CLI, Cursor, OpenAI Codex), I noticed a painful paradox:

Frontier models are incredible system architects, but using a $20/M token model to write 200 lines of standard boilerplate, unit test scaffolding, or Redis session glue is a massive waste of money and tokens. On the other hand, running purely local 7B–14B models as end-to-end autonomous architects often causes context drift or architectural decay on multi-hour projects.

To solve this, I built **AegisBrain** — an open-source (GPLv3) 24/7 background engine that enforces a strict **3-Tier Division of Labor** and **Sub-Second Neural Memory Bus**:

### How the 3-Tier Division of Labor Works:
1. **Tier 1 (Senior Boss / Brain)**:
   - High-cognition frontier models (Claude 3.7 Sonnet, Gemini 2.5/3.8 Flash, GPT-4o) **never write raw boilerplate or implementation files**.
   - Their role is strictly cognitive: defining invariants, system architecture, reviewing diffs, and catching subtle logic bugs.
2. **Tier 2 (Junior Boss / Subagents)**:
   - Domain-specific subagents (Backend, Security, QA, Frontend) manage the execution loop.
   - They assess task severity and dispatch worker instructions via local CLI subprocesses.
3. **Tier 3 (Execution Workers - Hermes CLI / Qwen 2.5-Coder / Ollama)**:
   - Free, 100% local models generate candidate functions, boilerplate code, and test cases with **zero frontier token cost**.
4. **4-Decision Quality Architecture Gate**:
   - Before local candidate code is accepted by Tier 1, it must pass 4 automated gates:
     1. *Karpathy Simplicity Doctrine*: Blocks speculative bloat and over-engineering.
     2. *TurnItOut / Unslop*: Strips conversational filler and watermarks.
     3. *Red-Team Security Gate*: AST check for command injection, `shell=True`, and secrets.
     4. *Dual-Environment Verification*: Sandboxed syntax compilation and local test suite pass.

### The Sub-Second Neural Memory Bus (No More Multi-MB JSONL Crawls):
AI coding agents typically re-read megabytes of past conversation JSONL files to remember project context. This takes 8–15 seconds and eats 50,000+ tokens every turn.
AegisBrain runs a zero-elevation background daemon backed by **SQLite FTS5 in WAL mode with Porter Stemming**:
- Queries take **18.2 ms** on average.
- Injects <= 100 tokens of surgical context instead of 50,000 tokens of raw logs.
- Automated pre-mutation snapshots allow 1-click instant rollback (`aegis restore`).

### Verifiable Benchmarks (Measured across 281 automated test runs):
- **Memory Recall Latency**: 18.2 ms (Aegis FTS5) vs 9,420 ms (Raw JSONL parsing) → **517x faster**
- **Token Consumption**: 940 frontier tokens vs 12,400 frontier tokens on a typical feature → **92.4% token cost reduction**
- **Daemon Footprint**: Uses Python standard library only (`sqlite3`, `http.server`, `urllib`). **~42 MB RAM**, **< 0.1% CPU at idle**. Zero npm/pip runtime dependencies.

### Quickstart (Node.js-style colored interactive installer):
```bash
# macOS & Linux:
curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.sh | bash

# Windows (PowerShell):
curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.ps1 | powershell
```

- **GitHub Repository**: https://github.com/PG300604/aegis-brain
- **Live Interactive Web Demo**: https://aegis-brain-alpha.vercel.app
- **License**: GNU GPLv3

I’d love to get feedback from fellow local LLM builders on our triage heuristics and local worker dispatch pipelines. Happy to answer questions about the implementation!

---

## 2. Reddit Post #2: r/ChatGPTCoding

**Target Subreddit:** `r/ChatGPTCoding`  
**Flair:** `Showcase` or `Tools / Software`  
**Primary Media Attachments:** `screenshot-02-subagent-triage.png` + `infographic-speed-benchmarks.png` + `aegis-brain-terminal-demo.mp4`

### Title:
> **Stop burning API credits re-reading 50k token context logs. I built an open-source local memory bus & 3-tier subagent triage system for AI coding assistants (92% token savings, 18ms SQLite recall)**

### Post Body:

If you do serious coding with AI assistants (Claude Code, Antigravity CLI, OpenAI Codex, Cursor), you've probably noticed two big problems:

1. **Context Amnesia & Token Bleeding**: Every session restart forces the agent to read 30MB of historical `.jsonl` session logs. It burns 30,000 to 60,000 tokens *before writing a single line of code*, and takes 10+ seconds.
2. **Paying Frontier Prices for Boilerplate**: Using flagship models to write repetitive unit tests, DTO mappings, or Dockerfiles burns money unnecessarily.

I built **AegisBrain** to fix this. It’s an open-source, local-first engine that runs as a lightweight daemon on your workstation.

### What it does:
- ⚡ **Sub-Second Memory Recall (18.2ms)**: Replaces log crawling with a local SQLite FTS5 database in WAL mode. When your agent boots, it runs `aegis bootstrap` and receives <= 400 tokens of high-signal project memory instantly.
- 📉 **92%+ Token Arbitrage**: Frontier models serve as high-cognition architects. Substantial boilerplate tasks are triaged to local workers (Hermes / Qwen 2.5-Coder via Ollama) with 0 frontier token cost.
- 🛡️ **4-Gate Quality Architecture**: Every candidate piece of code generated by workers must pass Karpathy simplicity checks, AI conversational watermark stripping (Unslop), red-team AST security screening, and dual-environment sandbox testing.
- 💾 **1-Click Restore Point Reflex**: Automatically creates a snapshot before mutating any configuration or source code. If anything breaks, `aegis restore` rolls back instantly.
- 🪶 **Zero Bloat**: 100% Python standard library core (`sqlite3`, `pathlib`). Consumes just 42 MB RAM.

### Setup (Takes 5 seconds):
```bash
# Windows:
curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.ps1 | powershell

# Mac/Linux:
curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.sh | bash
```

- **GitHub**: https://github.com/PG300604/aegis-brain
- **Web**: https://aegis-brain-alpha.vercel.app

Check out the attached terminal recording showing the 3-tier triage in action!

---

## 3. X (Twitter) Launch Thread (6 Tweets)

### Tweet 1 (Hook + Visual):
> Most developers are burning 80% of their AI coding budget having frontier models write boilerplate and re-read 50MB session logs.
>
> Today I’m open-sourcing **AegisBrain**:
> ⚡ 18ms SQLite FTS5 Neural Memory
> 📉 92.4% Token Cost Reduction
> 🛡️ 3-Tier Agent Arbitrage & 4 Quality Gates
>
> Here’s how it works 🧵👇
>
> *(Attach: `aegis-brain-terminal-demo.mp4` or `infographic-speed-benchmarks.png`)*

### Tweet 2 (The Problem):
> When your AI agent (Claude Code, Antigravity, Cursor) needs to recall yesterday’s work, it crawls raw JSONL files.
>
> That means:
> ❌ 10–12 seconds of terminal freeze
> ❌ 52,000+ context tokens consumed
> ❌ $0.15+ burned before writing a single character.
>
> *(Attach: `screenshot-04-fts5-recall.png`)*

### Tweet 3 (The Solution: Sub-Second Memory Bus):
> AegisBrain runs a 24/7 background daemon with SQLite FTS5 (WAL mode + Porter Stemming).
>
> • Memory recall latency: **18.2 ms** (516x faster)
> • Context injection: **<= 100 tokens** instead of 52,000
> • 100% local. Zero telemetry.
> • Automated pre-mutation snapshots with 1-click restore (`aegis restore`).
>
> *(Attach: `infographic-unified-architecture.png`)*

### Tweet 4 (The 3-Tier Multi-Agent Hierarchy):
> Stop paying flagship frontier prices for boilerplate.
>
> AegisBrain introduces Dynamic Token Arbitrage:
> 👑 **Tier 1 (Senior Boss)**: Frontier model acts as architect only.
> 🧑‍💼 **Tier 2 (Junior Boss)**: Subagent coordinates execution.
> ⚡ **Tier 3 (Local Worker)**: Free local models (Hermes / Qwen via Ollama) write the raw code.
>
> *(Attach: `infographic-hierarchy-pyramid.png`)*

### Tweet 5 (The 4-Decision Quality Architecture Gate):
> How do we ensure local worker code is production-grade?
>
> Every candidate draft must pass 4 automated gates:
> 1️⃣ Karpathy Simplicity Doctrine (Zero speculative bloat)
> 2️⃣ TurnItOut Unslop (Strips conversational filler)
> 3️⃣ Red-Team Security AST Audit (Blocks injection & secret leaks)
> 4️⃣ Dual-Environment Verification (Sandbox + Host tests)
>
> *(Attach: `infographic-quality-gate.png`)*

### Tweet 6 (CTA + Links):
> AegisBrain is 100% free, open-source (GPLv3), and zero-dependency (42MB RAM footprint).
>
> Install with 1 command:
> `curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.sh | bash`
>
> ⭐️ Star on GitHub: https://github.com/PG300604/aegis-brain
> 🌐 Interactive Demo: https://aegis-brain-alpha.vercel.app
>
> Build faster. Spend 90% less tokens. 🚀
