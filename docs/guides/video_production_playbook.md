# Deep-Tech Product Demo Video Production Playbook
*A Standardized Engineering Guide for High-Conversion Developer & AI Product Demos*

---

## 1. Architectural Foundation & Design Philosophy

The production pipeline is built on a hybrid of three battle-tested design engines:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           MASTER VIDEO PIPELINE                                 │
├──────────────────────────┬────────────────────────────┬─────────────────────────┤
│ 1. EXPLAINROO EDITORIAL  │ 2. HUASHU ART MOTION VOX   │ 3. ACTIVE FOCUS CAPTIONS│
│    (vincentsch)          │    (alchaincyf Y2 Vox)     │    (Karaoke ASS Engine) │
├──────────────────────────┼────────────────────────────┼─────────────────────────┤
│ • Dark obsidian canvas   │ • Continuous easing zooms  │ • Spoken word glow      │
│   (#0A0B0E / #0E0F14)    │ • Left margin clamp        │   (#FFE020 / amber)     │
│ • Monospace OS telemetry │   (fx=600 anchor)          │ • Inactive words white  │
│ • Official wordmark dot  │ • Dynamic action focal     │ • Charcoal pill pill    │
│ • Concrete metric tiles  │   targets (fy=560..840)    │   background            │
│ • Zero AI marketing slop │ • Corner tape badges (DOC) │ • Clamped bottom margin │
└──────────────────────────┴────────────────────────────┴─────────────────────────┘
```

---

## 2. Step-by-Step Production Workflow

### Step 1: Raw Session Capture
- **Tool**: Recordly / OBS Studio / OS Screen Recorder.
- **Resolution**: 1920x1080 @ 30fps or 60fps (constant framerate).
- **Setup**: High-contrast terminal (e.g. Ghostty / Windows Terminal / Alacritty), dark theme (`#0D0E12`), font size 14–16pt (JetBrains Mono / SF Mono).
- **Execution**: Run the full lifecycle live (startup, prompt typing, subagent orchestration, worker dispatch, test certification, CLI commands, rollback, exit).

### Step 2: Screen Coordinate & Geometry Profiling
*Before editing, calculate exact window boundaries to prevent arbitrary zooms.*
- **Terminal Window Coordinates**:
  - Left edge: $x = 96\text{px}$
  - Text prompt starting column: $x = 115\text{px}$
  - Terminal text width envelope: $x = 115\text{px} \dots 1100\text{px}$
  - Terminal top: $y = 68\text{px}$
  - Terminal bottom: $y = 940\text{px}$
- **Action Focal Points**:
  - Startup & Headers: $y \approx 320\text{px}$
  - Subagent Hierarchy Dispatch: $y \approx 340\text{px}$
  - Pytest Passing Summary & Security Score: $y \approx 560\text{px}$
  - Morning Briefing Table: $y \approx 680\text{px}$
  - Prompt Typing Area: $y \approx 720\text{px}$
  - Worker CLI Code Synthesis: $y \approx 740\text{px}$
  - Standalone CLI Execution: $y \approx 820\text{px}$
  - Snapshot Rollback Execution: $y \approx 840\text{px}$

### Step 3: Script & Master Audio Generation
- **Audio Length**: ~176.40s narration + 7.60s outro fade = 184.00s master timeline.
- **Speech Engine**: ElevenLabs / Edge-TTS / Local TTS with natural pacing, clear technical enunciation, and neutral tone.
- **Alignment**: Generate sentence-level SRT with exact start/end timestamps.

### Step 4: Speed Curve & PTS Retiming
Each video segment slices a raw time window and retimes it to match narration duration:
$$\text{speed} = \frac{\text{raw\_duration}}{\text{target\_duration}}, \quad \text{pts\_mult} = \frac{1.0}{\text{speed}}$$
FFmpeg video filter: `[0:v]setpts=<pts_mult>*PTS,fps=30[speedv]`

### Step 5: Continuous Mathematical Camera Easing (Huashu Art Motion)
Rather than jarring instant jump-cuts, implement smooth 4-phase camera motion:
1. **Lead-in hold**: $1.0\text{s} - 1.5\text{s}$ at $z = 1.0\text{x}$ (overview).
2. **Smooth Push-In**: Linear or cubic ramp to $z_{\max} = 1.70\text{x} \dots 1.80\text{x}$ over $1.2\text{s} - 1.5\text{s}$.
3. **Focal Hold**: Hold on the close-up action for $6.5\text{s} - 17.0\text{s}$.
4. **Smooth Pull-Back**: Return to overview before transition.

FFmpeg `zoompan` formula with clamped bounds:
```python
def make_zoompan_str(c, fps=30, iw=1920, ih=1080):
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
    # Clamp x so left margin (x=96) is never cropped
    x_expr = f"min(max(0,{fx}-(iw/zoom/2)),iw-(iw/zoom))"
    y_expr = f"min(max(0,{fy}-(ih/zoom/2)),ih-(ih/zoom))"
    return f"zoompan=z='{z_expr}':x='{x_expr}':y='{y_expr}':d=1:s={iw}x{ih}:fps={fps}"
```

### Step 6: Active Word-by-Word Focus Captions (Karaoke ASS)
- Convert raw SRT subtitles into Substation Alpha (`.ass`).
- Split sentences into short, readable chunks of 5–8 words.
- In each chunk, interpolate word start/end times and wrap the active word in amber/gold color tags:
  `{\c&H0020E0FF\b1}<active_word>{\r}`
- Subtitle style:
  ```ini
  [V4+ Styles]
  Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
  Style: Default,Segoe UI,32,&H00FFFFFF,&H000000FF,&H00000000,&H900D0E12,1,0,0,0,100,100,0,0,3,4,0,2,60,60,42,1
  ```
- Opening title card (0–8s) is kept clean with zero subtitles.

### Step 7: Unslopped Deep-Tech Title Cards
- Author HTML/CSS with dark grid canvas (`#0A0B0E`), Inter / SF Pro typography, official branding wordmark, OS telemetry badges, and concrete metric boxes.
- Render to 1920x1080 PNG using Headless Microsoft Edge / Chromium:
  ```powershell
  msedge.exe --headless --disable-gpu --screenshot="card.png" --window-size=1920,1080 "card.html"
  ```

### Step 8: Multi-Stream Assembly & Mastering
1. Render each video segment with `zoompan` and overlay transparent tape badges.
2. Concatenate all segments via FFmpeg `concat` demuxer (`-c copy`).
3. Mux master audio and burn active focus captions via `subtitles`:
   ```bash
   ffmpeg -y -i stitched.mp4 -i audio.mp3 -filter_complex "subtitles='path/to/focus.ass',fade=t=out:st=182.5:d=1.5" -c:v libx264 -crf 17 -preset medium -c:a aac -b:a 192k -t 184.0 output.mp4
   ```

---

## 3. Critical Mistakes Encountered & Root-Cause Solutions

| # | Mistake Observed | Root Cause | Exact Solution Applied |
| :- | :--- | :--- | :--- |
| **1** | **Left Margin Cropped & Text Unreadable** | Camera centered at $fx = 720\dots750$ with $z_{\max}=2.0\text{x}$. Viewport started at $x = 270$, truncating columns 1–35 of code and prompts. | **Locked $fx = 600$** with $z_{\max} = 1.70\dots1.80$. Viewport begins at $x = 52$, capturing the red margin, prompt arrows, and 100% of line text. |
| **2** | **Camera Missing Actual Action Areas** | Fixed vertical focus at $fy = 320\dots420$ (top of screen), while prompts were typed at $y = 735$ and commands executed at $y = 840$. | **Targeted Vertical Calibration**: Calibrated each segment's $fy$ to its specific action: typing ($fy=720$), Hermes synthesis ($fy=740$), pytest summary ($fy=560$), CLI ($fy=820$), restore ($fy=840$). |
| **3** | **AI-Slop Marketing Intro Cards** | Rhetorical clickbait questions ("▶ THE CODING AGENT DILEMMA"), generic play badges, and blurry neon glow halos. | **Deep-Tech Architecture Standard**: Replaced with concrete engineering taxonomy: wordmark with `#E11D48` crimson dot, OS telemetry (`SPEC // LINUX • MACOS • WINDOWS // CI 286/286`), title, technical summary, and 4 high-contrast metric tiles. |
| **4** | **Plain / Missing / Overlapping Captions** | Static VTT subtitles covered bottom terminal prompts or were omitted completely. | **Word-by-Word Active Focus ASS**: Spoken words glow in amber/gold (`#FFE020`) on a dark charcoal pill (`&H900D0E12`) at `MarginV=42`. Title card (0–8s) kept clean. |
| **5** | **Abrupt Ending Truncation** | Video stopped abruptly at the beginning of the briefing table, cutting off session end. | **Extended Slice Coverage**: Segment 9 extended through timestamp 1144s (19:04), showing the complete completed tasks, radar news, and prompt return. |
| **6** | **FFmpeg Windows Subtitle Path Parsing** | Colons in Windows paths (`P:\...`) cause FFmpeg filter graph syntax parsing errors. | **Path Escaping**: Convert backslashes to forward slashes and escape the drive colon: `subtitles='P\:/path/to/captions.ass'`. |

---

## 4. Reusable Segment Specification Matrix

Use this matrix as the reference blueprint for future video segments:

| Seg | Name | Raw Slice | Dur (s) | Camera Zoom ($fx, fy, z_{\max}$) | Overlay Type | Target Action Displayed |
| :-: | :--- | :---: | :---: | :--- | :--- | :--- |
| **00** | Intro Architecture Card | Image | 8.0s | Static 1.0x Overview | Explainroo Spec Card | Brand identity, telemetry, key metrics |
| **01** | Session Boot & Amnesia | 5s – 26s | 10.5s | $fx: 600, fy: 320, z: 1.70$ | `DOC 01` Tape Badge | Antigravity CLI startup, bootstrap speed |
| **02** | Pre-Flight & Restore Pt | 26s – 63s | 19.5s | $fx: 600, fy: 380, z: 1.75$ | `DOC 02` Tape Badge | Snapshot create, memory bus ingestion |
| **03** | Redis Limiter Prompt | 135s – 210s | 22.7s | **$fx: 600, fy: 720, z: 1.80$** | `DOC 03` Tape Badge | Prompt typing, sub-second recall output |
| **04** | Agent Hierarchy Triad | 225s – 330s | 21.1s | $fx: 600, fy: 340, z: 1.75$ | `DOC 04` Tape Badge | Tier 1 Manager dispatch to Tier 2 |
| **05** | Hermes Synthesis & Gate | 390s – 525s | 23.2s | **$fx: 600, fy: 740, z: 1.80$** | `DOC 05` Tape Badge | Local worker CLI execution, Lua precision fix |
| **06** | Pytest 11/11 & AST Security| 815s – 910s | 16.6s | **$fx: 600, fy: 560, z: 1.80$** | `DOC 06` Tape Badge | Pytest pass summary, 0 secrets certification |
| **07** | Standalone CLI Suite | 980s – 1060s| 24.6s | **$fx: 600, fy: 820, z: 1.80$** | `DOC 07` Tape Badge | `aegis recall` & `aegis challenge` execution |
| **08** | Snapshot Rollback | 1060s – 1120s| 12.7s | **$fx: 600, fy: 840, z: 1.75$** | `DOC 08` Tape Badge | `aegis restore 1 -f`, 8 files restored |
| **09** | Full Morning Radar Briefing | 1120s – 1144s| 13.5s | **$fx: 600, fy: 680, z: 1.65$** | `DOC 09` Tape Badge | Complete briefing table through 19:04 exit |
| **10** | Launch Outro Card | Image | 11.6s | Static 1.0x Overview | Explainroo Outro Card | `pip install aegis-brain`, GitHub links |

---

## 5. Toolchain & Dependencies

- **FFmpeg 6.0+ / 7.0+** with `libx264`, `libass`, `aac`, and `setpts` support.
- **Python 3.10+** standard library (`re`, `subprocess`, `pathlib`, `shutil`).
- **Headless Chromium / Microsoft Edge** for pixel-accurate title card rasterization.
- **Substation Alpha (.ass) Engine** for karaoke-style word highlighting.
