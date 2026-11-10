"""Assemble, edit, and render the master LinkedIn demonstration video.

Key Improvements:
- Fully implements AegisBrain website design language (Japanese craftsmanship / neo-brutalist)
- Replaces generic glowing AI slop with crisp, high-craft HUD telemetry panels
- Integrates native AegisBrain logo (white text + #B91C1C crimson dot) and active daemon badge
- Features live benchmark metrics (92.4% token arbitrage, 18.2ms recall, 286/286 invariants)
- Dynamic zoom-ins on command typing, test results (11/11 passed), and tool outputs
- Solves abrupt ending: Segment 9 captures the complete aegis briefing through 19:04
- Extended 11.6s outro card allows the final CTA to play out smoothly with gentle fade-out
"""

import os
import shutil
import subprocess
import time
from pathlib import Path

REPO_ROOT = Path("P:/open-source/aegis-brain")
MARKETING_DIR = REPO_ROOT / "assets" / "marketing" / "linkedin_demo"
EDIT_DIR = MARKETING_DIR / "master_edit"
HUD_DIR = EDIT_DIR / "hud_overlays"
EDIT_DIR.mkdir(parents=True, exist_ok=True)

RAW_VIDEO = Path(r"C:\Users\priya\Downloads\export-1794342963909.mp4")
AUDIO_PATH = MARKETING_DIR / "master_narration.mp3"
SUBTITLES_VTT = MARKETING_DIR / "master_narration.vtt"
OUTPUT_MP4 = MARKETING_DIR / "aegis-brain-linkedin-master-edit.mp4"
DOWNLOADS_OUTPUT = Path(r"C:\Users\priya\Downloads\AegisBrain_LinkedIn_Master_Demo_1080p.mp4")

