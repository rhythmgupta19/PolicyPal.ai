"""Tests for the configuration module."""

import pytest
from src.config import (
    AppConfig,
    QueryConfig,
    LanguageConfig,
    ResponseConfig,
    SessionConfig,
    NetworkConfig,
    config,
)


class TestQueryConfig:
    """Tests for QueryConfig."""
    
    def test_default_values(self):
        """Test that QueryConfig has correct default values."""
        query_config = QueryConfig()
        assert query_config.MAX_QUERY_LENGTH == 500
        assert query_config.MIN_QUERY_LENGTH == 1


class TestLanguageConfig:
    """Tests for LanguageConfig."""
    
    def test_default_values(self):
        """Test that LanguageConfig has correct default values."""
        lang_config = LanguageConfig()
        assert lang_config.DEFAULT_LANGUAGE == "hi"
        assert lang_config.CONFIDENCE_THRESHOLD == 0.7
        assert len(lang_config.SUPPORTED_LANGUAGES) == 5
        assert "hi" in lang_config.SUPPORTED_LANGUAGES
        assert "ta" in lang_config.SUPPORTED_LANGUAGES
        assert "te" in lang_config.SUPPORTED_LANGUAGES
        assert "bn" in lang_config.SUPPORTED_LANGUAGES
        assert "mr" in lang_config.SUPPORTED_LANGUAGES


class TestResponseConfig:
    """Tests for ResponseConfig."""
    
    def test_default_values(self):
        """Test that ResponseConfig has correct default values."""
        response_config = ResponseConfig()
        assert response_config.MAX_RESPONSE_WORDS == 120
        assert response_config.MAX_RESPONSE_BYTES == 10240
        assert response_config.MAX_ACTION_STEPS == 5
        assert response_config.MAX_SCHEME_RESULTS == 3


class TestSessionConfig:
    """Tests for SessionConfig."""
    
    def test_default_values(self):
        """Test that SessionConfig has correct default values."""
        session_config = SessionConfig()
        assert session_config.SESSION_TIMEOUT_MINUTES == 30
        assert session_config.MAX_HISTORY_LENGTH == 10


class TestNetworkConfig:
    """Tests for NetworkConfig."""
    
    def test_default_values(self):
        """Test that NetworkConfig has correct default values."""
        network_config = NetworkConfig()
        assert network_config.MAX_RETRIES == 2
        assert network_config.TIMEOUT_SECONDS == 5
        # assert network_config.TARGET_NETWORK_SPEED == "2G"


class TestAppConfig:
    """Tests for AppConfig."""
    
    def test_initialization(self):
        """Test that AppConfig initializes all sub-configs."""
        app_config = AppConfig()
        assert isinstance(app_config.query, QueryConfig)
        assert isinstance(app_config.language, LanguageConfig)
        assert isinstance(app_config.response, ResponseConfig)
        assert isinstance(app_config.session, SessionConfig)
        assert isinstance(app_config.network, NetworkConfig)
    
    def test_api_defaults(self):
        """Test that API settings have correct defaults."""
        app_config = AppConfig()
        assert app_config.API_HOST == "0.0.0.0"
        assert app_config.API_PORT == 8000
        assert app_config.API_RELOAD is False
    
    def test_data_path_defaults(self):
        """Test that data paths have correct defaults."""
        app_config = AppConfig()
        assert app_config.SCHEME_DATA_PATH == "data/schemes.json"


class TestGlobalConfig:
    """Tests for the global config instance."""
    
    def test_global_config_exists(self):
        """Test that global config instance is available."""
        assert config is not None
        assert isinstance(config, AppConfig)
    
    def test_global_config_accessible(self):
        """Test that global config values are accessible."""
        assert config.query.MAX_QUERY_LENGTH == 500
        assert config.language.DEFAULT_LANGUAGE == "hi"
        assert config.response.MAX_RESPONSE_WORDS == 120
        assert config.session.SESSION_TIMEOUT_MINUTES == 30
        assert config.network.MAX_RETRIES == 2
