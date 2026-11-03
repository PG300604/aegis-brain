---
name: aegis
description: "Universal local neural memory bus, instant memory recall, and context governor for Antigravity, Claude Code, Codex, Cursor, Windsurf, and OpenCode."
tools: [claude-code, codex, gemini-cli, antigravity, hermes, cursor, opencode, aider]
category: memory
risk: safe
tags: [agent-memory, context-governor, ollama, local-ai, fts5, sqlite, prompt-caching, open-higgsfield, instant-recall]
---

# AegisBrain Universal Controller Skill

AegisBrain provides deterministic workspace memory, sub-second instant recall, active context compiling ($\le 400$ tokens), and skill proxying for all major autonomous AI coding agents:
- **Google Antigravity CLI**
- **Anthropic Claude Code**
- **OpenAI Codex CLI**
- **Nous Research Hermes Agent**
- **Cursor / Windsurf / Continue / Cline**
- **OpenCode CLI & Aider**

## Slash Commands

Whenever invoked via `/aegis` or asked to recall project decisions:

| Command | Action | Output / Behavior |
|---|---|---|
| `/aegis recall [q]` | **Instant memory recall** | Sub-second recall of recent tasks, workflows, or FTS5 keyword match |
| `/aegis search <q>` | Query memory bus | Sub-millisecond SQLite FTS5 search across architectural records |
| `/aegis bootstrap` | Compile workspace context | Generates `~/.aegis-brain/ACTIVE_CONTEXT.md` ($\le 400$ tokens) |
| `/aegis status` | Inspect system health | Daemon state, autostart runner, tracked PRs, recorded decisions |
| `/aegis decision` | Record technical decision | Persists decision, rationale, and tags to SQLite WAL index |
| `/aegis mode private` | Ephemeral stealth mode | Zero-disk logging; completely bypasses disk writes |
| `/aegis mode public` | Persistent memory mode | Enables SQLite WAL storage and automatic full-text indexing |
| `/aegis poll` | Sweep GitHub pull requests | Checks CI checks, triage labels, and review comments |
| `/aegis media <p>` | OpenHiggsfield generation | Dispatches prompt to Flux/Seedance and logs output metadata |
| `/aegis autostart [on/off]`| Control system boot runner | Configures zero-elevation logon/wake background execution |
| `/aegis stop` | Stop background daemon | Gracefully closes HTTP server and releases WAL locks |

---

## Autonomous Instant Recall Protocol (Zero-Token-Waste Heuristic)

Whenever a user asks any question involving:
- *"What was the last task we done / did?"*
- *"Recall past decisions / conventions / architecture"*
- *"What did we do previously on [topic]?"*
- *"Check current project context / status"*

### 1. Mandatory Reflex (Zero-Token-Waste)
- **DO NOT** crawl through multi-megabyte `transcript.jsonl` files, history directories, or raw shell output.
- **DO NOT** make multiple exploratory filesystem searches.
- **IMMEDIATELY** run:
  ```bash
  # For latest tasks & decisions:
  aegis recall -n 5

  # For specific keyword or topic lookups:
  aegis recall "<topic>"
  ```
- Retrieval takes **<50ms** via SQLite FTS5 in WAL mode and returns structured records in **<100 tokens** (95%+ token savings).

### 2. Context Bootstrapping
Before beginning large multi-step architectural changes or when launching a new session, run:
```bash
aegis bootstrap
```
This loads active conventions, tracked PRs, and recent architectural rules in $\le 400$ tokens.

---

## Universal Agent Integration Rules

### 1. In Google Antigravity
Registered at `~/.gemini/config/skills/aegis/SKILL.md`. Antigravity's global operating directives (`GEMINI.md`) designate `aegis recall` as the primary reflex for memory lookup, completely eliminating session log crawling.

### 2. In Anthropic Claude Code
Place this skill file in `~/.claude/skills/aegis/SKILL.md` or `.claude/skills/aegis/SKILL.md` in your repository.
Claude Code automatically activates `/aegis` commands and invokes `aegis recall` during memory queries.

### 3. In OpenAI Codex CLI & Aider
Codex and Aider consume `~/.aegis-brain/ACTIVE_CONTEXT.md` on startup. Configure `.aider.conf.yml` or Codex prompt hooks:
```yaml
# In .aider.conf.yml
read: ~/.aegis-brain/ACTIVE_CONTEXT.md
```

### 4. In Cursor / Windsurf / VS Code
Add to your project's `.cursorrules` or `.windsurfrules`:
```markdown
Always inspect ~/.aegis-brain/ACTIVE_CONTEXT.md before proposing architectural changes.
Instantly recall past decisions with `aegis recall "<topic>"`.
```
