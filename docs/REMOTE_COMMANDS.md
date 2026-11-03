# AegisBrain Mobile Remote Control & Security Reference

AegisBrain includes a zero-dependency remote management bridge that allows developers to supervise local AI coding agents, execute terminal commands, type ideas via voice dictation into the active IDE chat, view generated artifacts, and physically lock the workstation against tampering via **Telegram** or **WhatsApp** from anywhere.

---

## 1. Quick Onboarding (60 Seconds)

AegisBrain connects to Telegram via an outbound **HTTPS long-polling daemon**. This requires:
* **Zero inbound open ports**
* **Zero public IP or dynamic DNS**
* **Zero webhook infrastructure or tunnels (no ngrok or Cloudflare needed)**
* **Works seamlessly behind firewalls, NAT, and mobile hotspots**

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
   * AegisBrain will authenticate your phone, whitelist your unique Chat ID, activate the **Caffeinate** sleep-prevention lock, and grant interactive access.

### Do You Have to Reconnect Every Session or After Reboots?

**No.** Pairing is strictly a one-time step.

* **Persistent Identity**: Once you send `/auth <PIN>`, AegisBrain writes your unique Telegram Chat ID to `~/.aegis-brain/remote.json`. It remembers your phone permanently across all future sessions.
* **Auto-Start Across Reboots**: Run `aegis autostart on` once on your machine. On Windows, this places a silent VBS launcher into your user Startup folder (`aegis-brain-startup.vbs`); on Linux, it registers a user systemd service.
* **Zero Maintenance**: Whenever your machine powers on or wakes up, the background daemon starts automatically and resumes polling. You can pick up your phone at any time and send commands immediately without touching your PC.

---

## 2. Interactive Voice Mode & IDE Chat Typing

When away from your desk, you can prompt your AI agents (Antigravity, Cursor, VS Code, Windsurf) by typing or speaking from your phone:

### How Phone Voice Mode Works
1. Open your Telegram bot on your phone.
2. Tap the **Microphone** icon on your smartphone keyboard (Gboard on Android, Apple Dictation on iOS) to dictate your idea or prompt hands-free.
3. Send it as:
   ```text
   /type Refactor the authentication service to use JWT RS256 with key rotation
   ```
   or switch to auto-typing mode:
   ```text
   /mode chat
   ```
4. AegisBrain instantly places your prompt onto the workstation clipboard and injects `Ctrl+V` followed by `Enter` into the desktop window. The AI agent immediately receives your thought and begins coding!

### Chat Commands

| Command | Action | Behavior |
| :--- | :--- | :--- |
| `/type <prompt>` | Direct Chat Injection | Copies prompt to system clipboard and simulates `Ctrl+V` + `Enter` in the active desktop window |
| `/prompt <prompt>` | Voice Mode Alias | Exact alias for `/type`, designed for mobile speech-to-text workflows |
| `/paste <text>` | Paste Without Submit | Copies text and pastes (`Ctrl+V`) into desktop without pressing Enter |
| `/clip [text]` | Clipboard Sync | Sets workstation clipboard if text provided, or replies with current PC clipboard contents |
| `/mode <chat\|exec>` | Mode Switch | `chat`: all unprefixed messages/dictations type into desktop chat; `exec`: run as shell commands |

---

## 3. Physical Device Security & Anti-Tamper Lockdown

When leaving your workstation unattended in a shared office, coffee shop, or home desk, AegisBrain protects your physical hardware:

### Security Matrix

| Threat | Command | Action Taken |
| :--- | :--- | :--- |
| **Passersby watching or touching screen** | `/lock` | Instantly switches Windows to the Lock Screen (`user32.LockWorkStation`). Passersby see only the Windows login screen. Background AI agents, compilation tasks, Caffeinate AwayMode, and Telegram bot remain **100% active at full speed**. |
| **Physical keyboard or mouse tampering** | `/blockinput on` | Disables physical keyboard and mouse hardware input (`user32.BlockInput`). Send `/blockinput off` to restore hardware controls. |
| **Suspicious activity detected near desk** | `/alarm` | Plays urgent audible warning tones on the workstation speakers to alert and deter intruders. |
| **Emergency remote standby** | `/sleep` | Disengages Caffeinate and puts the PC into system standby mode. |
| **Emergency remote power off** | `/shutdown` | Safely closes sessions and initiates PC shutdown with a 15-second abort countdown (`shutdown /a` on PC to cancel). |

---

## 4. Complete Remote Command Catalog

Send any of the following commands directly to your Telegram bot:

### Input & Voice Bridge
* `/type <text>` - Type text into active IDE chat & submit (`Ctrl+V` + `Enter`)
* `/prompt <text>` - Voice mode alias for `/type`
* `/paste <text>` - Paste text without pressing Enter
* `/clip [text]` - Read or set workstation clipboard contents
* `/mode <chat|exec>` - Switch default behavior for plain text

### Workstation Physical Security
* `/lock` - Instantly lock screen (AI agents keep running in background)
* `/blockinput <on|off>` - Freeze or unfreeze desk keyboard and mouse
* `/alarm` - Sound warning alert chimes on PC speakers
* `/sleep` - Turn off caffeinate and suspend PC
* `/shutdown` - Safely power off PC (15-second abort delay)

### Agent & Workspace Supervision
* `/status` - Workstation status, RAM, branch, mode, caffeinate uptime
* `/caffeinate <on|off>` - Toggle anti-sleep wake-lock
* `/recall <query>` - Sub-50ms SQLite FTS5 search across memories and decisions
* `/artifacts` - View the 4 newest generated artifacts and reports
* `/git status` - Inspect working tree, staged files, and untracked changes
* `/git diff` - View unstaged code changes directly in chat
* `/git commit -m "..."` - Stage and commit local code changes
* `/git push` - Push commits to remote git repository
* `/exec <command>` - Execute arbitrary shell command in workspace

---

## 5. Workstation CLI Commands

You can also control the remote subsystem directly from your PC terminal:

```bash
# Setup remote bridge (Telegram or WhatsApp)
aegis remote setup

# View remote bridge status, token, and pairing state
aegis remote status

# Test outbound mobile message dispatch
aegis remote test

# Start the background remote listener and daemon
aegis remote start

# Instantly lock screen while keeping AI agents active
aegis lock

# Type text into active desktop window from CLI
aegis type "Run full test suite and build release"

# Manage Caffeinate independently
aegis caffeinate on
aegis caffeinate off
aegis caffeinate status
aegis caffeinate lock
```

---

## 6. Security & Isolation Model

* **Pairing PIN**: First-time connections must pass `/auth <PIN>`. Unauthenticated messages are rejected immediately.
* **ID Whitelisting**: Upon successful authentication, your unique Telegram Chat ID or phone number is persisted to `~/.aegis-brain/remote.json`. Messages from any other account are ignored.
* **Execution Timeout**: All remote shell executions have a hard 60-second execution cap to prevent runaway commands from hanging the machine.
* **Buffer Truncation**: Output buffers exceeding 1,300 characters are safely truncated to comply with mobile messaging limits while preserving the head and exit code.
