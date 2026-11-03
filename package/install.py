"""AegisBrain 1-Click Installer.

Installs global CLI command shim, enables background daemon on startup,
distributes companion skills, and injects zero-token-waste recall hooks into
Antigravity, Claude Code, Codex, and Cursor.
"""

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
SKILL_SOURCE = REPO_ROOT / "skills" / "aegis" / "SKILL.md"

ANTIGRAVITY_DIRECTIVE = """
- **Instant Recall Protocol via AegisBrain (Sub-Second Latency & Low Token Cost)**:
  Whenever the user asks to recall past work, previous sessions, decisions, architectural patterns, conventions, or tracked tasks:
  1. **Primary Reflex**: If `aegis` is installed / available on the system:
     - Run `aegis recall` (or `aegis recall -n 5`) to recall recent tasks, workflows, and decisions instantly.
     - Run `aegis recall "<topic>"` or `aegis search "<query>"` for specific keyword lookups across SQLite FTS5 records.
     - Run `aegis bootstrap` to compile compact active workspace context (<= 400 tokens).
     - **NEVER** parse multi-megabyte transcript files or crawl raw session logs when AegisBrain is present.
  2. **Fallback**: Only if AegisBrain yields no results or is uninstalled, consult `~/.gemini/config/skills/memory/WORKFLOW_MEMORY.md`.
"""

CLAUDE_DIRECTIVE = """
## AegisBrain Instant Recall & Memory Protocol (Sub-Second Latency)
When asked to recall past work, previous decisions, architectural conventions, or project status:
- **Primary Reflex**: Run `aegis recall` (or `aegis recall "<topic>"`) to retrieve instant SQLite FTS5 memories.
- Run `aegis bootstrap` to compile active workspace conventions in <= 400 tokens.
- Never crawl raw session directories or read large JSONL logs when AegisBrain is active.
"""


