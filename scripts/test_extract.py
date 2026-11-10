import subprocess, os

os.makedirs('P:/open-source/aegis-brain/assets/marketing/linkedin_demo/debug_frames', exist_ok=True)
video = r'C:\Users\priya\Downloads\AegisBrain_LinkedIn_Master_Demo_1080p.mp4'
times = [3, 15, 30, 48, 70, 95, 115, 135, 155, 175]
for t in times:
    out = f'P:/open-source/aegis-brain/assets/marketing/linkedin_demo/debug_frames/frame_{t:03d}s.jpg'
    cmd = ['ffmpeg', '-y', '-ss', str(t), '-i', video, '-frames:v', '1', out]
    subprocess.run(cmd, capture_output=True)
print("Done extracting frames")
