import re
from pathlib import Path

srt_path = Path("P:/open-source/aegis-brain/assets/marketing/linkedin_demo/master_narration.srt")
ass_path = Path("P:/open-source/aegis-brain/assets/marketing/linkedin_demo/master_narration_focus.ass")

def parse_time(t_str):
    # 00:00:07,904 -> seconds
    h, m, s = t_str.strip().split(':')
    s, ms = s.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

def fmt_time(t_sec):
    h = int(t_sec // 3600)
    m = int((t_sec % 3600) // 60)
    s = int(t_sec % 60)
    cs = int(round((t_sec - int(t_sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

# Read SRT entries
with open(srt_path, "r", encoding="utf-8") as f:
    content = f.read()

entries = re.split(r'\n\s*\n', content.strip())
parsed_cues = []

for entry in entries:
    lines = entry.strip().split('\n')
    if len(lines) >= 3:
        idx = lines[0].strip()
        time_match = re.match(r'(\d+:\d+:\d+,\d+)\s*-->\s*(\d+:\d+:\d+,\d+)', lines[1].strip())
        if time_match:
            start_t = parse_time(time_match.group(1))
            end_t = parse_time(time_match.group(2))
            text = " ".join(l.strip() for l in lines[2:])
            parsed_cues.append({
                "idx": idx,
                "start": start_t,
                "end": end_t,
                "text": text
            })

print(f"Parsed {len(parsed_cues)} cues from SRT.")

# ASS Header
ass_header = """[Script Info]
Title: AegisBrain Master Narration Focus Captions
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Segoe UI,32,&H00FFFFFF,&H000000FF,&H00000000,&H900D0E12,1,0,0,0,100,100,0,0,3,4,0,2,60,60,42,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# Generate word-by-word focus events
dialogues = []

for cue in parsed_cues:
    # If during the opening title card (0s to 7.9s), don't render to let title card be pristine
    if cue["end"] <= 8.0:
        continue
    
    start_t = cue["start"]
    end_t = cue["end"]
    # If spans over 8.0, clamp start to 8.0
    if start_t < 8.0:
        start_t = 8.0
        
    dur = end_t - start_t
    words = cue["text"].split()
    if not words:
        continue
        
    # Split long sentence into chunks of 5-8 words so it stays on 1-2 lines
    chunk_size = 7
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(words[i:i+chunk_size])
        
    num_chunks = len(chunks)
    chunk_dur = dur / num_chunks
    
    for c_idx, chunk in enumerate(chunks):
        c_start = start_t + c_idx * chunk_dur
        c_end = c_start + chunk_dur
        word_dur = chunk_dur / len(chunk)
        
        for w_idx in range(len(chunk)):
            w_start = c_start + w_idx * word_dur
            w_end = w_start + word_dur
            
            # Format line: all words white, active word highlighted in bright gold (&H0033EEFF / #FFE333)
            line_parts = []
            for j, w in enumerate(chunk):
                if j == w_idx:
                    line_parts.append(f"{{\\c&H0020E0FF\\b1}}{w}{{\\r}}")
                else:
                    line_parts.append(w)
            line_str = " ".join(line_parts)
            dialogues.append(f"Dialogue: 0,{fmt_time(w_start)},{fmt_time(w_end)},Default,,0,0,0,,{line_str}")

with open(ass_path, "w", encoding="utf-8") as f:
    f.write(ass_header)
    f.write("\n".join(dialogues))
    f.write("\n")

print(f"Generated {len(dialogues)} active-focus word events in {ass_path}")
