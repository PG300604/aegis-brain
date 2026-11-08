import unittest
from aegis.environment import (
    scan_environment,
    get_pending_installations,
    queue_pending_installation,
    resolve_pending_installation,
    detect_host_platform,
    run_doctor,
    get_host_capabilities,
    save_host_capabilities,
    format_doctor_report,
    install_tool,
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

    def test_detect_host_platform(self):
        plat = detect_host_platform()
        self.assertIn("os", plat)
        self.assertIn(plat["os"], ["windows", "macos", "linux"])
        self.assertIn("shell", plat)
        self.assertIn("pkg_manager", plat)

    def test_run_doctor_and_tiers(self):
        doc = run_doctor()
        self.assertIn("platform", doc)
        self.assertIn("tiers", doc)
        self.assertIn("core_essentials", doc)
        self.assertIn("sensory_accelerators", doc)
        self.assertIn("token_arbitrage_workers", doc)
        self.assertIn("workstation_modifiers", doc)
        self.assertIn("summary", doc)

        core = doc["core_essentials"]
        self.assertIn("python", core)
        self.assertIn("git", core)
        self.assertIn("sqlite3", core)
        self.assertEqual(core["python"]["status"], "INSTALLED")
        self.assertIn("impact", core["python"])
        self.assertIn("install_cmd", core["python"])

        sensory = doc["sensory_accelerators"]
        self.assertIn("ffmpeg", sensory)
        self.assertIn("whisper", sensory)

        workers = doc["token_arbitrage_workers"]
        self.assertIn("ollama", workers)
        self.assertIn("hermes", workers)
        self.assertIn("opencode", workers)
        self.assertIn("uv", workers)

        modifiers = doc["workstation_modifiers"]
        self.assertIn("komorebi", modifiers)
        self.assertIn("vim", modifiers)

        summary = doc["summary"]
        self.assertIn("total_items", summary)
        self.assertIn("healthy", summary)
        self.assertIn("standard_desktop_mode", summary)

    def test_save_and_get_host_capabilities(self):
        doc = run_doctor()
        save_host_capabilities(doc)
        caps = get_host_capabilities()
        self.assertIn("os", caps)
        self.assertIn("shell", caps)
        self.assertIn("pkg_manager", caps)
        self.assertIn("has_ffmpeg", caps)
        self.assertIn("has_whisper", caps)
        self.assertIn("has_ollama", caps)
        self.assertIn("has_hermes", caps)
        self.assertIn("has_tiling", caps)
        self.assertIn("has_vim", caps)
        self.assertIn("standard_desktop_mode", caps)
        self.assertIsInstance(caps["has_ffmpeg"], bool)
        self.assertIsInstance(caps["standard_desktop_mode"], bool)

    def test_format_doctor_report(self):
        doc = run_doctor()
        report = format_doctor_report(doc, show_fix=False)
        self.assertIn("Doctor & Host Capabilities Scorecard", report)
        self.assertIn("Core Essentials", report)
        self.assertIn("Sensory Perception Accelerators", report)
        self.assertIn("Token Arbitrage Workers", report)
        self.assertIn("Workstation & Terminal Modifiers", report)
        self.assertIn("Recommended Next Actions", report)

        report_fix = format_doctor_report(doc, show_fix=True)
        self.assertIn("Scorecard", report_fix)


if __name__ == "__main__":
    unittest.main()
