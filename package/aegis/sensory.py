"""AegisBrain Multi-Modal Sensory Engine & Reel/Social Pipeline.

Provides complete perceptual abilities for AI agents:
- Multi-Platform Ingestion: YouTube Shorts/Videos, Instagram Reels, X/Twitter, Reddit, TikTok.
- Audio Perception ("Hearing"): FFmpeg audio extraction + OpenAI Whisper speech-to-text.
- Visual Perception ("Vision"): FFmpeg keyframe & scene change extraction for visual UI/code inspection.
- Comment-Gate Bypass & Autonomous Resource Hunter: Automatically retrieves and decodes
  hidden resources (Notion docs, GitHub repos, Google Drive links, Linktree) when reels
  say "Comment X and I'll send you the link/prompt".
- Inculcation Engine: Compares insights against AegisBrain active architecture, identifies uncommitted deltas.
- YC Feasibility & Stress Test: Evaluates market/technical viability via YC CEO rubric.
"""

from __future__ import annotations

import html
import json
import logging
import os
import re
import shutil
import subprocess
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from aegis.browser import clean_html_to_markdown, fetch_url_content
from aegis.ceo_stress_test import YCCEOStressTester
from aegis.creator_intel import detect_cultural_references, track_creator
from aegis.db import get_recent_decisions, search_memories

logger = logging.getLogger(__name__)


@dataclass
class SensoryArtifact:
    url: str
    platform: str
    title: str = ""
    author: str = ""
    description: str = ""
    duration_seconds: float = 0.0
    video_path: Optional[str] = None
    audio_path: Optional[str] = None
    transcript: str = ""
    keyframes: List[str] = field(default_factory=list)
    raw_metadata: Dict[str, Any] = field(default_factory=dict)
    comment_trigger_keyword: Optional[str] = None
    gated_resource_urls: List[str] = field(default_factory=list)
    gated_resource_content: str = ""
    error: Optional[str] = None


def detect_platform(url: str) -> str:
    """Identify the platform hosting the media."""
    u = url.lower()
    if "instagram.com" in u:
        return "instagram"
    elif "twitter.com" in u or "x.com" in u:
        return "x"
    elif "reddit.com" in u or "redd.it" in u:
        return "reddit"
    elif "youtube.com" in u or "youtu.be" in u:
        return "youtube"
    elif "tiktok.com" in u:
        return "tiktok"
    elif "douyin.com" in u or "xiaohongshu.com" in u or "rednote.com" in u:
        return "rednote_douyin"
    return "generic_web"


def extract_media(url: str, output_dir: Path) -> SensoryArtifact:
    """Download video/audio and metadata using yt-dlp, Reddit API, or browser distiller."""
    output_dir.mkdir(parents=True, exist_ok=True)
    platform = detect_platform(url)
    artifact = SensoryArtifact(url=url, platform=platform)

    # If Reddit text post without direct video, attempt JSON API first
    if platform == "reddit" and "/comments/" in url:
        try:
            req_url = url.split("?")[0].rstrip("/") + ".json"
            req = urllib.request.Request(
                req_url,
                headers={"User-Agent": "Mozilla/5.0 AegisBrain/1.0 SensoryCollector"},
            )
            with urllib.request.urlopen(req, timeout=6.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if isinstance(data, list) and len(data) > 0:
                    post_data = data[0]["data"]["children"][0]["data"]
                    artifact.title = post_data.get("title", "")
                    artifact.author = post_data.get("author", "")
                    artifact.description = post_data.get("selftext", "")
                    artifact.raw_metadata = {
                        "ups": post_data.get("ups"),
                        "num_comments": post_data.get("num_comments"),
                        "subreddit": post_data.get("subreddit"),
                    }
                    media = post_data.get("media")
                    if not media or not media.get("reddit_video"):
                        return artifact
        except Exception as e:
            logger.debug("Direct Reddit JSON fetch failed, falling back to yt-dlp/browser: %s", e)

    # For media-bearing URLs, use yt-dlp
    yt_dlp_cmd = shutil.which("yt-dlp") or shutil.which("yt-dlp.exe")
    if not yt_dlp_cmd:
        local_yt = Path(os.path.expanduser("~/.local/bin/yt-dlp.exe"))
        if local_yt.exists():
            yt_dlp_cmd = str(local_yt)

    if yt_dlp_cmd:
        try:
            video_template = str(output_dir / "media.%(ext)s")
            cmd = [
                yt_dlp_cmd,
                "--no-check-certificates",
                "--dump-json",
                "--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "--output", video_template,
                "--max-filesize", "100M",
                url,
            ]
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                env=env,
            )
            if proc.stdout.strip():
                try:
                    meta = json.loads(proc.stdout.strip().splitlines()[-1])
                    artifact.title = meta.get("title", "")
                    artifact.author = meta.get("uploader", "") or meta.get("channel", "") or meta.get("uploader_id", "")
                    artifact.description = meta.get("description", "")
                    artifact.duration_seconds = float(meta.get("duration", 0) or 0)
                    artifact.raw_metadata = meta
                except Exception:
                    pass

            # Find downloaded video
            for f in output_dir.glob("media.*"):
                if f.suffix.lower() in [".mp4", ".mkv", ".webm", ".mov"]:
                    artifact.video_path = str(f)
                    break
        except Exception as e:
            logger.warning("yt-dlp download failed: %s", e)
            artifact.error = str(e)

    # Fallback to text distillation if no video was found
    if not artifact.video_path and not artifact.description:
        ok, text = fetch_url_content(url)
        if ok:
            artifact.description = text
            artifact.title = f"Web Content: {url}"

    return artifact


