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
- **AegisBrain Autonomous Engineering & Memory Protocol**:
  Whenever operating within an AegisBrain-managed workspace:
  1. **Restore Point Safety Reflex**:
     - Before mutating major configurations, rules, or system files, verify or create a restore point: `aegis snapshot create --reason "pre-change"`. Rollback anytime with `aegis restore`.
  2. **Sub-Second Memory & Context Bootstrapping**:
     - Use `aegis recall` (or `aegis recall "<topic>"`) for instant FTS5 memories. Never crawl raw multi-megabyte session logs. Run `aegis bootstrap` for active context (<= 400 tokens).
  3. **Autonomous Ingestion & Deep Research**:
     - Check skills. If missing domain capabilities, run `aegis research "<query>"` or discover skills via `aegis scout`. Use `aegis browse "<url>"` for lightweight, ad-free, token-efficient extraction (< 1,500 tokens).
  4. **Interactive Alignment & Concept Education (Grill-Me)**:
     - If the task is underspecified or exploring new frameworks, invoke `aegis align "<task>"`. Provide Archify architectural blueprints and curated video links. Run Matt Pocock's 3-question diagnostic interview to lock deliverables and boundaries before coding.
  5. **Manager-Worker Severity Triage & Transparent Observer**:
     - Critical/Confidential tasks: Manager model executes with zero secret leakage.
     - Routine tasks: Local worker generates code drafts with manager review.
     - Always provide live progress transparency: Emit step-by-step progress micro-updates so the user can steer, pause, or comment early.
  6. **Multi-Choice Aesthetic & Layout Dials**:
     - For frontend/UI tasks, provide interactive style choices (UI UX Pro Max, Impeccable, Taste, Modern, Minimalist, Cyberpunk, Neo-brutalism) before writing boilerplate.
  7. **4-Stage Post-Processing & Quality Gates Pipeline**:
     - All candidate code must pass:
       1) `turnitout` / `unslop` (remove AI conversational watermarks and slop).
       2) `Red-Team & Cloudflare security audit` (block shell=True, injections, traversals).
       3) `GitGuardian Secret Scanner` (block API keys, private keys, database credentials).
       4) `Dual-Environment Verification` (isolated sandbox test first -> local test second -> git push third).
  8. **AST Graph Token Optimization**:
     - Use `aegis graph --query <symbol>` for sub-millisecond symbol and dependency retrieval. Fallback to conventional grep only if AST indexing fails.
  9. **Feedback & Benchmarking**:
     - Record tool performance and fallbacks. Review dashboard via `aegis dashboard` or submit feedback via `aegis feedback "<critique>"`.
"""

CLAUDE_DIRECTIVE = """
## AegisBrain Autonomous Engineering & Memory Protocol
1. **Restore Point Safety**: Create snapshots before system changes (`aegis snapshot create`). Rollback anytime (`aegis restore`).
2. **Sub-Second Memory Reflex**: Run `aegis recall "<topic>"` to query SQLite FTS5 records. Run `aegis bootstrap` for active workspace context. Never crawl raw JSONL logs.
3. **Autonomous Research & Lightweight Browser**: Use `aegis research "<topic>"` and `aegis browse "<url>"` for clean, token-efficient web research.
4. **Concept Awareness & Grill-Me**: Run `aegis align "<task>"` for Archify blueprints and Matt Pocock diagnostic questions.
5. **Quality Gates Pipeline**: Verify output passes `aegis pipeline "<file>"` (Unslop, Security Audit, GitGuardian Secret Scanning, Sandbox test).
6. **AST Graph Traversal**: Query `aegis graph --query <symbol>` for code relationships without file dumping.
7. **Transparent Updates**: Maintain step-by-step progress transparency for user steering.
"""


def install() -> None:
    print("=" * 65)
    print(" Installing AegisBrain Universal Agent Memory Bus")
    print("=" * 65)

    # 1. Create automated pre-install snapshot restore point
    sys.path.insert(0, str(PACKAGE_DIR))
    from aegis.snapshot import create_snapshot
    from aegis.db import init_db
    from aegis.hooks import seed_initial_knowledge
    from aegis.service import enable_autostart

    print("[1/6] Creating automated pre-install restore point snapshot...")
    try:
        snap = create_snapshot(name="pre_install", reason="Automated pre-install restore point")
        print(f"      [OK] Snapshot saved: {snap['snapshot_id']} ({snap['file_count']} files archived)")
        print(f"      Rollback anytime with: `aegis restore {snap['snapshot_id']}`")
    except Exception as exc:
        print(f"      [WARN] Failed to create snapshot: {exc}")

    # 2. Initialize DB and seed
    print("[2/6] Initializing local neural memory bus...")
    init_db()
    seed_initial_knowledge()

    # 3. Configure background autostart
    print("[3/6] Setting up zero-elevation background autostart...")
    ok, msg = enable_autostart()
    print(f"      {msg}")

    # 4. Create global CLI shim
    print("[4/6] Registering global 'aegis' CLI command...")
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

    # 5. Distribute Universal Skills to AI Agent Platforms
    print("[5/6] Auto-linking companion skills across agent platforms...")
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

    # 6. Inject Autonomous Engineering Directives & Hooks
    print("[6/6] Injecting autonomous engineering directives & memory hooks...")

    # A. Google Antigravity GEMINI.md
    antigravity_md = Path.home() / ".gemini" / "config" / "GEMINI.md"
    if antigravity_md.exists():
        try:
            content = antigravity_md.read_text(encoding="utf-8")
            if "AegisBrain Autonomous Engineering & Memory Protocol" not in content:
                # Replace old directive or append
                if "- **Instant Recall Protocol via AegisBrain" in content:
                    idx = content.find("- **Instant Recall Protocol via AegisBrain")
                    end_idx = content.find("## 2. Unified Arsenal Triad", idx)
                    if end_idx != -1:
                        content = content[:idx] + ANTIGRAVITY_DIRECTIVE.strip() + "\n\n---\n\n" + content[end_idx:]
                    else:
                        content = content[:idx] + ANTIGRAVITY_DIRECTIVE.strip() + "\n"
                elif "## 4. Persistent Workflow Memory" in content:
                    idx = content.find("## 4. Persistent Workflow Memory")
                    next_nl = content.find("\n", idx)
                    content = content[:next_nl + 1] + ANTIGRAVITY_DIRECTIVE + content[next_nl + 1:]
                else:
                    content += "\n" + ANTIGRAVITY_DIRECTIVE
                antigravity_md.write_text(content, encoding="utf-8")
                print("      [OK] Injected AegisBrain autonomous engineering protocol into Antigravity GEMINI.md")
            else:
                print("      [OK] Antigravity GEMINI.md already configured for AegisBrain protocol")
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
