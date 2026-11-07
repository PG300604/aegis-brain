from aegis.browser import clean_html_to_markdown
from aegis.pipeline import QualityGatesPipeline
from aegis.alignment import AlignmentEngine
from aegis.transparent_observer import TransparentObserver
from aegis.dashboard import (
    record_feedback,
    record_benchmark,
    record_tool_fallback,
    get_dashboard_summary,
    format_dashboard_tui,
    render_dashboard_html
)


def test_clean_html_to_markdown():
    raw_html = """
    <html>
      <head><script>alert('noise');</script><style>body { color: red; }</style></head>
      <body>
        <header><nav><a href="/home">Home</a></nav></header>
        <h1>Main Architecture</h1>
        <p>This is a <b>vital</b> paragraph.</p>
        <pre><code>def test_fn():\n    return 42</code></pre>
        <footer>Copyright 2026</footer>
      </body>
    </html>
    """
    md = clean_html_to_markdown(raw_html)
    assert "alert('noise')" not in md
    assert "body { color: red; }" not in md
    assert "Copyright 2026" not in md
    assert "# Main Architecture" in md
    assert "vital" in md
    assert "def test_fn():" in md


def test_pipeline_unslop_and_gitguardian_detection():
    sloppy_code = """Certainly! Here is the implementation:
# Import statements
import os

// Helper function
def get_secret():
    # OpenAI token
    return "sk-1234567890abcdef1234567890abcdef"

I hope this helps! Feel free to ask more questions.
"""
    res = QualityGatesPipeline.run_pipeline(sloppy_code)

    # 1. Unslop check
    assert res.unslop_applied is True
    assert "Certainly!" not in res.cleaned_code
    assert "I hope this helps!" not in res.cleaned_code

    # 2. GitGuardian Secret Scanner check
    assert len(res.secret_findings) >= 1
    assert any("OpenAI" in f["detail"] for f in res.secret_findings)
    assert res.passed is False  # Blocked due to leaked secret


def test_pipeline_pristine_clean_code():
    clean_code = """
def calculate_hash(data: str) -> str:
    import hashlib
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
"""
    res = QualityGatesPipeline.run_pipeline(clean_code)
    assert res.passed is True
    assert len(res.secret_findings) == 0
    assert res.security_score == 100


def test_alignment_engine():
    blueprint = AlignmentEngine.generate_educational_blueprint("Spring AI chat client", tech_key="spring")
    assert "Spring Boot & Spring AI Architecture" in blueprint
    assert "https://www.youtube.com/watch?v=9SGDpanrc8U" in blueprint
    assert "mermaid" in blueprint

    questions = AlignmentEngine.generate_grill_me_interview("Build payment webhook")
    assert len(questions) == 3
    assert any("deliverable" in q["id"] for q in questions)


def test_transparent_observer():
    obs = TransparentObserver(task_name="Refactor Auth", total_steps=3, verbose=False)
    events = []
    obs.add_listener(lambda e: events.append(e))

    obs.emit("RESEARCH", 1, "Exploring dependencies")
    obs.emit("WORKER", 2, "Writing patch")
    obs.steer("Keep backwards compatibility with v1 API")

    assert len(events) == 3
    assert events[0].phase == "RESEARCH"
    assert events[1].phase == "WORKER"
    assert "Keep backwards compatibility" in obs.get_active_steering()


def test_dashboard_and_feedback(tmp_path, monkeypatch):
    monkeypatch.setattr("aegis.config.get_db_path", lambda: tmp_path / "brain.db")
    monkeypatch.setattr("aegis.dashboard.get_db_path", lambda: tmp_path / "brain.db")

    fb_id = record_feedback("code_quality", 5, "Clean Karpathy simplicity", task_ref="Task #1")
    assert fb_id > 0

    bm_id = record_benchmark("code_graph", tokens_used=120, tokens_saved=4500, latency_ms=18.5)
    assert bm_id > 0

    fbk_id = record_tool_fallback("ast_graph", "ripgrep", reason="File too large")
    assert fbk_id > 0

    summary = get_dashboard_summary()
    assert summary["benchmarks"]["total_runs"] >= 1
    assert summary["benchmarks"]["tokens_saved"] == 4500
    assert len(summary["feedbacks"]) >= 1

    tui = format_dashboard_tui()
    assert "AEGISBRAIN AUTONOMOUS INTELLIGENCE DASHBOARD" in tui
    assert "Tokens Saved:" in tui

    html = render_dashboard_html()
    assert "<!DOCTYPE html>" in html
    assert "4,500" in html
    assert "Clean Karpathy simplicity" in html
