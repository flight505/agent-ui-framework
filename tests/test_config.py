"""Tests for configuration management."""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from agentui.config import AgentConfig, ProviderType, TUIConfig


class TestAgentConfig:
    """Test AgentConfig class."""

    def test_defaults(self) -> None:
        """Test default configuration values."""
        config = AgentConfig()

        assert config.provider == ProviderType.CLAUDE
        assert config.model is None
        assert config.api_key is None
        assert config.max_tokens == 4096
        assert config.temperature == 0.7
        assert config.system_prompt == "You are a helpful AI assistant."
        assert config.max_tool_iterations == 10
        assert config.theme == "catppuccin-mocha"
        assert config.app_name == "AgentUI"
        assert config.tagline == "AI Agent Interface"

    def test_custom_values(self) -> None:
        """Test creating config with custom values."""
        config = AgentConfig(
            provider=ProviderType.OPENAI,
            model="gpt-4",
            api_key="test-key",
            max_tokens=8192,
            temperature=0.5,
            theme="charm-dark",
        )

        assert config.provider == ProviderType.OPENAI
        assert config.model == "gpt-4"
        assert config.api_key == "test-key"
        assert config.max_tokens == 8192
        assert config.temperature == 0.5
        assert config.theme == "charm-dark"

    def test_from_env_defaults(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test loading config from environment with no variables set."""
        # Clear any existing env vars
        for key in ["AGENTUI_MODEL", "AGENTUI_PROVIDER", "AGENTUI_MAX_TOKENS",
                    "AGENTUI_TEMPERATURE", "AGENTUI_THEME"]:
            monkeypatch.delenv(key, raising=False)

        config = AgentConfig.from_env()

        assert config.provider == ProviderType.CLAUDE
        assert config.model is None
        assert config.max_tokens == 4096
        assert config.temperature == 0.7
        assert config.theme == "catppuccin-mocha"

    def test_from_env_custom_values(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test loading config from environment variables."""
        monkeypatch.setenv("AGENTUI_MODEL", "claude-opus-4")
        monkeypatch.setenv("AGENTUI_PROVIDER", "openai")
        monkeypatch.setenv("AGENTUI_MAX_TOKENS", "8192")
        monkeypatch.setenv("AGENTUI_TEMPERATURE", "0.5")
        monkeypatch.setenv("AGENTUI_THEME", "charm-dark")

        config = AgentConfig.from_env()

        assert config.model == "claude-opus-4"
        assert config.provider == ProviderType.OPENAI
        assert config.max_tokens == 8192
        assert config.temperature == 0.5
        assert config.theme == "charm-dark"

    def test_from_env_invalid_provider(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test loading config with invalid provider falls back to default."""
        monkeypatch.setenv("AGENTUI_PROVIDER", "invalid-provider")

        config = AgentConfig.from_env()

        # Should fall back to default CLAUDE provider
        assert config.provider == ProviderType.CLAUDE

    def test_from_file(self) -> None:
        """Test loading config from YAML file."""
        config_data = {
            "provider": "openai",
            "model": "gpt-4",
            "max_tokens": 8192,
            "temperature": 0.5,
            "system_prompt": "Custom prompt",
            "theme": "charm-dark",
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = Path(f.name)

        try:
            config = AgentConfig.from_file(temp_path)

            assert config.provider == "openai"
            assert config.model == "gpt-4"
            assert config.max_tokens == 8192
            assert config.temperature == 0.5
            assert config.system_prompt == "Custom prompt"
            assert config.theme == "charm-dark"
        finally:
            temp_path.unlink()

    def test_from_file_not_found(self) -> None:
        """Test loading config from non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            AgentConfig.from_file(Path("/nonexistent/config.yaml"))

    def test_from_file_partial_config(self) -> None:
        """Test loading config from file with partial values uses defaults."""
        config_data = {
            "model": "gpt-4",
            "temperature": 0.3,
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = Path(f.name)

        try:
            config = AgentConfig.from_file(temp_path)

            # Specified values
            assert config.model == "gpt-4"
            assert config.temperature == 0.3

            # Default values
            assert config.provider == ProviderType.CLAUDE
            assert config.max_tokens == 4096
            assert config.system_prompt == "You are a helpful AI assistant."
        finally:
            temp_path.unlink()


class TestTUIConfig:
    """Test TUIConfig class."""

    def test_defaults(self) -> None:
        """Test default TUI config values."""
        config = TUIConfig()

        assert config.theme == "catppuccin-mocha"
        assert config.app_name == "AgentUI"
        assert config.tagline == "AI Agent Interface"
        assert config.tui_path is None
        assert config.debug is False
        assert config.reconnect_attempts == 3
        assert config.reconnect_delay == 1.0

    def test_custom_values(self) -> None:
        """Test creating TUI config with custom values."""
        config = TUIConfig(
            theme="charm-dark",
            app_name="My Agent",
            tagline="Custom Tagline",
            tui_path="/custom/path/agentui-tui",
            debug=True,
            reconnect_attempts=5,
            reconnect_delay=2.0,
        )

        assert config.theme == "charm-dark"
        assert config.app_name == "My Agent"
        assert config.tagline == "Custom Tagline"
        assert config.tui_path == "/custom/path/agentui-tui"
        assert config.debug is True
        assert config.reconnect_attempts == 5
        assert config.reconnect_delay == 2.0

    def test_from_env_defaults(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test loading TUI config from environment with no variables set."""
        # Clear any existing env vars
        for key in ["AGENTUI_THEME", "AGENTUI_TUI_PATH", "AGENTUI_DEBUG"]:
            monkeypatch.delenv(key, raising=False)

        config = TUIConfig.from_env()

        assert config.theme == "catppuccin-mocha"
        assert config.tui_path is None
        assert config.debug is False

    def test_from_env_custom_values(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test loading TUI config from environment variables."""
        monkeypatch.setenv("AGENTUI_THEME", "charm-light")
        monkeypatch.setenv("AGENTUI_TUI_PATH", "/custom/tui")
        monkeypatch.setenv("AGENTUI_DEBUG", "1")

        config = TUIConfig.from_env()

        assert config.theme == "charm-light"
        assert config.tui_path == "/custom/tui"
        assert config.debug is True

    def test_from_env_debug_values(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test various debug environment variable values."""
        # Empty string = False
        monkeypatch.setenv("AGENTUI_DEBUG", "")
        config = TUIConfig.from_env()
        assert config.debug is False

        # Any non-empty string = True
        monkeypatch.setenv("AGENTUI_DEBUG", "true")
        config = TUIConfig.from_env()
        assert config.debug is True

        monkeypatch.setenv("AGENTUI_DEBUG", "false")
        config = TUIConfig.from_env()
        assert config.debug is True  # bool("false") is True

        monkeypatch.setenv("AGENTUI_DEBUG", "0")
        config = TUIConfig.from_env()
        assert config.debug is True  # bool("0") is True


class TestProviderType:
    """Test ProviderType enum."""

    def test_enum_values(self) -> None:
        """Test provider type enum values."""
        assert ProviderType.CLAUDE.value == "claude"
        assert ProviderType.OPENAI.value == "openai"
        assert ProviderType.GEMINI.value == "gemini"
        assert ProviderType.OLLAMA.value == "ollama"

    def test_enum_from_string(self) -> None:
        """Test creating provider type from string."""
        assert ProviderType("claude") == ProviderType.CLAUDE
        assert ProviderType("openai") == ProviderType.OPENAI
        assert ProviderType("gemini") == ProviderType.GEMINI
        assert ProviderType("ollama") == ProviderType.OLLAMA

    def test_enum_invalid_value(self) -> None:
        """Test creating provider type with invalid value."""
        with pytest.raises(ValueError):
            ProviderType("invalid")


class TestBackwardCompatibility:
    """Test backward compatibility with types.py re-exports."""

    def test_import_from_types(self) -> None:
        """Test that configs can still be imported from types module."""
        from agentui.types import AgentConfig as TypesAgentConfig
        from agentui.types import ProviderType as TypesProviderType
        from agentui.types import TUIConfig as TypesTUIConfig

        # Verify they're the same classes
        assert TypesAgentConfig is AgentConfig
        assert TypesProviderType is ProviderType
        assert TypesTUIConfig is TUIConfig

    def test_import_from_config(self) -> None:
        """Test that configs can be imported from new config module."""
        from agentui.config import AgentConfig as ConfigAgentConfig
        from agentui.config import ProviderType as ConfigProviderType
        from agentui.config import TUIConfig as ConfigTUIConfig

        # Verify they're the same classes
        assert ConfigAgentConfig is AgentConfig
        assert ConfigProviderType is ProviderType
        assert ConfigTUIConfig is TUIConfig

    def test_cross_module_compatibility(self) -> None:
        """Test that instances work across module imports."""
        from agentui.config import AgentConfig as ConfigAgentConfig
        from agentui.types import AgentConfig as TypesAgentConfig

        # Create with one import, use with another
        config1 = ConfigAgentConfig(model="test-model")
        config2 = TypesAgentConfig(model="test-model")

        assert isinstance(config1, TypesAgentConfig)
        assert isinstance(config2, ConfigAgentConfig)
        assert type(config1) is type(config2)
