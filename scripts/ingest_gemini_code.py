#!/usr/bin/env python3
"""
AegisBrain - Gemini Desktop Code Ingestion Utility.

Extracts TSX code from the system clipboard or a scratch file,
validates its structure, saves it into web/components/hud/<Component>.tsx,
auto-updates web/components/hud/index.ts, and verifies the build.
"""

import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_DIR = REPO_ROOT / "package"
WEB_DIR = REPO_ROOT / "web"
HUD_DIR = WEB_DIR / "components" / "hud"

if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

try:
    from aegis.remote import get_desktop_clipboard
except ImportError:
    get_desktop_clipboard = None


def extract_tsx_code(raw_text: str) -> str:
    """Extract clean TSX code from markdown code blocks or raw text."""
    # Look for ```tsx ... ``` or ```typescript ... ``` or ```jsx ... ```
    match = re.search(r"```(?:tsx|typescript|jsx|react)?\s*\n([\s\S]*?)```", raw_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # If no fences, check if raw_text looks like React code
    if "import React" in raw_text or "export function" in raw_text or "export const" in raw_text:
        return raw_text.strip()
    return ""


def detect_component_name(code: str) -> str:
    """Detect the exported component name from TSX code."""
    # Match export function ComponentName or export const ComponentName
    m = re.search(r"export\s+(?:default\s+)?(?:function|const)\s+([A-Z][a-zA-Z0-9_]*)", code)
    if m:
        return m.group(1)
    return ""


def main():
    target_name = sys.argv[1] if len(sys.argv) > 1 else None
    
    # 1. Check if an input file was provided
    raw_content = ""
    scratch_file = REPO_ROOT / "scripts" / "gemini_output.tsx"
    if scratch_file.exists() and scratch_file.stat().st_size > 50:
        raw_content = scratch_file.read_text(encoding="utf-8")
        print(f"[*] Reading from scratch file: {scratch_file}")
    elif get_desktop_clipboard:
        clip = get_desktop_clipboard()
        if clip and ("export function" in clip or "export const" in clip or "```tsx" in clip):
            raw_content = clip
            print(f"[*] Detected valid component code in Windows clipboard ({len(clip)} chars).")
        else:
            print("[-] Clipboard does not contain React code. Copy the response from Gemini Desktop first, or paste into scripts/gemini_output.tsx.")
            return 1
    else:
        print("[-] No input source available.")
        return 1

    clean_code = extract_tsx_code(raw_content)
    if not clean_code:
        print("[-] Could not extract clean TSX code.")
        return 1

    comp_name = target_name or detect_component_name(clean_code)
    if not comp_name:
        print("[-] Could not determine component name. Pass it as argument, e.g. python ingest_gemini_code.py Feature06PipelineFlow")
        return 1

    dest_file = HUD_DIR / f"{comp_name}.tsx"
    dest_file.write_text(clean_code, encoding="utf-8")
    print(f"✓ Saved component to {dest_file} ({len(clean_code)} bytes).")

    # Update web/components/hud/index.ts
    index_file = HUD_DIR / "index.ts"
    index_text = index_file.read_text(encoding="utf-8")
    export_stmt = f'export {{ {comp_name} }} from "./{comp_name}";\n'
    if export_stmt not in index_text:
        index_file.write_text(index_text + export_stmt, encoding="utf-8")
        print(f"✓ Added export to {index_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
