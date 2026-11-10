import subprocess
from pathlib import Path

raw_video = r"C:\Users\priya\Downloads\export-1794342963909.mp4"
out_dir = Path("P:/open-source/aegis-brain/assets/marketing/linkedin_demo/test_zooms")
out_dir.mkdir(parents=True, exist_ok=True)

# Test Seg 3 (Redis prompt typing & recall, raw: 135s-210s)
# At 150s: prompt is typed at y=720..885, x=115..600
# With zoom=1.75, iw/zoom=1097, ih/zoom=617.
# If fx=644 (so x_min = 644 - 1097/2 = 96, matching left edge of terminal window!)
# And fy=640 (so y_min = 640 - 617/2 = 331, y_max = 948, capturing bottom prompt!)

test_filter = (
    "zoompan=z='if(lte(on,30),1.05,if(lte(on,75),1.05+0.70*((on-30)/45),if(lte(on,500),1.75,if(lte(on,550),1.75-0.70*((on-500)/50),1.05))))':"
    "x='min(max(0,644-(iw/zoom/2)),iw-(iw/zoom))':"
    "y='min(max(0,640-(ih/zoom/2)),ih-(ih/zoom))':"
    "d=1:s=1920x1080:fps=30"
)

out_mp4 = out_dir / "test_seg3_zoom.mp4"
cmd = [
    "ffmpeg", "-y",
    "-ss", "135", "-t", "20",
    "-i", raw_video,
    "-vf", test_filter,
    "-c:v", "libx264", "-crf", "18", "-preset", "fast",
    str(out_mp4)
]
subprocess.run(cmd, check=True)

# Extract test frame at t=5s (during zoom hold)
test_frame = out_dir / "test_seg3_zoomed_frame.png"
subprocess.run(["ffmpeg", "-y", "-ss", "5", "-i", str(out_mp4), "-frames:v", "1", str(test_frame)], check=True)
print("Done rendering test zoom")
