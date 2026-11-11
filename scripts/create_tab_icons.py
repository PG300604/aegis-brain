import subprocess
from pathlib import Path

WEB_DIR = Path("P:/open-source/aegis-brain/web")
APP_DIR = WEB_DIR / "app"
PUBLIC_DIR = WEB_DIR / "public"
SCRIPTS_DIR = Path("P:/open-source/aegis-brain/scripts")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 1. Favicon SVG for micro-tab resolutions (16x16, 32x32, 64x64)
# High-contrast, thick strokes, centered shield with signature crimson dot
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="100%" height="100%">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0E1017"/>
      <stop offset="100%" stop-color="#050608"/>
    </linearGradient>
    <linearGradient id="border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E11D48" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#222530" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#E11D48" stop-opacity="0.7"/>
    </linearGradient>
  </defs>

  <!-- Background squircle -->
  <rect x="2" y="2" width="124" height="124" rx="28" fill="url(#bg)" stroke="url(#border)" stroke-width="3"/>

  <!-- Centered Aegis Shield & Neural Pulse -->
  <g transform="translate(64, 62)">
    <!-- Aegis Shield Contour -->
    <path d="M 0,-38 L 32,-22 C 32,16 20,38 0,50 C -20,38 -32,16 -32,-22 Z" 
          fill="#13151F" stroke="#FFFFFF" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/>
    
    <!-- Inner Neural Arc -->
    <path d="M -16,-6 C -16,14 0,24 0,32 C 0,24 16,14 16,-6" 
          fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-dasharray="3 3"/>
    
    <!-- Upper Node (White) -->
    <circle cx="0" cy="-6" r="4.5" fill="#FFFFFF"/>
    
    <!-- Signature Crimson Core Pulse Dot -->
    <circle cx="0" cy="12" r="5" fill="#E11D48"/>
  </g>
</svg>"""

def build_icons():
    # Save SVG
    svg_app_path = APP_DIR / "icon.svg"
    svg_public_path = PUBLIC_DIR / "icon.svg"
    svg_app_path.write_text(FAVICON_SVG, encoding="utf-8")
    svg_public_path.write_text(FAVICON_SVG, encoding="utf-8")
    print(f"  [OK] Saved icon.svg to {svg_app_path}")

    # Render PNGs at various resolutions using HTML + Edge headless
    html_content = f"""<!DOCTYPE html>
<html>
<head><style>
  body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; }}
  svg {{ width: 100vw; height: 100vh; display: block; }}
</style></head>
<body>
{FAVICON_SVG}
</body>
</html>"""

    tmp_html = SCRIPTS_DIR / "tmp_icon.html"
    tmp_html.write_text(html_content, encoding="utf-8")

    sizes = [
        ("icon-32.png", 32),
        ("icon-48.png", 48),
        ("icon-64.png", 64),
        ("icon-192.png", 192),
        ("apple-icon.png", 180),
        ("icon-512.png", 512),
    ]

    for name, s in sizes:
        out_png = SCRIPTS_DIR / name
        cmd = [
            EDGE_PATH,
            "--headless",
            "--disable-gpu",
            f"--window-size={s},{s}",
            f"--screenshot={out_png}",
            f"file:///{tmp_html.resolve()}"
        ]
        subprocess.run(cmd, check=True)
        print(f"  [OK] Rendered {name} ({s}x{s})")

    # Copy primary pngs
    icon_png_32 = SCRIPTS_DIR / "icon-32.png"
    apple_png_180 = SCRIPTS_DIR / "apple-icon.png"

    # Copy to app and public
    import shutil
    shutil.copy2(icon_png_32, APP_DIR / "icon.png")
    shutil.copy2(icon_png_32, PUBLIC_DIR / "icon.png")
    shutil.copy2(apple_png_180, APP_DIR / "apple-icon.png")
    shutil.copy2(apple_png_180, PUBLIC_DIR / "apple-icon.png")

    # Generate multi-size favicon.ico using ffmpeg
    # ffmpeg can combine sizes or convert directly to .ico
    ico_target_app = APP_DIR / "favicon.ico"
    ico_target_public = PUBLIC_DIR / "favicon.ico"
    
    cmd_ico = [
        "ffmpeg", "-y",
        "-i", str(SCRIPTS_DIR / "icon-64.png"),
        str(ico_target_app)
    ]
    subprocess.run(cmd_ico, check=True, capture_output=True)
    shutil.copy2(ico_target_app, ico_target_public)
    print(f"  [OK] Generated favicon.ico ({ico_target_app.stat().st_size:,} bytes)")

    if tmp_html.exists():
        tmp_html.unlink()

if __name__ == "__main__":
    build_icons()