# Total Planned Duration: 184.00s (Audio: 176.40s + 7.60s graceful outro hold)
SEGMENTS = [
    # Seg 0: Intro Title Card (8.00s)
    {
        "type": "image",
        "file": EDIT_DIR / "intro_card.png",
        "duration": 8.00,
        "out": EDIT_DIR / "seg_00_intro.mp4",
    },
    # Seg 1: Startup & Context Ingestion (10.50s)
    # Raw: 00:05 to 00:26 (21s @ 2.0x -> 10.5s)
    {
        "type": "video",
        "start": 5,
        "raw_dur": 21,
        "target_dur": 10.50,
        "speed": 21.0 / 10.50,
        "crop": "crop=1600:900:100:60,scale=1920:1080",
        "hud": HUD_DIR / "hud_seg01.png",
        "out": EDIT_DIR / "seg_01_startup.mp4",
    },
    # Seg 2: Mock Project Setup & Pre-Flight Briefing (19.50s)
    # Raw: 00:26 to 01:03 (37s @ 1.897x -> 19.5s)
    {
        "type": "video",
        "start": 26,
        "raw_dur": 37,
        "target_dur": 19.50,
        "speed": 37.0 / 19.50,
        "crop": "crop=1480:832:120:70,scale=1920:1080",
        "hud": HUD_DIR / "hud_seg02.png",
        "out": EDIT_DIR / "seg_02_briefing.mp4",
    },
    # Seg 3: Redis Limiter Prompt & Sub-Second Recall (22.70s)
    # Raw: 02:15 to 03:30 (75s @ 3.304x -> 22.7s)
    # Zoomed into command typing & SQLite FTS5 table
    {
        "type": "video",
        "start": 135,
        "raw_dur": 75,
        "target_dur": 22.70,
        "speed": 75.0 / 22.70,
        "crop": "crop=1400:788:110:140,scale=1920:1080",
        "hud": HUD_DIR / "hud_seg03.png",
        "out": EDIT_DIR / "seg_03_recall.mp4",
    },
    # Seg 4: 3-Tier Multi-Agent Hierarchy & Hermes CLI (21.10s)
    # Raw: 03:45 to 05:30 (105s @ 4.976x -> 21.1s)
    # Zoomed into Hermes CLI command line invocation
    {
        "type": "video",
        "start": 225,
        "raw_dur": 105,
        "target_dur": 21.10,
        "speed": 105.0 / 21.10,
        "crop": "crop=1450:815:100:80,scale=1920:1080",
        "hud": HUD_DIR / "hud_seg04.png",
        "out": EDIT_DIR / "seg_04_hierarchy.mp4",
    },
    # Seg 5: Hermes Code Synthesis & 4-Stage Quality Gate (23.20s)
    # Raw: 06:30 to 08:45 (135s @ 5.819x -> 23.2s)
    # Zoomed into Lua code diff & flaw correction coaching loop
    {
        "type": "video",
        "start": 390,
        "raw_dur": 135,
        "target_dur": 23.20,
        "speed": 135.0 / 23.20,
        "crop": "crop=1450:815:100:120,scale=1920:1080",
        "hud": HUD_DIR / "hud_seg05.png",
        "out": EDIT_DIR / "seg_05_quality_gate.mp4",
    },
    # Seg 6: Unit Test Execution & AST Security Certification (16.60s)
    # Raw: 13:35 to 15:10 (95s @ 5.723x -> 16.6s)
    # Zoomed in tight on pytest: 11 passed in 0.72s
    {
        "type": "video",
        "start": 815,
        "raw_dur": 95,
        "target_dur": 16.60,
        "speed": 95.0 / 16.60,
        "crop": "crop=1350:760:110:180,scale=1920:1080",
        "hud": HUD_DIR / "hud_seg06.png",
        "out": EDIT_DIR / "seg_06_pytest.mp4",
    },
    # Seg 7: Exiting CLI to Standalone Aegis Tools (24.60s)
    # Raw: 16:20 to 17:40 (80s @ 3.252x -> 24.6s)
    # Zoomed in on PowerShell running aegis recall & aegis challenge
    {
        "type": "video",
        "start": 980,
        "raw_dur": 80,
        "target_dur": 24.60,
        "speed": 80.0 / 24.60,
        "crop": "crop=1480:832:100:70,scale=1920:1080",
        "hud": HUD_DIR / "hud_seg07.png",
        "out": EDIT_DIR / "seg_07_standalone.mp4",
    },
    # Seg 8: Zero-Residue Snapshot Rollback (12.70s)
    # Raw: 17:40 to 18:40 (60s @ 4.724x -> 12.7s)
    # Zoomed on snapshot hash & restored 8 files
    {
        "type": "video",
        "start": 1060,
        "raw_dur": 60,
        "target_dur": 12.70,
        "speed": 60.0 / 12.70,
        "crop": "crop=1450:815:100:100,scale=1920:1080",
        "hud": HUD_DIR / "hud_seg08.png",
        "out": EDIT_DIR / "seg_08_rollback.mp4",
    },
    # Seg 9: Full Morning Briefing Dashboard (13.50s)
    # Raw: 18:40 to 19:04.17 (24s @ 1.777x -> 13.5s)
    # Captures the complete aegis briefing output through the end of the video!
    {
        "type": "video",
        "start": 1120,
        "raw_dur": 24,
        "target_dur": 13.50,
        "speed": 24.0 / 13.50,
        "crop": "crop=1480:832:100:80,scale=1920:1080",
        "hud": HUD_DIR / "hud_seg09.png",
        "out": EDIT_DIR / "seg_09_briefing_full.mp4",
    },
    # Seg 10: Master Outro Card (11.60s)
    # Clean holding card with GitHub release, install command, and smooth fade
    {
        "type": "image",
        "file": EDIT_DIR / "outro_card.png",
        "duration": 11.60,
        "out": EDIT_DIR / "seg_10_outro.mp4",
    },
]


