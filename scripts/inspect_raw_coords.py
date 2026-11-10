import subprocess
from pathlib import Path

raw_video = r"C:\Users\priya\Downloads\export-1794342963909.mp4"
out_dir = Path("P:/open-source/aegis-brain/assets/marketing/linkedin_demo/raw_inspection")
out_dir.mkdir(parents=True, exist_ok=True)

# Timestamps to inspect in the raw recording
checkpoints = [
    (10, "raw_seg1_startup.png"),
    (45, "raw_seg2_preflight.png"),
    (150, "raw_seg3_prompt_typing.png"),
    (180, "raw_seg3_recall_response.png"),
    (270, "raw_seg4_hierarchy_agent.png"),
    (450, "raw_seg5_hermes_dispatch.png"),
    (860, "raw_seg6_pytest_output.png"),
    (1000, "raw_seg7_standalone_commands.png"),
    (1090, "raw_seg8_snapshot_restore.png"),
    (1135, "raw_seg9_final_briefing.png"),
]

for t, name in checkpoints:
    out = out_dir / name
    cmd = ["ffmpeg", "-y", "-ss", str(t), "-i", raw_video, "-frames:v", "1", str(out)]
    subprocess.run(cmd, check=True, capture_output=True)

print(f"Extracted {len(checkpoints)} raw frames for coordinate inspection.")
