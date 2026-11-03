"""AegisBrain 1-Click Installer.

Installs global CLI command shim and enables background daemon on startup.
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent


def install() -> None:
    print("=" * 50)
    print("🧠 Installing AegisBrain...")
    print("=" * 50)

    # 1. Initialize DB and seed
    sys.path.insert(0, str(PACKAGE_DIR))
    from aegis.db import init_db
    from aegis.hooks import seed_initial_knowledge
    from aegis.service import enable_autostart

    print("[1/3] Initializing local neural memory bus...")
    init_db()
    seed_initial_knowledge()

    # 2. Configure background autostart
    print("[2/3] Setting up zero-elevation background autostart...")
    ok, msg = enable_autostart()
    print(f"      {msg}")

    # 3. Create global CLI shim
    print("[3/3] Registering global 'aegis' CLI command...")
    home_bin = Path.home() / ".local" / "bin"
    home_bin.mkdir(parents=True, exist_ok=True)

    if platform.system() == "Windows":
        cmd_path = home_bin / "aegis.cmd"
        cmd_content = f"""@echo off
set PYTHONPATH={PACKAGE_DIR};%PYTHONPATH%
python -m aegis.cli %*
"""
        cmd_path.write_text(cmd_content, encoding="utf-8")
        print(f"      Created Windows shim: {cmd_path}")
        print("      (Ensure ~/.local/bin is in your PATH)")
    else:
        sh_path = home_bin / "aegis"
        sh_content = f"""#!/usr/bin/env bash
export PYTHONPATH="{PACKAGE_DIR}:$PYTHONPATH"
exec python3 -m aegis.cli "$@"
"""
        sh_path.write_text(sh_content, encoding="utf-8")
        sh_path.chmod(0o755)
        print(f"      Created POSIX shim: {sh_path}")

    print("\n✅ AegisBrain successfully installed and running!")
    print("   Run 'aegis status' in your terminal to inspect status.\n")


if __name__ == "__main__":
    install()
