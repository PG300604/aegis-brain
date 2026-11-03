# AegisBrain CLI Reference 📖

AegisBrain provides an intuitive, high-speed command line interface.

## Commands Overview

| Command | Arguments | Description |
|---|---|---|
| `aegis status` | None | Displays daemon running state, autostart status, mode, database location, and active PRs. |
| `aegis autostart` | `on` / `off` / `status` | Configures system startup automation (Windows User Startup, Linux systemd, macOS LaunchAgent). |
| `aegis start` | None | Launches the background daemon server detached from current terminal. |
| `aegis stop` | None | Gracefully shuts down the background daemon via remote `/shutdown` endpoint. |
| `aegis mode` | `public` / `private` | Toggles storage persistence mode. Private mode writes zero disk logs. |
| `aegis search` | `<query> [-n LIMIT]` | Sub-millisecond FTS5 search across all decisions and architectural memories. |
| `aegis bootstrap` | `[-w WORKSPACE]` | Compiles active context markdown for current or specified workspace. |
| `aegis decision` | `-t TITLE -d DESC [-c CAT] [-r RAT] [--tags TAGS]` | Records a new architectural or design decision. |
| `aegis poll` | None | Runs an immediate sweep against GitHub API for tracked PR status updates. |
| `aegis seed` | None | Seeds default memories and decisions into database. |
| `aegis daemon` | `[--host] [--port] [--interval]` | Starts daemon in foreground (for debugging or containerized runtimes). |

---

## Examples

### 1. Check System Health & Alerts
```bash
aegis status
```

### 2. Search Memories Instantly
```bash
aegis search "low cardinality"
```

### 3. Record an Architectural Decision
```bash
aegis decision \
  -c "BACKEND" \
  -t "Idempotent Webhook Processing" \
  -d "Store Stripe event IDs in Redis with a 24-hour TTL before processing" \
  -r "Prevents double-charging during network retry loops" \
  --tags "payments" "stripe" "redis"
```

### 4. Switch to Private Stealth Mode
```bash
aegis mode private
# When done with sensitive work:
aegis mode public
```
