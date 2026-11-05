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
from aegis.token_guard import (
    check_token_emergency_lock,
    is_priority_task,
    save_token_guard_config,
    get_token_guard_config,
)


@pytest.fixture(autouse=True)
def setup_guard_config(tmp_path, monkeypatch):
    monkeypatch.setattr("aegis.token_guard.get_aegis_dir", lambda: tmp_path)


def test_normal_budget_allowed():
    allowed, msg = check_token_emergency_lock(remaining_pct=35.0, task_description="Draft a button")
    assert allowed is True
    assert "Token budget normal" in msg


def test_emergency_cap_blocks_routine_task():
    allowed, msg = check_token_emergency_lock(remaining_pct=8.5, task_description="Explain this meme")
    assert allowed is False
    assert "EMERGENCY TOKEN CAP TRIGGERED" in msg


def test_emergency_cap_allows_spring_ai_and_fyp():
    # Spring AI
    allowed, msg = check_token_emergency_lock(remaining_pct=7.0, task_description="Implement Spring AI VectorStore integration")
    assert allowed is True
    assert "Emergency 10% token reserve unlocked" in msg

    # Final Year Project
    allowed, msg = check_token_emergency_lock(remaining_pct=5.0, task_description="Refactor my Final Year Project algorithm")
    assert allowed is True
    assert "Emergency 10% token reserve unlocked" in msg

    # Explicit override
    allowed, msg = check_token_emergency_lock(remaining_pct=4.0, task_description="Routine fix", explicit_override=True)
    assert allowed is True


def test_save_and_read_config():
    save_token_guard_config(cap_pct=15.0, keywords=["important", "urgent"])
    cfg = get_token_guard_config()
    assert cfg["emergency_cap_pct"] == 15.0
    assert "important" in cfg["priority_keywords"]
