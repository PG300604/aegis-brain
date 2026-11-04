"""Unit tests for Hierarchical Nested Multi-Agent Swarm, Away Mode & Mobile Polls."""

import pytest
from aegis.swarm import run_nested_swarm, format_swarm_display
from aegis.remote import (
    is_away_mode_active,
    set_away_mode,
    TerminalMirror,
    register_active_poll,
    get_active_poll,
    handle_remote_command,
    load_remote_config,
    save_remote_config,
)


@pytest.fixture(autouse=True)
def ensure_authorized_number():
    cfg = load_remote_config()
    allowed = cfg.get("allowed_numbers", [])
    if "2119188945" not in allowed:
        allowed.append("2119188945")
        cfg["allowed_numbers"] = allowed
        save_remote_config(cfg)
    yield


def test_nested_swarm_execution():
    """Verify 4-tier swarm decomposes into 3 domain leads and executes in parallel."""
    task = "Build Async Cross-Chain Event Relayer"
    res = run_nested_swarm(task, simulate_workers=True)

    assert res["task"] == task
    assert res["status"] in ("success", "refined")
    assert len(res["domains"]) == 3
    domains = [d["domain"] for d in res["domains"]]
    assert any("Architecture" in d for d in domains)
    assert any("Implementation" in d for d in domains)
    assert any("Verification" in d for d in domains)
    assert res["total_tokens_saved"] >= 1500
    assert "execute_contract" in res["final_synthesis"]
    assert "process_task" in res["final_synthesis"]


def test_format_swarm_display():
    """Verify formatted output for mobile and CLI."""
    task = "Benchmark AST Graph Indexer"
    res = run_nested_swarm(task, simulate_workers=True)
    display = format_swarm_display(res)

    assert "Hierarchical Swarm Execution" in display
    assert "Frontier Boss" in display
    assert "Tokens Saved" in display
    assert "Architecture & Contracts" in display


def test_away_mode_lifecycle():
    """Verify away mode toggles and persists properly."""
    set_away_mode(True)
    assert is_away_mode_active() is True

    set_away_mode(False)
    assert is_away_mode_active() is False


def test_terminal_mirror_buffer():
    """Verify thread-safe ring buffer and pagination."""
    mirror = TerminalMirror(capacity=5)
    for i in range(7):
        mirror.append(f"Log event #{i}", source="test")

    # Ring buffer should have capped at 5
    items, page, total_pages = mirror.get_page(page=1, page_size=2)
    assert len(items) == 2
    assert total_pages == 3
    # Check that older events 0 and 1 were evicted
    texts = [it["text"] for it in mirror.buffer]
    assert "Log event #0" not in texts
    assert "Log event #6" in texts


def test_poll_and_callback_registry():
    """Verify active poll registration for Telegram 1-tap decision handling."""
    poll_id = "test_poll_999"
    question = "Which execution tier should Aegis run?"
    options = ["Qwen 2.5 Coder (<4GB)", "Lightweight MoE (7.5GB)", "Frontier Arbitrage"]

    register_active_poll(poll_id, question, options)
    retrieved = get_active_poll(poll_id)

    assert retrieved is not None
    assert retrieved["question"] == question
    assert len(retrieved["options"]) == 3
    assert retrieved["options"][1] == "Lightweight MoE (7.5GB)"


def test_remote_command_bot_username_normalization():
    """Verify commands clicked from Telegram menu with @bot_username are stripped cleanly."""
    res_help = handle_remote_command("2119188945", "/help@HHAACLIBot")
    assert "AegisBrain Remote Commands" in res_help

    res_status = handle_remote_command("2119188945", "/status@HHAACLIBot")
    assert "AegisBrain Workstation Status" in res_status


def test_remote_command_typo_fallback():
    """Verify typos like /help0 return fuzzy match suggestion."""
    res = handle_remote_command("2119188945", "/help0")
    # In Telegram mode, typo returns empty string because it sent inline keyboard
    # If not registered, it suggests close match
    assert res == "" or "Did you mean" in res or "Unknown Command" in res


def test_remote_command_lock_activates_away():
    """Verify /lock locks workstation and activates Away Mode."""
    handle_remote_command("2119188945", "/lock")
    assert is_away_mode_active() is True
    # Cleanup
    set_away_mode(False)


def test_remote_command_nav_and_away():
    """Verify /away on/off and /nav commands."""
    res_away = handle_remote_command("2119188945", "/away on")
    assert "Away Mode ON" in res_away
    assert is_away_mode_active() is True

    res_away_off = handle_remote_command("2119188945", "/away off")
    assert "Away Mode OFF" in res_away_off
    assert is_away_mode_active() is False

    mirror = TerminalMirror()
    mirror.append("CLI compilation finished with 0 errors")
    res_nav = handle_remote_command("2119188945", "/nav")
    # Sends inline buttons or pager text
    assert res_nav == "" or "Terminal Output" in res_nav


def test_remote_artifacts_and_prompt_execution():
    """Verify /artifacts and natural language swarm dispatch."""
    res = handle_remote_command("2119188945", "/artifacts")
    assert "Artifacts" in res or "No recent artifacts" in res

    # Verify natural language prompt submits to active coding session
    prompt_res = handle_remote_command("2119188945", "Please design and implement a distributed event queue")
    assert "Prompt Sent" in prompt_res or "Typed and submitted" in prompt_res

    # Verify explicit /swarm command triggers swarm
    swarm_res = handle_remote_command("2119188945", "/swarm Design event queue")
    assert "Hierarchical Swarm Execution" in swarm_res or "Task:" in swarm_res
