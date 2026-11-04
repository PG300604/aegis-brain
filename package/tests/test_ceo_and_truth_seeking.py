"""Tests for AegisBrain YC CEO Stress-Testing and Anti-Sycophancy Truth-Seeking Protocol."""

import tempfile
from pathlib import Path
from aegis.ceo_stress_test import YCCEOStressTester, CEOCritique
from aegis.truth_seeking import SkepticalTruthReviewer, MistakeLedger, SkepticalAuditResult


def test_ceo_stress_test_leetcode():
    critique = YCCEOStressTester.evaluate("Brave extension to sync LeetCode solutions to GitHub")
    assert isinstance(critique, CEOCritique)
    assert critique.feasibility_score >= 8
    assert critique.risk_level in ["Low", "Medium"]
    assert "LeetCode" in critique.urgent_pain_assessment or "Manifest V3" in critique.why_now_inflection
    assert len(critique.fatal_failure_modes) >= 2
    assert "problems/" in critique.smallest_verifiable_mvp or "Manifest" in critique.smallest_verifiable_mvp

    md = critique.to_markdown()
    assert "# 🏢 YC CEO Ideation & Stress-Test Report" in md
    assert "Feasibility Score" in md


def test_ceo_stress_test_agent():
    critique = YCCEOStressTester.evaluate("Aegis autonomous lightweight CLI agent on drive P")
    assert isinstance(critique, CEOCritique)
    assert critique.feasibility_score >= 7
    assert len(critique.actionable_next_steps) >= 2


def test_truth_reviewer_detects_sycophancy():
    flawed_text = "Everything looks great! All tests pass without checking and no bugs found anywhere."
    res = SkepticalTruthReviewer.audit_proposal_or_code(flawed_text)
    assert isinstance(res, SkepticalAuditResult)
    assert res.sycophancy_detected is True
    assert res.verdict == "REJECT"
    assert any("Sycophantic optimism" in f for f in res.flaws_found)


def test_truth_reviewer_detects_windows_illegal_characters():
    text_with_colon = 'create_file("problems/3551: Minimum Swaps.java")'
    res = SkepticalTruthReviewer.audit_proposal_or_code(text_with_colon)
    assert res.has_critical_flaws is True
    assert res.verdict == "REJECT"
    assert any("illegal character ':'" in f for f in res.flaws_found)


def test_truth_reviewer_detects_trailing_dots():
    text_with_dots = 'write_file("test_code..java")'
    res = SkepticalTruthReviewer.audit_proposal_or_code(text_with_dots)
    assert res.has_critical_flaws is True
    assert any("Trailing double-dots" in f for f in res.flaws_found)


def test_truth_reviewer_detects_requests_dependency():
    text_with_req = "import requests\nresp = requests.get('https://api.github.com')"
    res = SkepticalTruthReviewer.audit_proposal_or_code(text_with_req)
    assert res.verdict in ["WARNING", "REJECT"]
    assert any("urllib" in r for r in res.counter_recommendations)


def test_truth_reviewer_passes_clean_code():
    clean_text = """
import urllib.request
import json

def fetch_data():
    req = urllib.request.Request("https://api.github.com", headers={"User-Agent": "Aegis"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))
"""
    res = SkepticalTruthReviewer.audit_proposal_or_code(clean_text)
    assert res.has_critical_flaws is False
    assert res.sycophancy_detected is False
    assert res.verdict == "VERIFIED_SOUND"


def test_mistake_ledger_init_and_query():
    with tempfile.TemporaryDirectory() as tmpdir:
        ledger_file = Path(tmpdir) / "mistakes.json"
        ledger = MistakeLedger(ledger_path=ledger_file)

        entries = ledger.get_all()
        assert len(entries) >= 4  # Pre-seeded entries

        # Query Windows traps
        win_mistakes = ledger.query_mistakes("windows")
        assert len(win_mistakes) >= 1
        assert any("NTFS" in m.root_cause or "colons" in m.root_cause for m in win_mistakes)

        # Query requests trap
        req_mistakes = ledger.query_mistakes("requests")
        assert len(req_mistakes) >= 1
        assert any("urllib" in m.corrective_action for m in req_mistakes)


def test_mistake_ledger_record_and_recall():
    with tempfile.TemporaryDirectory() as tmpdir:
        ledger_file = Path(tmpdir) / "mistakes.json"
        ledger = MistakeLedger(ledger_path=ledger_file)

        new_entry = ledger.record_mistake(
            task="asyncio socket test",
            mistake_description="Event loop closed prematurely before socket teardown",
            root_cause="Missing await on writer.drain() before writer.close()",
            corrective_action="Always await writer.wait_closed() in finally block",
            tags=["asyncio", "socket", "network"]
        )

        assert new_entry.id.startswith("mistake_")
        matches = ledger.query_mistakes("socket drain")
        assert len(matches) >= 1
        assert matches[0].id == new_entry.id
