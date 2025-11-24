from pathlib import Path
import sys


def get_base_path() -> Path:
    """Return base path that works both in development and PyInstaller builds."""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


BASE_PATH = get_base_path()


def resource_path(*relative_parts: str) -> str:
    """Join the base path with provided relative parts and return as string."""
    return str(BASE_PATH.joinpath(*relative_parts))


def ensure_resource_path(path: str | None) -> str | None:
    """Ensure a path is absolute relative to the packaged resources."""
    if path is None or path == "":
        return path

    candidate = Path(path)
    if candidate.is_absolute():
        return str(candidate)

    return str(BASE_PATH / candidate)
