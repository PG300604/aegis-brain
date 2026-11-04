import unittest
from aegis.hardware import get_hardware_status, recommend_model_tier
from aegis.governance import (
    load_governance_config,
    save_governance_config,
    get_active_worker_model,
    get_telemetry_terms,
)
from aegis.diagnostics import sanitize_text, generate_diagnostic_bundle, get_github_issue_url
from aegis.remote import handle_remote_command, load_remote_config, save_remote_config


class TestGovernanceAndRemote(unittest.TestCase):

    def test_hardware_status_and_tier_recommendation(self):
        hw = get_hardware_status()
        self.assertIn("total_ram_gb", hw)
        self.assertIn("avail_ram_gb", hw)
        self.assertGreater(hw["total_ram_gb"], 0)

        # Micro headroom
        tier_micro, rec_micro, _ = recommend_model_tier(2.0)
        self.assertEqual(tier_micro, "MICRO_OR_OFFLOAD")

        # Balanced headroom (e.g. 5GB free on 16GB PC with VM/Brave running)
        tier_std, rec_std, _ = recommend_model_tier(5.0)
        self.assertEqual(tier_std, "STANDARD_BALANCED")
        self.assertIn("7b", rec_std.lower())

        # Expanded headroom
        tier_exp, rec_exp, _ = recommend_model_tier(10.0)
        self.assertEqual(tier_exp, "EXPANDED_HIGH_FIDELITY")

    def test_model_governance(self):
        cfg = load_governance_config()
        self.assertIn("manager_model", cfg)
        self.assertIn("worker_model", cfg)
        self.assertFalse(cfg["telemetry_enabled"])  # Default-deny

        active_worker = get_active_worker_model()
        self.assertTrue(len(active_worker) > 0)

        terms = get_telemetry_terms()
        self.assertIn("Zero-Leakage Guarantee", terms)

    def test_diagnostic_sanitization(self):
        dummy_sid = "AC" + "0123456789abcdef0123456789abcdef"
        sample_secret = f"Token is 123456789:ABCdef-ghIJKlmnoPQRstuvwxyz1234567 and SID is {dummy_sid}"
        sanitized = sanitize_text(sample_secret)
        self.assertNotIn("123456789:ABCdef", sanitized)
        self.assertIn("[REDACTED_TELEGRAM_TOKEN]", sanitized)
        self.assertIn("[REDACTED_TWILIO_SID]", sanitized)

        url = get_github_issue_url(title="Test Crash", error_desc="Failed memory check")
        self.assertIn("github.com", url)
        self.assertIn("Test+Crash", url)

    def test_remote_typo_fuzzy_matching_and_fallback(self):
        sender = "2119188945"
        cfg = load_remote_config()
        if sender not in cfg.get("allowed_numbers", []):
            cfg.setdefault("allowed_numbers", []).append(sender)
            save_remote_config(cfg)

        # Typo: /help0 should suggest /help
        res1 = handle_remote_command(sender, "/help0")
        self.assertIn("Did you mean", res1)
        self.assertIn("/help", res1)

        # Typo: /hel0 should suggest /help
        res2 = handle_remote_command(sender, "/hel0")
        self.assertIn("Did you mean", res2)
        self.assertIn("/help", res2)

        # Typo: /statuss should suggest /status
        res3 = handle_remote_command(sender, "/statuss")
        self.assertIn("Did you mean", res3)
        self.assertIn("/status", res3)

        # Unrecognized command with slash should NEVER be typed into desktop
        res4 = handle_remote_command(sender, "/nonexistentcommand12345")
        self.assertIn("Unknown Command", res4)
        self.assertNotIn("Typed and submitted", res4)


if __name__ == "__main__":
    unittest.main()
