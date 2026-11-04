import unittest
from aegis.environment import (
    scan_environment,
    get_pending_installations,
    queue_pending_installation,
    resolve_pending_installation,
)
from aegis.taste import load_taste_profile, format_taste_prompt, format_taste_display
from aegis.planner import format_suggestion_panel, create_default_suggestions_for_task
from aegis.orchestrator import run_manager_worker_pipeline, get_distillation_summary


class TestEnvironmentTasteOrchestrator(unittest.TestCase):

    def test_environment_scan_and_pending_queue(self):
        env = scan_environment()
        self.assertIn("hardware", env)
        self.assertIn("tools", env)
        self.assertIn("ollama", env["tools"])
        self.assertIn("opencode", env["tools"])

        # Queue a pending installation requirement
        row_id = queue_pending_installation("docker-ce", "winget", "Containerized local evaluations", requires_admin=True)
        self.assertGreater(row_id, 0)

        pending = get_pending_installations()
        names = [p["package_name"] for p in pending]
        self.assertIn("docker-ce", names)

        # Resolve it
        ok = resolve_pending_installation(row_id)
        self.assertTrue(ok)

    def test_taste_profile(self):
        prof = load_taste_profile()
        self.assertEqual(prof["user_name"], "Priyanshu")
        self.assertIn("communication", prof)
        self.assertIn("coding_philosophy", prof)

        prompt_txt = format_taste_prompt()
        self.assertIn("Andrej Karpathy", prompt_txt)
        self.assertIn("Clarification Gate", prompt_txt)

        display_txt = format_taste_display()
        self.assertIn("Taste & Persona Profile", display_txt)

    def test_suggestion_panel_planning(self):
        suggs = create_default_suggestions_for_task("Multi-model LLM architecture")
        self.assertGreaterEqual(len(suggs), 2)
        panel = format_suggestion_panel("LLM Strategy", suggs, recommended_index=0)
        self.assertIn("Suggestion Panel", panel)
        self.assertIn("(Recommended)", panel)
        self.assertIn("Footprint", panel)

    def test_manager_worker_orchestration_and_distillation(self):
        res = run_manager_worker_pipeline("Format timestamp in ISO 8601", simulate_worker=True)
        self.assertEqual(res["status"], "success")
        self.assertIn("manager_model", res)
        self.assertIn("worker_model", res)
        self.assertGreater(res["tokens_saved_estimate"], 0)

        summary = get_distillation_summary()
        self.assertGreaterEqual(summary["trajectories_count"], 1)
        self.assertGreater(summary["total_tokens_saved"], 0)


if __name__ == "__main__":
    unittest.main()