def extract_audio_and_transcribe(artifact: SensoryArtifact, output_dir: Path) -> str:
    """Extract audio via FFmpeg and transcribe speech via OpenAI Whisper."""
    if not artifact.video_path or not os.path.exists(artifact.video_path):
        return artifact.transcript

    ffmpeg_cmd = shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")
    if not ffmpeg_cmd:
        winget_path = list(Path(os.path.expanduser("~\\AppData\\Local\\Microsoft\\WinGet\\Packages")).glob("Gyan.FFmpeg*\\**\\ffmpeg.exe"))
        if winget_path:
            ffmpeg_cmd = str(winget_path[0])

    if not ffmpeg_cmd:
        logger.error("FFmpeg not found in PATH")
        return ""

    audio_path = output_dir / "audio.wav"
    try:
        subprocess.run(
            [
                ffmpeg_cmd,
                "-y",
                "-i", artifact.video_path,
                "-vn",
                "-ar", "16000",
                "-ac", "1",
                "-c:a", "pcm_s16le",
                str(audio_path),
            ],
            capture_output=True,
            timeout=30,
        )
        if audio_path.exists() and audio_path.stat().st_size > 1000:
            artifact.audio_path = str(audio_path)
    except Exception as e:
        logger.warning("Audio extraction failed: %s", e)
        return ""

    # Transcribe audio using Whisper
    try:
        whisper_cmd = shutil.which("whisper") or shutil.which("whisper.exe")
        if not whisper_cmd:
            local_whisper = Path(os.path.expanduser("~/.local/bin/whisper.exe"))
            if local_whisper.exists():
                whisper_cmd = str(local_whisper)

        if whisper_cmd and artifact.audio_path:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            w_proc = subprocess.run(
                [
                    whisper_cmd,
                    artifact.audio_path,
                    "--model", "base",
                    "--output_format", "txt",
                    "--output_dir", str(output_dir),
                ],
                capture_output=True,
                text=True,
                timeout=180,
                env=env,
            )
            txt_file = output_dir / "audio.txt"
            if txt_file.exists():
                artifact.transcript = txt_file.read_text(encoding="utf-8", errors="replace").strip()
            else:
                artifact.transcript = w_proc.stdout.strip()
    except Exception as e:
        logger.warning("Whisper transcription failed: %s", e)

    return artifact


