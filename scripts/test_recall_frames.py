import subprocess, os

video = r'P:\open-source\aegis-brain\assets\marketing\linkedin_demo\master_edit\enh_03_recall.mp4'
os.makedirs('P:/open-source/aegis-brain/assets/marketing/linkedin_demo/debug_recall', exist_ok=True)
for t in [0.5, 3.0, 8.0, 15.0, 21.0]:
    out = f'P:/open-source/aegis-brain/assets/marketing/linkedin_demo/debug_recall/t_{t:.1f}s.jpg'
    cmd = ['ffmpeg', '-y', '-ss', str(t), '-i', video, '-frames:v', '1', out]
    subprocess.run(cmd, capture_output=True)
print("Extracted recall frames")
