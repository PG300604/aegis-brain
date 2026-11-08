# Chapter 09: Mobile Remote & Whisper Bridge

This chapter specifies AegisBrain's 24/7 mobile remote control architecture, local speech-to-text voice pipeline, Win32 console injection mechanics, and in-flight session steering via Telegram (`@HHAACLIBot`) and WhatsApp.

---

## 1. Mobile Remote Architecture

AegisBrain enables developers to steer, monitor, and query long-running coding sessions from their smartphone while away from their workstation:

```
    [ Developer's Smartphone ]
    (Telegram: @HHAACLIBot / WhatsApp)
                │
                │ Voice Note (.oga) or Text Command
                ▼
  ┌────────────────────────────────────────────────────────┐
  │ AegisBrain Remote Listener Subsystem                   │
  │ - 24/7 Long-Polling Daemon Thread                      │
  │ - Inbound Message Verification & PIN Auth Gate         │
  └────────────────────────────┬───────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
     [ Voice Message ]                     [ Text Command ]
            │                                     │
            ▼                                     │
  ┌────────────────────────┐                      │
  │ Audio Preprocessing    │                      │
  │ - FFmpeg 16kHz Mono    │                      │
  └─────────┬──────────────┘                      │
            ▼                                     │
  ┌────────────────────────┐                      │
  │ Local Whisper Engine   │                      │
  │ - 100% Offline (.exe)  │                      │
  │ - Zero Cloud API Keys  │                      │
  └─────────┬──────────────┘                      │
            ▼                                     │
  [ Transcribed Text Prompt ]                     │
            │                                     │
            └──────────────────┬──────────────────┘
                               │
                               ▼
  ┌────────────────────────────────────────────────────────┐
  │ Win32 Native Console Injection Subsystem               │
  │ - AttachConsole() & WriteConsoleInputW()               │
  │ - Zero Focus Stealing / Tiling-Window-Manager Safe     │
  │ - Calibrated Vim Insert-Mode Enter Protocol            │
  └────────────────────────────┬───────────────────────────┘
                               │
                               ▼
  ┌────────────────────────────────────────────────────────┐
  │ Active Coding Session (Antigravity / Claude / Codex)   │
  │                                                        │
  │  - Streams terminal progress back to mobile            │
  │  - Emits '🏁 Execution Completed!' banner upon finish │
  └────────────────────────────────────────────────────────┘
```

---

## 2. Voice Note Ingestion via Local Whisper

AegisBrain transcribes voice notes completely offline without transmitting developer audio to third-party cloud APIs:

1. **Receipt**: The Telegram listener receives an incoming `.oga` voice note.
2. **Audio Transcoding**: The background pipeline invokes FFmpeg:
   ```bash
   ffmpeg -i voice_note.oga -ar 16000 -ac 1 -c:a pcm_s16le voice_note.wav
   ```
3. **Local Whisper Inference**: The audio is processed using `whisper.exe` (model: `base`):
   ```bash
   whisper.exe voice_note.wav --model base --language en --output_format txt
   ```
4. **Prompt Preparation**: The transcribed text is validated, tagged with `[VOICE_NOTE]`, and queued for desktop injection.

---

## 3. Calibrated Vim Mode & Win32 Console Injection

Injecting text into terminal applications on Windows without stealing focus or breaking tiling window managers (e.g., Komorebi or GlazeWM) requires native Win32 API calls.

### 3.1 Direct Console Buffer Injection
Rather than using fragile synthetic keystrokes (`SendKeys`), AegisBrain utilizes:
- `AttachConsole(process_id)`
- `WriteConsoleInputW(hConsoleInput, records, length, &written)`

This writes input events directly into the console input buffer, operating even when:
- The terminal window is minimized or behind other windows.
- The workstation display is locked.

### 3.2 The Calibrated Vim Insert-Mode Execution Protocol
Many developers run their coding agents inside Neovim or terminal emulators with Vi keybindings. Naive text injection often dumps commands while in Normal Mode, triggering erratic editor commands (e.g. deleting lines or jumping buffers).

AegisBrain enforces the **Calibrated Vim Execution Protocol**:
1. **Escape Sequence**: Sends `VK_ESCAPE`, `VK_ESCAPE` to ensure a clean state.
2. **Insert Mode Transition**: Sends `i` to enter Insert Mode.
3. **Payload Injection**: Writes the prompt payload character by character into the buffer.
4. **Insert-Mode Enter Invariant**: **Presses `<Enter>` directly in Insert Mode** without returning to Normal Mode! This prevents the classic "trapped prompt" bug where `<Enter>` is intercepted as a Normal Mode motion key.

---

## 4. In-Flight Remote Commands

While a task is running, developers can issue specialized control commands from Telegram:

| Command | Action | Description |
| :--- | :--- | :--- |
| `/altm` or ending `/alt+m` | In-Flight Interrupt | Injects an `Alt+M` key chord into the active terminal to safely interrupt running agent loops. |
| `/btw <question>` | Memory Query | Queries neural memory or hardware stats without interrupting the currently executing agent task. |
| `/status` | Telemetry Check | Returns CPU load, memory headroom, active branch, and recent commits. |
| `/lock` | Workstation Lock | Locks the desktop immediately via Win32 `LockWorkStation()` while agents keep running. |

---

## 5. Execution Completion Banners

When an agent finishes executing a prompt and running tests, AegisBrain detects the terminal idle state and dispatches an immediate notification to Telegram:

```
🏁 Execution Completed!
Code execution and tests finished on main (commit 98f4a12).
All 281 tests passing. Working directory clean.
Ready for next directive.
```

This alerts the developer that they can send their next instruction without having to check their workstation.
