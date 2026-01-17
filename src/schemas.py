from pydantic import BaseModel, Field
from typing import List, Optional


class QueryRequest(BaseModel):
    """Incoming user query."""

    q: str = Field(..., min_length=1, max_length=500)
    lang: Optional[str] = Field(default="hi")


class SchemeInfo(BaseModel):
    """Minimal scheme info (compact)."""

    id: str
    name: str
    benefit: str


class AssistantResponse(BaseModel):
    """
    Compact response optimized for low bandwidth.
    Field names are intentionally short.
    """

    msg: str                   # main answer text
    schemes: List[SchemeInfo] = []
    steps: List[str] = []
    lang: str = "hi"
