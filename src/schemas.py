from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class QueryRequest:
    """Incoming user query."""

    q: str
    lang: Optional[str] = "hi"


@dataclass
class SchemeInfo:
    """Minimal scheme info (compact)."""

    id: str
    name: str
    benefit: str


@dataclass
class AssistantResponse:
    """
    Compact response optimized for low bandwidth.
    Field names are intentionally short.
    """

    msg: str
    schemes: List[dict] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    lang: str = "hi"

    def model_dump(self):
        return {
            "msg": self.msg,
            "schemes": self.schemes,
            "steps": self.steps,
            "lang": self.lang,
        }
