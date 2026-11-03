---
name: aegis
description: Manage AegisBrain local neural memory bus, logon autostart, public/private modes, architectural memory recall, and OpenHiggsfield media generation.
---

# AegisBrain Controller Skill

Use this skill whenever the user asks to manage, query, or reconfigure AegisBrain, or uses any `/aegis` slash command.

## Available Slash Commands

- `/aegis status`: Check background daemon state, autostart status, tracked PRs, and decisions.
- `/aegis autostart on`: Enable automatic background launch on Windows logon and system wake.
- `/aegis autostart off`: Disable startup automation and stop the background daemon.
- `/aegis mode public`: Enable SQLite WAL persistence and sub-millisecond FTS5 search.
- `/aegis mode private`: Activate zero-disk stealth mode (no sessions or memories touch disk).
- `/aegis search <query>`: Search architectural decisions and project knowledge instantly.
- `/aegis bootstrap [path]`: Generate an ultra-compact active context block for any workspace.
- `/aegis poll`: Sweep tracked GitHub pull requests (e.g. Spring AI PR #7308) for new comments/labels.
- `/aegis media <prompt>`: Dispatch image/video generation to OpenHiggsfield and log to memory bus.
- `/aegis stop`: Gracefully stop the background daemon.

## Operational Mapping

| User Intent | Execution Command |
|---|---|
| View Status | `aegis status` |
| Enable Autostart | `aegis autostart on` |
| Disable Autostart | `aegis autostart off` |
| Private Stealth Mode | `aegis mode private` |
| Public Memory Mode | `aegis mode public` |
| Recall Knowledge | `aegis search "<query>"` |
| Inspect Context | `aegis bootstrap` |
| Check GitHub PRs | `aegis poll` |
| Generate AI Media | `aegis media --prompt "<prompt>"` |
| Stop Daemon | `aegis stop` |