def build_segments():
    print("\n--- 1. Rendering All 11 Video Segments ---")
    for idx, seg in enumerate(SEGMENTS):
        out_file = seg["out"]
        target_dur = seg.get("duration", seg.get("target_dur"))
        print(f"Rendering Segment #{idx:02d}: {out_file.name} (Target: {target_dur}s)...")
        
        if seg["type"] == "image":
            # Image loop to video with subtle fade in/out if desired
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
            print(f"  [OK] Image Segment #{idx:02d} created: {out_file.stat().st_size:,} bytes")

        elif seg["type"] == "video":
            # Video slice + speedup + crop + HUD overlay
            raw_dur = seg["raw_dur"]
            start = seg["start"]
            crop_flt = seg["crop"]
            speed = seg["speed"]
            pts_mult = 1.0 / speed
            hud = seg["hud"]

            # Filter chain:
            # 1. Crop and zoom base video, apply setpts speedup
            # 2. Overlay full 1920x1080 transparent HUD at 0:0
            filter_str = (
                f"[0:v]{crop_flt},setpts={pts_mult}*PTS,fps=30[base]; "
                f"[base][1:v]overlay=0:0[v]"
            )

            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start),
                "-t", str(raw_dur),
                "-i", str(RAW_VIDEO),
                "-loop", "1",
                "-i", str(hud),
                "-filter_complex", filter_str,
                "-map", "[v]",
                "-t", str(target_dur),
                "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                str(out_file)
            ]
            res = subprocess.run(cmd, capture_output=True)
            if out_file.exists() and out_file.stat().st_size > 1000:
                print(f"  [OK] Video Segment #{idx:02d} created: {out_file.stat().st_size:,} bytes")
            else:
                print(f"  [FAIL] Segment #{idx:02d} failed: {res.stderr.decode(errors='ignore')[:300]}")


def stitch_and_master():
    print("\n--- 2. Concatenating All Segments ---")
    concat_txt = EDIT_DIR / "concat_list_v2.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for seg in SEGMENTS:
            f.write(f"file '{seg['out'].name}'\n")

    stitched_video = EDIT_DIR / "stitched_v2.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(stitched_video)
    ]
    subprocess.run(cmd_concat, check=True, cwd=str(EDIT_DIR))
    print(f"  [OK] Stitched video created: {stitched_video.stat().st_size:,} bytes")

    print("\n--- 3. Merging Audio Narration & Burning Styled Subtitles ---")
    # Subtitle styling: Neo-brutalist dark semi-transparent pill, crisp white text
    sub_vtt_escaped = str(SUBTITLES_VTT).replace("\\", "/").replace(":", "\\:")
    sub_style = (
        "FontSize=11.5,"
        "FontName=Segoe UI,"
        "PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,"
        "BackColour=&HB0070709,"
        "BorderStyle=4,"
        "MarginV=26,"
        "Alignment=2"
    )
    
    # Filter complex:
    # Burns subtitles, applies smooth 1.5s fade-out at end (around 182.5s -> 184s)
    vf_chain = (
        f"subtitles='{sub_vtt_escaped}':force_style='{sub_style}',"
        f"fade=t=out:st=182.5:d=1.5"
    )

    cmd_master = [
        "ffmpeg", "-y",
        "-i", str(stitched_video),
        "-i", str(AUDIO_PATH),
        "-filter_complex", vf_chain,
        "-c:v", "libx264", "-crf", "17", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k",
        "-t", "184.0",
        str(OUTPUT_MP4)
    ]
    print("Running final encode and mastering...")
    subprocess.run(cmd_master, check=True)
    print(f"  [OK] Master LinkedIn Video created: {OUTPUT_MP4.stat().st_size:,} bytes")

    # Copy to Downloads
    print(f"\n--- 4. Copying to User Downloads: {DOWNLOADS_OUTPUT} ---")
    shutil.copy2(OUTPUT_MP4, DOWNLOADS_OUTPUT)
    print(f"  [OK] Successfully copied to {DOWNLOADS_OUTPUT}")


if __name__ == "__main__":
    t0 = time.time()
    build_segments()
    stitch_and_master()
    elapsed = time.time() - t0
    print(f"\n✨ Video Build Complete in {elapsed:.1f}s!")
