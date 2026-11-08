# Chapter 02: Installation & Shell Hooks

This guide details the universal installation procedures, shell hook integrations, and operating system autostart service configurations for AegisBrain across Windows, Linux, and macOS.

---

## 1. Universal Installation

### 1.1 Direct PyPI Installation

Install AegisBrain into your global or isolated Python 3.10+ environment using `pip` or `uv`:

```bash
# Using standard pip
pip install aegis-brain

# Using uv (sub-second install)
uv pip install aegis-brain
```

### 1.2 From Source (Editable Developer Mode)

For developers contributing to AegisBrain or customizing heuristics:

```bash
git clone https://github.com/PG300604/aegis-brain.git
cd aegis-brain/package
pip install -e .
```

Verify the installation:
```bash
aegis --help
```

---

## 2. Shell Hooks (`aegis hook`)

AegisBrain provides zero-latency shell hooks that synchronize active project context and branch status into every new terminal session in less than 25 milliseconds.

### 2.1 Supported Shells

| Shell | Configuration File | Hook Command |
| :--- | :--- | :--- |
| **PowerShell** | `$PROFILE` | `if (Get-Command aegis -ErrorAction SilentlyContinue) { aegis hook --shell powershell \| Out-String \| Invoke-Expression }` |
| **Bash** | `~/.bashrc` | `command -v aegis >/dev/null 2>&1 && eval "$(aegis hook --shell bash)"` |
| **Zsh** | `~/.zshrc` | `command -v aegis >/dev/null 2>&1 && eval "$(aegis hook --shell zsh)"` |
| **Fish** | `~/.config/fish/config.fish` | `type -q aegis; and aegis hook --shell fish \| source` |

### 2.2 How the Shell Hook Operates

When a new terminal opens or the current working directory changes:
1. The hook executes `aegis bootstrap --compact`.
2. The Context Governor inspects:
   - Current Git branch and dirty working-tree state.
   - Latest commit hash and unpushed commits.
   - Active tracked PRs.
   - Top 4 architectural decisions from `brain.db`.
3. It refreshes `~/.aegis-brain/ACTIVE_CONTEXT.md` in under 30 ms.
4. Any coding agent running in that directory reads `ACTIVE_CONTEXT.md` for immediate zero-token amnesia recovery.

---

## 3. Zero-Elevation OS Autostart Services

To ensure 24/7 background availability for Telegram remote control, memory recall, and file watchdogs without manual invocation, AegisBrain installs non-intrusive autostart services that require **zero administrator privileges** and **zero UAC prompts**.

### 3.1 Windows Implementation

On Windows, AegisBrain utilizes the User Startup folder:
- **Target Path**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\aegis-brain-startup.vbs`
- **Execution Host**: `wscript.exe` with `WindowStyle = 0` (completely hidden; zero console flashes).

#### Generated VBScript Content:
```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "python.exe -m aegis.server", 0, False
Set WshShell = Nothing
```

#### Windows Task Scheduler Alternative:
For systems with strict startup folder policies, AegisBrain can register a Windows Scheduled Task:
- **Task Name**: `AegisBrainDaemonKeepAlive`
- **Trigger**: At log on of any user, repeating every 5 minutes if process is terminated.
- **Run Level**: Least Privileges (standard user token).

### 3.2 Linux Implementation (systemd User Unit)

On Linux distributions running systemd, AegisBrain configures a user-level service that runs independent of root:
- **Unit Path**: `~/.config/systemd/user/aegis-brain.service`

```ini
[Unit]
Description=AegisBrain 24/7 Autonomous Engineering Chassis
After=network.target

[Service]
Type=simple
ExecStart=%h/.local/bin/aegis start --foreground
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
```

Enable and activate:
```bash
systemctl --user daemon-reload
systemctl --user enable --now aegis-brain
```

### 3.3 macOS Implementation (LaunchAgent)

On macOS, AegisBrain installs a user LaunchAgent:
- **Plist Path**: `~/Library/LaunchAgents/com.aegis.brain.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aegis.brain</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>-m</string>
        <string>aegis.server</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/tmp/aegis-brain.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/aegis-brain.out</string>
</dict>
</plist>
```

Load the LaunchAgent:
```bash
launchctl load -w ~/Library/LaunchAgents/com.aegis.brain.plist
```

---

## 4. Service Management CLI

Manage background services directly from the unified CLI:

```bash
# Enable OS autostart service for current platform
aegis autostart on

# Disable OS autostart service
aegis autostart off

# Check autostart service configuration and path
aegis autostart status

# Inspect live daemon status, PID, and memory
aegis status
```
