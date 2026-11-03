"""Generate Anti-Slop Visual Assets via OpenHiggsfield API.

Uses the OpenHiggsfield generation bridge with calibrated anti-slop prompts
(industrial design photography, Dieter Rams minimalism, macro tactile materials,
zero holographic blur, zero purple glow) across Flux 2, Seedance 2.5, and Recraft 4.1.
"""

import argparse
import sys
from pathlib import Path

# Add package to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "package"))

from aegis.media import generate_media

ANTI_SLOP_PROMPTS = {
    "hero_hardware": (
        "Industrial design studio photograph of a minimal matte black anodized aluminum neural coprocessor unit "
        "sitting on a dark slate workbench. Precision laser-engraved typography reads 'AEGIS BRAIN'. "
        "A tiny monochromatic e-ink status display shows 'WAL: 0.8ms' and 'TOKENS: 382'. "
        "Top-down 45-degree isometric angle, sharp macro focus, tactile bead-blasted metal texture, "
        "diffused neutral studio softbox lighting, 8k resolution, photorealistic, Dieter Rams industrial minimalism, "
        "no neon glow, no purple gradients, no floating holograms, no fantasy tropes."
    ),
    "hud_telemetry": (
        "Crisp macro view of a high-contrast dark monospace terminal interface on an OLED display. "
        "White and subtle amber text displaying active context telemetry: 'DATABASE: brain.db | WAL MODE: ACTIVE'. "
        "Shallow depth of field, sharp subpixel rendering, real optical glass reflection, ultra-realistic."
    ),
    "demo_video": (
        "Slow cinematic camera pan across a precision milled aluminum desktop hardware bus with soft diffused "
        "edge lighting. Subtle amber status LED pulses once per second. High production value, 4k 60fps."
    ),
}


def main():
    parser = argparse.ArgumentParser(description="Generate anti-slop media assets for AegisBrain")
    parser.add_argument("--preset", default="hero_hardware", choices=list(ANTI_SLOP_PROMPTS.keys()))
    parser.add_argument("--model", default="flux-2", help="Model name (e.g. flux-2, recraft-4.1, seedance-2.5, kling-3)")
    parser.add_argument("--ratio", default="16:9", choices=["16:9", "9:16", "1:1"])
    args = parser.parse_args()

    prompt = ANTI_SLOP_PROMPTS[args.preset]
    print("=" * 60)
    print("AegisBrain Anti-Slop Asset Generator (OpenHiggsfield)")
    print("=" * 60)
    print(f"Preset: {args.preset}")
    print(f"Model:  {args.model}")
    print(f"Prompt:\n  {prompt}\n")

    result = generate_media(model=args.model, prompt=prompt, aspect_ratio=args.ratio)
    print(f"Status: {result.get('status', 'unknown').upper()}")
    if "images" in result:
        for img in result["images"]:
            print(f"Image URL: {img.get('url')}")
    if "video" in result:
        print(f"Video URL: {result['video'].get('url')}")
    if "message" in result:
        print(f"Note: {result['message']}")


if __name__ == "__main__":
    main()
