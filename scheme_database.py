import json
from typing import List, Dict, Optional


class SchemeDatabase:
    def __init__(self, filepath: str):
        """
        Initialize the SchemeDatabase.

        :param filepath: Path to JSON file containing scheme records
        """
        self.filepath = filepath
        self._schemes: List[Dict] = []
        self._load()

    def _load(self) -> None:
        """Load schemes from JSON file into memory."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self._schemes = json.load(f)
        except FileNotFoundError:
            self._schemes = []
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

    def get_by_id(self, scheme_id: str) -> Optional[Dict]:
        """
        Retrieve a scheme by its ID.

        :param scheme_id: Unique scheme identifier
        :return: Scheme dict or None if not found
        """
        for scheme in self._schemes:
            if scheme.get("id") == scheme_id:
                return scheme
        return None

    def get_all(self) -> List[Dict]:
        """
        Retrieve all schemes.

        :return: List of scheme records
        """
        return self._schemes
