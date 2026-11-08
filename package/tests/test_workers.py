"""Unit tests for Aegis Worker Model Onboarding & Discovery Wizard."""

import json
from pathlib import Path
from unittest.mock import patch

from aegis.db import (
    clear_worker_models,
    get_worker_cascade,
    get_worker_models,
    save_worker_model,
)
from aegis.workers import (
    detect_hermes_fallbacks,
    detect_ollama_local_models,
    detect_opencode_models,
    format_worker_cascade_report,
    get_worker_setup_advice,
    run_fast_test,
    run_workers_wizard,
)


def test_detect_opencode_no_guesswork(tmp_path):
    """Verify Strict No-Guesswork Rule when OpenCode config lacks static model declarations."""
    fake_config = tmp_path / "opencode.jsonc"
    fake_config.write_text("{\n  // plugins only\n  \"plugins\": [\"./test\"]\n}", encoding="utf-8")

    with patch("aegis.workers._find_opencode_config_paths", return_value=[fake_config]), \
         patch("shutil.which", return_value="C:\\Fake\\opencode.cmd"):

        res = detect_opencode_models()
        assert res["installed"] is True
        assert res["needs_user_input"] is True
        assert "cannot be proven statically without guessing" in res["prompt_message"]
        assert "DeepSeek V4.1 Flash Free" in res["suggested_free_models"]


def test_detect_opencode_with_static_models(tmp_path):
    """Verify OpenCode model extraction when models are explicitly declared in config."""
    fake_config = tmp_path / "opencode.jsonc"
    fake_config.write_text(
        json.dumps({
            "model": "openrouter/deepseek-v3.1:free",
            "favorites": ["openrouter/flint-40b:free"]
        }),
        encoding="utf-8",
    )

    with patch("aegis.workers._find_opencode_config_paths", return_value=[fake_config]), \
         patch("shutil.which", return_value="C:\\Fake\\opencode.cmd"):

        res = detect_opencode_models()
        assert res["installed"] is True
        assert res["needs_user_input"] is False
        assert "openrouter/deepseek-v3.1:free" in res["models"]
        assert "openrouter/flint-40b:free" in res["models"]


def test_detect_hermes_fallbacks(tmp_path):
    """Verify Hermes config parser extracts primary model and fallback chain."""
    fake_yaml = tmp_path / "config.yaml"
    fake_yaml.write_text(
        """
model:
  default: nvidia/nemotron-3.5-bolt-e4b
  provider: nvidia

fallback_providers:
  - model: thinkingmachines/inkling:free
  - model: cohere/north-mini-code:free
  - model: google/gemma4-31b-it:free
        """,
        encoding="utf-8",
    )

    with patch("aegis.workers._find_hermes_config_paths", return_value=[fake_yaml]):
        res = detect_hermes_fallbacks()
        assert res["status"] == "detected"
        assert res["primary"] == "nvidia/nemotron-3.5-bolt-e4b"
        assert "thinkingmachines/inkling:free" in res["fallbacks"]
        assert "cohere/north-mini-code:free" in res["fallbacks"]
        assert len(res["models"]) == 4


def test_detect_ollama_local_models(tmp_path):
    """Verify Ollama manifest scanning finds local models on disk without daemon running."""
    # Setup mock structure: registry.ollama.ai/library/qwen2.5-coder/7b
    model_dir = tmp_path / "registry.ollama.ai" / "library" / "qwen2.5-coder"
    model_dir.mkdir(parents=True, exist_ok=True)
    (model_dir / "7b").write_text("manifest content", encoding="utf-8")

    with patch("aegis.workers._find_ollama_manifests_dir", return_value=tmp_path):
        res = detect_ollama_local_models()
        assert res["status"] == "detected"
        assert "qwen2.5-coder:7b" in res["models"]
        assert res["offline_ready"] is True


def test_worker_setup_advice():
    """Verify zero-cost setup advice formatting for tools."""
    gen_advice = get_worker_setup_advice()
    assert "AegisBrain Zero-Cost Worker Model Setup Guide" in gen_advice
    assert "OpenCode" in gen_advice
    assert "Hermes" in gen_advice
    assert "Ollama" in gen_advice

    opencode_advice = get_worker_setup_advice("opencode")
    assert "DeepSeek V4.1 Flash Free" in opencode_advice

    ollama_advice = get_worker_setup_advice("ollama")
    assert "qwen2.5-coder:7b" in ollama_advice
    assert "RAM Protection Policy" in ollama_advice


def test_workers_wizard_unconfigured_advice():
    """Verify wizard returns setup advice when user indicates tools are unconfigured."""
    res = run_workers_wizard(user_answers={"configured": False}, auto_save=False)
    assert res["setup_advice_needed"] is True
    assert "Zero-Cost Worker Model Setup Guide" in res["setup_advice"]


def test_workers_wizard_and_db_persistence():
    """Verify wizard completes priority cascade and persists to SQLite database."""
    clear_worker_models()

    user_answers = {
        "opencode_models": ["DeepSeek V4.1 Flash Free", "Flint 40B Free"],
    }

    res = run_workers_wizard(user_answers=user_answers, auto_save=True)
    assert res["saved_count"] > 0
    assert len(res["cascade"]) > 0

    # Verify database query
    cascade = get_worker_cascade()
    p1 = cascade["priority_1_opencode"]
    p2 = cascade["priority_2_hermes"]
    p3 = cascade["priority_3_ollama"]

    assert len(p1) == 2
    assert p1[0]["model_name"] == "DeepSeek V4.1 Flash Free"
    assert p1[0]["is_primary"] == 1

    # Verify Markdown formatting
    report = format_worker_cascade_report(cascade)
    assert "# ⚡ AegisBrain Worker Model Cascade" in report
    assert "DeepSeek V4.1 Flash Free" in report
    assert "Priority 1 (OpenCode)" in report

    clear_worker_models()
    assert len(get_worker_models()) == 0


def test_fast_path_testing(tmp_path):
    """Verify fast-path in-memory AST verification runs in < 1s."""
    sample_file = tmp_path / "sample.py"
    sample_file.write_text("def add(a: int, b: int) -> int:\n    return a + b\n", encoding="utf-8")

    res = run_fast_test(str(sample_file))
    assert res["status"] == "pass"
    assert res["ast_valid"] is True
    assert res["elapsed_ms"] < 1000.0


def test_cli_workers_command(monkeypatch, capsys):
    """Verify aegis workers CLI commands work as expected."""
    from aegis.cli import main

    # 1. Advice
    monkeypatch.setattr("sys.argv", ["aegis", "workers", "advice"])
    main()
    captured = capsys.readouterr()
    assert "Zero-Cost Worker Model Setup Guide" in captured.out

    # 2. Setup with screenshot/user confirmation
    monkeypatch.setattr("sys.argv", ["aegis", "workers", "setup", "--models", "DeepSeek V4.1 Flash Free, Flint 40B Free", "--json"])
    main()
    captured_json = capsys.readouterr()
    data = json.loads(captured_json.out)
    assert data["saved_count"] > 0
    assert len(data["cascade"]) >= 2
