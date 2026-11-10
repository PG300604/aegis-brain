import subprocess
from pathlib import Path
import shutil

VIDEO = Path("P:/open-source/aegis-brain/assets/marketing/linkedin_demo/aegis-brain-linkedin-master-edit.mp4")
ARTIFACT_DIR = Path("C:/Users/priya/.gemini/antigravity-cli/brain/bf289319-8249-4711-9087-6c6a28d79662")

FRAMES = [
    {"name": "final_frame_01_intro_spec.png", "t": "4.0", "label": "Deep-Tech Spec Intro Card (Unslopped)"},
    {"name": "final_frame_02_prompt_typing_zoom.png", "t": "45.0", "label": "Zoom on Prompt Typing (Readable Text & Left Margin)"},
    {"name": "final_frame_03_pytest_verified_zoom.png", "t": "120.0", "label": "Zoom on Pytest 11/11 Passed & AST Certification"},
    {"name": "final_frame_04_standalone_tools_zoom.png", "t": "145.0", "label": "Zoom on Standalone Aegis CLI in PowerShell"},
    {"name": "final_frame_05_snapshot_restore_zoom.png", "t": "160.0", "label": "Zoom on Snapshot Rollback"},
    {"name": "final_frame_06_morning_briefing_full.png", "t": "170.0", "label": "Full Morning Radar Briefing through 19:04"},
    {"name": "final_frame_07_outro_launch.png", "t": "180.0", "label": "Open Source Launch Outro Card"},
]

def export_frames():
    if not VIDEO.exists():
        print(f"Video {VIDEO} does not exist yet!")
        return
    for item in FRAMES:
        out_path = ARTIFACT_DIR / item["name"]
        cmd = [
            "ffmpeg", "-y",
            "-ss", item["t"],
            "-i", str(VIDEO),
            "-frames:v", "1",
            "-q:v", "2",
            str(out_path)
        ]
        subprocess.run(cmd, capture_output=True)
        if out_path.exists():
            print(f"  [OK] Exported {item['name']} ({item['label']}): {out_path.stat().st_size:,} bytes")
        else:
            print(f"  [FAIL] Failed to export {item['name']}")

if __name__ == "__main__":
    export_frames()
