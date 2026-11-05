"""Unit tests for AegisBrain Deep Planning, Feasibility & Cascading Alignment Engine."""

from aegis.deep_planner import (
    DeepPlanningEngine,
    DeepPlanReport,
    ArchitectureOption,
    ClarifyingQuestion,
    HierarchicalAgentDialog,
)


def test_discover_arsenal_frontend():
    niche, tools = DeepPlanningEngine.discover_arsenal("Create a modern responsive dashboard UI in React")
    assert niche == "frontend"
    assert "uipro" in tools
    assert "tailwindcss" in tools


def test_discover_arsenal_backend():
    niche, tools = DeepPlanningEngine.discover_arsenal("Design high throughput REST API with PostgreSQL database")
    assert niche == "backend"
    assert "pg-aiguide" in tools
    assert "fastapi-patterns" in tools


def test_evaluate_yc_feasibility():
    score, flaws = DeepPlanningEngine.evaluate_yc_feasibility(
        task="Create an autonomous multi-agent task orchestrator",
        niche="general-engineering"
    )
    assert 30 <= score <= 95
    assert len(flaws) >= 2
    assert all(isinstance(f, str) and len(f) > 15 for f in flaws)


def test_generate_architecture_options():
    options = DeepPlanningEngine.generate_architecture_options(
        task="Build modern landing page",
        niche="frontend"
    )
    assert len(options) >= 3
    for opt in options:
        assert isinstance(opt, ArchitectureOption)
        assert len(opt.pros) > 0
        assert len(opt.cons) > 0
        assert 0 <= opt.feasibility_score <= 100
        assert 1 <= opt.complexity <= 10


def test_generate_clarifying_interview_question_count():
    questions = DeepPlanningEngine.generate_clarifying_interview(
        task="Build distributed microservice",
        niche="backend",
        count=6
    )
    assert len(questions) == 6
    for q in questions:
        assert isinstance(q, ClarifyingQuestion)
        assert len(q.options) >= 2
        assert q.category in ["Scope", "UI/UX", "Backend Logic", "Security & Reliability"]


def test_simulate_hierarchical_alignment():
    dialogs = DeepPlanningEngine.simulate_hierarchical_alignment(
        task="Deploy code reviewer subagent",
        niche="general-engineering"
    )
    assert len(dialogs) >= 4
    for d in dialogs:
        assert isinstance(d, HierarchicalAgentDialog)
        assert d.status == "RESOLVED"
        assert len(d.question) > 10
        assert len(d.answer) > 10


def test_create_plan_end_to_end():
    plan = DeepPlanningEngine.create_plan(
        task="Build a resilient Telegram remote control bridge with Whisper speech transcription",
        question_count=5
    )
    assert isinstance(plan, DeepPlanReport)
    assert plan.niche in ("media-processing", "research-and-sensory")
    assert len(plan.architecture_options) >= 3
    assert len(plan.clarifying_questions) == 5
    assert len(plan.task_ledger) >= 5
    assert not plan.is_clarified  # By default, needs user clarification

    # Test markdown formatting
    md = plan.to_markdown()
    assert "AegisBrain Deep Planning & Feasibility Report" in md
    assert "CLARIFICATION REQUIRED" in md
    assert "Y-Combinator Feasibility & Flaw Detection" in md
    assert "Multi-Approach Architectural Scenarios" in md
    assert "Interactive Clarification Interview" in md
    assert "Product Requirements Document (PRD)" in md
    assert "Technical Requirements & Architecture (TRD)" in md
    assert "classDiagram" in md