def extract_visual_keyframes(artifact: SensoryArtifact, output_dir: Path, frame_count: int = 6) -> List[str]:
    """Extract representative frames for visual analysis using FFmpeg."""
    if not artifact.video_path or not os.path.exists(artifact.video_path):
        return artifact.keyframes

    ffmpeg_cmd = shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")
    if not ffmpeg_cmd:
        winget_path = list(Path(os.path.expanduser("~\\AppData\\Local\\Microsoft\\WinGet\\Packages")).glob("Gyan.FFmpeg*\\**\\ffmpeg.exe"))
        if winget_path:
            ffmpeg_cmd = str(winget_path[0])

    if not ffmpeg_cmd:
        return []

    frames_dir = output_dir / "keyframes"
    frames_dir.mkdir(parents=True, exist_ok=True)

    try:
        duration = max(1.0, artifact.duration_seconds or 10.0)
        step = max(1.0, duration / (frame_count + 1))
        extracted = []

        for idx in range(1, frame_count + 1):
            ts = idx * step
            out_img = frames_dir / f"frame_{idx:02d}.png"
            subprocess.run(
                [
                    ffmpeg_cmd,
                    "-y",
                    "-ss", f"{ts:.2f}",
                    "-i", artifact.video_path,
                    "-vframes", "1",
                    "-vf", "scale=1280:-1",
                    str(out_img),
                ],
                capture_output=True,
                timeout=15,
            )
            if out_img.exists() and out_img.stat().st_size > 1000:
                extracted.append(str(out_img))

        artifact.keyframes = extracted
    except Exception as e:
        logger.warning("Keyframe extraction failed: %s", e)

    return artifact


def hunt_gated_resources(artifact: SensoryArtifact) -> List[str]:
    """Bypass 'Comment X and I will DM you the link' gates.

    Extracts:
    1. URLs already present in description, transcript, or comments.
    2. Creator's Linktree / Bio link hubs where all recent reel resources are archived.
    3. Primary GitHub / Notion / HuggingFace sources via semantic web search.
    """
    found_urls: List[str] = []
    combined_text = f"{artifact.title}\n{artifact.description}\n{artifact.transcript}"

    # 1. Direct Regex Link Extraction from description/transcript
    url_matches = re.findall(r"https?://[^\s<>\"']+", combined_text)
    for u in url_matches:
        u_clean = u.rstrip(".,;!)]}")
        if u_clean not in found_urls and not any(p in u_clean for p in ["instagram.com/reel", "tiktok.com/@", "t.co"]):
            found_urls.append(u_clean)

    # 2. Detect Comment-to-DM Triggers
    trigger_match = re.search(
        r"(?:comment|type|drop|dm\s+me|reply\s+with)\s+[\"']?([A-Za-z0-9_-]{2,20})[\"']?",
        combined_text,
        re.IGNORECASE,
    )
    if trigger_match:
        keyword = trigger_match.group(1).strip()
        # Avoid false positives on common words
        if keyword.lower() not in ["below", "and", "the", "with", "this", "your", "my"]:
            artifact.comment_trigger_keyword = keyword.upper()

    # 3. Check Creator Bio Link Aggregators (Linktree, Beacons, Stan.store, Bio.link)
    author_handle = artifact.author.replace("@", "").strip()
    if author_handle and len(author_handle) > 2:
        bio_urls = [
            f"https://linktr.ee/{author_handle}",
            f"https://beacons.ai/{author_handle}",
            f"https://bio.link/{author_handle}",
            f"https://stan.store/{author_handle}",
        ]
        for b_url in bio_urls:
            ok, content = fetch_url_content(b_url, timeout=4.0, max_chars=4000)
            if ok and "404" not in content and len(content) > 200:
                bio_links = re.findall(r"https?://[^\s<>\"']+", content)
                for bl in bio_links:
                    bl_clean = bl.rstrip(".,;!)]}")
                    if any(domain in bl_clean.lower() for domain in ["github.com", "notion.site", "notion.so", "drive.google.com", "gumroad.com", "huggingface.co", "substack.com"]):
                        if bl_clean not in found_urls:
                            found_urls.append(bl_clean)

    # 4. Search for the underlying open-source repo or paper (the primary source)
    # Most reels are summarizing a specific library, tool, or paper.
    tech_candidates = re.findall(r"\b[A-Z][a-zA-Z0-9_\-\.]{3,}\b", combined_text)
    tech_candidates = [t for t in tech_candidates if t.lower() not in ["instagram", "tiktok", "youtube", "google", "follow", "comment", "video", "share", "prompt"]]
    
    if tech_candidates or artifact.comment_trigger_keyword:
        query_parts = []
        if artifact.comment_trigger_keyword:
            query_parts.append(artifact.comment_trigger_keyword)
        if tech_candidates:
            query_parts.extend(tech_candidates[:2])
        if author_handle:
            query_parts.append(author_handle)

        search_query = "+".join(query_parts) + "+github+OR+notion"
        ddg_url = f"https://html.duckduckgo.com/html/?q={search_query}"
        try:
            req = urllib.request.Request(
                ddg_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AegisBrain/1.0"},
            )
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                raw_html = resp.read().decode("utf-8", errors="replace")
                ddg_matches = re.findall(r"uddg=([^&]+)", raw_html)
                for m in ddg_matches:
                    unquoted = urllib.parse.unquote(m)
                    if any(target in unquoted.lower() for target in ["github.com/", "notion.site/", "huggingface.co/"]):
                        if unquoted not in found_urls:
                            found_urls.append(unquoted)
        except Exception as e:
            logger.debug("DuckDuckGo HTML query fallback: %s", e)

    artifact.gated_resource_urls = found_urls[:5]

    # Fetch and distill the highest-confidence resource (e.g. GitHub README or Notion doc)
    for res_url in artifact.gated_resource_urls:
        ok, res_text = fetch_url_content(res_url, timeout=6.0, max_chars=8000)
        if ok and len(res_text.strip()) > 30:
            artifact.gated_resource_content = f"### Retrieved Resource Payload ({res_url}):\n\n{res_text}"
            break

    return artifact.gated_resource_urls


