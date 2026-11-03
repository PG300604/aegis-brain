# AegisBrain Mobile Remote Control & Command Reference

AegisBrain includes a zero-dependency remote management bridge that allows developers to supervise local AI coding agents, execute terminal commands, view generated artifacts, and prevent machine sleep via **Telegram** or **WhatsApp** from anywhere.

---

## 1. Quick Onboarding (60 Seconds)

AegisBrain connects to Telegram via an outbound **HTTPS long-polling daemon**. This requires:
* **Zero inbound open ports**
* **Zero public IP / DDNS**
* **Zero webhook infrastructure or tunnels (no ngrok / Cloudflare needed)**
* **Works seamlessly behind NAT and home Wi-Fi**

### Step-by-Step Setup

1. **Create your Bot on Telegram**:
   * Open Telegram and search for `@BotFather`.
   * Send `/newbot`.
   * Follow the prompt to provide a bot display name and username ending in `bot` (e.g., `MyAegisBrainBot`).
   * BotFather will output your **HTTP API Token** (e.g., `1234567890:FakeBotToken`).

2. **Configure AegisBrain**:
   Run the interactive setup wizard in your terminal:
   ```bash
   aegis remote setup
   ```
   Select `1` (Telegram), paste your Bot Token, and confirm your 4-digit Pairing PIN (default: `8765`).

3. **Start the AegisBrain Daemon**:
   ```bash
   aegis remote start
   # or run the full daemon:
   aegis start
   ```

4. **Pair from your Phone**:
   * Open your newly created bot on your phone in Telegram.
   * Send:
     ```text
     /auth 8765
     ```
   * AegisBrain will authenticate your phone, whitelist your unique Chat ID, activate the **Caffeinate** sleep-prevention lock, and grant interactive shell access.

---

## 2. Interactive Shell vs. Silent Idle Mode

A common question is whether the bot continuously prints every background terminal log to your phone. 

AegisBrain uses an **Explicit On-Demand Architecture**:

| State | Behavior |
| :--- | :--- |
| **Idle State (Default)** | The bot remains **100% quiet and idle**. It consumes zero CPU cycles and will **never** spam your chat with unprompted logs or terminal dumps. |
| **Command Execution** | When you send a command (e.g., `git status`, `dir`, `pytest`, `cargo build`), AegisBrain runs it inside your active workspace directory and streams the real-time stdout/stderr response directly to your phone. |
| **Artifact Inspection** | If your AI coding agent (Antigravity, Claude Code, Cursor, Aider) generates new plans, architectural blueprints, or markdown diffs, send `/artifacts` to inspect recent files, timestamps, and disk locations. |
| **Autonomous Watchdog** | If you enable PR tracking via `aegis track <PR_URL>`, the background watchdog monitors CI check runs and review approvals. Only critical status shifts trigger an autonomous mobile alert. |

---

## 3. Remote Command Catalog

Send any of the following commands directly to your Telegram bot:

### System & Power Management

| Command | Description | Example Response |
| :--- | :--- | :--- |
| `/status` | Displays workstation health, RAM, git branch, and caffeinate state | `💻 AegisBrain Workstation: Online (Caffeinate: Active, Branch: main)` |
| `/caffeinate on` | Activates OS-level wake lock (Win32 AwayMode pulse thread) | `☕ Caffeinate ON: System sleep and screen timeout suspended.` |
| `/caffeinate off` | Releases wake lock, allowing normal OS power management | `💤 Caffeinate OFF: Normal system sleep restored.` |
| `/sleep` | Disengages caffeinate and puts the PC into system sleep | `💤 Putting PC into sleep mode now. Goodbye!` |
| `/shutdown` | Gracefully terminates open sessions and shuts down the PC | `🛑 Initiating system shutdown in 5 seconds.` |
| `/help` or `/start` | Displays interactive command menu and usage guide | Lists all available commands with usage tips. |

### AI Agents & Workspace Supervision

| Command | Description | Example Usage |
| :--- | :--- | :--- |
| `/artifacts` | Scans session directory and returns the 4 newest generated reports | `/artifacts` |
| `/recall <query>` | Performs sub-50ms SQLite FTS5 neural memory retrieval | `/recall rate limiting bug fix` |
| `/git status` | Inspects working tree, staged files, and untracked changes | `/git status` |
| `/git diff` | Shows unstaged git diff lines directly in chat | `/git diff` |
| `/git commit -m "..."` | Stages and commits local changes with verified message | `/git commit -m "fix: rate limit leak"` |
| `/git push` | Pushes current branch commits to origin remote | `/git push` |
| `<any CLI command>` | Executes arbitrary terminal command in the workspace directory | `dir`, `git log -n 3`, `pytest`, `npm test` |

---

## 4. Workstation CLI Commands

You can also control the remote subsystem directly from your PC terminal using the `aegis` CLI:

```bash
# Setup remote bridge (Telegram or WhatsApp)
aegis remote setup

# View remote bridge status, token, and pairing state
aegis remote status

# Test outbound mobile message dispatch
aegis remote test

# Start the background remote listener and daemon
aegis remote start

# Manage Caffeinate independently
aegis caffeinate on
aegis caffeinate off
aegis caffeinate status
```

---

## 5. Security & Isolation Model

* **Pairing PIN**: First-time connections must pass `/auth <PIN>`. Unauthenticated messages are rejected immediately.
* **ID Whitelisting**: Upon successful authentication, your unique Telegram Chat ID or phone number is persisted to `~/.aegis-brain/remote.json`. Messages from any other account are ignored.
* **Execution Timeout**: All remote shell executions have a hard 60-second execution cap to prevent runaway commands from hanging the machine.
* **Buffer Truncation**: Output buffers exceeding 1,300 characters are safely truncated to comply with mobile messaging limits while preserving the head and exit code.