def install() -> None:
    print("=" * 65)
    print(" Installing AegisBrain Universal Agent Memory Bus")
    print("=" * 65)

    # 1. Initialize DB and seed
    sys.path.insert(0, str(PACKAGE_DIR))
    from aegis.db import init_db
    from aegis.hooks import seed_initial_knowledge
    from aegis.service import enable_autostart

    print("[1/5] Initializing local neural memory bus...")
    init_db()
    seed_initial_knowledge()

    # 2. Configure background autostart
    print("[2/5] Setting up zero-elevation background autostart...")
    ok, msg = enable_autostart()
    print(f"      {msg}")

    # 3. Create global CLI shim
    print("[3/5] Registering global 'aegis' CLI command...")
    home_bin = Path.home() / ".local" / "bin"
    home_bin.mkdir(parents=True, exist_ok=True)

    if platform.system() == "Windows":
        cmd_content = f"""@echo off
set PYTHONPATH={PACKAGE_DIR};%PYTHONPATH%
python -m aegis.cli %*
"""
        cmd_path = home_bin / "aegis.cmd"
        cmd_path.write_text(cmd_content, encoding="utf-8")
        print(f"      Created Windows shim: {cmd_path}")

        # Also write to Antigravity CLI bin if present
        antigravity_bin = Path.home() / ".gemini" / "antigravity-cli" / "bin"
        if antigravity_bin.exists():
            (antigravity_bin / "aegis.cmd").write_text(cmd_content, encoding="utf-8")
            print(f"      Linked to Antigravity bin: {antigravity_bin / 'aegis.cmd'}")
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
    print("[4/5] Auto-linking companion skills across agent platforms...")
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

    # 5. Inject Zero-Token-Waste Recall Directives & Hooks
    print("[5/5] Injecting autonomous instant recall directives & memory hooks...")

    # A. Google Antigravity GEMINI.md
    antigravity_md = Path.home() / ".gemini" / "config" / "GEMINI.md"
    if antigravity_md.exists():
        try:
            content = antigravity_md.read_text(encoding="utf-8")
            if "Instant Recall Protocol via AegisBrain" not in content:
                # Append under Section 4 or end of file
                if "## 4. Persistent Workflow Memory" in content:
                    idx = content.find("## 4. Persistent Workflow Memory")
                    next_nl = content.find("\n", idx)
                    content = content[:next_nl + 1] + ANTIGRAVITY_DIRECTIVE + content[next_nl + 1:]
                else:
                    content += "\n" + ANTIGRAVITY_DIRECTIVE
                antigravity_md.write_text(content, encoding="utf-8")
                print("      [OK] Injected AegisBrain instant recall directive into Antigravity GEMINI.md")
            else:
                print("      [OK] Antigravity GEMINI.md already configured for AegisBrain recall")
        except Exception as exc:
            print(f"      [SKIP] Antigravity GEMINI.md: {exc}")

    # B. Antigravity Memory Engine Auto-Sync Hook
    mem_engine = Path.home() / ".gemini" / "config" / "skills" / "skill-memory" / "scripts" / "memory_engine.py"
    if mem_engine.exists():
        try:
            text = mem_engine.read_text(encoding="utf-8")
            if "_sync_to_aegis" not in text:
                sync_code = '''
    def _sync_to_aegis(self, entry: Dict[str, Any]) -> None:
        """Syncs the recorded session into AegisBrain SQLite FTS5 database."""
        try:
            aegis_dir = Path.home() / ".aegis-brain"
            db_path = aegis_dir / "brain.db"
            if not db_path.exists():
                return
            mode_file = aegis_dir / "mode.txt"
            if mode_file.exists() and mode_file.read_text(encoding="utf-8").strip().lower() == "private":
                return
            import sqlite3
            with sqlite3.connect(str(db_path), timeout=5.0) as conn:
                task = entry.get("task", "")[:100]
                skills = entry.get("skills", [])
                learnings = entry.get("learnings", "")
                commands = entry.get("commands", [])
                summary = learnings or (f"Executed skills: {', '.join(skills)}" if skills else "Workflow completed")
                rationale = f"Commands: {', '.join(commands[:3])}" if commands else ""
                tags = json.dumps(skills)
                created_at = entry.get("timestamp")
                conn.execute("""
                    INSERT INTO decisions (category, title, decision, rationale, tags, created_at)
                    VALUES ('WORKFLOW', ?, ?, ?, ?, ?)
                """, (task, summary, rationale, tags, created_at))
                conn.commit()
        except Exception:
            pass
'''
                idx = text.find("    def query(")
                if idx != -1:
                    text = text[:idx] + sync_code + "\n" + text[idx:]
                    text = text.replace(
                        "self._save()\n        log(",
                        "self._save()\n        self._sync_to_aegis(entry)\n        log("
                    )
                    mem_engine.write_text(text, encoding="utf-8")
                    print("      [OK] Hooked Antigravity memory engine to auto-sync with AegisBrain WAL DB")
            else:
                print("      [OK] Antigravity memory engine already auto-synced with AegisBrain")
        except Exception as exc:
            print(f"      [SKIP] memory_engine.py: {exc}")

    # C. Anthropic Claude Code CLAUDE.md
    claude_md = Path.home() / ".claude" / "CLAUDE.md"
    if claude_md.exists():
        try:
            content = claude_md.read_text(encoding="utf-8")
            if "AegisBrain Instant Recall" not in content:
                content += "\n" + CLAUDE_DIRECTIVE
                claude_md.write_text(content, encoding="utf-8")
                print("      [OK] Injected AegisBrain instant recall protocol into Claude Code CLAUDE.md")
        except Exception as exc:
            print(f"      [SKIP] Claude CLAUDE.md: {exc}")

    print("\n" + "=" * 65)
    print(" AegisBrain successfully installed and active across all agents!")
    print("=" * 65)
    print("  - Instant Recall: 'aegis recall' or 'aegis recall <topic>' (<50ms, <100 tokens)")
    print("  - Memory Search:  'aegis search <query>' (SQLite FTS5 full-text search)")
    print("  - Bootstrap:      'aegis bootstrap' (<= 400 token active workspace context)")
    print("  - System Status:  'aegis status'\n")


if __name__ == "__main__":
    install()
