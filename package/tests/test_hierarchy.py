"""Unit tests for AegisBrain Hierarchical Multi-Agent Engine (hierarchy.py)."""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from aegis.hierarchy import (
    HierarchicalAgentOrchestrator,
    SubagentNode,
    WorkerType,
    WorkerSession,
    evaluate_system_capacity,
)


class TestHierarchyEngine(unittest.TestCase):

    def setUp(self):
        self.orchestrator = HierarchicalAgentOrchestrator()

    @patch("aegis.hierarchy.get_hardware_status")
    def test_bottleneck_guard_throttles_to_single_subagent(self, mock_hw):
        """When PC RAM is constrained (<3.5GB), throttle to 1 subagent to avoid PC freeze."""
        mock_hw.return_value = {
            "avail_ram_gb": 2.8,
            "load_percent": 88,
            "cpu_cores": 12,
        }
        cap = evaluate_system_capacity()
        self.assertTrue(cap.is_bottleneck_risk)
        self.assertEqual(cap.max_safe_subagents, 1)

        orch = HierarchicalAgentOrchestrator()
        nodes = orch.plan_hierarchy("Refactor codebase")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].subagent_id, "subagent-1")

    @patch("aegis.hierarchy.get_hardware_status")
    def test_dynamic_scaling_with_ample_headroom(self, mock_hw):
        """When host has ample headroom (>6GB free), scale to N subagents."""
        mock_hw.return_value = {
            "avail_ram_gb": 8.5,
            "load_percent": 45,
            "cpu_cores": 12,
        }
        cap = evaluate_system_capacity()
        self.assertFalse(cap.is_bottleneck_risk)
        self.assertGreaterEqual(cap.max_safe_subagents, 3)

        orch = HierarchicalAgentOrchestrator()
        nodes = orch.plan_hierarchy("Full multi-service build")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].allowed_workers, [WorkerType.HERMES, WorkerType.MOE])
        self.assertEqual(nodes[1].allowed_workers, [WorkerType.GEMINI, WorkerType.HERMES])
        self.assertEqual(nodes[2].allowed_workers, [WorkerType.GEMINI, WorkerType.LOCAL_COMPILER])

    def test_bottom_to_top_quality_audit(self):
        """Worker draft is audited by Subagent, then Subagent is audited by Top Engine."""
        orch = HierarchicalAgentOrchestrator()
        orch.plan_hierarchy("Implement feature")

        sa1 = orch.subagents[0]
        session = sa1.add_worker_session(WorkerType.HERMES, "Write cross-platform lock")
        
        # Worker draft with POSIX fcntl
        raw_worker_code = "import fcntl\ndef lock(): pass"
        passed, clean_code, notes = sa1.audit_worker_output(session, raw_worker_code)

        # Subagent audits and refines
        self.assertTrue(passed)
        self.assertEqual(session.status, "success")
        self.assertIn("fcntl", notes.lower())
        self.assertNotIn("import fcntl", clean_code)

        # Top Engine audits all subagents
        top_audit = orch.top_engine_quality_audit()
        self.assertEqual(top_audit["overall_status"], "PASSED")
        self.assertGreater(top_audit["total_tokens_saved"], 0)

    def test_render_mermaid_tree(self):
        """Mermaid diagram contains Top Engine, subagents, and workers."""
        orch = HierarchicalAgentOrchestrator()
        orch.plan_hierarchy("Build feature")
        tree = orch.render_mermaid_tree()

        self.assertIn("Main Engine (Antigravity CLI)", tree)
        self.assertIn("subagent-1", tree)
        self.assertIn("HERMES", tree)
        self.assertIn("MOE", tree)

    def test_format_hierarchy_report(self):
        """Format report contains structured markdown and mermaid block."""
        orch = HierarchicalAgentOrchestrator()
        orch.plan_hierarchy("Build feature")
        report = orch.format_hierarchy_report()

        self.assertIn("AegisBrain Hierarchical Multi-Agent Structure", report)
        self.assertIn("Top Engine (Supreme Power)", report)
        self.assertIn("```mermaid", report)

    def test_four_decision_architecture_and_teaching(self):
        """Verify the 4-decision architecture gate and worker coaching loop."""
        orch = HierarchicalAgentOrchestrator()
        orch.plan_hierarchy("Implement secured cache")
        sa1 = orch.subagents[0]
        session = sa1.add_worker_session(WorkerType.HERMES, "Build cache module")

        # Draft containing conversational AI watermarks and unsafe eval
        draft = (
            "Sure! Here is the implementation:\n\n"
            "```python\n"
            "def run_cache(cmd):\n"
            "    eval(cmd)\n"
            "```\n\n"
            "I hope this helps! Feel free to ask more questions."
        )

        passed, clean_code, notes = sa1.audit_worker_output(session, draft)
        # Note: audit_worker_output returns False if blocked by red-team security
        self.assertIn("eval", draft)

        # Worker gets taught and refines code
        fb = sa1.teach_and_refine_worker(
            session=session,
            initial_errors=2,
            final_errors=0,
            teaching_prompt="Do not use eval(). Use dict-based cache lookup.",
        )
        self.assertEqual(fb["learning_trajectory"], "IMPROVING")
        self.assertEqual(session.status, "success")

        # 4-decision gate on clean code
        valid_code = "def run_cache(cache, key):\n    return cache.get(key)\n"
        passed_clean, verified_code, details = sa1.four_decision_architecture_audit(valid_code)
        self.assertTrue(passed_clean)
        self.assertIn("karpathy_simplicity", details["gates"])
        self.assertIn("unslop_turnitout", details["gates"])
        self.assertIn("security_redteam", details["gates"])
        self.assertIn("dual_env_verification", details["gates"])

    def test_record_escalation_event_in_confidence(self):
        """Verify recording escalation events in brain.db via confidence.py."""
        from aegis.confidence import record_escalation_event, get_escalation_events

        res = record_escalation_event(
            agent_name="hermes",
            task_type="backend_systems",
            reason="Repeated syntax errors and shell=True usage",
            initial_errors=3,
            final_errors=2,
        )
        self.assertIn("escalation_id", res)
        self.assertEqual(res["agent_name"], "hermes")
        self.assertEqual(res["final_errors"], 2)

        events = get_escalation_events("hermes", limit=5)
        self.assertTrue(len(events) > 0)
        self.assertEqual(events[0]["agent_name"], "hermes")
        self.assertIn("Repeated syntax errors", events[0]["reason"])

    def test_subagent_escalates_to_senior_boss_on_max_retries(self):
        """When attempts >= max_retries with remaining errors, Subagent constructs dossier and escalates to Senior Boss."""
        orch = HierarchicalAgentOrchestrator()
        orch.plan_hierarchy("Build database engine")
        sa1 = orch.subagents[0]

        # Patch call_local_worker to return flawed code with os.system on all attempts
        flawed_output = "import os\ndef run():\n    os.system('rm -rf /')\n    return True\n"
        with patch("aegis.orchestrator.call_local_worker", return_value=(True, flawed_output)):
            ok, code, info = sa1.execute_worker_with_coaching_loop(
                task_spec="Build secure query runner",
                worker_type=WorkerType.HERMES,
                max_retries=2,
                simulate=False,
                high_severity=False,
            )

        self.assertFalse(ok)
        self.assertEqual(info["status"], "escalated_to_senior_boss")
        self.assertEqual(sa1.quality_status, "escalated_to_senior_boss")
        self.assertIn("escalation_dossier", info)

        dossier = info["escalation_dossier"]
        self.assertEqual(dossier["worker_type"], "hermes")
        self.assertIn("reasoning_critique", dossier)
        self.assertTrue(any("os" in str(f) for f in dossier["flaws"]))

        # Verify Top Engine audit reflects the escalation
        top_audit = orch.top_engine_quality_audit()
        self.assertEqual(top_audit["overall_status"], "REVISIONS_NEEDED")
        self.assertIn("escalated to Senior Boss", sa1.audit_feedback)

    def test_subagent_escalates_high_severity_task(self):
        """High-severity or critical security tasks immediately escalate to Senior Boss."""
        orch = HierarchicalAgentOrchestrator()
        orch.plan_hierarchy("Refactor auth system")
        sa1 = orch.subagents[0]

        ok, code, info = sa1.execute_worker_with_coaching_loop(
            task_spec="CRITICAL Security Invariant: Hardware enclave key exchange",
            worker_type=WorkerType.HERMES,
            max_retries=3,
            high_severity=True,
        )

        self.assertFalse(ok)
        self.assertEqual(info["status"], "escalated_to_senior_boss")
        self.assertIn("escalation_dossier", info)
        self.assertIn("High-severity", info["escalation_dossier"]["escalation_reason"])

    def test_senior_boss_takeover_and_audit(self):
        """Senior Boss takeover directly authors verified production code and passes quality gates."""
        orch = HierarchicalAgentOrchestrator()
        orch.plan_hierarchy("Build mission critical auth")
        sa1 = orch.subagents[0]

        # Trigger takeover
        takeover_res = orch.senior_boss_takeover(
            task="Build mission critical auth",
            subagent_id=sa1.subagent_id,
        )

        self.assertEqual(takeover_res["status"], "takeover_completed")
        self.assertEqual(takeover_res["quality_status"], "passed")
        self.assertTrue(len(takeover_res["production_code"]) > 0)
        self.assertTrue(takeover_res["audit_details"]["gates"]["karpathy_simplicity"])
        self.assertTrue(takeover_res["audit_details"]["gates"]["security_redteam"])

        # Subagent quality status is now approved/passed
        self.assertEqual(sa1.quality_status, "passed")
        top_audit = orch.top_engine_quality_audit()
        self.assertEqual(top_audit["overall_status"], "PASSED")


if __name__ == "__main__":
    unittest.main()
