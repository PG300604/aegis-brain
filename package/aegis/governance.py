"""User Model Governance, Dynamic Resource Sizing & Transparent Telemetry Controls.

Gives users complete sovereignty and customization over:
1. Manager Model: Frontier high-reasoning orchestrator (Gemini 3.8 Flash High, Claude 3.7/Opus, GPT-6 Codex, Custom).
2. Worker Model: Local efficient code synthesizer (Qwen 2.5 Coder 7B/14B, DeepSeek R1, FreeToken 250B+ MoE, Ollama).
3. Resource Limits: Dynamic RAM caps ensuring Spotify, Brave tabs, and 8GB VMs never freeze.
4. Transparent Opt-In Telemetry: Strict default-deny. Clear terms & conditions explaining zero code/prompt leakage.
5. Self-Healing & Diagnostic Feedback: Automatic error tracking with developer reporting.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from .config import get_aegis_dir
from .hardware import get_hardware_status, recommend_model_tier


def get_governance_path() -> Path:
    return get_aegis_dir() / "governance.json"


DEFAULT_GOVERNANCE: Dict[str, Any] = {
    "manager_model": "gemini-3.8-flash-high",
    "manager_provider": "google-antigravity",
    "manager_api_url": "",
    "worker_model": "auto",
    "worker_provider": "ollama",
    "freetoken_endpoint": "http://127.0.0.1:8000/v1",
    "auto_ram_sizing": True,
    "max_ram_budget_gb": 4.5,
    "max_moe_ram_gb": 7.5,
    "model_dir": "P:\\aegis-models" if Path("P:/").exists() else "",
    "telemetry_enabled": False,
    "telemetry_acknowledged": False,
    "self_healing": True,
    "reporting_target": "github",
}


def load_governance_config() -> Dict[str, Any]:
    p = get_governance_path()
    if p.exists():
        try:
            loaded = json.loads(p.read_text(encoding="utf-8"))
            cfg = dict(DEFAULT_GOVERNANCE)
            cfg.update(loaded)
            return cfg
        except Exception:
            pass
    return dict(DEFAULT_GOVERNANCE)


def save_governance_config(cfg: Dict[str, Any]) -> None:
    p = get_governance_path()
    p.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def get_active_worker_model() -> str:
    """Return the active worker model, resolving 'auto' via live hardware inspection."""
    cfg = load_governance_config()
    model = cfg.get("worker_model", "auto")
    if model == "auto":
        hw = get_hardware_status()
        _, rec, _ = recommend_model_tier(hw["avail_ram_gb"])
        return rec.split()[0]
    return model


def get_telemetry_terms() -> str:
    """Clear, transparent disclosure of AegisBrain telemetry policy."""
    return (
        "📜 *AegisBrain Transparent Telemetry Policy:*\n\n"
        "🔒 *Strict Zero-Leakage Guarantee:*\n"
        "• We *NEVER* collect, log, or transmit your code, prompts, git commits, or file contents.\n"
        "• We *NEVER* access API keys, passwords, authentication PINs, or confidential paths.\n\n"
        "📊 *What Telemetry Collects (ONLY IF EXPLICITLY OPTED IN):*\n"
        "• Model latency and token arbitrage efficiency ratios.\n"
        "• Anonymized tool error codes to improve self-healing and bug-fixing recipes.\n"
        "• Feature adoption metrics (e.g. whether FreeToken MoE co-execution succeeded on your hardware).\n\n"
        "⚙️ *Current Default:* `DISABLED (OFF)`\n"
        "To toggle: Send `/config telemetry on` or run `aegis config --telemetry on`."
    )


def format_governance_status() -> str:
    """Format user governance settings and current model orchestration pipeline."""
    cfg = load_governance_config()
    hw = get_hardware_status()
    active_worker = get_active_worker_model()
    tier, _, _ = recommend_model_tier(hw["avail_ram_gb"])

    telem_status = "🟢 ENABLED (Opted-in)" if cfg.get("telemetry_enabled") else "🔴 DISABLED (Default-Deny)"
    healing_status = "🟢 ACTIVE" if cfg.get("self_healing") else "⚪ OFF"
    auto_ram = "🟢 AUTO-SIZING (Active)" if cfg.get("auto_ram_sizing") else f"Fixed ({cfg.get('max_ram_budget_gb')} GB)"
    from .config import get_model_dir
    active_model_dir = cfg.get("model_dir") or str(get_model_dir())

    lines = [
        "👑 *AegisBrain Model Governance & Orchestration*",
        f"• *Manager (Boss):* `{cfg.get('manager_model')}` ({cfg.get('manager_provider')})",
        f"• *Worker (Synthesizer):* `{active_worker}` (Config: `{cfg.get('worker_model')}`)",
        f"• *Worker Backend:* `{cfg.get('worker_provider')}`",
        f"• *Model Storage Drive:* `{active_model_dir}`",
        f"• *MoE Memory Cap:* `{cfg.get('max_moe_ram_gb', 7.5)} GB` (Lightweight FreeToken Mode)",
        f"• *FreeToken Endpoint:* `{cfg.get('freetoken_endpoint')}`",
        "",
        "🛡️ *Resource & Privacy Governance:*",
        f"• *RAM Governor:* {auto_ram} [Current Tier: `{tier}`]",
        f"• *Available RAM Headroom:* {hw['avail_ram_gb']} GB (Protected for VM/Brave/Spotify)",
        f"• *Self-Healing Engine:* {healing_status}",
        f"• *Anonymous Telemetry:* {telem_status}",
        "",
        "💡 *Customization Shortcuts (via CLI or Telegram):*",
        "• `/config manager <model>` - Set Manager (e.g. `gemini-3.8-flash-high`, `claude-3-7-sonnet`, `gpt-6`)",
        "• `/config worker <model>` - Set Worker (`auto`, `qwen2.5-coder:7b`, `deepseek-r1:7b`)",
        "• `/config model_dir <path>` - Set model storage disk (e.g. `P:\\aegis-models`)",
        "• `/config moe_ram <gb>` - Set max RAM for lightweight MoE (default: `7.5`)",
        "• `/config telemetry <on|off>` - Toggle opt-in telemetry",
    ]
    return "\n".join(lines)
