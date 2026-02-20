import json
from pathlib import Path

from src.config import config


def load_schemes():
    """Load scheme data from local JSON file."""
    path = Path(config.SCHEME_DATA_PATH)

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    if isinstance(loaded, list):
        return loaded

    # Graceful fallback for malformed or legacy files.
    return []


# Load once at startup (important for speed)
SCHEMES = load_schemes()
