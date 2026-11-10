"""Assemble, edit, and master the enhanced LinkedIn video using Explainroo & Huashu Art Motion.

Architecture Integration:
1. Explainroo (vincentsch/explainroo):
   - Editorial explainer design: unslopped deep-tech architecture intro card & launch outro card
   - High-readability studio canvas (#0A0B0E), Inter/SF Pro typography, telemetry specs
2. Huashu Art Motion (alchaincyf/huashu-art-motion - Y2 Vox):
   - Dynamic continuous camera movement (ZOOM-IN and ZOOM-OUT) via mathematical easing
   - Calibrated focal points with fx=600 anchor (zero left margin text crop)
   - Targets exact action areas: prompt typing (fy=720), Hermes synthesis (fy=740), pytest output (fy=560), standalone CLI (fy=820), rollback (fy=840)
   - Authentic Vox documentary clippings: corner tape badges (DOC 01-09) and note cards
3. Active Word-by-Word Focus Captions:
   - Word-level synchronization from master_narration_focus.ass
   - Highlights active spoken word in vibrant amber/gold (#FFE020) on charcoal background pill
"""

import os
import shutil
import subprocess
import time
from pathlib import Path

REPO_ROOT = Path("P:/open-source/aegis-brain")
MARKETING_DIR = REPO_ROOT / "assets" / "marketing" / "linkedin_demo"
EDIT_DIR = MARKETING_DIR / "master_edit"
VOX_DIR = EDIT_DIR / "vox_overlays"
EDIT_DIR.mkdir(parents=True, exist_ok=True)

RAW_VIDEO = Path(r"C:\Users\priya\Downloads\export-1794342963909.mp4")
AUDIO_PATH = MARKETING_DIR / "master_narration.mp3"
SUBTITLES_ASS = MARKETING_DIR / "master_narration_focus.ass"
OUTPUT_MP4 = MARKETING_DIR / "aegis-brain-linkedin-master-edit.mp4"
DOWNLOADS_OUTPUT = Path(r"C:\Users\priya\Downloads\AegisBrain_LinkedIn_Master_Demo_1080p.mp4")

