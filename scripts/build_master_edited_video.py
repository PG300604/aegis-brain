"""Assemble, edit, and render the master LinkedIn demonstration video.

Pipeline:
- Slices key narrative sections from the user's 19-minute recording.
- Applies crop-to-terminal & zoom-ins to eliminate desktop whitespace.
- Fast-forwards long background thinking/synthesis phases (3x - 7x).
- Overlays transparent floating feature badges with glow effects.
- Concatenates with intro and outro title cards.
- Synchronizes with ChristopherNeural master narration (163.68s).
- Burns in subtitle cards with high-contrast styling.
"""

import os
import subprocess
import time
from pathlib import Path

REPO_ROOT = Path("P:/open-source/aegis-brain")
MARKETING_DIR = REPO_ROOT / "assets" / "marketing" / "linkedin_demo"
EDIT_DIR = MARKETING_DIR / "master_edit"
BADGES_DIR = EDIT_DIR / "badges"

RAW_VIDEO = Path(r"C:\Users\priya\Downloads\export-1794342963909.mp4")
AUDIO_PATH = MARKETING_DIR / "master_narration.mp3"
SUBTITLES_VTT = MARKETING_DIR / "master_narration.vtt"
OUTPUT_MP4 = MARKETING_DIR / "aegis-brain-linkedin-master-edit.mp4"

SEGMENTS = [
    # Seg 0: Intro Card (7.5s)
    {
        "type": "image",
        "file": EDIT_DIR / "intro_card.png",
        "duration": 7.50,
        "out": EDIT_DIR / "seg_00_intro.mp4",
    },
    # Seg 1: Context Amnesia & Antigravity Startup (11.0s)
    # Raw: 00:05 to 00:27 (22s @ 2.0x -> 11.0s)
    {
        "type": "video",
        "start": 5,
        "raw_dur": 22,
        "target_dur": 11.00,
        "speed": 2.0,
        "crop": "crop=1735:975:92:52,scale=1920:1080",
        "badge": BADGES_DIR / "badge_preflight.png",
        "out": EDIT_DIR / "seg_01_startup.mp4",
    },
    # Seg 2: Pre-Flight Briefing & Mock Project Setup (19.5s)
    # Raw: 00:28 to 01:05 (37s @ 1.897x -> 19.5s)
    {
        "type": "video",
        "start": 28,
        "raw_dur": 37,
        "target_dur": 19.50,
        "speed": 37.0 / 19.50,
        "crop": "crop=1550:872:120:60,scale=1920:1080",
        "badge": BADGES_DIR / "badge_preflight.png",
        "out": EDIT_DIR / "seg_02_briefing.mp4",
    },
    # Seg 3: Redis Limiter Prompt & Sub-Second Recall (22.6s)
    # Raw: 02:22 to 03:40 (78s @ 3.451x -> 22.6s)
    {
        "type": "video",
        "start": 142,
        "raw_dur": 78,
        "target_dur": 22.60,
        "speed": 78.0 / 22.60,
        "crop": "crop=1450:815:100:200,scale=1920:1080",
        "badge": BADGES_DIR / "badge_recall.png",
        "out": EDIT_DIR / "seg_03_recall.mp4",
    },
    # Seg 4: 3-Tier Multi-Agent Hierarchy & Hermes CLI (21.2s)
    # Raw: 03:45 to 05:35 (110s @ 5.188x -> 21.2s)
    {
        "type": "video",
        "start": 225,
        "raw_dur": 110,
        "target_dur": 21.20,
        "speed": 110.0 / 21.20,
        "crop": "crop=1500:844:110:70,scale=1920:1080",
        "badge": BADGES_DIR / "badge_triad.png",
        "out": EDIT_DIR / "seg_04_hierarchy.mp4",
    },
    # Seg 5: Hermes Code Synthesis & 4-Stage Quality Gate (23.2s)
    # Raw: 06:30 to 08:45 (135s @ 5.819x -> 23.2s)
    {
        "type": "video",
        "start": 390,
        "raw_dur": 135,
        "target_dur": 23.20,
        "speed": 135.0 / 23.20,
        "crop": "crop=1500:844:110:120,scale=1920:1080",
        "badge": BADGES_DIR / "badge_quality_gate.png",
        "out": EDIT_DIR / "seg_05_quality_gate.mp4",
    },
    # Seg 6: Unit Test Execution & 100% Security Certification (16.6s)
    # Raw: 13:40 to 15:40 (120s @ 7.228x -> 16.6s)
    {
        "type": "video",
        "start": 820,
        "raw_dur": 120,
        "target_dur": 16.60,
        "speed": 120.0 / 16.60,
        "crop": "crop=1450:815:100:100,scale=1920:1080",
        "badge": BADGES_DIR / "badge_pytest.png",
        "out": EDIT_DIR / "seg_06_pytest.mp4",
    },
    # Seg 7: Exiting CLI to Standalone Aegis Tools (24.6s)
    # Raw: 16:20 to 17:40 (80s @ 3.252x -> 24.6s)
    {
        "type": "video",
        "start": 980,
        "raw_dur": 80,
        "target_dur": 24.60,
        "speed": 80.0 / 24.60,
        "crop": "crop=1650:928:92:52,scale=1920:1080",
        "badge": BADGES_DIR / "badge_standalone.png",
        "out": EDIT_DIR / "seg_07_standalone.mp4",
    },
    # Seg 8: Zero-Residue Snapshot Rollback & Briefing (12.0s)
    # Raw: 17:40 to 18:55 (75s @ 6.25x -> 12.0s)
    {
        "type": "video",
        "start": 1060,
        "raw_dur": 75,
        "target_dur": 12.00,
        "speed": 75.0 / 12.00,
        "crop": "crop=1550:872:92:60,scale=1920:1080",
        "badge": BADGES_DIR / "badge_rollback.png",
        "out": EDIT_DIR / "seg_08_rollback.mp4",
    },
    # Seg 9: Outro Card (5.48s)
    {
        "type": "image",
        "file": EDIT_DIR / "outro_card.png",
        "duration": 5.48,
        "out": EDIT_DIR / "seg_09_outro.mp4",
    },
]


