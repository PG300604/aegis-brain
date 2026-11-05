"""Tests for AegisBrain Multi-Modal Sensory Engine & Reel/Social Pipeline."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from aegis.sensory import (
    SensoryArtifact,
    detect_platform,
    extract_audio_and_transcribe,
    extract_media,
    extract_visual_keyframes,
    hunt_gated_resources,
    inculcate_and_evaluate,
    process_sensory_link,
)


def test_detect_platform():
    assert detect_platform("https://www.instagram.com/reel/DC12345/") == "instagram"
    assert detect_platform("https://x.com/karpathy/status/123456789") == "x"
    assert detect_platform("https://twitter.com/sama/status/987654321") == "x"
    assert detect_platform("https://www.reddit.com/r/LocalLLaMA/comments/abc/new_model/") == "reddit"
    assert detect_platform("https://youtu.be/dQw4w9WgXcQ") == "youtube"
    assert detect_platform("https://www.tiktok.com/@creator/video/123") == "tiktok"
    assert detect_platform("https://blog.langchain.dev/agents") == "generic_web"


def test_hunt_gated_resources_comment_trigger():
    artifact = SensoryArtifact(
        url="https://www.instagram.com/reel/XYZ123/",
        platform="instagram",
        author="ai_architect",
        title="Automate Cursor with this new open source harness",
        description="I spent 40 hours building this agent workflow. Comment AGENT below and I will send you the GitHub repo and Notion guide!",
        transcript="Hey guys, comment AGENT below and I will DM you the exact prompt and repo link.",
    )

    with patch("aegis.sensory.fetch_url_content") as mock_fetch:
        mock_fetch.return_value = (
            True,
            "# Awesome Cursor Agent\nFull autonomous loop and instructions.",
        )
        with patch("urllib.request.urlopen") as mock_url:
            mock_resp = MagicMock()
            mock_resp.read.return_value = b'<a class="result__url" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fgithub.com%2Fexample%2Fawesome-agent&rut=1"></a>'
            mock_url.return_value.__enter__.return_value = mock_resp

            urls = hunt_gated_resources(artifact)

    assert artifact.comment_trigger_keyword == "AGENT"
    assert "https://github.com/example/awesome-agent" in artifact.gated_resource_urls
    assert "Awesome Cursor Agent" in artifact.gated_resource_content


def test_inculcate_and_evaluate():
    artifact = SensoryArtifact(
        url="https://youtube.com/shorts/123",
        platform="youtube",
        title="Micro-Agent Swarms with Fast Vector Search",
        transcript="Building decentralized micro-agents using local SQLite and Chroma.",
        gated_resource_content="GitHub repo with 500 stars, contains clean python implementation.",
    )

    evaluation = inculcate_and_evaluate(artifact)
    assert "summary" in evaluation
    assert "keywords" in evaluation
    assert "yc_ceo_feasibility" in evaluation
    ceo = evaluation["yc_ceo_feasibility"]
    assert "strategic_verdict" in ceo
    assert "feasibility_score" in ceo
    assert 1 <= ceo["feasibility_score"] <= 10


def test_process_sensory_link_mocked(tmp_path: Path):
    with patch("aegis.sensory.extract_media") as mock_extract, \
         patch("aegis.sensory.extract_audio_and_transcribe") as mock_audio, \
         patch("aegis.sensory.extract_visual_keyframes") as mock_frames, \
         patch("aegis.sensory.hunt_gated_resources") as mock_hunt:

        mock_art = SensoryArtifact(
            url="https://x.com/example/status/123",
            platform="x",
            title="State of Local Agents",
            transcript="Here is how to run reasoning loops locally.",
            keyframes=[str(tmp_path / "frame_01.png")],
        )
        mock_extract.return_value = mock_art
        mock_audio.return_value = mock_art.transcript
        mock_frames.return_value = mock_art.keyframes
        mock_hunt.return_value = ["https://github.com/example/repo"]

        result = process_sensory_link("https://x.com/example/status/123", output_base=tmp_path)

        assert result["status"] == "success"
        assert result["artifact"]["platform"] == "x"
        assert Path(result["manifest_path"]).exists()

        manifest = json.loads(Path(result["manifest_path"]).read_text(encoding="utf-8"))
        assert manifest["artifact"]["title"] == "State of Local Agents"
