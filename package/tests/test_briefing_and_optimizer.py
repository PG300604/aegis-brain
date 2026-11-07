"""Unit tests for AegisBrain Offline Briefing and Arsenal Optimizer."""

import unittest
from aegis.briefing import OfflineBriefingEngine
from aegis.arsenal_optimizer import ArsenalOptimizer, OptimizationPlan


class TestBriefingAndArsenalOptimizer(unittest.TestCase):
    def test_briefing_generation(self):
        briefing_md = OfflineBriefingEngine.generate_briefing("Priyanshu")
        self.assertIn("Priyanshu", briefing_md)
        self.assertIn("Completed in Last Session", briefing_md)
        self.assertIn("Community & Tech Radar", briefing_md)
        self.assertIn("Tracked Pull Requests", briefing_md)
        self.assertIn("Suggested Next Action", briefing_md)

    def test_session_close_protocol(self):
        from aegis.session_close import close_session, format_session_close_display
        res = close_session(agent_name="test_agent", summary="Test session summary")
        self.assertIn("session_id", res)
        self.assertIn("snapshot", res)
        self.assertEqual(res["status"], "archived")
        display = format_session_close_display(res)
        self.assertIn("Session Safely Closed & Archived", display)
        self.assertIn("/exit", display)

    def test_salutation_time_ranges(self):
        self.assertIn("Priyanshu", OfflineBriefingEngine.get_greeting_salutation("Priyanshu"))

    def test_arsenal_optimizer_frontend(self):
        plan = ArsenalOptimizer.analyze_and_optimize("Build an accessible responsive navbar in React")
        self.assertIsInstance(plan, OptimizationPlan)
        self.assertIn("frontend", plan.detected_niches)
        skill_names = [s["name"] for s in plan.activated_skills]
        self.assertTrue(any(s in ("uipro", "impeccable", "gsap") for s in skill_names))
        md = plan.to_markdown()
        self.assertIn("Aegis Arsenal & Research Optimization Activated", md)

    def test_arsenal_optimizer_security_database(self):
        plan = ArsenalOptimizer.analyze_and_optimize("Audit Postgres hypertables for SQL injection and security leaks")
        self.assertTrue("database" in plan.detected_niches or "security" in plan.detected_niches)
        skill_names = [s["name"] for s in plan.activated_skills]
        self.assertTrue(any(s in ("pg-aiguide", "artemis", "pentagi", "gitguardian") for s in skill_names))


if __name__ == "__main__":
    unittest.main()
