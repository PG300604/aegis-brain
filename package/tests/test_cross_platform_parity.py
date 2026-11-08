"""Cross-Platform Parity & Universal Agent Interchangeability Test Suite.

Verifies:
1. Path normalization across Windows, macOS, and Linux.
2. Shell script generation & executable resolution across OSes.
3. CaffeinateEngine & power management fallback across macOS, Linux, and Windows.
4. Universal agent combinations (OpenCode Boss + Codex Worker, Codex Boss + OpenCode Worker,
   Antigravity Boss + Hermes Worker, Claude Boss + Ollama Worker) returning UniversalAgentEnvelope.
5. Dynamic `hermes fallback list` and `opencode models` CLI discovery and free model tagging.
"""

import json
import os
import sys
import unittest
from pathlib import Path, PurePosixPath, PureWindowsPath
from unittest.mock import MagicMock, patch

from aegis.agent_adapters import (
    AgentDescriptor,
    AgentExecutionResponse,
    AgentRole,
    UniversalAgentEnvelope,
    dispatch_universal_task,
)
from aegis.caffeinate import CaffeinateEngine
from aegis.environment import detect_host_platform
from aegis.hierarchy import HierarchicalAgentOrchestrator, WorkerType
from aegis.orchestrator import (
    find_claude_executable,
    find_codex_executable,
    find_gemini_executable,
    find_hermes_executable,
    find_opencode_executable,
)
from aegis.service import _enable_linux, _enable_macos, _enable_windows
from aegis.workers import (
    detect_hermes_fallbacks,
    detect_opencode_models,
    is_free_model,
)


