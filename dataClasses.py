"""
Core data models and interfaces for the Local Language Assistant.

This module implements the data models as specified in the design document,
optimized for low-bandwidth operation and multi-language support.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


# -----------------------------
# Query Processing Models
# -----------------------------

class QueryStatus(Enum):
    """Status of query processing."""
    VALID = "valid"
    EMPTY = "empty"
    TRUNCATED = "truncated"


@dataclass
class ProcessedQuery:
    """
    Processed and validated user query.
    
    Validates: Requirements 1.4, 1.5
    """
    original_text: str
    normalized_text: str
    status: QueryStatus
    detected_language: Optional[str]
    character_count: int


# -----------------------------
# Scheme Models
# -----------------------------

@dataclass
class Scheme:
    """
    Government scheme information with localized content.
    
    Validates: Requirements 3.3, 6.1
    """
    scheme_id: str
    name: Dict[str, str]  # Localized names: {"hi": "...", "en": "..."}
    description: Dict[str, str]  # Localized descriptions
    category: str
    eligibility_criteria: List[str]
    required_documents: List[str]
    application_steps: List[str]
    contact_office: str
    keywords: List[str]


@dataclass
class SchemeMatch:
    """
    Scheme matched to user query with relevance scoring.
    
    Validates: Requirements 3.2, 3.6
    """
    scheme: Scheme
    relevance_score: float
    matched_criteria: List[str]


# -----------------------------
# Response Models
# -----------------------------

@dataclass
class ActionStep:
    """
    Specific, actionable instruction for the user.
    
    Validates: Requirements 4.1, 4.2, 4.3, 4.4
    """
    step_number: int
    instruction: str
    location: Optional[str]  # e.g., "Gram Panchayat office"
    documents: List[str]


@dataclass
class AssistantResponse:
    """
    Complete response to user query with action steps.
    
    Validates: Requirements 4.5, 5.1, 5.4
    """
    message: str
    action_steps: List[ActionStep]
    schemes_mentioned: List[str]
    has_more: bool  # True if response was split
    language: str
    byte_size: int


# -----------------------------
# Session Models
# -----------------------------

@dataclass
class SessionContext:
    """
    Active conversation context (no PII stored).
    
    Validates: Requirements 6.1, 6.2, 6.5
    """
    session_id: str
    language: str
    last_activity: datetime
    mentioned_schemes: List[str] = field(default_factory=list)
    conversation_history: List[Dict] = field(default_factory=list)
    user_attributes: Dict[str, str] = field(default_factory=dict)  # Non-PII attributes like "category: farmer"


@dataclass
class SessionRecord:
    """
    Stored session data (no PII).
    
    Validates: Requirements 6.3, 6.4, 6.5
    """
    session_id: str
    created_at: datetime
    last_activity: datetime
    language: str
    
    # Context (no personal information)
    mentioned_scheme_ids: List[str]
    user_category: Optional[str]  # e.g., "farmer", "student"
    conversation_turns: int
    
    # Compressed history (last N turns only)
    recent_intents: List[str]
