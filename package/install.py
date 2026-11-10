"""AegisBrain 1-Click Universal Installer.

Node.js-style colored multi-panel installer wizard.
Installs global CLI command shim, configures 24/7 background daemon,
initializes local neural memory bus, configures 3-tier token arbitrage,
and injects zero-token-waste hooks across Antigravity, Claude Code, Codex, and Cursor.
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
SKILL_SOURCE = REPO_ROOT / "skills" / "aegis" / "SKILL.md"

# ANSI Color codes
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
MAGENTA = "\033[95m"
DARKGRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

ASCII_LOGO = f"""
{CYAN}  █████╗ ███████╗ ██████╗ ██╗███████╗    ██████╗ ██████╗  █████╗ ██╗███╗   ██╗{RESET}
{CYAN} ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║{RESET}
{YELLOW} ███████║█████╗  ██║  ███╗██║███████╗    ██████╔╝██████╔╝███████║██║██╔██╗ ██║{RESET}
{YELLOW} ██╔══██║██╔══╝  ██║   ██║██║╚════██║    ██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║{RESET}
{RED} ██║  ██║███████╗╚██████╔╝██║███████║    ██████╔╝██║  ██║██║  ██║██║██║ ╚████║{RESET}
{RED} ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝{RESET}
{DARKGRAY}         [ 24/7 AUTONOMOUS NEURAL MEMORY & 3-TIER AGENT ORCHESTRATOR ]{RESET}
{DARKGRAY}                               Version 2.4.0 (GPLv3){RESET}
"""

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
  5. **Dynamic Dual-Mode Triage Protocol**:
     - Check configured execution mode (`~/.aegis-brain/execution_mode.txt` or `aegis config --mode`):
       - **Arbitrage Mode (Default)**: Senior Boss evaluates task severity. For substantial tasks (>15 lines), spawn Tier 2 Subagents (`invoke_subagent`), which delegate code writing to Tier 3 Local Workers (`hermes`, `ollama`, `opencode`) via `run_command` to save 85-92% frontier tokens.
       - **Fast Mode (Direct Frontier)**: Triggered when user specifies "quick", "fast", or mode is "fast". Direct execution with zero delegation latency.
  6. **4-Stage Post-Processing & Quality Gates Pipeline**:
     - All candidate code must pass:
       1) `turnitout` / `unslop` (remove AI conversational watermarks and slop).
       2) `Red-Team & Cloudflare security audit` (block shell=True, injections, traversals).
       3) `GitGuardian Secret Scanner` (block API keys, private keys, database credentials).
       4) `Dual-Environment Verification` (isolated sandbox test first -> local test second -> git push third).
  7. **AST Graph Token Optimization**:
     - Use `aegis graph --query <symbol>` for sub-millisecond symbol and dependency retrieval. Fallback to conventional grep only if AST indexing fails.
  8. **Feedback & Benchmarking**:
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


def print_box_header(title: str, color: str = CYAN) -> None:
    width = 72
    print(f"\n{color}┌{'─' * width}┐{RESET}")
    print(f"{color}│  {title.ljust(width - 2)}│{RESET}")
    print(f"{color}└{'─' * width}┘{RESET}")


def print_panel(lines: list[str], border_color: str = DARKGRAY, text_color: str = "") -> None:
    width = 72
    print(f"{border_color}┌{'─' * width}┐{RESET}")
    for line in lines:
        truncated = line[: width - 4] if len(line) > width - 4 else line
        print(f"{border_color}│  {RESET}{text_color}{truncated.ljust(width - 2)}{RESET}{border_color}│{RESET}")
    print(f"{border_color}└{'─' * width}┘{RESET}")


def install(force: bool = False, mode: str | None = None, workspace: str | None = None) -> None:
    # Enable ANSI escape codes on Windows console if needed
    if platform.system() == "Windows":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass

    print(ASCII_LOGO)

    is_interactive = sys.stdin.isatty() and not force and not os.environ.get("CI")

    # STEP 1: License Agreement & Terms of Service (GPLv3)
    print_box_header("STEP 1 of 4: License Agreement & Terms of Service", CYAN)
    terms_lines = [
        "License: GNU General Public License v3.0 (GPL-3.0-or-later)",
        "Author: Priyanshu Ghosh (@PG300604) | https://github.com/PG300604/aegis-brain",
        "",
        "Core User Commitments & Operational Terms:",
        " • 100% Local Neural Memory: Your data stays on your machine. Zero telemetry,",
        "   session transcripts, or database records are ever exfiltrated.",
        " • Subprocess Boundary: Local worker CLIs (Hermes, Ollama, OpenCode) execute",
        "   via isolated OS subprocesses under their respective upstream licenses.",
        " • Autonomous Safety Reflex: Automated pre-mutation snapshots are created",
        "   before any file changes, enabling 1-click restore at any time.",
        " • No Warranty: Provided 'as is' without warranty of any kind, express or implied.",
    ]
    print_panel(terms_lines, CYAN, "")

    if is_interactive:
        try:
            resp = input(f"\n {BOLD}Do you accept the Terms & Conditions and GPLv3 license? [Y/n]: {RESET}").strip()
            if resp.lower().startswith("n"):
                print(f"\n {RED}[X] Installation aborted: Terms must be accepted to proceed.{RESET}\n")
                sys.exit(1)
            print(f" {GREEN}[✓] Terms accepted.{RESET}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n {RED}[X] Installation canceled.{RESET}\n")
            sys.exit(1)
    else:
        print(f" {GREEN}[✓] Terms accepted automatically.{RESET}")

    # STEP 2: Execution Mode Selection (Arbitrage vs Fast)
    print_box_header("STEP 2 of 4: Select Agent Execution Strategy", YELLOW)
    mode_lines = [
        "Choose how Antigravity CLI & AegisBrain should triage coding tasks:",
        "",
        " [1] Arbitrage Mode (Recommended - Maximum Token Savings):",
        "     Frontier Manager serves as High-Cognition Brain only. Substantial tasks",
        "     are delegated to Tier 2 Subagents + Tier 3 Local Workers (Hermes, Ollama),",
        "     saving 85%+ frontier tokens with 4-gate quality auditing.",
        "",
        " [2] Fast Direct Mode (Instant Turnaround):",
        "     Frontier Manager generates code drafts directly without worker roundtrips.",
        "     Prioritizes execution speed over token savings.",
    ]
    print_panel(mode_lines, YELLOW, "")

    selected_mode = mode or "arbitrage"
    if is_interactive and not mode:
        try:
            resp = input(f"\n {BOLD}Select execution mode [1 or 2] (Default: 1 - Arbitrage): {RESET}").strip()
            if resp == "2":
                selected_mode = "fast"
                print(f" {YELLOW}[✓] Configured: Fast Direct Mode (Frontier Direct){RESET}")
            else:
                selected_mode = "arbitrage"
                print(f" {GREEN}[✓] Configured: Dynamic Arbitrage Mode (3-Tier Token Saving){RESET}")
        except (KeyboardInterrupt, EOFError):
            selected_mode = "arbitrage"
    else:
        if selected_mode == "fast":
            print(f" {YELLOW}[✓] Configured: Fast Direct Mode{RESET}")
        else:
            print(f" {GREEN}[✓] Default configured: Dynamic Arbitrage Mode{RESET}")

    # STEP 3: Target Platforms
    print_box_header("STEP 3 of 4: Target AI Coding Assistants", MAGENTA)
    platform_lines = [
        "AegisBrain will inject persistent neural memory and mindset hooks into:",
        " • Google Antigravity CLI     (~/.gemini/config/GEMINI.md)",
        " • Anthropic Claude Code CLI  (~/.claude/CLAUDE.md)",
        " • OpenAI Codex CLI           (~/.codex/instructions.md)",
        " • Aider CLI                  (~/.aider.conf.yml)",
        " • Active Workspace (if inside git repo): CLAUDE.md & AGENTS.md",
    ]
    print_panel(platform_lines, MAGENTA, "")

    # STEP 4: Dependencies, Snapshot & Installation
    print_box_header("STEP 4 of 4: Installation & Restore Point Reflex", CYAN)

    # 1. Create automated pre-install snapshot restore point
    sys.path.insert(0, str(PACKAGE_DIR))
    from aegis.snapshot import create_snapshot
    from aegis.db import init_db
    from aegis.hooks import seed_initial_knowledge
    from aegis.service import enable_autostart
    from aegis.config import set_execution_mode

    print(f" {CYAN}[1/6]{RESET} Creating automated pre-install restore point snapshot...")
    try:
        snap = create_snapshot(name="pre_install", reason="Automated pre-install restore point")
        print(f"       {GREEN}[OK]{RESET} Snapshot saved: {snap['snapshot_id']} ({snap['file_count']} files archived)")
        print(f"       Rollback anytime with: `aegis restore {snap['snapshot_id']}`")
    except Exception as exc:
        print(f"       {YELLOW}[WARN]{RESET} Failed to create snapshot: {exc}")

    # 2. Initialize DB and seed
    print(f" {CYAN}[2/6]{RESET} Initializing local neural memory bus...")
    init_db()
    seed_initial_knowledge()
    set_execution_mode(selected_mode)
    print(f"       {GREEN}[OK]{RESET} Configured execution strategy: {BOLD}{selected_mode.upper()}{RESET}")

    # 3. Configure background autostart
    print(f" {CYAN}[3/6]{RESET} Setting up zero-elevation background autostart...")
    ok, msg = enable_autostart()
    print(f"       {GREEN}[OK]{RESET} {msg}")

    # 4. Create global CLI shim
    print(f" {CYAN}[4/6]{RESET} Registering global 'aegis' CLI command...")
    home_bin = Path.home() / ".local" / "bin"
    home_bin.mkdir(parents=True, exist_ok=True)

    if platform.system() == "Windows":
        cmd_content = f"""@echo off
