"""Tests for Creator Intelligence, Cultural Lingo & Community Radar."""

from unittest.mock import MagicMock, patch

from aegis.creator_intel import (
    NERD_LEXICON,
    detect_cultural_references,
    get_all_tracked_creators,
    radar_sweep,
    scrape_tech_subreddit,
    track_creator,
)


def test_detect_cultural_references():
    text = "Bro is literally vibe coding on an Arch Linux setup saying i use arch btw and complaining about AI slop."
    refs = detect_cultural_references(text)
    terms = [r["term"] for r in refs]
    assert "i use arch btw" in terms
    assert "vibe coding" in terms
    assert "slop" in terms


def test_track_creator_and_retrieve():
    prof = track_creator(
        handle="karpathy",
        platform="youtube",
        title="Building LLMs from Scratch",
        topics=["llm", "neural_networks", "python"],
        link="https://youtu.be/kCc8FmEb1nY",
    )
    assert prof.handle == "karpathy"
    assert prof.videos_count >= 1
    assert "llm" in prof.topics

    all_creators = get_all_tracked_creators()
    handles = [c.handle for c in all_creators]
    assert "karpathy" in handles


def test_scrape_tech_subreddit_mocked():
    sample_json = {
        "data": {
            "children": [
                {
                    "data": {
                        "title": "New 7B model beats 70B on coding benchmarks",
                        "permalink": "/r/LocalLLaMA/comments/1234/test",
                        "score": 420,
                        "selftext": "Benchmark results and quant comparison...",
                    }
                }
            ]
        }
    }
    with patch("urllib.request.urlopen") as mock_url:
        mock_resp = MagicMock()
        mock_resp.read.return_value = bytes(__import__("json").dumps(sample_json), "utf-8")
        mock_url.return_value.__enter__.return_value = mock_resp

        trends = scrape_tech_subreddit("LocalLLaMA", limit=1)
        assert len(trends) == 1
        assert "New 7B model" in trends[0]["title"]
        assert trends[0]["score"] == 420
