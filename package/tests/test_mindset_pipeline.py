"""Unit and Integration Tests for Aegis Universal Mindset Override & Rollback Pipeline."""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
INSTALL_PS1 = SCRIPTS_DIR / "install.ps1"
RESTORE_PS1 = SCRIPTS_DIR / "restore.ps1"
INSTALL_SH = SCRIPTS_DIR / "install.sh"
RESTORE_SH = SCRIPTS_DIR / "restore.sh"


def test_scripts_exist():
    assert INSTALL_PS1.exists(), f"Missing {INSTALL_PS1}"
    assert RESTORE_PS1.exists(), f"Missing {RESTORE_PS1}"
    assert INSTALL_SH.exists(), f"Missing {INSTALL_SH}"
    assert RESTORE_SH.exists(), f"Missing {RESTORE_SH}"


def test_powershell_mindset_override_and_restore(tmp_path):
    """Test full cycle: pre-existing files + new files -> install.ps1 -> verify -> restore.ps1 -> verify zero residue."""
    mock_home = tmp_path / "mock_user"
    mock_home.mkdir(parents=True, exist_ok=True)

    # 1. Setup pre-existing files
    gemini_dir = mock_home / ".gemini" / "config"
    gemini_dir.mkdir(parents=True, exist_ok=True)
    gemini_md = gemini_dir / "GEMINI.md"
    original_gemini_content = "# Pre-existing Antigravity Directives\n- Rule 1: Always test\n"
    gemini_md.write_text(original_gemini_content, encoding="utf-8")

    claude_dir = mock_home / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    claude_md = claude_dir / "CLAUDE.md"
    original_claude_content = "# Pre-existing Claude Guidelines\n"
    claude_md.write_text(original_claude_content, encoding="utf-8")

    # Workspace
    mock_ws = tmp_path / "mock_workspace"
    mock_ws.mkdir(parents=True, exist_ok=True)
    (mock_ws / ".git").mkdir()

    # Codex and Aider do NOT exist yet before install
    codex_instr = mock_home / ".codex" / "instructions.md"
    aider_conf = mock_home / ".aider.conf.yml"
    aider_conv = mock_home / ".aider" / "conventions.md"
    assert not codex_instr.exists()
    assert not aider_conf.exists()
    assert not aider_conv.exists()

    # 2. Run install.ps1 with isolated USERPROFILE
    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", str(INSTALL_PS1),
        "-Force",
        "-WorkspacePath", str(mock_ws)
    ]
    env = os.environ.copy()
    env["USERPROFILE"] = str(mock_home)
    env["HOME"] = str(mock_home)
    env["CI"] = "1"

    proc = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == 0, f"install.ps1 failed: {proc.stdout}\n{proc.stderr}"
    assert "WARNING: AEGISBRAIN UNIVERSAL AGENT MINDSET OVERRIDE" in proc.stdout
    assert "AegisBrain Universal Mindset Override successfully active!" in proc.stdout

    # 3. Verify Mindset Injections
    # Antigravity GEMINI.md
    assert gemini_md.exists()
    gemini_txt = gemini_md.read_text(encoding="utf-8")
    assert "<!-- AEGIS_BRAIN_MINDSET_START -->" in gemini_txt
    assert "Manager-Worker Hierarchical Workflow" in gemini_txt
    assert "AST Graph Symbol Retrieval" in gemini_txt
    assert "Subagent Token Arbitrage" in gemini_txt
    assert "Andrej Karpathy Simplicity Doctrine" in gemini_txt
    assert original_gemini_content.strip() in gemini_txt

    # Claude Code CLAUDE.md
    assert claude_md.exists()
    claude_txt = claude_md.read_text(encoding="utf-8")
    assert "<!-- AEGIS_BRAIN_MINDSET_START -->" in claude_txt

    # Codex instructions.md (newly created)
    assert codex_instr.exists()
    codex_txt = codex_instr.read_text(encoding="utf-8")
    assert "<!-- AEGIS_BRAIN_MINDSET_START -->" in codex_txt

    # Aider conventions and conf (newly created)
    assert aider_conv.exists()
    assert "<!-- AEGIS_BRAIN_MINDSET_START -->" in aider_conv.read_text(encoding="utf-8")
    assert aider_conf.exists()
    assert "conventions.md" in aider_conf.read_text(encoding="utf-8")

    # Workspace CLAUDE.md and AGENTS.md
    assert (mock_ws / "CLAUDE.md").exists()
    assert (mock_ws / "AGENTS.md").exists()

    # 4. Verify Snapshot was recorded
    snap_dir = mock_home / ".aegis-brain" / "snapshots"
    assert snap_dir.exists()
    latest_file = snap_dir / "LATEST_MINDSET_SNAPSHOT.txt"
    assert latest_file.exists()
    snap_id = latest_file.read_text(encoding="utf-8").strip()
    manifest_file = snap_dir / snap_id / "manifest.json"
    assert manifest_file.exists()
    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert manifest_data["snapshot_id"] == snap_id
    assert len(manifest_data["files"]) >= 2
    assert len(manifest_data["created_files"]) >= 3

    # 5. Run restore.ps1 with isolated USERPROFILE
    restore_cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", str(RESTORE_PS1),
        "-Force"
    ]
    restore_proc = subprocess.run(restore_cmd, env=env, capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert restore_proc.returncode == 0, f"restore.ps1 failed: {restore_proc.stdout}\n{restore_proc.stderr}"
    assert "Mindset override rolled back successfully with ZERO RESIDUE!" in restore_proc.stdout

    # 6. Verify ZERO RESIDUE on restore
    # Pre-existing files must match original content exactly
    restored_gemini = gemini_md.read_text(encoding="utf-8")
    assert restored_gemini == original_gemini_content
    assert "<!-- AEGIS_BRAIN_MINDSET_START -->" not in restored_gemini

    restored_claude = claude_md.read_text(encoding="utf-8")
    assert restored_claude == original_claude_content
    assert "<!-- AEGIS_BRAIN_MINDSET_START -->" not in restored_claude

    # Newly created files must be deleted completely
    assert not codex_instr.exists(), "Codex instructions.md should have been deleted"
    assert not aider_conf.exists(), "Aider conf should have been deleted"
    assert not aider_conv.exists(), "Aider conventions should have been deleted"
    assert not (mock_ws / "CLAUDE.md").exists(), "Workspace CLAUDE.md should have been deleted"
    assert not (mock_ws / "AGENTS.md").exists(), "Workspace AGENTS.md should have been deleted"


def test_bash_mindset_override_and_restore(tmp_path):
    """Test POSIX bash implementation using Git Bash."""
    git_bash = Path(r"C:\Program Files\Git\bin\bash.exe")
    if not git_bash.exists():
        pytest.skip("Git Bash not found on Windows host")

    mock_home = tmp_path / "mock_bash_user"
    mock_home.mkdir(parents=True, exist_ok=True)

    gemini_dir = mock_home / ".gemini" / "config"
    gemini_dir.mkdir(parents=True, exist_ok=True)
    gemini_md = gemini_dir / "GEMINI.md"
    original_gemini = "# Antigravity Bash Baseline\n"
    gemini_md.write_text(original_gemini, encoding="utf-8")

    claude_dir = mock_home / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    claude_md = claude_dir / "CLAUDE.md"
    original_claude = "# Claude Bash Baseline\n"
    claude_md.write_text(original_claude, encoding="utf-8")

    mock_ws = tmp_path / "mock_bash_ws"
    mock_ws.mkdir(parents=True, exist_ok=True)
    (mock_ws / ".git").mkdir()

    env = os.environ.copy()
    env["HOME"] = str(mock_home).replace("\\", "/")
    env["USERPROFILE"] = str(mock_home)
    env["CI"] = "1"

    # Convert paths to cygwin / git bash style if needed or forward slashes
    install_sh_posix = str(INSTALL_SH).replace("\\", "/")
    restore_sh_posix = str(RESTORE_SH).replace("\\", "/")
    ws_posix = str(mock_ws).replace("\\", "/")

    # Run install.sh
    proc = subprocess.run(
        [str(git_bash), install_sh_posix, "-f", "-w", ws_posix],
        env=env,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT)
    )
    assert proc.returncode == 0, f"install.sh failed: {proc.stdout}\n{proc.stderr}"
    assert "WARNING: AEGISBRAIN UNIVERSAL AGENT MINDSET OVERRIDE" in proc.stdout
    assert "AegisBrain Universal Mindset Override successfully active!" in proc.stdout

    # Verify injection
    assert "<!-- AEGIS_BRAIN_MINDSET_START -->" in gemini_md.read_text(encoding="utf-8")
    assert "<!-- AEGIS_BRAIN_MINDSET_START -->" in claude_md.read_text(encoding="utf-8")
    assert (mock_home / ".codex" / "instructions.md").exists()
    assert (mock_home / ".aider" / "conventions.md").exists()
    assert (mock_home / ".aider.conf.yml").exists()

    # Run restore.sh
    restore_proc = subprocess.run(
        [str(git_bash), restore_sh_posix, "-f"],
        env=env,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT)
    )
    assert restore_proc.returncode == 0, f"restore.sh failed: {restore_proc.stdout}\n{restore_proc.stderr}"
    assert "Mindset override rolled back successfully with ZERO RESIDUE!" in restore_proc.stdout

    # Verify zero residue
    assert gemini_md.read_text(encoding="utf-8") == original_gemini
    assert claude_md.read_text(encoding="utf-8") == original_claude
    assert not (mock_home / ".codex" / "instructions.md").exists()
    assert not (mock_home / ".aider" / "conventions.md").exists()
    assert not (mock_home / ".aider.conf.yml").exists()
    assert not (mock_ws / "CLAUDE.md").exists()
    assert not (mock_ws / "AGENTS.md").exists()