# Total Planned Duration: 184.00s (Audio: 176.40s + 7.60s outro music fade-out)
# Terminal bounds: Left=96, Right=1824, Top=68, Bottom=940. Text starts at x=115.
# With fx=600 and z_max=1.75-1.80, window starts around x=52-70, fully capturing the left margin without cropping text.
SEGMENTS = [
    # Seg 0: Explainroo Deep-Tech Architecture Intro Card (8.00s)
    {
        "type": "image",
        "file": EDIT_DIR / "intro_card.png",
        "duration": 8.00,
        "out": EDIT_DIR / "enh_00_intro.mp4",
    },
    # Seg 1: Context Amnesia & Startup (10.50s)
    {
        "type": "video",
        "start": 5,
        "raw_dur": 21,
        "target_dur": 10.50,
        "camera": {
            "t_in": 1.0, "d_in": 1.2, "d_hold": 6.5, "d_out": 1.2,
            "z_base": 1.0, "z_max": 1.70, "fx": 600, "fy": 320
        },
        "overlay": VOX_DIR / "vox_seg01.png",
        "out": EDIT_DIR / "enh_01_startup.mp4",
    },
    # Seg 2: Mock Project Setup & Pre-Flight (19.50s)
    {
        "type": "video",
        "start": 26,
        "raw_dur": 37,
        "target_dur": 19.50,
        "camera": {
            "t_in": 1.5, "d_in": 1.4, "d_hold": 13.0, "d_out": 1.4,
            "z_base": 1.0, "z_max": 1.75, "fx": 600, "fy": 380
        },
        "overlay": VOX_DIR / "vox_seg02.png",
        "out": EDIT_DIR / "enh_02_briefing.mp4",
    },
    # Seg 3: Redis Limiter Prompt Typing & Sub-Second Recall (22.70s)
    # Zooms directly on prompt typing area at fy=720
    {
        "type": "video",
        "start": 135,
        "raw_dur": 75,
        "target_dur": 22.70,
        "camera": {
            "t_in": 1.2, "d_in": 1.5, "d_hold": 17.0, "d_out": 1.5,
            "z_base": 1.0, "z_max": 1.80, "fx": 600, "fy": 720
        },
        "overlay": VOX_DIR / "vox_seg03.png",
        "out": EDIT_DIR / "enh_03_recall.mp4",
    },
    # Seg 4: 3-Tier Multi-Agent Hierarchy Dispatch (21.10s)
    {
        "type": "video",
        "start": 225,
        "raw_dur": 105,
        "target_dur": 21.10,
        "camera": {
            "t_in": 1.5, "d_in": 1.4, "d_hold": 15.0, "d_out": 1.4,
            "z_base": 1.0, "z_max": 1.75, "fx": 600, "fy": 340
        },
        "overlay": VOX_DIR / "vox_seg04.png",
        "out": EDIT_DIR / "enh_04_hierarchy.mp4",
    },
    # Seg 5: Hermes Code Synthesis & 4-Stage Quality Gate (23.20s)
    # Zooms directly on Hermes CLI worker execution at fy=740
    {
        "type": "video",
        "start": 390,
        "raw_dur": 135,
        "target_dur": 23.20,
        "camera": {
            "t_in": 1.5, "d_in": 1.5, "d_hold": 17.0, "d_out": 1.5,
            "z_base": 1.0, "z_max": 1.80, "fx": 600, "fy": 740
        },
        "overlay": VOX_DIR / "vox_seg05.png",
        "out": EDIT_DIR / "enh_05_quality_gate.mp4",
    },
    # Seg 6: Unit Test Execution (11/11 passed) & AST Security (16.60s)
    # Zooms directly on pytest summary and security certification at fy=560
    {
        "type": "video",
        "start": 815,
        "raw_dur": 95,
        "target_dur": 16.60,
        "camera": {
            "t_in": 1.0, "d_in": 1.2, "d_hold": 12.0, "d_out": 1.2,
            "z_base": 1.0, "z_max": 1.80, "fx": 600, "fy": 560
        },
        "overlay": VOX_DIR / "vox_seg06.png",
        "out": EDIT_DIR / "enh_06_pytest.mp4",
    },
    # Seg 7: Standalone Aegis Tools in PowerShell (24.60s)
    # Zooms on aegis recall and challenge typing at fy=820
    {
        "type": "video",
        "start": 980,
        "raw_dur": 80,
        "target_dur": 24.60,
        "camera": {
            "t_in": 1.5, "d_in": 1.5, "d_hold": 18.5, "d_out": 1.5,
            "z_base": 1.0, "z_max": 1.80, "fx": 600, "fy": 820
        },
        "overlay": VOX_DIR / "vox_seg07.png",
        "out": EDIT_DIR / "enh_07_standalone.mp4",
    },
    # Seg 8: Zero-Residue Snapshot Rollback (12.70s)
    # Zooms on aegis restore execution at fy=840
    {
        "type": "video",
        "start": 1060,
        "raw_dur": 60,
        "target_dur": 12.70,
        "camera": {
            "t_in": 1.2, "d_in": 1.2, "d_hold": 8.0, "d_out": 1.2,
            "z_base": 1.0, "z_max": 1.75, "fx": 600, "fy": 840
        },
        "overlay": VOX_DIR / "vox_seg08.png",
        "out": EDIT_DIR / "enh_08_rollback.mp4",
    },
    # Seg 9: Full Morning Briefing Dashboard through 19:04 (13.50s)
    # Displays full briefing table through final session exit
    {
        "type": "video",
        "start": 1120,
        "raw_dur": 24,
        "target_dur": 13.50,
        "camera": {
            "t_in": 1.2, "d_in": 1.2, "d_hold": 9.0, "d_out": 1.2,
            "z_base": 1.0, "z_max": 1.65, "fx": 600, "fy": 680
        },
        "overlay": VOX_DIR / "vox_seg09.png",
        "out": EDIT_DIR / "enh_09_briefing_full.mp4",
    },
    # Seg 10: Explainroo Product Launch Outro Card (11.60s)
    {
        "type": "image",
        "file": EDIT_DIR / "outro_card.png",
        "duration": 11.60,
        "out": EDIT_DIR / "enh_10_outro.mp4",
    },
]


