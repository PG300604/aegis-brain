"""Cross-platform service and autostart manager for AegisBrain.

Manages headless, background startup at user logon and system wake:
- Windows: Headless VBS runner in User Startup folder (zero elevation, zero console popup).
- Linux: Systemd user service (~/.config/systemd/user/aegis-brain.service).
- macOS: LaunchAgent plist (~/Library/LaunchAgents/com.aegis.brain.plist).
"""

import os
import platform
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, Tuple
from .config import DEFAULT_PORT

REPO_ROOT = Path(__file__).resolve().parent.parent


def is_daemon_running(port: int = DEFAULT_PORT) -> bool:
    """Check if AegisBrain daemon is actively responding on localhost."""
    url = f"http://127.0.0.1:{port}/health"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AegisBrain-Service/1.0"})
        with urllib.request.urlopen(req, timeout=1.0) as res:
            return res.status == 200
    except Exception:
        return False


def stop_daemon(port: int = DEFAULT_PORT) -> Tuple[bool, str]:
    """Gracefully request the running daemon to shut down."""
    if not is_daemon_running(port):
        return True, "AegisBrain daemon is not currently running."

    url = f"http://127.0.0.1:{port}/shutdown"
    try:
        req = urllib.request.Request(url, data=b"{}", headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=2.0) as res:
            if res.status == 200:
                return True, "AegisBrain daemon stopped cleanly."
    except Exception as e:
        pass

    return False, "Could not send shutdown signal to daemon."


def _get_python_runner(windowless: bool = False) -> str:
    """Return python executable for background execution."""
    if sys.platform == "win32":
        py_name = "pythonw.exe" if windowless else "python.exe"
        py312 = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Python" / "Python312" / py_name
        if py312.exists():
            return str(py312)
        if windowless:
            pyw = Path(sys.executable).parent / "pythonw.exe"
            if pyw.exists():
                return str(pyw)
    return sys.executable


# --- Windows Implementation ---

def _get_windows_startup_vbs() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        appdata = str(Path.home() / "AppData" / "Roaming")
    startup_dir = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    startup_dir.mkdir(parents=True, exist_ok=True)
    return startup_dir / "aegis-brain-startup.vbs"


def _enable_windows() -> Tuple[bool, str]:
    vbs_path = _get_windows_startup_vbs()
    runner = _get_python_runner()
    repo_dir = str(REPO_ROOT)

    log_path = Path.home() / ".aegis-brain" / "daemon.log"
    # Prefer pythonw.exe on Windows for zero-console headless execution
    pythonw_runner = runner.parent / "pythonw.exe"
    actual_runner = pythonw_runner if pythonw_runner.exists() else runner

    # VBScript executes completely headlessly (0 = invisible window, False = don't wait, On Error Resume Next suppresses dialogs)
    vbs_content = f'''On Error Resume Next
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c set PYTHONIOENCODING=utf-8&&set PYTHONPATH={repo_dir}&&cd /d ""{repo_dir}""&&""{actual_runner}"" -m aegis.server >> ""{log_path}"" 2>&1", 0, False
'''
    vbs_path.write_text(vbs_content, encoding="utf-8")
    return True, f"Windows autostart enabled via {vbs_path}"


def _disable_windows() -> Tuple[bool, str]:
    vbs_path = _get_windows_startup_vbs()
    if vbs_path.exists():
        vbs_path.unlink()
        return True, "Windows autostart disabled (startup script removed)."
    return True, "Windows autostart was already disabled."


# --- Linux Implementation ---

def _get_linux_systemd_file() -> Path:
    unit_dir = Path.home() / ".config" / "systemd" / "user"
    unit_dir.mkdir(parents=True, exist_ok=True)
    return unit_dir / "aegis-brain.service"


def _enable_linux() -> Tuple[bool, str]:
    service_file = _get_linux_systemd_file()
    python_bin = sys.executable
    repo_dir = str(REPO_ROOT)

    content = f"""[Unit]
Description=AegisBrain Neural Memory Daemon
After=network.target

[Service]
Type=simple
WorkingDirectory={repo_dir}
ExecStart={python_bin} -m aegis.server
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
"""
    service_file.write_text(content, encoding="utf-8")
    subprocess.run(["systemctl", "--user", "daemon-reload"], capture_output=True)
    subprocess.run(["systemctl", "--user", "enable", "aegis-brain"], capture_output=True)
    return True, f"Linux systemd autostart enabled via {service_file}"