def build_segments():
    print("\n--- 1. Rendering All 10 Video Segments ---")
    for idx, seg in enumerate(SEGMENTS):
        out_file = seg["out"]
        print(f"Rendering Segment #{idx}: {out_file.name} (Target: {seg.get('duration', seg.get('target_dur'))}s)...")
        
        if seg["type"] == "image":
            # Image loop to video
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(seg["file"]),
                "-t", str(seg["duration"]),
                "-vf", "fps=30,format=yuv420p,scale=1920:1080",
                "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                str(out_file)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  [OK] Image Segment #{idx} created.")

        elif seg["type"] == "video":
            # Video slice + speedup + crop + badge overlay
            raw_dur = seg["raw_dur"]
            target_dur = seg["target_dur"]
            start = seg["start"]
            crop_flt = seg["crop"]
            speed = seg["speed"]
            pts_mult = 1.0 / speed
            badge = seg["badge"]

            # Filter chain:
            # 1. crop and scale base video to 1920:1080
            # 2. apply setpts to speed up
            # 3. overlay badge at x=1230, y=40
            # 4. set fps=30
            filter_str = (
                f"[0:v]{crop_flt},setpts={pts_mult}*PTS,fps=30[base]; "
                f"[base][1:v]overlay=1230:40:shortest=1[v]"
            )

            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start),
                "-t", str(raw_dur),
                "-i", str(RAW_VIDEO),
                "-loop", "1",
                "-i", str(badge),
                "-filter_complex", filter_str,
                "-map", "[v]",
                "-t", str(target_dur),
                "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                str(out_file)
            ]
            res = subprocess.run(cmd, capture_output=True)
            if out_file.exists() and out_file.stat().st_size > 1000:
                print(f"  [OK] Video Segment #{idx} created: {out_file.stat().st_size:,} bytes")
            else:
                print(f"  [FAIL] Segment #{idx} failed: {res.stderr.decode(errors='ignore')[:300]}")


def stitch_and_master():
    print("\n--- 2. Concatenating Segments ---")
    concat_txt = EDIT_DIR / "concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for seg in SEGMENTS:
            f.write(f"file '{seg['out'].as_posix()}'\n")

    stitched_temp = EDIT_DIR / "stitched_temp.mp4"
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(stitched_temp)
    ]
    subprocess.run(concat_cmd, check=True, capture_output=True)
    print(f"Stitched temporary video created: {stitched_temp.name}")

    print("\n--- 3. Merging Master Audio & Burning Subtitles ---")
    # Using subtitles filter to burn in captions with semi-transparent black pill box
    # On Windows paths, colons and backslashes need proper escaping for ffmpeg filter
    escaped_vtt = SUBTITLES_VTT.as_posix().replace(":", r"\:")
    sub_style = (
        "FontName=Segoe UI,FontSize=10.5,PrimaryColour=&H00FFFFFF,"
        "BackColour=&H90000000,BorderStyle=4,Outline=1,Shadow=0,MarginV=20,Alignment=2"
    )
    video_filter = f"subtitles='{escaped_vtt}':force_style='{sub_style}'"

    master_cmd = [
        "ffmpeg", "-y",
        "-i", str(stitched_temp),
        "-i", str(AUDIO_PATH),
        "-vf", video_filter,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(OUTPUT_MP4)
    ]
    res = subprocess.run(master_cmd, capture_output=True)
    if OUTPUT_MP4.exists() and OUTPUT_MP4.stat().st_size > 1000:
        print(f"\n[SUCCESS] Master Video Created: {OUTPUT_MP4.name} ({OUTPUT_MP4.stat().st_size:,} bytes)!")
    else:
        print(f"\n[FAIL] Master video generation failed: {res.stderr.decode(errors='ignore')[:400]}")


if __name__ == "__main__":
    build_segments()
    stitch_and_master()
