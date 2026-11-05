"""Unit tests for AegisBrain Agent Confidence Scoring & Learning Curve Tracker."""

import unittest
from pathlib import Path
from aegis.confidence import (
    record_score,
    get_agent_confidence,
    get_all_agents_confidence,
    format_confidence_report,
    recommend_agent,
    init_confidence_table,
)


class TestConfidence(unittest.TestCase):

    def setUp(self):
        init_confidence_table()
        import sqlite3
        from aegis.db import get_db_path
        with sqlite3.connect(get_db_path()) as conn:
            conn.execute("DELETE FROM agent_confidence WHERE agent_name LIKE 'test-%' OR agent_name LIKE '%hermes%' OR agent_name LIKE '%coder%'")

    def test_record_and_get_confidence(self):
        record_score("test-agent-alpha", 9, accepted=True, revision_rounds=0, task_type="python")
        record_score("test-agent-alpha", 8, accepted=True, revision_rounds=0, task_type="python")
        record_score("test-agent-alpha", 10, accepted=True, revision_rounds=0, task_type="python")

        conf = get_agent_confidence("test-agent-alpha")
        self.assertEqual(conf["agent"], "test-agent-alpha")
        self.assertEqual(conf["success_rate"], 100.0)
        self.assertGreaterEqual(conf["avg_score"], 8.5)
        self.assertEqual(conf["total_tasks"], 3)
        self.assertEqual(conf["learning_curve"], "insufficient_data")

    def test_learning_curve_improving(self):
        # Insert 8 scores in chronological order: older scores lower (5,5,6,6), newer scores higher (9,9,10,10)
        # Note: get_agent_confidence orders by DESC (newest first: 10, 10, 9, 9, 6, 6, 5, 5)
        for s in [5, 5, 6, 6, 9, 9, 10, 10]:
            record_score("test-agent-improving", s, accepted=True, task_type="reasoning")

        conf = get_agent_confidence("test-agent-improving", window=8)
        self.assertEqual(conf["learning_curve"], "improving")

    def test_learning_curve_degrading(self):
        # Chronological: 10, 10, 9, 9, 5, 5, 4, 4
        # Newest first: 4, 4, 5, 5, 9, 9, 10, 10
        for s in [10, 10, 9, 9, 5, 5, 4, 4]:
            record_score("test-agent-degrading", s, accepted=False, revision_rounds=2)

        conf = get_agent_confidence("test-agent-degrading", window=8)
        self.assertEqual(conf["learning_curve"], "degrading")

    def test_empty_agent_confidence(self):
        conf = get_agent_confidence("non-existent-agent-xyz")
        self.assertEqual(conf["total_tasks"], 0)
        self.assertEqual(conf["learning_curve"], "unknown")
        self.assertEqual(conf["success_rate"], 0.0)

    def test_format_confidence_report(self):
        record_score("hermes-reporter", 9, accepted=True)
        report = format_confidence_report()
        self.assertIn("Agent Confidence Scoreboard", report)
        self.assertIn("hermes-reporter", report)

    def test_recommend_agent(self):
        # 3 tasks minimum for recommendation
        for _ in range(3):
            record_score("specialist-coder", 10, accepted=True, task_type="frontend")
            record_score("general-coder", 7, accepted=True, task_type="frontend")

        rec = recommend_agent(task_type="frontend")
        self.assertEqual(rec, "specialist-coder")

        # Unknown type falls back to hermes
        rec_unknown = recommend_agent(task_type="non-existent-domain-404")
        self.assertEqual(rec_unknown, "hermes")

    def test_record_agent_task_feedback_and_improvement(self):
        from aegis.confidence import record_agent_task_feedback, can_delegate_complex_task

        # Worker starts with 5 errors, reduced to 1 after coaching (delta = +4 improvement)
        fb = record_agent_task_feedback(
            agent_name="hermes-worker-v1",
            initial_errors=5,
            final_errors=1,
            teaching_notes="Avoid unvalidated regexes and duplicate imports.",
            task_type="backend_refactor",
        )
        self.assertIsInstance(fb, dict)
        self.assertGreater(fb["record_id"], 0)
        self.assertEqual(fb["error_delta"], 4)

        conf = get_agent_confidence("hermes-worker-v1")
        self.assertEqual(conf["agent"], "hermes-worker-v1")
        self.assertEqual(conf["total_tasks"], 1)

        # Delegate complex task check
        for _ in range(3):
            record_agent_task_feedback(
                agent_name="experienced-hermes",
                initial_errors=4,
                final_errors=0,
                teaching_notes="Coached on Karpathy simplicity.",
            )
        can_delegate, avg_score, reason = can_delegate_complex_task("experienced-hermes")
        self.assertTrue(can_delegate)
        self.assertIn("Approved for complex delegation", reason)


if __name__ == "__main__":
    unittest.main()