def _disable_linux() -> Tuple[bool, str]:
    service_file = _get_linux_systemd_file()
    subprocess.run(["systemctl", "--user", "disable", "--now", "aegis-brain"], capture_output=True)
    if service_file.exists():
        service_file.unlink()
    subprocess.run(["systemctl", "--user", "daemon-reload"], capture_output=True)
    return True, "Linux systemd autostart disabled."


# --- macOS Implementation ---

def _get_macos_launch_agent_file() -> Path:
    agent_dir = Path.home() / "Library" / "LaunchAgents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    return agent_dir / "com.aegis.brain.plist"


def _enable_macos() -> Tuple[bool, str]:
    plist_file = _get_macos_launch_agent_file()
    python_bin = sys.executable
    repo_dir = str(REPO_ROOT)
    log_path = Path.home() / ".aegis-brain" / "daemon.log"

    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aegis.brain</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_bin}</string>
        <string>-m</string>
        <string>aegis.server</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{repo_dir}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{log_path}</string>
    <key>StandardErrorPath</key>
    <string>{log_path}</string>
</dict>
</plist>
"""
    plist_file.write_text(content, encoding="utf-8")
    subprocess.run(["launchctl", "load", str(plist_file)], capture_output=True)
    return True, f"macOS autostart enabled via {plist_file}"


def _disable_macos() -> Tuple[bool, str]:
    plist_file = _get_macos_launch_agent_file()
    subprocess.run(["launchctl", "unload", str(plist_file)], capture_output=True)
    if plist_file.exists():
        plist_file.unlink()
    return True, "macOS autostart disabled."


# --- Public Interface ---

def is_autostart_enabled() -> bool:
    system = platform.system()
    if system == "Windows":
        return _get_windows_startup_vbs().exists()
    elif system == "Linux":
        return _get_linux_systemd_file().exists()
    elif system == "Darwin":
        return _get_macos_launch_agent_file().exists()
    return False


def enable_autostart() -> Tuple[bool, str]:
    system = platform.system()
    if system == "Windows":
        ok, msg = _enable_windows()
    elif system == "Linux":
        ok, msg = _enable_linux()
    elif system == "Darwin":
        ok, msg = _enable_macos()
    else:
        return False, f"Autostart not supported on {system}"

    # Also start the daemon immediately if it's not running
    if not is_daemon_running():
        start_daemon()

    return ok, msg


def disable_autostart() -> Tuple[bool, str]:
    system = platform.system()
    if system == "Windows":
        ok, msg = _disable_windows()
    elif system == "Linux":
        ok, msg = _disable_linux()
    elif system == "Darwin":
        ok, msg = _disable_macos()
    else:
        return False, f"Autostart not supported on {system}"

    # Stop running daemon
    stop_daemon()
    return ok, msg


def start_daemon(port: int = DEFAULT_PORT) -> Tuple[bool, str]:
    """Start daemon in background detached from current process."""
    if is_daemon_running(port):
        return True, f"AegisBrain daemon is already running on port {port}."

    runner = _get_python_runner()
    repo_dir = str(REPO_ROOT)
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{repo_dir};{env.get('PYTHONPATH', '')}"

    log_path = Path.home() / ".aegis-brain" / "daemon.log"
    log_file = open(log_path, "a", encoding="utf-8")

    if platform.system() == "Windows":
        runner_w = _get_python_runner(windowless=True)
        DETACHED_PROCESS = 0x00000008
        CREATE_NO_WINDOW = 0x08000000
        subprocess.Popen(
            [runner_w, "-m", "aegis.server"],
            cwd=repo_dir,
            env=env,
            creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW,
            stdin=subprocess.DEVNULL,
            stdout=log_file,
            stderr=log_file,
            close_fds=True,
        )
    else:
        subprocess.Popen(
            [runner, "-m", "aegis.server"],
            cwd=repo_dir,
            env=env,
            start_new_session=True,
            stdin=subprocess.DEVNULL,
            stdout=log_file,
            stderr=log_file,
        )

    # Wait briefly to confirm startup
    import time
    for _ in range(10):
        time.sleep(0.15)
        if is_daemon_running(port):
            return True, f"AegisBrain daemon started in background on http://127.0.0.1:{port}"

    return True, "AegisBrain daemon launch initiated."
