import os
from pathlib import Path

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_OPEN_SOURCE_ROOT = Path("P:/open-source")


def get_aegis_dir() -> Path:
    env_dir = os.environ.get("AEGIS_DIR")
    if env_dir:
        p = Path(env_dir)
    else:
        p = Path.home() / ".aegis-brain"
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_db_path() -> Path:
    return get_aegis_dir() / "brain.db"


def get_active_context_path() -> Path:
    return get_aegis_dir() / "ACTIVE_CONTEXT.md"


def get_mode_file() -> Path:
    return get_aegis_dir() / "mode.txt"


def get_model_dir() -> Path:
    """Return model storage directory. Defaults to P:/aegis-models if Drive P exists, else ~/.aegis-brain/models."""
    env_models = os.environ.get("AEGIS_MODEL_DIR")
    if env_models:
        p = Path(env_models)
    elif Path("P:/").exists():
        p = Path("P:/aegis-models")
    else:
        p = get_aegis_dir() / "models"
    p.mkdir(parents=True, exist_ok=True)
    return p


def set_model_dir(target_dir: str) -> Path:
    """Configure custom model storage drive/directory for local worker models."""
    p = Path(target_dir).resolve()
    p.mkdir(parents=True, exist_ok=True)
    os.environ["AEGIS_MODEL_DIR"] = str(p)
    return p


# Module-level aliases for backwards compatibility
@property
def DB_PATH() -> Path:
    return get_db_path()


def get_execution_mode_file() -> Path:
    return get_aegis_dir() / "execution_mode.txt"


def get_execution_mode() -> str:
    """Return execution mode: 'auto' (Dual NLP Auto-Triage, default), 'arbitrage', or 'fast'."""
    env_mode = os.environ.get("AEGIS_EXECUTION_MODE")
    if env_mode in ("auto", "adaptive", "arbitrage", "fast"):
        return "auto" if env_mode == "adaptive" else env_mode

    mode_file = get_execution_mode_file()
    if mode_file.exists():
        try:
            mode = mode_file.read_text(encoding="utf-8").strip().lower()
            if mode in ("auto", "adaptive", "arbitrage", "fast"):
                return "auto" if mode == "adaptive" else mode
        except Exception:
            pass
    return "auto"


def set_execution_mode(mode: str) -> str:
    """Set execution mode ('auto', 'arbitrage', or 'fast')."""
    cleaned = mode.strip().lower()
    if cleaned == "adaptive":
        cleaned = "auto"
    if cleaned not in ("auto", "arbitrage", "fast"):
        raise ValueError("Execution mode must be 'auto', 'arbitrage', or 'fast'")

    os.environ["AEGIS_EXECUTION_MODE"] = cleaned
    get_execution_mode_file().write_text(cleaned, encoding="utf-8")
    return cleaned


def get_current_mode() -> str:
    """Return 'public' or 'private'. Defaults to 'public'."""
    env_mode = os.environ.get("AEGIS_MODE")
    if env_mode in ("private", "public"):
        return env_mode

    mode_file = get_mode_file()
    if mode_file.exists():
        try:
            mode = mode_file.read_text(encoding="utf-8").strip().lower()
            if mode in ("private", "public"):
                return mode
        except Exception:
            pass
    return "public"


def set_current_mode(mode: str) -> str:
    """Set the system mode ('public' or 'private')."""
    cleaned = mode.strip().lower()
    if cleaned not in ("public", "private"):
        raise ValueError("Mode must be either 'public' or 'private'")

    os.environ["AEGIS_MODE"] = cleaned
    get_mode_file().write_text(cleaned, encoding="utf-8")
    return cleaned
