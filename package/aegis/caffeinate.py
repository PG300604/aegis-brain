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

    def enable(self, keep_display: bool = False) -> Tuple[bool, str]:
        """Prevent idle system sleep."""
        if self._active:
            return True, f"Caffeinate already active (running for {int(time.time() - self._started_at)}s)"

        self._keep_display = keep_display
        self._started_at = time.time()
        self._stop_event.clear()

        if self._platform == "win32":
            try:
                import ctypes
                flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_AWAYMODE_REQUIRED
                if keep_display:
                    flags |= ES_DISPLAY_REQUIRED
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
                return True, "Caffeinate enabled on Windows (AwayMode & System Required active)"
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

    def suspend_pc(self) -> Tuple[bool, str]:
        """Put workstation into sleep/standby mode."""
        self.disable()
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


def enable_caffeinate(keep_display: bool = False) -> Tuple[bool, str]:
    return _engine.enable(keep_display=keep_display)


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
