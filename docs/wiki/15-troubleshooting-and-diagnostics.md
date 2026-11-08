# Chapter 15: Troubleshooting & Diagnostics

This chapter provides an Arch Linux Wiki-style troubleshooting manual for AegisBrain, detailing exact error messages, underlying root causes, diagnostic recipes, and recovery procedures.

---

## 1. Quick Diagnostic Recipes

Before manual debugging, execute AegisBrain's automated diagnostic suite:

```bash
# Run comprehensive environment health check
aegis doctor

# Automatically repair directory permissions, missing paths, and database indices
aegis doctor --fix

# Run deep inspection on Tier 3 worker endpoints
aegis doctor --models

# Generate a sanitized diagnostic report and bundle for GitHub issues
aegis report
```

---

## 2. Troubleshooting Matrix

### 2.1 Daemon Socket Connection Refused

#### Symptom
```
ConnectionRefusedError: [Errno 111] Connection refused
# or on Windows:
urllib.error.URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
```

#### Cause
The AegisBrain background daemon (`aegis.server` on port `8765`) is not running, or was terminated unexpectedly.

#### Recovery Procedure
1. Check if a stale PID file exists:
   ```bash
   cat ~/.aegis-brain/daemon.pid
   ```
2. Check for port collisions:
   ```powershell
   # Windows
   netstat -ano | findstr :8765

   # Linux / macOS
   lsof -i :8765
   ```
3. Start the daemon in foreground mode to inspect boot logs:
   ```bash
   aegis daemon --port 8765
   ```
4. If healthy, restart as a detached background service:
   ```bash
   aegis start
   ```

---

### 2.2 SQLite WAL Database Lock Contention

#### Symptom
```
sqlite3.OperationalError: database is locked
```

#### Cause
An external process opened `brain.db` without asserting `PRAGMA journal_mode = WAL`, causing an exclusive table lock that blocked concurrent agent threads.

#### Recovery Procedure
1. Terminate all orphaned agent processes holding file handles on `brain.db`.
2. Inspect and reset database journal mode using the SQLite CLI:
   ```bash
   sqlite3 ~/.aegis-brain/brain.db "PRAGMA journal_mode = WAL; PRAGMA wal_checkpoint(TRUNCATE);"
   ```
3. Run `aegis doctor --fix` to verify database health.

---

### 2.3 Vim Insert-Mode Trapped Prompt Bug

#### Symptom
Text injected via mobile remote appears as garbled command sequences (e.g. `dd`, `dw`, or line jumps), or pressing `<Enter>` fails to submit the prompt.

#### Cause
The console window was in Neovim/Vim Normal Mode, and synthetic input was injected without the calibrated insert-mode transition.

#### Recovery Procedure
AegisBrain enforces the **Calibrated Vim Execution Protocol**:
1. In your mobile prompt, prefix with `/altm` to break out of any trapped dialogs.
2. Ensure you are using the latest `aegis type` binary which automatically asserts `VK_ESCAPE`, `VK_ESCAPE`, `i`, injects payload, and presses `<Enter>` directly in Insert Mode.
3. Test manual injection:
   ```bash
   aegis type "echo 'Vim test'"
   ```

---

### 2.4 Telegram Remote Polling / 401 Unauthorized

#### Symptom
```
telegram.error.Unauthorized: Invalid token
# or listener continuously disconnects with ConnectionResetError
```

#### Cause
The Telegram Bot Token in `~/.aegis-brain/remote_config.json` is missing, expired, or another instance of the daemon is running with the same token.

#### Recovery Procedure
1. Verify `~/.aegis-brain/remote_config.json`:
   ```json
   {
     "service": "telegram",
     "telegram_bot_token": "YOUR_VALID_TOKEN",
     "authorized_chat_id": 123456789
   }
   ```
2. Only one process may long-poll Telegram's `getUpdates` API at a time. Kill duplicate listeners:
   ```bash
   aegis stop
   aegis start
   ```

---

### 2.5 Local Whisper Voice Transcription Failure

#### Symptom
```
FileNotFoundError: [Errno 2] No such file or directory: 'whisper.exe'
# or FFmpeg transcoding fails with exit status 1
```

#### Cause
`whisper.exe` or `ffmpeg` is not present in the system `PATH`.

#### Recovery Procedure
1. Check executable visibility:
   ```powershell
   Get-Command ffmpeg, whisper -ErrorAction SilentlyContinue
   ```
2. If using standalone Whisper, place `whisper.exe` in `~/.local/bin/` or install via winget / brew:
   ```bash
   # Windows
   winget install Gyan.FFmpeg

   # macOS
   brew install ffmpeg
   ```
3. Verify offline conversion manually:
   ```bash
   ffmpeg -version
   ```

---

### 2.6 Playwright Browser Binaries Missing in Hands Engine

#### Symptom
```
playwright._impl._errors.Error: Executable doesn't exist at C:\Users\...\AppData\Local\ms-playwright\chromium-...
```

#### Cause
The Python `playwright` package is installed, but the headless Chromium browser binaries were never downloaded.

#### Recovery Procedure
1. Install the headless Chromium browser binaries:
   ```bash
   playwright install chromium
   ```
2. If operating in an environment without internet access or restricted binary execution, use AegisBrain's zero-dependency fallback:
   ```bash
   # AegisBrain will automatically use LightweightDOMParser if Playwright fails
   aegis hands http://localhost:3000
   ```

---

### 2.7 Tier 3 Worker Cascade Unavailability

#### Symptom
```
RuntimeError: No Tier 3 execution workers available (OpenCode, Hermes, and Ollama all failed).
```

#### Cause
All worker endpoints failed: OpenCode free models exhausted quota, Hermes cloud API was unreachable, and local Ollama daemon was not running.

#### Recovery Procedure
1. Start your local Ollama daemon:
   ```bash
   ollama serve
   ollama pull qwen2.5-coder:7b
   ```
2. Verify worker setup instructions:
   ```bash
   aegis workers advice
   ```
3. Run the interactive Worker Wizard to configure at least one free endpoint:
   ```bash
   aegis setup --workers
   ```

---

### 2.8 Slow Shell Hook Startup (> 50ms)

#### Symptom
Opening a new PowerShell, Bash, or Zsh terminal takes noticeably longer than usual.

#### Cause
The shell hook is executing full Git commit log traversals or network requests during every prompt render.

#### Recovery Procedure
1. Ensure the hook uses the cached `--compact` mode:
   ```bash
   aegis hook --shell bash
   ```
2. Check `~/.aegis-brain/ACTIVE_CONTEXT.md` write latency:
   ```bash
   aegis bootstrap
   ```
3. If Git status in massive monorepos is slow, add `.aegisignore` or turn off dirty-tree scanning in `~/.aegis-brain/config.json`.
