"""Sandbox and Multi-Tool Governance Integration Test Suite for AegisBrain.

Verifies:
1. Multi-tool execution worker governance (Hermes, Claude Code, Codex, OpenCode, Ollama/MoE).
2. The 4-Decision Quality Architecture Gate across multi-tool outputs.
3. Interactive Planning Phase with Research and Options exploration (Pros & Cons).
4. Codebase generalization (zero hardcoded machine paths).
"""

import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from aegis.hierarchy import (
    HierarchicalAgentOrchestrator,
    SubagentNode,
    WorkerType,
    WorkerSession,
)
from aegis.orchestrator import (
    call_local_worker,
    find_hermes_executable,
    find_claude_executable,
    find_codex_executable,
    find_opencode_executable,
    find_gemini_executable,
)


class TestMultiToolGovernanceAndSandbox(unittest.TestCase):
    """Test multi-tool execution worker governance in isolated sandbox environment."""

    def test_worker_discovery_functions_cross_platform(self):
        """Tool discovery must return a string path or None without raising exceptions."""
        h = find_hermes_executable()
        self.assertTrue(h is None or isinstance(h, str))

        c = find_claude_executable()
        self.assertTrue(c is None or isinstance(c, str))

        cx = find_codex_executable()
        self.assertTrue(cx is None or isinstance(cx, str))

        oc = find_opencode_executable()
        self.assertTrue(oc is None or isinstance(oc, str))

        g = find_gemini_executable()
        self.assertTrue(g is None or isinstance(g, str))

    def test_sandbox_simulation_mode_across_all_tools(self):
        """In sandbox mode, call_local_worker must successfully simulate any worker tool."""
        tools = ["hermes", "claude", "codex", "opencode", "moe", "gemini"]
        for tool in tools:
            ok, out = call_local_worker("Write a math function", model=tool, simulate=True)
            self.assertTrue(ok, f"Worker {tool} simulation failed")
            self.assertIn("execute_task", out)
            self.assertIn(tool, out.lower())

    def test_targeted_claude_code_dispatch(self):
        """Claude Code CLI dispatch executes with -p flag."""
        with patch("aegis.orchestrator.find_claude_executable") as mock_find, \
             patch("subprocess.run") as mock_run:
            mock_find.return_value = "/usr/local/bin/claude"
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_proc.stdout = "def add(a, b):\n    return a + b\n"
            mock_run.return_value = mock_proc

            ok, out = call_local_worker("Implement add function", model="claude")
            self.assertTrue(ok)
            self.assertIn("def add", out)
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            self.assertEqual(args[0], "/usr/local/bin/claude")
            self.assertEqual(args[1], "-p")

    def test_targeted_codex_dispatch(self):
        """Codex CLI dispatch executes with exec argument."""
        with patch("aegis.orchestrator.find_codex_executable") as mock_find, \
             patch("subprocess.run") as mock_run:
            mock_find.return_value = "/usr/local/bin/codex"
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_proc.stdout = "def multiply(a, b):\n    return a * b\n"
            mock_run.return_value = mock_proc

            ok, out = call_local_worker("Implement multiply", model="codex")
            self.assertTrue(ok)
            self.assertIn("def multiply", out)
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            self.assertEqual(args[0], "/usr/local/bin/codex")
            self.assertEqual(args[1], "exec")

    def test_four_decision_quality_gate_on_claude_output(self):
        """Junior Boss audits Claude Code output through all 4 quality gates."""
        sa = SubagentNode(
            subagent_id="subagent-claude",
            name="Claude Code Junior Boss",
            domain="backend_systems",
            allowed_workers=[WorkerType.CLAUDE],
        )

        # Flawed draft containing conversational slop and shell=True
        flawed_claude_draft = (
            "Here is the solution you requested:\n"
            "import os\n"
            "def run_command():\n"
            "    os.system('ls')\n"
            "    return True\n"
            "Hope this helps!"
        )
        passed, clean_code, details = sa.four_decision_architecture_audit(flawed_claude_draft)
        self.assertFalse(passed)
        self.assertFalse(details["gates"]["security_redteam"])
        self.assertTrue(any("Security Alert" in iss or "high-risk" in iss for iss in details["issues"]))

    def test_planning_phase_and_options_exploration(self):
        """HierarchicalAgentOrchestrator generates research, options with pros/cons, and communication log."""
        orch = HierarchicalAgentOrchestrator()
        task = "Design high-concurrency rate limiter"
        plan = orch.plan_with_research_and_options(task)

        self.assertEqual(plan["task"], task)
        self.assertIn("research", plan)
        self.assertIn("options", plan)
        self.assertGreaterEqual(len(plan["options"]), 3)

        # Check that options have pros and cons
        for opt in plan["options"]:
            self.assertIn("pros", opt)
            self.assertIn("cons", opt)
            self.assertGreater(len(opt["pros"]), 0)
            self.assertGreater(len(opt["cons"]), 0)

        # Check communication flow
        self.assertIn("communication_flow", plan)
        phases = [c["phase"] for c in plan["communication_flow"]]
        self.assertTrue(any("Task Scoping" in p for p in phases))
        self.assertTrue(any("Quality Architecture Gate" in p for p in phases))

        # Check markdown formatting
        md = orch.format_planning_and_options_report(plan)
        self.assertIn("Architectural Planning & Research Phase", md)
        self.assertIn("Implementation Options Explored (Pros & Cons)", md)
        self.assertIn("Hierarchical Boss-Worker Communications", md)
        self.assertIn("graph TD", md)

    def test_repo_generalization_no_hardcoded_user_paths(self):
        """Assert core modules contain zero hardcoded user-specific path references."""
        aegis_pkg = Path(__file__).resolve().parent.parent / "aegis"
        sensitive_modules = ["caffeinate.py", "remote.py", "hierarchy.py", "orchestrator.py"]

        for mod_name in sensitive_modules:
            mod_file = aegis_pkg / mod_name
            self.assertTrue(mod_file.exists(), f"Module {mod_name} does not exist")
            content = mod_file.read_text(encoding="utf-8", errors="replace")
            # Should not contain hardcoded Windows user paths like C:\Users\priya
            self.assertNotIn("c:\\users\\priya", content.lower())
            self.assertNotIn("p:\\open-source", content.lower())


if __name__ == "__main__":
    unittest.main()