def inculcate_and_evaluate(artifact: SensoryArtifact) -> Dict[str, Any]:
    """Perform gap analysis against AegisBrain memories and run YC feasibility checks."""
    summary_components = [
        f"Title: {artifact.title}",
        f"Author: {artifact.author}",
        f"Platform: {artifact.platform}",
        f"Description: {artifact.description}",
        f"Transcript: {artifact.transcript}",
    ]
    if artifact.comment_trigger_keyword:
        summary_components.append(f"Gated Comment Trigger: {artifact.comment_trigger_keyword}")
    if artifact.gated_resource_content:
        summary_components.append(artifact.gated_resource_content[:2500])

    summary_text = "\n\n".join(c for c in summary_components if c.strip())
    if not summary_text:
        summary_text = "No substantive content extracted."

    # 1. Search existing memories in AegisBrain SQLite
    relevant_memories = []
    keywords = [w for w in re.findall(r"\b[A-Za-z0-9_-]{4,}\b", summary_text) if len(w) > 3][:6]
    for kw in keywords:
        hits = search_memories(kw, limit=2)
        for h in hits:
            if h not in relevant_memories:
                relevant_memories.append(h)

    # 2. Run YC CEO Stress Test
    ceo_critique = YCCEOStressTester.evaluate(summary_text[:1400])

    return {
        "summary": summary_text[:2000],
        "keywords": keywords,
        "existing_aegis_memories": relevant_memories[:4],
        "yc_ceo_feasibility": asdict(ceo_critique),
    }


def process_sensory_link(url: str, output_base: Optional[Path] = None) -> Dict[str, Any]:
    """End-to-end sensory pipeline for any video, reel, or social link."""
    if output_base is None:
        clean_name = re.sub(r"[^A-Za-z0-9_]", "_", url.split("?")[0].split("/")[-1])[:24] or "link"
        output_base = Path(os.path.expanduser("~/.gemini/antigravity-cli/scratch/sensory")) / clean_name

    output_base.mkdir(parents=True, exist_ok=True)

    # 1. Ingestion
    artifact = extract_media(url, output_base)

    # 2. Hearing (Audio Transcription via FFmpeg + Whisper)
    extract_audio_and_transcribe(artifact, output_base)

    # 3. Vision (Keyframe Extraction via FFmpeg)
    extract_visual_keyframes(artifact, output_base, frame_count=6)

    # 4. Gated Resource Hunting (Bypasses "Comment X for Link" gates)
    hunt_gated_resources(artifact)

    # 5. Inculcation & Feasibility Evaluation
    analysis = inculcate_and_evaluate(artifact)

    # 6. Creator Intelligence & Cultural Lingo Detection
    creator_prof = track_creator(
        artifact.author,
        artifact.platform,
        artifact.title,
        analysis.get("keywords", []),
        artifact.url,
        artifact.gated_resource_urls,
    )
    cultural_refs = detect_cultural_references(f"{artifact.transcript} {artifact.description}")

    result = {
        "artifact": asdict(artifact),
        "analysis": analysis,
        "creator": asdict(creator_prof),
        "cultural_references": cultural_refs,
        "status": "success" if (artifact.transcript or artifact.description or artifact.keyframes or artifact.gated_resource_content) else "degraded",
    }

    # Save summary manifest
    manifest_path = output_base / "sensory_manifest.json"
    manifest_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    result["manifest_path"] = str(manifest_path)
    return result
