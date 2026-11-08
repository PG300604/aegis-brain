"""Comprehensive Unit & Invariant Test Suite for AegisBrain Jev Semantic Decision Engine."""

import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path

from aegis.jev import (
    ModelTier,
    RiskLevel,
    JevDecision,
    JevDecisionEngine,
    decide,
    route,
)


class TestJevSemanticEngine(unittest.TestCase):

    def setUp(self):
        self.engine = JevDecisionEngine()

    def test_zero_external_dependencies_invariant(self):
        """Invariant: package/aegis/jev.py must strictly use Python standard library only."""
        jev_file = Path(__file__).parent.parent / "aegis" / "jev.py"
        self.assertTrue(jev_file.exists(), f"{jev_file} does not exist!")

        content = jev_file.read_text(encoding="utf-8")
        tree = ast.parse(content)

        allowed_modules = {
            "dataclasses", "typing", "json", "re", "math", "time", "sqlite3",
            "enum", "pathlib", "sys", "os", "__future__", "collections",
            "itertools", "functools", "aegis"
        }

        violations = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    if root not in allowed_modules:
                        violations.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.level > 0:
                    continue  # Relative import within package
                if node.module:
                    root = node.module.split(".")[0]
                    if root not in allowed_modules:
                        violations.append(node.module)

        self.assertEqual(violations, [], f"Found non-standard library imports: {violations}")

    def test_sub_100ms_execution_latency_invariant(self):
        """Invariant: Jev decision execution must be token-free and strictly under 100ms."""
        prompts = [
            "Write a unit test for user model",
            "Deploy Spring AI to production cluster",
            "Audit postgres database query index and slow log",
            "Analyze system architecture invariants and threat model",
            "rm -rf / --no-preserve-root with api_key leaked",
            "Generate css tailwind layout for dashboard frontend",
            "Create remotion video animation with audio sync",
        ]

        for prompt in prompts:
            decision = self.engine.decide(prompt)
            self.assertLess(
                decision.latency_ms,
                100.0,
                f"Latency exceeded 100ms: {decision.latency_ms}ms on prompt: {prompt}"
            )
            # Typically sub-5ms
            self.assertGreater(decision.latency_ms, 0.0)

    def test_critical_risk_gating_and_tier1_locking(self):
        """Invariant: Prompts with secrets, destructive deletions, or root exploits MUST be CRITICAL and locked to Tier 1."""
        critical_prompts = [
            "Clean build cache and rm -rf /var/data directory",
            "Export database and drop table users immediately",
            "Deploy script with embedded api_key = 'mock_test_sample_key_abcdef123456'",
            "Execute root exploit payload and privilege escalation on host",
            "Here is the private_key -----BEGIN RSA PRIVATE KEY-----",
            "Send auth header bearer dummy_mock_test_token_abcdef1234567890",
        ]

        for prompt in critical_prompts:
            decision = self.engine.decide(prompt)
            self.assertEqual(
                decision.risk_level,
                RiskLevel.CRITICAL,
                f"Expected CRITICAL for prompt: {prompt}"
            )
            self.assertEqual(
                decision.model_tier,
                ModelTier.TIER_1,
                f"Expected locked TIER_1 for critical prompt: {prompt}"
            )
            self.assertEqual(
                decision.recommended_worker,
                "frontier_manager",
                f"Expected frontier_manager worker for critical prompt: {prompt}"
            )
            self.assertTrue(len(decision.risk_factors) > 0)

    def test_high_risk_production_and_billing_routing(self):
        """High risk tasks (prod deployment, payments, auth infra) route to Tier 1."""
        high_prompts = [
            "Deploy Spring AI release to production environment",
            "Update stripe billing webhook and payment processing handler",
            "Audit oauth provider jwt verification flow",
        ]

        for prompt in high_prompts:
            decision = self.engine.decide(prompt)
            self.assertEqual(
                decision.risk_level,
                RiskLevel.HIGH,
                f"Expected HIGH risk for: {prompt}"
            )
            self.assertEqual(
                decision.model_tier,
                ModelTier.TIER_1,
                f"Expected TIER_1 for: {prompt}"
            )
            self.assertEqual(decision.recommended_worker, "frontier_manager")

    def test_medium_risk_and_domain_coaching_routing(self):
        """Medium risk (multi-file refactor, architecture, code reviews, coaching) routes to Tier 2."""
        medium_prompts = [
            "Perform multi-file refactor across authentication and data services",
            "Conduct code review and coaching on PR pull request diff",
            "Investigate concurrency race condition in queue processor",
            "Run quality audit and coach junior worker on conventions",
        ]

        for prompt in medium_prompts:
            decision = self.engine.decide(prompt)
            self.assertEqual(
                decision.model_tier,
                ModelTier.TIER_2,
                f"Expected TIER_2 for: {prompt}"
            )
            self.assertEqual(decision.recommended_worker, "domain_coach")

    def test_low_risk_routine_tasks_routed_to_tier3_worker(self):
        """Routine low-risk tasks (boilerplate, unit tests, scripts, simple functions) route to Tier 3."""
        routine_prompts = [
            "Write pytest unit test for user model DTO",
            "Generate boilerplate schema parser for json payload",
            "Write python script to parse CSV files and print columns",
            "Format docstring and type hints for helper functions",
        ]

        for prompt in routine_prompts:
            decision = self.engine.decide(prompt)
            self.assertEqual(
                decision.risk_level,
                RiskLevel.LOW,
                f"Expected LOW risk for: {prompt}"
            )
            self.assertEqual(
                decision.model_tier,
                ModelTier.TIER_3,
                f"Expected TIER_3 for: {prompt}"
            )
            self.assertEqual(decision.recommended_worker, "hermes_worker")

    def test_dynamic_skill_pruning_and_selection(self):
        """Dynamic skill selection must return minimal 1 to 3 skills without context bloat."""
        # 1. Database task
        db_dec = self.engine.decide("Optimize postgresql database query with indexing and timescale hypertables")
        self.assertIn("pg-aiguide", db_dec.selected_skills)
        self.assertLessEqual(len(db_dec.selected_skills), 3)
        self.assertGreaterEqual(len(db_dec.selected_skills), 1)

        # 2. Architecture Diagram task
        diag_dec = self.engine.decide("Generate mermaid flowchart diagram for system architecture")
        self.assertIn("diagram-design", diag_dec.selected_skills)
        self.assertLessEqual(len(diag_dec.selected_skills), 3)

        # 3. AI Slop removal task
        slop_dec = self.engine.decide("Run unslop to remove AI conversational filler and buzzwords")
        self.assertIn("unslop-master", slop_dec.selected_skills)
        self.assertLessEqual(len(slop_dec.selected_skills), 3)

        # 4. Custom available_skills list
        custom_skills = ["custom-rust-skill", "custom-crypto-tool", "andrej-karpathy-skills"]
        custom_dec = self.engine.decide("Write clean rust code with minimal abstractions", available_skills=custom_skills)
        for s in custom_dec.selected_skills:
            self.assertIn(s, custom_skills)
        self.assertLessEqual(len(custom_dec.selected_skills), 3)

    def test_decision_data_structure_and_formatting(self):
        """JevDecision data structure serialization and format banner."""
        decision = self.engine.decide("Write simple unit tests for python calculator")
        d_dict = decision.to_dict()

        self.assertIsInstance(d_dict, dict)
        self.assertIn("prompt", d_dict)
        self.assertIn("model_tier", d_dict)
        self.assertIn("risk_level", d_dict)
        self.assertIn("selected_skills", d_dict)
        self.assertIn("skill_scores", d_dict)
        self.assertIn("recommended_worker", d_dict)
        self.assertIn("latency_ms", d_dict)
        self.assertIn("rationale", d_dict)
        self.assertIn("risk_factors", d_dict)

        banner = decision.format_banner()
        self.assertIn("Aegis Jev Semantic Decision Engine", banner)
        self.assertIn("Model Tier:", banner)
        self.assertIn("Execution Time:", banner)
        self.assertIn("Pruned Skills:", banner)

    def test_module_level_convenience_functions(self):
        """Test decide() and route() module-level entrypoints."""
        dec = decide("Write unit test for user model")
        self.assertIsInstance(dec, JevDecision)
        self.assertEqual(dec.model_tier, ModelTier.TIER_3)

        tier, worker, rationale = route("Deploy to production")
        self.assertEqual(tier, ModelTier.TIER_1)
        self.assertEqual(worker, "frontier_manager")
        self.assertTrue(len(rationale) > 0)

    def test_engine_status(self):
        """Test engine get_status()."""
        status = self.engine.get_status()
        self.assertEqual(status["engine"], "JevSemanticDecisionEngine")
        self.assertEqual(status["version"], "1.0.0")
        self.assertTrue(status["sub_100ms_invariant"])
        self.assertIn("TIER_1", status["supported_tiers"])
        self.assertIn("CRITICAL", status["supported_risk_levels"])

    def test_cli_subcommands(self):
        """Test aegis jev decide, route, and status CLI subcommands."""
        py_exe = sys.executable

        # 1. jev decide
        cmd1 = [py_exe, "-m", "aegis.cli", "jev", "decide", "Write unit tests for python scraper"]
        res1 = subprocess.run(cmd1, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res1.returncode, 0, f"CLI error: {res1.stderr}")
        self.assertIn("Aegis Jev Semantic Decision Engine", res1.stdout)

        # 2. jev decide --json
        cmd2 = [py_exe, "-m", "aegis.cli", "jev", "decide", "Deploy to production", "--json"]
        res2 = subprocess.run(cmd2, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res2.returncode, 0, f"CLI error: {res2.stderr}")
        parsed2 = json.loads(res2.stdout)
        self.assertEqual(parsed2["model_tier"], "TIER_1")
        self.assertEqual(parsed2["risk_level"], "HIGH")

        # 3. jev route
        cmd3 = [py_exe, "-m", "aegis.cli", "jev", "route", "Perform code review on PR"]
        res3 = subprocess.run(cmd3, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res3.returncode, 0, f"CLI error: {res3.stderr}")
        self.assertIn("Model Tier: TIER_2", res3.stdout)

        # 4. jev status --json
        cmd4 = [py_exe, "-m", "aegis.cli", "jev", "status", "--json"]
        res4 = subprocess.run(cmd4, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res4.returncode, 0, f"CLI error: {res4.stderr}")
        parsed4 = json.loads(res4.stdout)
        self.assertEqual(parsed4["engine"], "JevSemanticDecisionEngine")

    def test_jit_skill_expansion_recommendation(self):
        """Test Jev attaching expansion_recommendation in metadata on cross-domain prompts."""
        from aegis.armory import apply_archetype_profile
        apply_archetype_profile("developer")

        decision = self.engine.decide("Extract video frames using ffmpeg and transcribe audio with whisper")
        self.assertIn("metadata", decision.to_dict())
        rec = decision.metadata.get("expansion_recommendation")
        self.assertIsNotNone(rec)
        self.assertEqual(rec["target_archetype"], "creator")
        self.assertIn("aegis armory profile creator", rec["command"])

        banner = decision.format_banner()
        self.assertIn("Skill Expansion: JIT Mount Recommended", banner)


if __name__ == "__main__":
    unittest.main()
