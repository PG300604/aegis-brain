#!/usr/bin/env python3
"""AegisBrain - Gemini Desktop Worker Bridge (Gemini 4 Argon Delegation).

Enables Tier 1/2 agents to delegate UI element generation, boilerplate synthesis,
and design components to the locally running Gemini Desktop application on Windows.
Enforces Andrej Karpathy simplicity invariants and Aegis graphic novel aesthetic standards.

Zero external dependencies (pure Python standard library + Win32 ctypes).
"""

import argparse
import ctypes
from ctypes import wintypes
import os
import sys
import time
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

# Ensure aegis package is in sys.path
_PACKAGE_DIR = Path(__file__).resolve().parent.parent / "package"
if str(_PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(_PACKAGE_DIR))

try:
    from aegis.remote import (
        focus_desktop_window,
        copy_to_desktop_clipboard,
        get_desktop_windows,
        get_desktop_clipboard,
    )
except ImportError:
    focus_desktop_window = None
    copy_to_desktop_clipboard = None
    get_desktop_windows = None
    get_desktop_clipboard = None


def format_gemini_ui_prompt(
    element_description: str,
    component_name: str = "Feature06BlueprintCards",
    context: str = "Feature 06: Architectural System Blueprints in AegisBrain",
) -> str:
    """Format a UI generation prompt with strict Andrej Karpathy simplicity invariants,
    high-contrast graphic novel styling rules, and policy-compliant neutral technical phrasing.
    """
    return f"""You are an elite React and Tailwind CSS UI engineer following the Andrej Karpathy Simplicity Doctrine.

Your task is to build a single, self-contained, production-grade React component: `{component_name}`.

=== CONTEXT ===
{context}

=== ELEMENT SPECIFICATION ===
{element_description}

=== STRICT DESIGN & AESTHETIC INVARIANTS ===
1. GRAPHIC NOVEL EDITORIAL AESTHETIC:
   - High-contrast, sharp geometric shapes with crisp lines.
   - Distinct comic plate borders: `border-2 border-black` or `border border-zinc-800`.
   - Hard drop shadows: `shadow-[4px_4px_0px_#000000]` or `shadow-[3px_3px_0px_#B91C1C]`.
   - Sharp corners: prefer `rounded-none`, `rounded-sm`, or `rounded-md` (NEVER bubbly pill shapes).
2. COLOR PALETTE:
   - Deep background: `#070709` or `#101116`
   - High-contrast paper/plate: `#FAF8F5` or `#FBF9F5`
   - Ink black: `#000000` or `#0D0D11`
   - Accent Crimson: `#B91C1C` / `#DC2626`
   - Monochromatic text: text-zinc-100 / text-black / text-zinc-400
3. TYPOGRAPHY:
   - Uppercase monospace category/tag chips: `font-mono text-xs uppercase tracking-widest`.
   - Bold, impactful metric displays and titles.
4. ZERO SLOP:
   - NO rounded pill shapes (`rounded-full` buttons or tags are strictly forbidden).
   - NO generic floating purple/blue SaaS gradients.
   - NO bloated abstraction wrappers or speculative configurability.

=== ANDREJ KARPATHY SIMPLICITY INVARIANTS ===
1. Minimum code that solves the problem. Nothing speculative.
2. Self-contained in a single TSX file with clean TypeScript interface.
3. No single-use abstractions or helper functions.
4. Use standard `lucide-react` icons.
5. If stateful or interactive, mark with `"use client";`.

=== OUTPUT REQUIREMENT ===
Output ONLY the clean, self-contained TSX code inside a single ```tsx code block.
Do NOT include polite greetings, explanations, comments about how great the code is, or summary text.
"""


