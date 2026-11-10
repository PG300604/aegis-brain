import subprocess

ass_file = r"P:\open-source\aegis-brain\assets\marketing\linkedin_demo\master_narration_focus.ass"
# Escape for ffmpeg: P\:/...
ass_escaped = str(ass_file).replace("\\", "/").replace(":", r"\:")

cmd = [
    "ffmpeg", "-y",
    "-ss", "9", "-t", "3",
    "-i", r"P:\open-source\aegis-brain\assets\marketing\linkedin_demo\master_edit\stitched_enh.mp4",
    "-vf", f"subtitles='{ass_escaped}'",
    "-c:v", "libx264", "-crf", "18", "-preset", "fast",
    r"P:\open-source\aegis-brain\assets\marketing\linkedin_demo\test_zooms\test_focus_stitched.mp4"
]
subprocess.run(cmd, check=True)

out_frame = r"C:\Users\priya\.gemini\antigravity-cli\brain\bf289319-8249-4711-9087-6c6a28d79662\test_focus_stitched_frame.png"
subprocess.run(["ffmpeg", "-y", "-ss", "0.8", "-i", r"P:\open-source\aegis-brain\assets\marketing\linkedin_demo\test_zooms\test_focus_stitched.mp4", "-frames:v", "1", out_frame], check=True)
print("Focus caption frame extracted successfully")
