---
name: aegis
description: "Universal local neural memory bus, context governor, and cross-model skill proxy for Antigravity, Claude Code, Codex, Hermes, Cursor, and OpenCode."
tools: [claude-code, codex, gemini-cli, antigravity, hermes, cursor, opencode, aider]
category: memory
risk: safe
tags: [agent-memory, context-governor, ollama, local-ai, fts5, sqlite, prompt-caching, open-higgsfield]
---

# AegisBrain Universal Controller Skill

AegisBrain provides deterministic workspace memory, active context compiling ($\le 400$ tokens), and skill proxying for all major autonomous AI coding agents:
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
| `/aegis status` | Inspect system health | Daemon state, autostart runner, tracked PRs, recorded decisions |
| `/aegis bootstrap` | Compile workspace context | Generates `~/.aegis-brain/ACTIVE_CONTEXT.md` ($\le 400$ tokens) |
| `/aegis search <q>` | Query memory bus | Sub-millisecond SQLite FTS5 search across architectural records |
| `/aegis decision` | Record technical decision | Persists decision, rationale, and tags to SQLite WAL index |
| `/aegis mode private` | Ephemeral stealth mode | Zero-disk logging; completely bypasses disk writes |
| `/aegis mode public` | Persistent memory mode | Enables SQLite WAL storage and automatic full-text indexing |
| `/aegis poll` | Sweep GitHub pull requests | Checks CI checks, triage labels, and review comments |
| `/aegis media <p>` | OpenHiggsfield generation | Dispatches prompt to Flux/Seedance and logs output metadata |
| `/aegis autostart [on/off]`| Control system boot runner | Configures zero-elevation logon/wake background execution |
| `/aegis stop` | Stop background daemon | Gracefully closes HTTP server and releases WAL locks |

## Universal Agent Integration Rules

### 1. In Anthropic Claude Code
Place this skill file in `~/.claude/skills/aegis/SKILL.md` or `.claude/skills/aegis/SKILL.md` in your repository.
Claude Code automatically activates `/aegis` slash commands and executes `aegis` CLI commands natively.

### 2. In Google Antigravity
Registered at `~/.gemini/config/skills/aegis/SKILL.md`. Antigravity reads the active context on session launch and coordinates local Ollama models through the Aegis proxy (`127.0.0.1:8765/v1`).

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
Query past architectural decisions with `aegis search "<topic>"`.
```
