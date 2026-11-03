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


# Module-level aliases for backwards compatibility
@property
def DB_PATH() -> Path:
    return get_db_path()


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