def click_window_input(
    hwnd: int, relative_x_ratio: float = 0.5, bottom_offset_px: int = 75
) -> bool:
    """Simulate a mouse click inside the lower input area of a window."""
    if sys.platform != "win32":
        return False
    try:
        user32 = ctypes.windll.user32
        rect = wintypes.RECT()
        if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return False

        width = rect.right - rect.left
        height = rect.bottom - rect.top
        if width <= 0 or height <= 0:
            return False

        target_x = rect.left + int(width * relative_x_ratio)
        target_y = rect.bottom - bottom_offset_px

        # Move cursor and simulate left click
        user32.SetCursorPos(target_x, target_y)
        time.sleep(0.06)
        user32.mouse_event(0x0002, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
        time.sleep(0.05)
        user32.mouse_event(0x0004, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
        time.sleep(0.06)
        return True
    except Exception:
        return False


def simulate_paste_and_enter(press_enter: bool = True, clear_input: bool = True) -> bool:
    """Simulate Ctrl+A -> Backspace, then Ctrl+V, and optional Enter keystrokes using hardware scan codes."""
    if sys.platform != "win32":
        return False
    try:
        user32 = ctypes.windll.user32
        scan_ctrl = user32.MapVirtualKeyW(0x11, 0)
        scan_a = user32.MapVirtualKeyW(0x41, 0)
        scan_backspace = user32.MapVirtualKeyW(0x08, 0)
        scan_v = user32.MapVirtualKeyW(0x56, 0)
        scan_enter = user32.MapVirtualKeyW(0x0D, 0)

        # Clear existing text if requested (Ctrl+A -> Backspace)
        if clear_input:
            user32.keybd_event(0x11, scan_ctrl, 0, 0)
            user32.keybd_event(0x41, scan_a, 0, 0)
            time.sleep(0.05)
            user32.keybd_event(0x41, scan_a, 0x0002, 0)
            user32.keybd_event(0x11, scan_ctrl, 0x0002, 0)
            time.sleep(0.08)
            user32.keybd_event(0x08, scan_backspace, 0, 0)
            time.sleep(0.05)
            user32.keybd_event(0x08, scan_backspace, 0x0002, 0)
            time.sleep(0.12)

        # Press Ctrl+V
        user32.keybd_event(0x11, scan_ctrl, 0, 0)
        user32.keybd_event(0x56, scan_v, 0, 0)
        time.sleep(0.06)
        user32.keybd_event(0x56, scan_v, 0x0002, 0)
        user32.keybd_event(0x11, scan_ctrl, 0x0002, 0)
        time.sleep(0.20)

        # Press Enter if requested
        if press_enter:
            user32.keybd_event(0x0D, scan_enter, 0, 0)
            time.sleep(0.05)
            user32.keybd_event(0x0D, scan_enter, 0x0002, 0)
            time.sleep(0.08)

        return True
    except Exception:
        return False


def delegate_to_gemini_desktop(
    prompt: str,
    window_title: str = "Gemini",
    press_enter: bool = True,
    click_input: bool = True,
) -> Tuple[bool, str]:
    """Activate the Gemini Desktop window, copy prompt to clipboard,

    paste with Ctrl+V, and press Enter to generate UI code via Gemini 4 Argon.
    """
    if sys.platform != "win32":
        return False, "Gemini Desktop automation bridge requires Windows host."

    if copy_to_desktop_clipboard is None or focus_desktop_window is None:
        return False, "Aegis remote automation module not available."

    # 1. Copy prompt to clipboard
    if not copy_to_desktop_clipboard(prompt):
        return False, "Failed to copy prompt to workstation clipboard."

    # 2. Find and focus Gemini Desktop window
    ok_focus, focus_msg = focus_desktop_window(window_title)
    if not ok_focus:
        return False, f"Could not focus '{window_title}' window. {focus_msg}"

    # Allow window manager to complete transition
    time.sleep(0.25)

    # 3. Obtain HWND of the focused window
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()

    # 4. Click input box if enabled
    if click_input and hwnd:
        click_window_input(hwnd, relative_x_ratio=0.5, bottom_offset_px=75)
        time.sleep(0.15)

    # 5. Paste prompt and optionally press Enter
    ok_keys = simulate_paste_and_enter(press_enter=press_enter)
    if not ok_keys:
        return False, "Failed to simulate Ctrl+V / Enter keystrokes."

    action = "Typed and submitted" if press_enter else "Pasted into input box"
    return True, f"{action} in Gemini Desktop ({focus_msg}). Prompt size: {len(prompt)} chars."


def main():
    parser = argparse.ArgumentParser(
        description="AegisBrain - Gemini Desktop UI Generation Bridge"
    )
    parser.add_argument(
        "description",
        nargs="?",
        default="A refined graphic novel stats badge and invariant card for Feature 06: Master Architectural Blueprints. Displays key metrics (Speed: 1.8s, Cost Saved: 95.8%, Neural Latency: 24ms, Tests: 286/286) with sharp hard drop-shadows, paper-plate contrast, and 4 core mathematical invariants.",
        help="Description of the UI element to generate.",
    )
    parser.add_argument(
        "--component",
        "-c",
        default="Feature06StatsBadge",
        help="Component name (default: Feature06StatsBadge)",
    )
    parser.add_argument(
        "--context",
        default="Feature 06: Master Architectural Blueprints in AegisBrain",
        help="Context section or feature description.",
    )
    parser.add_argument(
        "--preview",
        "-p",
        action="store_true",
        help="Preview formatted prompt only (no desktop keystrokes)",
    )
    parser.add_argument(
        "--copy-only",
        action="store_true",
        help="Format and copy to clipboard only (no focus or keystrokes)",
    )
    parser.add_argument(
        "--no-enter",
        action="store_true",
        help="Paste prompt into Gemini Desktop but do NOT press Enter",
    )
    parser.add_argument(
        "--no-click",
        action="store_true",
        help="Skip clicking into input box before pasting",
    )
    parser.add_argument(
        "--window",
        default="Gemini",
        help="Desktop window title to focus (default: Gemini)",
    )

    args = parser.parse_args()

    prompt = format_gemini_ui_prompt(
        element_description=args.description,
        component_name=args.component,
        context=args.context,
    )

    if args.preview:
        print("=== FORMATTED GEMINI PROMPT ===")
        print(prompt)
        print("===============================")
        return 0

    if args.copy_only:
        if copy_to_desktop_clipboard and copy_to_desktop_clipboard(prompt):
            print(f"✓ Copied prompt to clipboard ({len(prompt)} chars).")
            return 0
        else:
            print("❌ Failed to copy to clipboard.")
            return 1

    print(f"[*] Dispatching UI generation task to Gemini Desktop ('{args.window}')...")
    ok, msg = delegate_to_gemini_desktop(
        prompt=prompt,
        window_title=args.window,
        press_enter=not args.no_enter,
        click_input=not args.no_click,
    )

    if ok:
        print(f"✓ {msg}")
        return 0
    else:
        print(f"❌ {msg}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
