# Zero-Elevation Background Automation 🚀

AegisBrain is designed to run silently in the background on your development PC without requiring administrator privileges, user prompts, or intrusive terminal windows.

---

## 🪟 Windows Implementation

On Windows, AegisBrain utilizes the **Windows User Startup Folder**:
- **Path**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\aegis-brain-startup.vbs`
- **Execution Engine**: `wscript.exe` with `WindowStyle 0`
- **Privilege Level**: Standard User (Zero UAC prompts, zero elevation required).
- **Behavior**:
  - When you power on, restart, or log into Windows, Windows Explorer automatically triggers the VBScript.
  - The script launches `python.exe -m aegis.server` completely invisibly in the background.
  - No command prompt or console window will ever appear on your desktop.
  - RAM usage remains under $25\text{ MB}$, and CPU load is 0% when idle.

### Controls:
```powershell
# Enable startup automation
aegis autostart on

# Disable startup automation anytime
aegis autostart off

# Check automation status
aegis autostart status
```

---

## 🐧 Linux Implementation

On Linux distributions, AegisBrain configures a **systemd user service**:
- **Path**: `~/.config/systemd/user/aegis-brain.service`
- **Service Type**: User Unit (`systemctl --user enable --now aegis-brain`)
- **Privilege Level**: User space (No `sudo` needed).
- **Behavior**: Starts automatically on user login and restarts automatically if terminated.

---

## 🍎 macOS Implementation

On macOS, AegisBrain configures a **LaunchAgent**:
- **Path**: `~/Library/LaunchAgents/com.aegis.brain.plist`
- **Privilege Level**: User space (`launchctl load`).
- **Behavior**: Runs headlessly upon login.
