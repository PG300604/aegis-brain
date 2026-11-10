"""Unit tests for AegisBrain Task Severity Triage & Bottleneck Guard."""

import unittest
from aegis.severity_triage import (
    SeverityTriageEngine,
    judge_task_severity,
    should_delegate_to_worker,
    SeverityLevel,
    ExecutionStrategy,
)


class TestSeverityTriage(unittest.TestCase):

    def test_critical_security_task(self):
        task = "Audit this JWT authentication token verification logic for potential security bypass"
        dec = judge_task_severity(task)
        self.assertEqual(dec.severity, SeverityLevel.CRITICAL)
        self.assertEqual(dec.execution_strategy, ExecutionStrategy.FRONTIER_DIRECT)
        self.assertEqual(dec.recommended_worker, "frontier_manager")
        self.assertGreaterEqual(dec.complexity_score, 8)
        self.assertIn("Zero data leakage", dec.invariants[0])

    def test_critical_spring_ai_production_task(self):
        task = "Deploy Spring AI PR #7308 to production cluster and migrate database"
        dec = judge_task_severity(task)
        self.assertEqual(dec.severity, SeverityLevel.CRITICAL)
        self.assertEqual(dec.execution_strategy, ExecutionStrategy.FRONTIER_DIRECT)

    def test_routine_boilerplate_task(self):
        task = "Generate unit test fixtures and pytest boilerplate for user registration DTO"
        dec = judge_task_severity(task)
        self.assertEqual(dec.severity, SeverityLevel.ROUTINE)
        self.assertIn(dec.execution_strategy, [
            ExecutionStrategy.LOCAL_WORKER_WITH_MANAGER_REVIEW,
            ExecutionStrategy.LIGHTWEIGHT_CLI
        ])
        self.assertLessEqual(dec.complexity_score, 4)

    def test_moderate_feature_task(self):
        task = "Implement user notification dispatcher supporting webhook payloads"
        dec = judge_task_severity(task)
        self.assertEqual(dec.severity, SeverityLevel.MODERATE)
        self.assertIn(dec.execution_strategy, [
            ExecutionStrategy.LOCAL_WORKER_WITH_MANAGER_REVIEW,
            ExecutionStrategy.LIGHTWEIGHT_CLI,
            ExecutionStrategy.PARALLEL_SUBAGENTS,
        ])
        self.assertEqual(dec.complexity_score, 6)

    def test_should_delegate_helper(self):
        delegate_routine, _ = should_delegate_to_worker("Write unit tests for the scraper")
        self.assertTrue(delegate_routine)

        delegate_crit, _ = should_delegate_to_worker("Fix critical secret leakage and private key exploit")
        self.assertFalse(delegate_crit)

        delegate_micro, dec_micro = should_delegate_to_worker("Fix small typo in README heading")
        self.assertFalse(delegate_micro)
        self.assertEqual(dec_micro.execution_strategy, ExecutionStrategy.SUBAGENT_DIRECT)

    def test_micro_task_typo_direct_subagent(self):
        task = "Fix single word typo in documentation"
        dec = judge_task_severity(task)
        self.assertEqual(dec.execution_strategy, ExecutionStrategy.SUBAGENT_DIRECT)
        self.assertEqual(dec.recommended_worker, "subagent_direct")
        self.assertEqual(dec.complexity_score, 1)
        self.assertEqual(dec.workers_per_subagent, 0)
        self.assertIn("Micro-task / typo", dec.rationale)

    def test_format_banner(self):
        dec = judge_task_severity("Extract metadata from Instagram reel")
        banner = dec.format_banner()
        self.assertIn("Aegis Severity Triage", banner)
        self.assertIn("Strategy:", banner)
        self.assertIn("PC Headroom:", banner)


if __name__ == "__main__":
    unittest.main()
