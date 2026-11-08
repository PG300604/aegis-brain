# Chapter 10: Power Management & Caffeinate

This chapter details AegisBrain's power management engine (`aegis.caffeinate`), system sleep prevention mechanics, Win32 Away Mode execution states, and remote power controls across Windows, macOS, and Linux.

---

## 1. The Sleep Interruption Problem

Modern desktop operating systems enforce aggressive power management policies: after 10 to 30 minutes of user inactivity, the OS enters standby or system sleep. 

For developer workstations running autonomous coding agents, this creates critical failures:
1. **Thread Suspension**: The agent process halts mid-execution, leaving half-written files or corrupted git states.
2. **Network Drops**: SSH sessions, Telegram long-polling listeners, and remote tunnels disconnect.
3. **Wasted Compute**: Long overnight benchmarks or extensive test suites fail to finish.

AegisBrain prevents unwanted suspension while respecting energy conservation by distinguishing between **Display Sleep** and **System Standby**.

---

## 2. Win32 Implementation & Away Mode

On Windows, AegisBrain interfaces with the Windows Power Management subsystem using `ctypes.windll.kernel32.SetThreadExecutionState`.

### 2.1 Execution State Flags

```python
# Execution state constants in aegis.caffeinate
ES_CONTINUOUS        = 0x80000000  # Informs OS that state remains active until reset
ES_SYSTEM_REQUIRED   = 0x00000001  # Forces CPU and core system to remain active
ES_DISPLAY_REQUIRED  = 0x00000002  # Forces monitor display to remain on
ES_AWAYMODE_REQUIRED = 0x00000040  # Enables Away Mode (silent headless background execution)
```

### 2.2 The Away Mode Advantage
In standard mode, keeping a PC awake requires keeping the display illuminated. On laptops or bedroom workstations, this produces light pollution and wastes power.

By asserting `ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_AWAYMODE_REQUIRED`:
- **The display turns off normally** after the user's configured screen-off timeout.
- **The system enters "Away Mode"**: audio outputs mute, and unnecessary peripherals sleep.
- **The CPU, network adapter, disk I/O, and Aegis daemon remain at 100% operational performance.**

### 2.3 The Continuous Pulse Thread
Certain third-party system utilities (or OEM battery managers) attempt to override thread states. AegisBrain runs a lightweight background daemon thread that re-asserts the execution state every **30 seconds**, ensuring that wake-locks never expire prematurely.

---

## 3. macOS Implementation (`caffeinate`)

On macOS Darwin systems, AegisBrain manages an internal `caffeinate` child process:

```python
# Child process invocation in aegis.caffeinate
cmd = ["caffeinate", "-s", "-i"]  # -s: system required, -i: idle sleep disabled
if keep_display:
    cmd.append("-d")              # -d: display required
proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

When caffeinate is disabled, AegisBrain sends `SIGTERM` to the process and cleans up process handles.

---

## 4. Linux Implementation (`systemd-inhibit`)

On Linux distributions running `systemd-logind`, AegisBrain invokes `systemd-inhibit`:

```bash
systemd-inhibit --what=idle:sleep --who="AegisBrain" --why="Running autonomous agent task" --mode=block python -m aegis.server
```

This registers an inhibitor lock on `org.freedesktop.login1`, preventing power managers (such as GNOME or KDE PowerDevil) from triggering suspend while agents are actively executing.

---

## 5. Remote Workstation Power Controls

Through the mobile remote bridge (`aegis.remote`), developers can manage their PC's physical power state from Telegram:

| Command | Win32 API Call | Description |
| :--- | :--- | :--- |
| `aegis lock` or `/lock` | `LockWorkStation()` | Instantly locks the desktop. Agent sessions and tests continue executing behind the lock screen. |
| `remote_suspend_pc()` | `SetSuspendState(0, 1, 0)` | Suspends the PC into S3 sleep once all queued overnight tasks have passed testing. |
| `remote_shutdown_pc()` | `ExitWindowsEx(EWX_POWEROFF, ...)` | Initiates a clean OS shutdown after all deliverables are saved and committed to git. |

---

## 6. CLI Usage

```bash
# Enable wake-lock allowing display to sleep while CPU stays awake (Away Mode)
aegis caffeinate enable

# Enable wake-lock keeping both CPU and monitor display awake
aegis caffeinate enable --keep-display

# Release wake-lock assertions (return to normal OS power policies)
aegis caffeinate disable

# Inspect active wake-lock status
aegis caffeinate status
```
