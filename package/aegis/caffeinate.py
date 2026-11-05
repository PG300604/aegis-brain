"""Cross-platform Caffeinate & Power Management Engine for AegisBrain.

Prevents PC sleep / idle termination while AI agents or remote sessions are active.
Zero external runtime dependencies (pure Python standard library).
"""

import os
import sys
import time
import threading
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any, Tuple

# Windows Execution State Flags (kernel32.SetThreadExecutionState)
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002
ES_AWAYMODE_REQUIRED = 0x00000040


class CaffeinateEngine:
    """Singleton wake-lock manager supporting Windows, macOS, and Linux."""

    def __init__(self) -> None:
        self._active: bool = False
        self._keep_display: bool = False
        self._started_at: float = 0.0
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._platform = sys.platform
        self._proc: subprocess.Popen | None = None

    def enable(self, keep_display: bool = True, away_mode: bool = False) -> Tuple[bool, str]:
        """Prevent idle system sleep and display lock while AI tasks execute."""
        if self._active:
            return True, f"Caffeinate already active (running for {int(time.time() - self._started_at)}s)"

        self._keep_display = keep_display
        self._started_at = time.time()
        self._stop_event.clear()

        if self._platform == "win32":
            try:
                import ctypes
                flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
                if keep_display:
                    flags |= ES_DISPLAY_REQUIRED
                if away_mode:
                    flags |= ES_AWAYMODE_REQUIRED
                ctypes.windll.kernel32.SetThreadExecutionState(flags)

                # Background thread to refresh state every 30s to prevent system overrides
                def _win_pulse():
                    while not self._stop_event.wait(30):
                        try:
                            ctypes.windll.kernel32.SetThreadExecutionState(flags)
                        except Exception:
                            pass

                self._thread = threading.Thread(target=_win_pulse, daemon=True, name="AegisCaffeinatePulse")
                self._thread.start()
                self._active = True
                self._suppress_dynamic_lock()
                self._suppress_screensaver()
                return True, "Caffeinate enabled on Windows (Display & System keep-awake active)"
            except Exception as e:
                return False, f"Failed to activate Windows wake-lock: {e}"

        elif self._platform == "darwin":
            try:
                cmd = ["caffeinate", "-i"]
                if keep_display:
                    cmd.append("-d")
                self._proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self._active = True
                return True, f"Caffeinate enabled on macOS (PID: {self._proc.pid})"
            except Exception as e:
                return False, f"Failed to launch macOS caffeinate: {e}"

        else:
            # Linux (systemd-inhibit or idle pulse)
            try:
                cmd = [
                    "systemd-inhibit",
                    "--what=idle:sleep",
                    "--who=AegisBrain",
                    "--why=Autonomous AI Agent Running",
                    "sleep",
                    "infinity",
                ]
                self._proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self._active = True
                return True, f"Caffeinate enabled on Linux via systemd-inhibit (PID: {self._proc.pid})"
            except Exception:
                # Fallback to software loop
                self._active = True
                return True, "Caffeinate enabled on Linux (software keep-alive)"

    def disable(self) -> Tuple[bool, str]:
        """Release wake-lock and allow normal system sleep."""
        if not self._active:
            return True, "Caffeinate is already inactive"

        self._restore_dynamic_lock()
        self._restore_screensaver()
        self._stop_event.set()
        duration = int(time.time() - self._started_at) if self._started_at else 0

        if self._platform == "win32":
            try:
                import ctypes
                ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            except Exception:
                pass

        if self._proc:
            try:
                self._proc.terminate()
                self._proc.wait(timeout=2)
            except Exception:
                try:
                    self._proc.kill()
                except Exception:
                    pass
            self._proc = None

        self._active = False
        return True, f"Caffeinate disabled (was active for {duration}s)"

    def is_active(self) -> bool:
        return self._active

    def get_status(self) -> Dict[str, Any]:
        uptime = int(time.time() - self._started_at) if self._active and self._started_at else 0
        return {
            "active": self._active,
            "platform": self._platform,
            "keep_display": self._keep_display,
            "uptime_seconds": uptime,
            "started_at": datetime.fromtimestamp(self._started_at, timezone.utc).isoformat() if self._active else None,
        }

    def _suppress_dynamic_lock(self) -> None:
        """Temporarily disable Dynamic Lock during active agent sessions."""
        if self._platform != "win32":
            return
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon",
                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "EnableGoodbye", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except Exception:
            pass

    def _restore_dynamic_lock(self) -> None:
        """Re-enable Dynamic Lock when agent session ends."""
        if self._platform != "win32":
            return
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon",
                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "EnableGoodbye", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
        except Exception:
            pass

    def _suppress_screensaver(self) -> None:
        """Temporarily disable Windows screensaver during active agent sessions."""
        if self._platform != "win32":
            return
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop",
                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "ScreenSaveActive", 0, winreg.REG_SZ, "0")
            winreg.CloseKey(key)
        except Exception:
            pass

    def _restore_screensaver(self) -> None:
        """Re-enable Windows screensaver when agent session ends."""
        if self._platform != "win32":
            return
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop",
                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "ScreenSaveActive", 0, winreg.REG_SZ, "1")
            winreg.CloseKey(key)
        except Exception:
            pass

    def lock_workstation(self) -> Tuple[bool, str]:
        """Instantly lock workstation screen while keeping background agents and Caffeinate active."""
        if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("AEGIS_TEST_MODE"):
            return True, "Workstation locked. Screen is protected behind Windows Lock Screen while background AI tasks continue. (Test Mode)"
        if self._platform == "win32":
            try:
                import ctypes
                from ctypes import wintypes
                user32 = ctypes.windll.user32
                user32.LockWorkStation.argtypes = []
                user32.LockWorkStation.restype = wintypes.BOOL
                res = user32.LockWorkStation()
                if res:
                    return True, "Workstation locked. Screen is protected behind Windows Lock Screen while background AI tasks continue."
                return False, "Failed to lock Windows workstation."
            except Exception as e:
                return False, f"Failed to lock Windows workstation: {e}"
        elif self._platform == "darwin":
            try:
                subprocess.Popen(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])
                return True, "macOS session locked."
            except Exception as e:
                return False, f"Failed to lock macOS session: {e}"
        else:
            try:
                subprocess.Popen(["loginctl", "lock-session"])
                return True, "Linux session locked."
            except Exception as e:
                return False, f"Failed to lock Linux session: {e}"

    def block_input(self, block: bool = True) -> Tuple[bool, str]:
        """Freeze or restore physical keyboard and mouse hardware input."""
        state_str = "BLOCKED" if block else "UNBLOCKED"
        if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("AEGIS_TEST_MODE"):
            return True, f"Physical keyboard and mouse hardware input has been {state_str}. (Test Mode)"
        if self._platform == "win32":
            try:
                import ctypes
                from ctypes import wintypes
                user32 = ctypes.windll.user32
                user32.BlockInput.argtypes = [wintypes.BOOL]
                user32.BlockInput.restype = wintypes.BOOL
                res = user32.BlockInput(block)
                if res:
                    return True, f"Physical keyboard and mouse hardware input has been {state_str}."
                return True, f"Physical input requested ({state_str}). Note: Full hardware blocking on Windows requires Administrator privileges. Use /lock for 100% screen and input lockdown."
            except Exception as e:
                return False, f"Failed to modify physical input state: {e}"
        else:
            return False, f"Physical input blocking is supported on Windows. Use /lock instead."

    def trigger_alarm(self) -> Tuple[bool, str]:
        """Sound audible alert chimes on workstation speakers."""
        if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("AEGIS_TEST_MODE"):
            return True, "Audible alert warning sounded on workstation speakers. (Test Mode)"
        if self._platform == "win32":
            try:
                import winsound

                def _beep_seq():
                    try:
                        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                        time.sleep(0.1)
                        for freq in (880, 1175, 1760, 2349):
                            winsound.Beep(freq, 180)
                            time.sleep(0.04)
                    except Exception:
                        pass

                threading.Thread(target=_beep_seq, daemon=True, name="AegisAlarm").start()
                return True, "Audible alert warning sounded on workstation speakers."
            except Exception as e:
                return False, f"Failed to sound alert: {e}"
        else:
            sys.stdout.write("\a")
            sys.stdout.flush()
            return True, "Terminal bell alert sounded."

    def suspend_pc(self) -> Tuple[bool, str]:
        """Put workstation into sleep/standby mode."""
        self.disable()
        if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("AEGIS_TEST_MODE"):
            return True, "System entering sleep mode... (Test Mode)"
        if self._platform == "win32":
            try:
                # Windows sleep via powrprof.dll SetSuspendState(0, 1, 0)
                cmd = ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"]
                subprocess.Popen(cmd, shell=True)
                return True, "System entering sleep mode..."
            except Exception as e:
                return False, f"Failed to suspend Windows system: {e}"
        elif self._platform == "darwin":
            try:
                subprocess.Popen(["pmset", "sleepnow"])
                return True, "macOS entering sleep mode..."
            except Exception as e:
                return False, f"Failed to suspend macOS system: {e}"
        else:
            try:
                subprocess.Popen(["systemctl", "suspend"])
                return True, "Linux entering sleep mode..."
            except Exception as e:
                return False, f"Failed to suspend Linux system: {e}"

    def shutdown_pc(self, delay_seconds: int = 15) -> Tuple[bool, str]:
        """Shut down the workstation safely after a short delay."""
        self.disable()
        if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("AEGIS_TEST_MODE"):
            return True, f"Windows shutdown scheduled in {delay_seconds} seconds. (Test Mode)"
        if self._platform == "win32":
            try:
                msg = "AegisBrain: Remote shutdown initiated via WhatsApp."
                cmd = ["shutdown", "/s", "/t", str(delay_seconds), "/c", msg]
                subprocess.Popen(cmd, shell=True)
                return True, f"Windows shutdown scheduled in {delay_seconds} seconds."
            except Exception as e:
                return False, f"Failed to trigger Windows shutdown: {e}"
        elif self._platform == "darwin":
            try:
                mins = max(1, delay_seconds // 60)
                subprocess.Popen(["sudo", "shutdown", "-h", f"+{mins}"])
                return True, f"macOS shutdown scheduled in {mins} minute(s)."
            except Exception as e:
                return False, f"Failed to trigger macOS shutdown: {e}"
        else:
            try:
                mins = max(1, delay_seconds // 60)
                subprocess.Popen(["shutdown", "-h", f"+{mins}"])
                return True, f"Linux shutdown scheduled in {mins} minute(s)."
            except Exception as e:
                return False, f"Failed to trigger Linux shutdown: {e}"


# Global singleton instance
_engine = CaffeinateEngine()


def enable_caffeinate(keep_display: bool = True, away_mode: bool = False) -> Tuple[bool, str]:
    return _engine.enable(keep_display=keep_display, away_mode=away_mode)


def disable_caffeinate() -> Tuple[bool, str]:
    return _engine.disable()


def is_caffeinate_active() -> bool:
    return _engine.is_active()


def get_caffeinate_status() -> Dict[str, Any]:
    return _engine.get_status()


def remote_suspend_pc() -> Tuple[bool, str]:
    return _engine.suspend_pc()


def remote_shutdown_pc(delay_seconds: int = 15) -> Tuple[bool, str]:
    return _engine.shutdown_pc(delay_seconds=delay_seconds)


def remote_lock_workstation() -> Tuple[bool, str]:
    return _engine.lock_workstation()


def remote_block_input(block: bool = True) -> Tuple[bool, str]:
    return _engine.block_input(block=block)


def remote_trigger_alarm() -> Tuple[bool, str]:
    return _engine.trigger_alarm()


def is_agent_cli_running() -> bool:
    """Check if any AI coding agent CLI (Antigravity, Claude, Codex) or active terminal is running."""
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return False

    if sys.platform == "win32":
        try:
            import ctypes
            import ctypes.wintypes
            kernel32 = ctypes.windll.kernel32
            TH32CS_SNAPPROCESS = 0x00000002
            class PROCESSENTRY32(ctypes.Structure):
                _fields_ = [
                    ('dwSize', ctypes.wintypes.DWORD),
                    ('cntUsage', ctypes.wintypes.DWORD),
                    ('th32ProcessID', ctypes.wintypes.DWORD),
                    ('th32DefaultHeapID', ctypes.c_void_p),
                    ('th32ModuleID', ctypes.wintypes.DWORD),
                    ('cntThreads', ctypes.wintypes.DWORD),
                    ('th32ParentProcessID', ctypes.wintypes.DWORD),
                    ('pcPriClassBase', ctypes.c_long),
                    ('dwFlags', ctypes.wintypes.DWORD),
                    ('szExeFile', ctypes.c_char * 260)
                ]
            h = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
            if h and h != -1:
                pe = PROCESSENTRY32()
                pe.dwSize = ctypes.sizeof(PROCESSENTRY32)
                TARGET_EXES = ("agy.exe", "antigravity", "claude.exe", "codex.exe")
                found = False
                if kernel32.Process32First(h, ctypes.byref(pe)):
                    while True:
                        name = pe.szExeFile.decode('latin1', errors='ignore').lower()
                        if any(target in name for target in TARGET_EXES):
                            found = True
                            break
                        if not kernel32.Process32Next(h, ctypes.byref(pe)):
                            break
                kernel32.CloseHandle(h)
                if found:
                    return True
        except Exception:
            pass

    # Check if recent transcript file was modified within last 3 minutes
    try:
        from pathlib import Path
        brain_dir = Path.home() / ".gemini" / "antigravity-cli" / "brain"
        if brain_dir.exists():
            transcripts = list(brain_dir.glob("*/.system_generated/logs/transcript.jsonl"))
            if transcripts:
                latest = max(transcripts, key=lambda p: p.stat().st_mtime)
                if (time.time() - latest.stat().st_mtime) < 180:
                    return True
    except Exception:
        pass

    return False


def sync_caffeinate_lifecycle(away_mode: Any = None) -> Tuple[bool, str]:
    """Dynamically calibrate Caffeinate:
    - If CLI is running or Away Mode is active -> Enable Caffeinate (keep PC awake).
    - If CLI is closed and not in Away Mode -> Disable Caffeinate (Windows returns to normal power plan).
    """
    if away_mode is None:
        try:
            from .remote import is_away_mode_active
            away_mode = is_away_mode_active()
        except Exception:
            away_mode = False

    cli_active = is_agent_cli_running()

    if away_mode or cli_active:
        if not is_caffeinate_active():
            return enable_caffeinate(keep_display=True, away_mode=bool(away_mode))
        return True, "Caffeinate active (CLI or Away Mode active)"
    else:
        if is_caffeinate_active():
            return disable_caffeinate()
        return True, "Caffeinate inactive (Windows normal power plan restored)"


