import pytest
from pathlib import Path
from aegis.moe_engine import (
    evaluate_hardware_headroom,
    select_execution_tier,
    format_tier_status_display,
    get_model_storage_path,
    TIER_PROFILES,
)
from aegis.code_graph import CodebaseGraph
from aegis.task_lifecycle import (
    init_task_db,
    create_task,
    list_active_tasks,
    complete_task,
    get_task_history,
    format_tasks_display,
)
from aegis.planner import evaluate_task_ambiguity, format_clarification_gate


def test_moe_hardware_headroom_and_storage():
    headroom = evaluate_hardware_headroom()
    assert "avail_ram_gb" in headroom
    assert "can_run_moe" in headroom
    assert headroom["max_moe_ram_cap_gb"] == 7.5

    storage = get_model_storage_path()
    assert isinstance(storage, Path)
    # Check Drive P: preference if exists
    if Path("P:/").exists():
        assert "P:" in str(storage)


def test_moe_tier_selection_and_latency():
    # Forced tier selection
    res_constrained = select_execution_tier(user_choice="constrained", estimated_output_tokens=320)
    assert res_constrained["tier"] == "constrained"
    assert res_constrained["throughput_tok_sec"] == 32.0
    assert res_constrained["estimated_latency_sec"] == 10.0  # 320 / 32 = 10.0s

    res_moe = select_execution_tier(user_choice="moe_lightweight", estimated_output_tokens=370)
    assert res_moe["tier"] == "moe_lightweight"
    assert res_moe["ram_footprint_gb"] == 7.5
    assert res_moe["estimated_latency_sec"] == 20.0  # 370 / 18.5 = 20.0s

    display = format_tier_status_display(estimated_tokens=200)
    assert "Dynamic MoE & Hardware Latency Scheduler" in display
    assert "7.5 GB" in display


def test_codebase_graph_ast_indexing(tmp_path):
    # Create sample python files
    file_a = tmp_path / "service.py"
    file_a.write_text("""
import math
from utils import helper

class OrderService:
    '''Handles order transactions.'''
    def process_order(self, order_id):
        return helper(order_id)
""", encoding="utf-8")

    file_b = tmp_path / "utils.py"
    file_b.write_text("""
def helper(x):
    '''Simple helper.'''
    return x * 2
""", encoding="utf-8")

    graph = CodebaseGraph(tmp_path)
    stats = graph.index_workspace(tmp_path)
    assert stats["files_indexed"] >= 2
    assert stats["functions_indexed"] >= 2

    # Query
    nodes = graph.query_graph("process_order")
    assert len(nodes) == 1
    assert nodes[0]["name"] == "process_order"
    assert nodes[0]["kind"] == "function"

    # Neighbors
    fn_id = nodes[0]["id"]
    neighbors = graph.get_neighbors(fn_id)
    assert "outgoing" in neighbors

    # Summary
    summary = graph.format_summary()
    assert "Native Codebase Graph" in summary


def test_task_lifecycle_memory_compaction():
    init_task_db()
    # Add active task
    tid = create_task(
        title="Add continuous Postgres rollup",
        description="Downsample metrics every hour",
        category="backend",
        priority="high"
    )
    assert tid > 0

    active_tasks = list_active_tasks()
    matching = [t for t in active_tasks if t["id"] == tid]
    assert len(matching) == 1
    assert matching[0]["status"] == "active"

    # Complete task
    ok = complete_task(tid, outcome="Downsampling migration verified", learning="Reduced storage by 80%")
    assert ok is True

    # Active memory should now be clean of this task
    active_after = list_active_tasks()
    assert all(t["id"] != tid for t in active_after)

    # Historical archive contains the task
    history = get_task_history()
    archived = [t for t in history if t["id"] == tid]
    assert len(archived) == 1
    assert archived[0]["status"] == "completed"
    assert "Downsampling migration verified" in archived[0]["outcome"]


def test_matt_pocock_clarification_gate():
    # Ambiguous prompt lacking storage details
    ambiguous_prompt = "Build a user activity tracking service to save session logs"
    eval_res = evaluate_task_ambiguity(ambiguous_prompt)
    assert eval_res["is_ambiguous"] is True
    assert len(eval_res["questions"]) > 0

    gate_display = format_clarification_gate(ambiguous_prompt, eval_res)
    assert "Matt Pocock Clarification Gate" in gate_display
    assert "Storage Backend" in gate_display