def make_zoompan_str(c, fps=30, iw=1920, ih=1080):
    """Generate mathematical continuous zoom-in and zoom-out expression."""
    t_in = c["t_in"]
    d_in = c["d_in"]
    d_hold = c["d_hold"]
    d_out = c["d_out"]
    z_base = c["z_base"]
    z_max = c["z_max"]
    fx = c["fx"]
    fy = c["fy"]

    n_in_start = int(t_in * fps)
    n_in_end = int((t_in + d_in) * fps)
    n_out_start = int((t_in + d_in + d_hold) * fps)
    n_out_end = int((t_in + d_in + d_hold + d_out) * fps)
    dz = z_max - z_base
    din = max(1, n_in_end - n_in_start)
    dout = max(1, n_out_end - n_out_start)

    z_expr = (
        f"if(lte(on,{n_in_start}),{z_base:.2f},"
        f"if(lte(on,{n_in_end}),{z_base:.2f}+{dz:.2f}*((on-{n_in_start})/{din}),"
        f"if(lte(on,{n_out_start}),{z_max:.2f},"
        f"if(lte(on,{n_out_end}),{z_max:.2f}-{dz:.2f}*((on-{n_out_start})/{dout}),{z_base:.2f}))))"
    )
    # Clamp x so left margin is never cropped
    x_expr = f"min(max(0,{fx}-(iw/zoom/2)),iw-(iw/zoom))"
    y_expr = f"min(max(0,{fy}-(ih/zoom/2)),ih-(ih/zoom))"
    return f"zoompan=z='{z_expr}':x='{x_expr}':y='{y_expr}':d=1:s={iw}x{ih}:fps={fps}"


def build_segments():
    print("\n--- 1. Rendering All 11 Enhanced Video Segments with Calibrated Focal Zoom ---")
    for idx, seg in enumerate(SEGMENTS):
        out_file = seg["out"]
        target_dur = seg.get("duration", seg.get("target_dur"))
        print(f"Rendering Segment #{idx:02d}: {out_file.name} (Target: {target_dur}s)...")

        if seg["type"] == "image":
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
            raw_dur = seg["raw_dur"]
            start = seg["start"]
            speed = raw_dur / target_dur
            pts_mult = 1.0 / speed
            zoompan_filter = make_zoompan_str(seg["camera"])
            overlay_file = seg["overlay"]

            # Filter chain:
            # 1. Speedup raw video slice to exact target duration
            # 2. Dynamic continuous camera zoompan (zoom-in, hold, zoom-out)
            # 3. Overlay transparent Vox documentary evidence PNG
            filter_str = (
                f"[0:v]setpts={pts_mult}*PTS,fps=30[speedv]; "
                f"[speedv]{zoompan_filter}[zoomed]; "
                f"[zoomed][1:v]overlay=0:0[v]"
            )

            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start),
                "-t", str(raw_dur),
                "-i", str(RAW_VIDEO),
                "-loop", "1",
                "-i", str(overlay_file),
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
    print("\n--- 2. Concatenating Enhanced Segments ---")
    concat_txt = EDIT_DIR / "concat_list_enh.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for seg in SEGMENTS:
            f.write(f"file '{seg['out'].name}'\n")

    stitched_video = EDIT_DIR / "stitched_enh.mp4"
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

    print("\n--- 3. Merging Master Audio & Burning Active Word-by-Word Focus Subtitles ---")
    sub_ass_escaped = str(SUBTITLES_ASS).replace("\\", "/").replace(":", "\\:")

    vf_chain = (
        f"subtitles='{sub_ass_escaped}',"
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
    print(f"Running final encode with active-focus subtitles from {SUBTITLES_ASS.name}...")
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
    print(f"\n✨ Enhanced Video Build Complete in {elapsed:.1f}s!")
