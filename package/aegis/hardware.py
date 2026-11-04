"""Hardware Resource Inspector and Dynamic Model Sizer for AegisBrain.

Inspects system memory (RAM), CPU cores, and hardware limits with zero external dependencies
using Windows ctypes Win32 API and standard library. Dynamically recommends local model tiers
to protect active multitasking (e.g. 8GB VMs, Brave browser tabs, Spotify) from memory bottlenecks.
"""

import os
import sys
import platform
from typing import Dict, Any, Tuple


def get_hardware_status() -> Dict[str, Any]:
    """Inspect total RAM, available RAM, memory load percentage, and CPU cores.
    
    Uses ctypes.windll.kernel32.GlobalMemoryStatusEx on Windows for sub-millisecond,
    zero-dependency memory queries.
    """
    total_ram_gb = 16.0
    avail_ram_gb = 8.0
    load_percent = 50
    cpu_cores = os.cpu_count() or 8

    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", wintypes.DWORD),
                    ("dwMemoryLoad", wintypes.DWORD),
                    ("ullTotalPhys", ctypes.c_uint64),
                    ("ullAvailPhys", ctypes.c_uint64),
                    ("ullTotalPageFile", ctypes.c_uint64),
                    ("ullAvailPageFile", ctypes.c_uint64),
                    ("ullTotalVirtual", ctypes.c_uint64),
                    ("ullAvailVirtual", ctypes.c_uint64),
                    ("ullAvailExtendedVirtual", ctypes.c_uint64),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            kernel32 = ctypes.windll.kernel32
            if kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                total_ram_gb = round(stat.ullTotalPhys / (1024 ** 3), 2)
                avail_ram_gb = round(stat.ullAvailPhys / (1024 ** 3), 2)
                load_percent = int(stat.dwMemoryLoad)
        except Exception:
            pass

    return {
        "platform": platform.platform(),
        "cpu_cores": cpu_cores,
        "total_ram_gb": total_ram_gb,
        "avail_ram_gb": avail_ram_gb,
        "used_ram_gb": round(total_ram_gb - avail_ram_gb, 2),
        "load_percent": load_percent,
    }


def recommend_model_tier(avail_ram_gb: float) -> Tuple[str, str, str]:
    """Recommend local model parameter size and quantization based on available RAM headroom.
    
    Protects 16GB systems running heavy multitasking (VMs, browser, audio players).
    
    Returns:
        (tier_name, model_recommendation, description)
    """
    if avail_ram_gb < 3.5:
        return (
            "MICRO_OR_OFFLOAD",
            "qwen2.5-coder:1.5b-instruct-q4_K_M (or Cloud Offload)",
            f"Available RAM is tight ({avail_ram_gb} GB). Use 1.5B model (~1.2 GB VRAM/RAM) or delegate heavy coding to frontier Manager to prevent system thrashing.",
        )
    elif avail_ram_gb < 6.5:
        return (
            "STANDARD_BALANCED",
            "qwen2.5-coder:7b-instruct-q4_K_M",
            f"Moderate RAM headroom ({avail_ram_gb} GB). 7B Q4 model (~4.5 GB) runs smoothly while preserving memory for Spotify, browser tabs, and IDEs.",
        )
    elif avail_ram_gb < 11.0:
        return (
            "EXPANDED_HIGH_FIDELITY",
            "qwen2.5-coder:14b-instruct-q4_K_M or FreeToken MoE",
            f"Strong RAM headroom ({avail_ram_gb} GB). 14B Q4 model or FreeToken 250B+ MoE edge-caching can execute without bottlenecking.",
        )
    else:
        return (
            "MAXIMUM_LOCAL",
            "qwen2.5-coder:32b or FreeToken 405B MoE",
            f"Abundant RAM headroom ({avail_ram_gb} GB). Full local reasoning models or high-concurrency FreeToken expert caching enabled.",
        )


def format_hardware_report() -> str:
    """Return formatted hardware status and recommendations for CLI or remote view."""
    hw = get_hardware_status()
    tier, rec, desc = recommend_model_tier(hw["avail_ram_gb"])

    lines = [
        "🖥️ *Workstation Hardware & Memory Profile*",
        f"• *Platform:* `{hw['platform']}`",
        f"• *CPU Cores:* {hw['cpu_cores']}",
        f"• *Total RAM:* {hw['total_ram_gb']} GB",
        f"• *Used RAM:* {hw['used_ram_gb']} GB ({hw['load_percent']}%)",
        f"• *Available RAM:* {hw['avail_ram_gb']} GB",
        "",
        f"⚙️ *AegisBrain Model Sizing Recommendation:*",
        f"• *Tier:* `{tier}`",
        f"• *Recommended Model:* `{rec}`",
        f"• *Rationale:* {desc}",
    ]
    return "\n".join(lines)
