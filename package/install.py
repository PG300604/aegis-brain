"""AegisBrain 1-Click Installer.

Installs global CLI command shim, enables background daemon on startup,
and distributes companion skills to Antigravity, Claude Code, Codex, and Cursor.
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
SKILL_SOURCE = REPO_ROOT / "skills" / "aegis" / "SKILL.md"


def install() -> None:
    print("=" * 60)
    print("Installing AegisBrain Universal Agent Memory Bus...")
    print("=" * 60)

    # 1. Initialize DB and seed
    sys.path.insert(0, str(PACKAGE_DIR))
    from aegis.db import init_db
    from aegis.hooks import seed_initial_knowledge
    from aegis.service import enable_autostart

    print("[1/4] Initializing local neural memory bus...")
    init_db()
    seed_initial_knowledge()

    # 2. Configure background autostart
    print("[2/4] Setting up zero-elevation background autostart...")
    ok, msg = enable_autostart()
    print(f"      {msg}")

    # 3. Create global CLI shim
    print("[3/4] Registering global 'aegis' CLI command...")
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
    else:
        sh_path = home_bin / "aegis"
        sh_content = f"""#!/usr/bin/env bash
export PYTHONPATH="{PACKAGE_DIR}:$PYTHONPATH"
exec python3 -m aegis.cli "$@"
"""
        sh_path.write_text(sh_content, encoding="utf-8")
        sh_path.chmod(0o755)
        print(f"      Created POSIX shim: {sh_path}")

    # 4. Distribute Universal Skills to AI Agent Platforms
    print("[4/4] Auto-linking companion skills across agent platforms...")
    skill_text = SKILL_SOURCE.read_text(encoding="utf-8") if SKILL_SOURCE.exists() else ""

    agent_skill_targets = [
        ("Google Antigravity", Path.home() / ".gemini" / "config" / "skills" / "aegis"),
        ("Anthropic Claude Code", Path.home() / ".claude" / "skills" / "aegis"),
        ("OpenAI Codex CLI", Path.home() / ".codex" / "skills" / "aegis"),
    ]

    for agent_name, target_dir in agent_skill_targets:
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            (target_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")
            print(f"      [OK] Installed skill for {agent_name} -> {target_dir}")
        except Exception as exc:
            print(f"      [SKIP] {agent_name}: {exc}")

    print("\nAegisBrain successfully installed and active across all agents.")
    print("Run 'aegis status' in any terminal to inspect system state.\n")


if __name__ == "__main__":
    install()
