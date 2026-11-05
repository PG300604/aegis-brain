"""Tests for AegisBrain Emergency Low-Token Survival Mode.

Verifies:
1. is_survival_mode() headroom and emergency flag detection.
2. enable_survival_mode() config persistence in ~/.aegis/config.json.
3. format_post_response_suggestions_and_review() formatting:
   - Matt Pocock Suggestion Panel (2-3 options, pros/cons, token impact, 1 recommended option).
   - Skeptical Truth-Seeking Review (anti-sycophancy audit, edge cases, verification status).
4. Full integration with nlp_router.py and orchestrator.py.
"""

import json
from pathlib import Path
try:
    import pytest
except ImportError:
    class _DummyPytest:
        @staticmethod
        def fixture(*args, **kwargs):
            def decorator(f):
                return f
            return decorator

        @staticmethod
        def skip(reason=""):
            pass

    pytest = _DummyPytest()

from aegis.survival_mode import (
    is_survival_mode,
    enable_survival_mode,
    disable_survival_mode,
    format_post_response_suggestions_and_review,
    build_suggestion_panel,
    build_skeptical_review,
)
from aegis.nlp_router import NLPIntentRouter, route_and_execute
from aegis.orchestrator import run_manager_worker_pipeline, format_distillation_report, orchestrate


@pytest.fixture(autouse=True)
def clean_survival_state(tmp_path, monkeypatch):
    """Isolate config directories to temporary path for deterministic testing."""
    test_aegis_dir = tmp_path / ".aegis"
    test_brain_dir = tmp_path / ".aegis-brain"
    test_aegis_dir.mkdir(parents=True, exist_ok=True)
    test_brain_dir.mkdir(parents=True, exist_ok=True)

    # Mock get_survival_config_paths to use temporary isolated directory
    temp_config_path = test_aegis_dir / "config.json"
    temp_brain_config = test_brain_dir / "config.json"
    monkeypatch.setattr(
        "aegis.survival_mode.get_survival_config_paths",
        lambda: [temp_config_path, temp_brain_config]
    )
    monkeypatch.setattr("aegis.token_guard.get_aegis_dir", lambda: test_brain_dir)

    # Clear any environment variables
    monkeypatch.delenv("AEGIS_SURVIVAL_MODE", raising=False)
    monkeypatch.delenv("AEGIS_EMERGENCY_FLAG", raising=False)
    monkeypatch.delenv("AEGIS_TOKEN_HEADROOM_PCT", raising=False)

    yield

    disable_survival_mode()


def test_survival_mode_default_false():
    assert is_survival_mode() is False


def test_survival_mode_explicit_headroom():
    assert is_survival_mode(headroom_pct=29.0) is True
    assert is_survival_mode(headroom_pct=30.0) is True
    assert is_survival_mode(headroom_pct=31.0) is False


def test_survival_mode_env_vars(monkeypatch):
    monkeypatch.setenv("AEGIS_SURVIVAL_MODE", "1")
    assert is_survival_mode() is True

    monkeypatch.setenv("AEGIS_SURVIVAL_MODE", "0")
    monkeypatch.setenv("AEGIS_EMERGENCY_FLAG", "true")
    assert is_survival_mode() is True

    monkeypatch.delenv("AEGIS_EMERGENCY_FLAG")
    monkeypatch.setenv("AEGIS_TOKEN_HEADROOM_PCT", "25.5")
    assert is_survival_mode() is True


def test_enable_survival_mode_persistence():
    enable_survival_mode("token_cap_29%")
    assert is_survival_mode() is True

    # Check that config has been written with survival details
    from aegis.survival_mode import get_survival_config_paths
    for cfg_p in get_survival_config_paths():
        if cfg_p.exists():
            with open(cfg_p, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert data.get("emergency_flag") is True
            assert data["survival_mode"]["enabled"] is True
            assert data["survival_mode"]["remaining_token_headroom_pct"] == 29.0
            assert "token_cap_29%" in data["survival_mode"]["reason"]

    # Verify disable resets status
    disable_survival_mode()
    assert is_survival_mode() is False


def test_format_post_response_suggestions_and_review():
    raw_response = "Synthesized AST visitor for python files."
    output = format_post_response_suggestions_and_review("AST Parsing", raw_response)

    # 1. Base response preserved
    assert "Synthesized AST visitor" in output

    # 2. Matt Pocock Suggestion Panel appended
    assert "AegisBrain Suggestion Panel: AST Parsing" in output
    assert "(Recommended)" in output
    assert "Footprint:" in output
    assert "Pros:" in output
    assert "Cons" in output

    # 3. Skeptical Truth-Seeking Review appended
    assert "Skeptical Truth-Seeking Review (Anti-Sycophancy Audit)" in output
    assert "Verdict" in output
    assert "Sycophancy Flag" in output
    assert "Verification Status" in output
    assert "Identified Flaws & Vulnerabilities" in output
    assert "Unhandled Edge Cases & Environmental Traps" in output


def test_format_post_response_detects_sycophancy():
    sycophantic_response = "Everything looks great! No bugs found and 100% complete without checking."
    output = format_post_response_suggestions_and_review("Sycophancy Check", sycophantic_response)

    assert "YES (Unsubstantiated Optimism Detected)" in output
    assert "REJECT" in output


def test_format_post_response_idempotence():
    raw_response = "Code change ready."
    first_pass = format_post_response_suggestions_and_review("Task", raw_response)
    second_pass = format_post_response_suggestions_and_review("Task", first_pass)

    # Should not duplicate the panel or review
    assert first_pass.count("AegisBrain Suggestion Panel") == 1
    assert second_pass.count("AegisBrain Suggestion Panel") == 1
    assert second_pass.count("Skeptical Truth-Seeking Review") == 1


def test_nlp_router_integration():
    output = route_and_execute("Analyze my code architecture", include_suggestions=True)

    # Contains original architecture content
    assert "AegisBrain Code Architecture Analysis" in output
    # Contains automatically appended Suggestion Panel
    assert "AegisBrain Suggestion Panel" in output
    assert "(Recommended)" in output
    # Contains automatically appended Skeptical Review
    assert "Skeptical Truth-Seeking Review" in output
    assert "Verification Status" in output


def test_nlp_router_greeting_integration():
    output = route_and_execute("Hello, what happened offline?", include_suggestions=True)

    # Contains briefing and post response suggestions + review
    assert "AegisBrain Suggestion Panel" in output
    assert "Skeptical Truth-Seeking Review" in output


def test_orchestrator_integration():
    res = run_manager_worker_pipeline("Parse JSON safely", simulate_worker=True)

    assert "response" in res
    assert "suggestions_and_review" in res
    assert "AegisBrain Suggestion Panel" in res["response"]
    assert "Skeptical Truth-Seeking Review" in res["response"]
    assert "(Recommended)" in res["response"]

    # Test orchestrate wrapper
    orch_output = orchestrate("Build cache eviction", simulate_worker=True)
    assert "Manager-Worker Execution Complete" in orch_output
    assert "AegisBrain Suggestion Panel" in orch_output
    assert "Skeptical Truth-Seeking Review" in orch_output


def test_orchestrator_distillation_report_integration():
    report = format_distillation_report()

    assert "AegisBrain Manager-Worker Token Arbitrage" in report
    assert "AegisBrain Suggestion Panel" in report
    assert "Skeptical Truth-Seeking Review" in report