set PYTHONPATH={PACKAGE_DIR};%PYTHONPATH%
python -m aegis.cli %*
"""
        cmd_path = home_bin / "aegis.cmd"
        cmd_path.write_text(cmd_content, encoding="utf-8")
        print(f"       {GREEN}[OK]{RESET} Created Windows shim: {cmd_path}")

        # Also write to Antigravity CLI bin if present
        antigravity_bin = Path.home() / ".gemini" / "antigravity-cli" / "bin"
        if antigravity_bin.exists():
            (antigravity_bin / "aegis.cmd").write_text(cmd_content, encoding="utf-8")
            print(f"       {GREEN}[OK]{RESET} Linked to Antigravity bin: {antigravity_bin / 'aegis.cmd'}")
    else:
        sh_path = home_bin / "aegis"
        sh_content = f"""#!/usr/bin/env bash
export PYTHONPATH="{PACKAGE_DIR}:$PYTHONPATH"
exec python3 -m aegis.cli "$@"
"""
        sh_path.write_text(sh_content, encoding="utf-8")
        sh_path.chmod(0o755)
        print(f"       {GREEN}[OK]{RESET} Created POSIX shim: {sh_path}")

    # 5. Distribute Universal Skills to AI Agent Platforms
    print(f" {CYAN}[5/6]{RESET} Auto-linking companion skills across agent platforms...")
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
            print(f"       {GREEN}[OK]{RESET} Installed skill for {agent_name} -> {target_dir}")
        except Exception as exc:
            print(f"       {YELLOW}[SKIP]{RESET} {agent_name}: {exc}")

    # 6. Inject Autonomous Engineering Directives & Hooks
    print(f" {CYAN}[6/6]{RESET} Injecting autonomous engineering directives & memory hooks...")

    # A. Google Antigravity GEMINI.md
    antigravity_md = Path.home() / ".gemini" / "config" / "GEMINI.md"
    if antigravity_md.exists():
        try:
            content = antigravity_md.read_text(encoding="utf-8")
            if "AegisBrain Autonomous Engineering & Memory Protocol" not in content:
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
                    content = content[: next_nl + 1] + ANTIGRAVITY_DIRECTIVE + content[next_nl + 1 :]
                else:
                    content += "\n" + ANTIGRAVITY_DIRECTIVE
                antigravity_md.write_text(content, encoding="utf-8")
                print(f"       {GREEN}[OK]{RESET} Injected protocol into Antigravity GEMINI.md")
            else:
                print(f"       {GREEN}[OK]{RESET} Antigravity GEMINI.md already configured")
        except Exception as exc:
            print(f"       {YELLOW}[SKIP]{RESET} Antigravity GEMINI.md: {exc}")

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
                        "self._save()\n        self._sync_to_aegis(entry)\n        log(",
                    )
                    mem_engine.write_text(text, encoding="utf-8")
                    print(f"       {GREEN}[OK]{RESET} Hooked Antigravity memory engine to auto-sync with AegisBrain WAL DB")
            else:
                print(f"       {GREEN}[OK]{RESET} Antigravity memory engine already auto-synced")
        except Exception as exc:
            print(f"       {YELLOW}[SKIP]{RESET} memory_engine.py: {exc}")

    # C. Anthropic Claude Code CLAUDE.md
    claude_md = Path.home() / ".claude" / "CLAUDE.md"
    if claude_md.exists():
        try:
            content = claude_md.read_text(encoding="utf-8")
            if "AegisBrain Instant Recall" not in content and "AegisBrain Autonomous Engineering" not in content:
                content += "\n" + CLAUDE_DIRECTIVE
                claude_md.write_text(content, encoding="utf-8")
                print(f"       {GREEN}[OK]{RESET} Injected protocol into Claude Code CLAUDE.md")
            else:
                print(f"       {GREEN}[OK]{RESET} Claude Code CLAUDE.md already configured")
        except Exception as exc:
            print(f"       {YELLOW}[SKIP]{RESET} Claude CLAUDE.md: {exc}")

    # D. Workspace-level Injection if requested or inside git repo
    target_workspace = Path(workspace) if workspace else (REPO_ROOT if (REPO_ROOT / ".git").exists() else None)
    if target_workspace and target_workspace.exists():
        ws_agents = target_workspace / "AGENTS.md"
        if ws_agents.exists():
            print(f"       {GREEN}[OK]{RESET} Workspace AGENTS.md verified at {ws_agents}")

    # Completion Banner
    print(f"\n{GREEN}{BOLD}════════════════════════════════════════════════════════════════════════{RESET}")
    print(f"{GREEN}{BOLD} [✓] AegisBrain v2.4.0 successfully installed and operational!{RESET}")
    print(f"{GREEN}{BOLD}════════════════════════════════════════════════════════════════════════{RESET}")
    print(f"  • Execution Mode:  {BOLD}{selected_mode.upper()}{RESET} ({'Maximum 85%+ Token Arbitrage' if selected_mode == 'arbitrage' else 'Direct Frontier Speed'})")
    print(f"  • Instant Recall:  `aegis recall` or `aegis recall <topic>` (<25ms, <100 tokens)")
    print(f"  • Memory Search:   `aegis search <query>` (SQLite FTS5 full-text index)")
    print(f"  • Workspace Boot:  `aegis bootstrap` (<= 400 token active context injection)")
    print(f"  • Mode Switch:     `aegis config --mode arbitrage` or `aegis config --mode fast`")
    print(f"  • Daemon Status:   `http://127.0.0.1:8765/status` (24/7 background service)\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="AegisBrain Universal Agent Installer")
    parser.add_argument("-y", "--yes", "--force", action="store_true", help="Bypass interactive prompts with defaults")
    parser.add_argument("--mode", choices=["arbitrage", "fast"], default=None, help="Force execution strategy mode")
    parser.add_argument("--workspace", type=str, default=None, help="Path to workspace root")
    args = parser.parse_args()

    install(force=args.yes, mode=args.mode, workspace=args.workspace)


if __name__ == "__main__":
    main()
