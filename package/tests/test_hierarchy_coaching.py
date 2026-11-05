import json
import pytest
from pathlib import Path
from aegis.hierarchy import (
    HierarchicalAgentOrchestrator,
    SubagentNode,
    WorkerType,
    WorkerSession,
    evaluate_system_capacity,
)


def test_subagent_four_decision_architecture_catches_flaws():
    sa = SubagentNode(
        subagent_id="test-sa",
        name="Test Lead",
        domain="testing",
        allowed_workers=[WorkerType.HERMES],
    )

    # Flawed code with AI watermark and dangerous shell=True
    flawed_code = (
        "Certainly! Here is the script:\n"
        "import subprocess\n"
        "subprocess.run('ls', shell=True)\n"
        "Happy coding!\n"
    )

    passed, clean, details = sa.four_decision_architecture_audit(flawed_code)
    assert passed is False
    assert details["gates"]["security_redteam"] is False
    assert any("shell=True" in iss or "high-risk" in iss for iss in details["issues"])


def test_subagent_coaching_loop_refines_worker_and_tracks_feedback():
    sa = SubagentNode(
        subagent_id="test-sa",
        name="Test Lead",
        domain="core_code",
        allowed_workers=[WorkerType.HERMES],
    )

    # Run with simulation=True (attempt 1 produces flaws, attempt 2 produces clean code)
    ok, code, info = sa.execute_worker_with_coaching_loop(
        task_spec="Build minimal math helper",
        worker_type=WorkerType.HERMES,
        max_retries=3,
        simulate=True,
    )

    assert ok is True
    assert info["attempts"] == 2
    assert info["initial_errors"] > 0
    assert info["final_errors"] == 0
    assert len(info["coaching_history"]) == 1
    assert "def execute_task" in code
    assert sa.quality_status == "passed"
    assert sa.confidence_score == 10


def test_hierarchical_orchestrator_execute_hierarchy():
    orch = HierarchicalAgentOrchestrator()
    res = orch.execute_hierarchy(
        task="Develop fast cache module",
        simulate=True,
    )

    assert res["task"] == "Develop fast cache module"
    assert res["top_audit"]["overall_status"] == "PASSED"
    assert len(res["subagent_executions"]) >= 1
    for sub in res["subagent_executions"]:
        assert sub["passed"] is True
        assert sub["final_errors"] == 0
