# AegisBrain Open-Source Marketing & Star Growth Playbook

> A tactical playbook to launch, distribute, and maximize GitHub stars for **AegisBrain** across developer communities, social platforms, and ecosystem repositories.

---

## 1. Core Narrative & Value Proposition

Developers star repositories when a tool solves an immediate, painful friction point with zero setup overhead:

| The Pain Point | The AegisBrain Solution | The Viral Hook |
|---|---|---|
| **Terminal Amnesia** | Context Governor compiles a deterministic $\le 400$-token snapshot on every session launch. | "Stop re-explaining your repo every time you open a terminal." |
| **Local Model Skill Gap** | Distills 500+ skills into semantic constraints via an OpenAI-compatible proxy (`:8765/v1`) for local Ollama models. | "Give small local models (Qwen, DeepSeek) the capabilities of frontier agents." |
| **Bloated Dependencies** | Zero external pip dependencies; pure Python 3 standard library (`sqlite3`, `http.server`, `urllib`). | "Boots in 45ms and uses < 25MB RAM. Pure stdlib." |
| **Client Privacy Concerns** | Native dual mode: `aegis mode private` guarantees zero bytes reach the disk. | "Work on private code without leaking prompt logs to disk." |

---

## 2. Platform-Specific Launch Blueprints

### A. Hacker News (`Show HN`)
- **Title**: `Show HN: AegisBrain – Zero-overhead local memory bus and context governor for AI coding agents`
- **Submission Timing**: Tuesday or Wednesday at 08:30 AM EST (13:30 UTC).
- **Body Draft**:
  ```text
  Hi HN,

  I built AegisBrain (https://github.com/PG300604/aegis-brain) because I was tired of "agent amnesia".

  Every time I opened a new CLI session in Claude Code, Antigravity, or Hermes, the agent had zero awareness of what we just implemented, what pull requests were awaiting triage, or what architectural decisions had already been made. Re-feeding context was burning thousands of tokens and wasting time.

  AegisBrain is a background daemon that solves this:
  1. Compiles an ultra-compact ACTIVE_CONTEXT.md (≤ 400 tokens) using active git state and SQLite WAL records.
  2. Sub-millisecond FTS5 search across all past architectural decisions.
  3. Acts as an OpenAI-compatible proxy (:8765/v1) in front of local Ollama models, injecting skill constraints into smaller models (Qwen, DeepSeek, Llama).
  4. Native private stealth mode (zero disk logging for confidential repos).
  5. Zero external dependencies: pure Python standard library (sqlite3, urllib, http.server). Boots in < 50ms and consumes < 25MB RAM.

  Works across Antigravity, Claude Code, OpenAI Codex, Cursor, Windsurf, Hermes, and Aider.

  Code: https://github.com/PG300604/aegis-brain
  License: GPLv3

  Feedback and critiques welcome!
  ```

---

### B. Reddit Launch (`r/LocalLLaMA` & `r/programming`)
- **Target Subreddits**:
  - `r/LocalLLaMA` (180k+ local AI enthusiasts)
  - `r/ClaudeAI` (120k+ Claude and Claude Code users)
  - `r/Python` (showcasing standard library engineering)
- **Title**: `I built a zero-dependency local memory bus and skill proxy for local coding agents (Ollama + Claude Code + Antigravity)`
- **Key Angle for r/LocalLLaMA**:
  - Focus on how AegisBrain proxies local Ollama models (`127.0.0.1:8765/v1` -> `11434/v1`) to inject Karpathy simplicity and architectural constraints, closing the skill gap between 7B/14B models and frontier models.

---

### C. Twitter / X Viral Launch Thread
- **Tweet 1 (Hook + Video/GIF)**:
  > Coding agents have a severe amnesia problem.  
  >
  > Every new terminal window you open in Claude Code, Codex, or Hermes burns thousands of tokens re-learning your workspace.  
  >
  > Today I'm releasing AegisBrain: A zero-dependency local memory bus & context governor.  
  >
  > 🧵 Here's how it works in 60 seconds: [Attach terminal video / GIF]
- **Tweet 2 (The Architecture)**:
  > AegisBrain runs a tiny background daemon (Python standard library only).  
  >
  > • Sub-millisecond SQLite WAL + FTS5 full-text engine  
  > • ≤ 400-token deterministic active workspace snapshot  
  > • < 25MB RAM footprint  
  > • < 50ms cold boot  
  >
  > [Attach assets/architecture-3d.svg]
- **Tweet 3 (Universal Compatibility)**:
  > Works out-of-the-box with:
  > ✦ Antigravity CLI  
  > ✦ Anthropic Claude Code  
  > ✦ OpenAI Codex  
  > ✦ Cursor & Windsurf  
  > ✦ Nous Research Hermes  
  > ✦ Local Ollama (Qwen, DeepSeek)  
- **Tweet 4 (Call to Action)**:
  > 100% open-source under GPLv3.  
  >
  > ⭐️ Star the repo on GitHub:  
  > https://github.com/PG300604/aegis-brain  
  >
  > Built by @PG300604

---

## 3. High-Value Ecosystem Inclusion (Pull Requests)

Submit PRs to high-traffic Awesome Lists to drive consistent passive star growth:

1. **`awesome-llm-agents`**: Submit under "Agent Memory & Orchestration".
2. **`awesome-local-ai`**: Submit under "Local Model Tooling & Proxies".
3. **`awesome-ollama`**: Submit under "Extensions, Plugins & Proxies".
4. **`awesome-claude`**: Submit under "Developer Tools & Skills".

---

## 4. Key Metrics & Star Milestone Goals

- **Milestone 1 (Launch Day)**: 50+ stars from r/LocalLLaMA and Twitter thread.
- **Milestone 2 (Week 1)**: 200+ stars via Show HN frontpage and Awesome-list merges.
- **Milestone 3 (Month 1)**: 500+ stars by writing a technical blog post detailing the SQLite WAL + FTS5 architecture.
