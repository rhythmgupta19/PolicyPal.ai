"""Configuration module for the Local Language Assistant.

This module contains all configuration settings for the application,
including API settings, language support, and performance constraints.
"""

from typing import List
from dataclasses import dataclass


@dataclass
class QueryConfig:
    """Configuration for query processing."""
    
    MAX_QUERY_LENGTH: int = 500
    MIN_QUERY_LENGTH: int = 1


@dataclass
class LanguageConfig:
    """Configuration for language support."""
    
    SUPPORTED_LANGUAGES: List[str] = None
    DEFAULT_LANGUAGE: str = "hi"  # Hindi
    CONFIDENCE_THRESHOLD: float = 0.7
    
    def __post_init__(self):
        if self.SUPPORTED_LANGUAGES is None:
            # Hindi, Tamil, Telugu, Bengali, Marathi
            self.SUPPORTED_LANGUAGES = ["hi", "ta", "te", "bn", "mr"]


@dataclass
class ResponseConfig:
    """Configuration for response generation."""
    
    MAX_RESPONSE_WORDS: int = 200
    MAX_RESPONSE_BYTES: int = 10240  # 10 KB
    MAX_ACTION_STEPS: int = 5
    MAX_SCHEME_RESULTS: int = 3


@dataclass
class SessionConfig:
    """Configuration for session management."""
    
    SESSION_TIMEOUT_MINUTES: int = 30
    MAX_HISTORY_LENGTH: int = 10


@dataclass
class NetworkConfig:
    """Configuration for network and performance."""
    
    MAX_RETRIES: int = 2
    TIMEOUT_SECONDS: int = 5
    TARGET_NETWORK_SPEED: str = "2G"  # 50 kbps minimum


@dataclass
class AppConfig:
    """Main application configuration."""
    
    query: QueryConfig
    language: LanguageConfig
    response: ResponseConfig
    session: SessionConfig
    network: NetworkConfig
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = False
    
    # Data paths
    SCHEME_DATA_PATH: str = "data/schemes.json"
    
    def __init__(self):
        self.query = QueryConfig()
        self.language = LanguageConfig()
        self.response = ResponseConfig()
        self.session = SessionConfig()
        self.network = NetworkConfig()


# Global configuration instance
config = AppConfig()
