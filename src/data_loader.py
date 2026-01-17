import json
from pathlib import Path
from config import config


def load_schemes():
    """Load scheme data from local JSON file."""
    path = Path(config.SCHEME_DATA_PATH)

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Load once at startup (important for speed)
SCHEMES = load_schemes()