class TestCrossPlatformParity(unittest.TestCase):
    """Parity tests ensuring AegisBrain behaves identically across Windows, macOS, and Linux."""

    # =========================================================================
    # 1. Path Normalization Parity
    # =========================================================================

    def test_path_normalization_slashes_and_drives(self):
        """Verify seamless path normalization between POSIX forward slashes and Windows backslashes."""
        win_str = r"P:\open-source\aegis-brain\package\aegis\db.py"
        posix_str = "P:/open-source/aegis-brain/package/aegis/db.py"

        # Conversion to PureWindowsPath / as_posix
        p_from_win = PureWindowsPath(win_str).as_posix()
        p_from_posix = Path(posix_str).as_posix()
        self.assertEqual(p_from_win, p_from_posix)
        self.assertEqual(p_from_win, "P:/open-source/aegis-brain/package/aegis/db.py")

        # Roundtrip via Path handles both separators interchangeably
        self.assertEqual(PureWindowsPath(win_str).name, "db.py")
        self.assertEqual(Path(posix_str).name, "db.py")
        self.assertEqual(PureWindowsPath(win_str).suffix, ".py")
        self.assertEqual(Path(posix_str).suffix, ".py")

    def test_config_paths_cross_platform_resolution(self, monkeypatch=None):
        """Verify configuration paths resolve cleanly without hardcoded OS assumptions."""
        from aegis.config import get_aegis_dir, get_db_path, get_model_dir

        aegis_dir = get_aegis_dir()
        db_path = get_db_path()
        model_dir = get_model_dir()

        self.assertTrue(str(db_path).startswith(str(aegis_dir)))
        self.assertEqual(db_path.name, "brain.db")
        self.assertTrue(isinstance(model_dir, Path))

    # =========================================================================
    # 2. Shell Script Generation & Executable Resolution
    # =========================================================================

    def test_shell_script_generation_windows(self, tmp_path_factory=None):
        """Verify Windows autostart generates clean VBScript with pythonw.exe and zero console window."""
        import tempfile
        fake_vbs = Path(tempfile.gettempdir()) / "test_aegis_startup.vbs"
        with patch("aegis.service._get_windows_startup_vbs", return_value=fake_vbs), \
             patch("aegis.service._get_python_runner", return_value=Path("C:/Python312/python.exe")):
            try:
                ok, msg = _enable_windows()
                self.assertTrue(ok)
                self.assertIn("Windows autostart enabled", msg)
                self.assertTrue(fake_vbs.exists())
                content = fake_vbs.read_text(encoding="utf-8")
                self.assertIn("WScript.Shell", content)
                self.assertIn("-m aegis.server", content)
                self.assertIn(", 0, False", content)
            finally:
                if fake_vbs.exists():
                    fake_vbs.unlink()

    def test_shell_script_generation_linux(self):
        """Verify Linux autostart generates valid systemd user service unit file."""
        import tempfile
        fake_unit = Path(tempfile.gettempdir()) / "test_aegis.service"
        with patch("aegis.service._get_linux_systemd_file", return_value=fake_unit), \
             patch("shutil.which", return_value="/bin/systemctl"), \
             patch("subprocess.run"):
            try:
                ok, msg = _enable_linux()
                self.assertTrue(ok)
                self.assertIn("Linux systemd autostart enabled", msg)
                self.assertTrue(fake_unit.exists())
                content = fake_unit.read_text(encoding="utf-8")
                self.assertIn("[Unit]", content)
                self.assertIn("[Service]", content)
                self.assertIn("ExecStart=", content)
                self.assertIn("-m aegis.server", content)
                self.assertIn("[Install]", content)
            finally:
                if fake_unit.exists():
                    fake_unit.unlink()

    def test_shell_script_generation_macos(self):
        """Verify macOS autostart generates valid LaunchAgent plist file."""
        import tempfile
        fake_plist = Path(tempfile.gettempdir()) / "test_com.aegis.brain.plist"
        with patch("aegis.service._get_macos_launch_agent_file", return_value=fake_plist), \
             patch("shutil.which", return_value="/bin/launchctl"), \
             patch("subprocess.run"):
            try:
                ok, msg = _enable_macos()
                self.assertTrue(ok)
                self.assertIn("macOS autostart enabled", msg)
                self.assertTrue(fake_plist.exists())
                content = fake_plist.read_text(encoding="utf-8")
                self.assertIn("<!DOCTYPE plist", content)
                self.assertIn("<key>Label</key>", content)
                self.assertIn("com.aegis.brain", content)
                self.assertIn("<key>RunAtLoad</key>", content)
            finally:
                if fake_plist.exists():
                    fake_plist.unlink()

    def test_detect_host_platform_across_os(self):
        """Verify detect_host_platform correctly classifies Windows, macOS, and Linux."""
        with patch("sys.platform", "win32"), \
             patch("os.environ", {"PSModulePath": "C:\\PS"}), \
             patch("shutil.which", return_value=None):
            p = detect_host_platform()
            self.assertEqual(p["os"], "windows")
            self.assertEqual(p["shell"], "powershell")

        with patch("sys.platform", "darwin"), \
             patch("os.environ", {"SHELL": "/bin/zsh"}), \
             patch("shutil.which", return_value=None):
            p = detect_host_platform()
            self.assertEqual(p["os"], "macos")
            self.assertEqual(p["shell"], "zsh")

        with patch("sys.platform", "linux"), \
             patch("os.environ", {"SHELL": "/bin/bash"}), \
             patch("shutil.which", return_value=None):
            p = detect_host_platform()
            self.assertEqual(p["os"], "linux")
            self.assertEqual(p["shell"], "bash")

    def test_executable_resolution_across_os(self):
        """Verify worker executable finders resolve executables cleanly."""
        with patch("shutil.which", side_effect=lambda x: f"/usr/local/bin/{x}"):
            self.assertIn("hermes", str(find_hermes_executable()))
            self.assertIn("opencode", str(find_opencode_executable()))
            self.assertIn("claude", str(find_claude_executable()))
            self.assertIn("codex", str(find_codex_executable()))
            self.assertIn("gemini", str(find_gemini_executable()))

    # =========================================================================
    # 3. Caffeinate / Power Management Fallback Parity
    # =========================================================================

    def test_caffeinate_windows_lifecycle(self):
        """Verify CaffeinateEngine on Windows uses SetThreadExecutionState."""
        engine = CaffeinateEngine()
        engine._platform = "win32"

        mock_kernel32 = MagicMock()
        mock_ctypes = MagicMock()
        mock_ctypes.windll.kernel32 = mock_kernel32

        with patch.dict("sys.modules", {"ctypes": mock_ctypes}):
            # Enable with away_mode=True
            ok, msg = engine.enable(keep_display=True, away_mode=True)
            self.assertTrue(ok)
            self.assertIn("Windows", msg)
            self.assertTrue(engine._active)

            # Disable
            ok_d, msg_d = engine.disable()
            self.assertTrue(ok_d)
            self.assertFalse(engine._active)

    def test_caffeinate_macos_lifecycle(self):
        """Verify CaffeinateEngine on macOS spawns caffeinate process."""
        engine = CaffeinateEngine()
        engine._platform = "darwin"

        mock_proc = MagicMock()
        mock_proc.pid = 4242

        with patch("subprocess.Popen", return_value=mock_proc):
            ok, msg = engine.enable(keep_display=True)
            self.assertTrue(ok)
            self.assertIn("macOS", msg)
            self.assertIn("4242", msg)
            self.assertTrue(engine._active)

            ok_d, msg_d = engine.disable()
            self.assertTrue(ok_d)
            self.assertFalse(engine._active)
            mock_proc.terminate.assert_called_once()

    def test_caffeinate_linux_lifecycle(self):
        """Verify CaffeinateEngine on Linux uses systemd-inhibit or software fallback."""
        engine = CaffeinateEngine()
        engine._platform = "linux"

        mock_proc = MagicMock()
        mock_proc.pid = 9999

        # Case A: systemd-inhibit available
        with patch("subprocess.Popen", return_value=mock_proc):
            ok, msg = engine.enable()
            self.assertTrue(ok)
            self.assertIn("Linux", msg)
            self.assertTrue(engine._active)
            engine.disable()

        # Case B: systemd-inhibit raises Exception -> software keep-alive
        with patch("subprocess.Popen", side_effect=FileNotFoundError("No systemd-inhibit")):
            ok, msg = engine.enable()
            self.assertTrue(ok)
            self.assertIn("software keep-alive", msg)
            self.assertTrue(engine._active)
            engine.disable()

    # =========================================================================
    # 4. Universal Agent Interchangeability Parity
    # =========================================================================

    def test_universal_agent_opencode_boss_codex_worker(self):
        """Test combination: OpenCode Boss (Tier 1) + Codex Worker (Tier 3)."""
        envelope = dispatch_universal_task(
            task="Write binary search",
            boss_name="opencode",
            boss_model="claude-opus-5-5",
            worker_name="codex",
            worker_model="gpt-6-astra",
            simulate=True,
        )
        self.assertIsInstance(envelope, UniversalAgentEnvelope)
        self.assertEqual(envelope.boss_name, "opencode")
        self.assertEqual(envelope.boss_model, "claude-opus-5-5")
        self.assertEqual(envelope.worker_name, "codex")
        self.assertEqual(envelope.worker_model, "gpt-6-astra")
        self.assertTrue(envelope.quality_gate_passed)
        self.assertTrue(envelope.gate_scores["karpathy_simplicity"])
        self.assertTrue(envelope.gate_scores["unslop_turnitout"])
        self.assertTrue(envelope.gate_scores["security_redteam"])
        self.assertTrue(envelope.gate_scores["dual_env_verification"])
        self.assertIn("Opencode (claude-opus-5-5)", envelope.executive_deliverable)
        self.assertIn("Codex (gpt-6-astra)", envelope.executive_deliverable)

        # JSON Envelope round-trip
        data = json.loads(envelope.to_json())
        self.assertEqual(data["boss_name"], "opencode")
        self.assertEqual(data["worker_name"], "codex")
        self.assertEqual(data["status"], "passed")

    def test_universal_agent_codex_boss_opencode_worker(self):
        """Test combination: Codex Boss (Tier 1) + OpenCode Worker (Tier 3)."""
        envelope = dispatch_universal_task(
            task="Refactor LRU Cache",
            boss_name="codex",
            boss_model="gpt-6-astra",
            worker_name="opencode",
            worker_model="deepseek-v4.1-flash-free",
            simulate=True,
        )
        self.assertEqual(envelope.boss_name, "codex")
        self.assertEqual(envelope.worker_name, "opencode")
        self.assertTrue(envelope.quality_gate_passed)
        self.assertEqual(envelope.status, "passed")
        self.assertIn("Codex (gpt-6-astra)", envelope.executive_deliverable)
        self.assertIn("Opencode (deepseek-v4.1-flash-free)", envelope.executive_deliverable)

    def test_universal_agent_antigravity_boss_hermes_worker(self):
        """Test combination: Antigravity Boss (Tier 1) + Hermes Worker (Tier 3)."""
        envelope = dispatch_universal_task(
            task="Implement Async Rate Limiter",
            boss_name="antigravity",
            boss_model="gemini-3.8-flash",
            worker_name="hermes",
            worker_model="nvidia/nemotron-3.5-bolt-e4b",
            simulate=True,
        )
        self.assertEqual(envelope.boss_name, "antigravity")
        self.assertEqual(envelope.worker_name, "hermes")
        self.assertTrue(envelope.quality_gate_passed)
        self.assertGreater(envelope.tokens_saved, 0)
        self.assertIn("Antigravity (gemini-3.8-flash)", envelope.executive_deliverable)

    def test_universal_agent_claude_boss_ollama_worker(self):
        """Test combination: Claude Boss (Tier 1) + Ollama Worker (Tier 3)."""
        envelope = dispatch_universal_task(
            task="Parse YAML stream cleanly",
            boss_name="claude",
            boss_model="claude-3-7-sonnet",
            worker_name="ollama",
            worker_model="qwen2.5-coder:7b",
            simulate=True,
        )
        self.assertEqual(envelope.boss_name, "claude")
        self.assertEqual(envelope.worker_name, "ollama")
        self.assertTrue(envelope.quality_gate_passed)
        self.assertIn("Claude (claude-3-7-sonnet)", envelope.executive_deliverable)

    def test_hierarchical_orchestrator_custom_boss_and_workers(self):
        """Verify HierarchicalAgentOrchestrator accepts arbitrary boss and worker setups."""
        orch = HierarchicalAgentOrchestrator(
            main_engine_name="Codex Top Boss",
            boss_model="gpt-6-astra",
            default_workers=[WorkerType.OPENCODE, WorkerType.HERMES],
        )
        self.assertEqual(orch.boss_name, "Codex Top Boss")
        self.assertEqual(orch.boss_model, "gpt-6-astra")

        nodes = orch.plan_hierarchy("Multi-service pipeline")
        self.assertGreaterEqual(len(nodes), 1)
        self.assertIn("Codex Top Boss", nodes[0].name)
        self.assertEqual(nodes[0].allowed_workers, [WorkerType.OPENCODE, WorkerType.HERMES])

        report = orch.format_hierarchy_report("Multi-service pipeline")
        self.assertIn("Codex Top Boss (gpt-6-astra)", report)

    # =========================================================================
    # 5. CLI Model Discovery & Free-Model Tagging
    # =========================================================================

    def test_hermes_cli_discovery(self):
        """Verify hermes fallback list output parsing via mock CLI."""
        cli_out = """
  Primary:   nvidia/nemotron-3.5-bolt-e4b  (via nvidia)

  Fallback chain (4 entries):
    1. thinkingmachines/inkling:free  (via nvidia)  [https://openrouter.ai/api/v1]
    2. cohere/north-mini-code:free  (via nvidia)  [https://openrouter.ai/api/v1]
    3. google/gemma4-31b-it:free  (via nvidia)  [https://openrouter.ai/api/v1]
    4. openrouter/free  (via nvidia)  [https://openrouter.ai/api/v1]

  Tried in order when the primary fails.
"""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = cli_out

        with patch("shutil.which", return_value="C:\\Fake\\hermes.exe"), \
             patch("subprocess.run", return_value=mock_proc):
            res = detect_hermes_fallbacks()
            self.assertEqual(res["status"], "detected")
            self.assertEqual(res["source"], "cli")
            self.assertEqual(res["primary"], "nvidia/nemotron-3.5-bolt-e4b")
            self.assertIn("thinkingmachines/inkling:free", res["fallbacks"])
            self.assertIn("cohere/north-mini-code:free", res["fallbacks"])
            self.assertEqual(len(res["models"]), 5)

    def test_opencode_cli_discovery_and_free_tagging(self):
        """Verify opencode models output parsing and automatic tagging of free models."""
        cli_out = """
opencode/beam-free
opencode/big-pickle
opencode/claude-opus-5-5
opencode/crouton-alpha-free
opencode/deepseek-v4.1-flash-free
opencode/flint-40b-free
opencode/gpt-6-astra
opencode/minimax-m3
opencode/nemotron-3.5-super-vl-free
"""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = cli_out

        with patch("shutil.which", return_value="C:\\Fake\\opencode.cmd"), \
             patch("subprocess.run", return_value=mock_proc):
            res = detect_opencode_models()
            self.assertEqual(res["status"], "detected")
            self.assertEqual(res["source"], "cli")
            self.assertEqual(len(res["models"]), 9)

            free_models = res["free_models"]
            self.assertIn("opencode/beam-free", free_models)
            self.assertIn("opencode/big-pickle", free_models)
            self.assertIn("opencode/deepseek-v4.1-flash-free", free_models)
            self.assertIn("opencode/flint-40b-free", free_models)
            self.assertIn("opencode/nemotron-3.5-super-vl-free", free_models)
            self.assertNotIn("opencode/claude-opus-5-5", free_models)
            self.assertNotIn("opencode/gpt-6-astra", free_models)

    def test_free_model_tagger_heuristics(self):
        """Verify is_free_model detects all free variations."""
        self.assertTrue(is_free_model("opencode/beam-free"))
        self.assertTrue(is_free_model("opencode/big-pickle"))
        self.assertTrue(is_free_model("deepseek/deepseek-chat:free"))
        self.assertTrue(is_free_model("Flint 40B Free"))
        self.assertTrue(is_free_model("crouton-alpha-free"))
        self.assertFalse(is_free_model("claude-opus-5-5"))
        self.assertFalse(is_free_model("gpt-6-astra"))
        self.assertFalse(is_free_model("gemini-3.8-flash"))


if __name__ == "__main__":
    unittest.main()
