"""
Tests for the app module (AgentApp).
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import yaml

from agentui.app import AgentApp, create_app, quick_chat
from agentui.types import AgentConfig, AppManifest, ProviderType, ToolDefinition


@pytest.fixture
def mock_api_key():
    """Set up a mock API key for testing."""
    old_key = os.environ.get("ANTHROPIC_API_KEY")
    os.environ["ANTHROPIC_API_KEY"] = "test-api-key-12345"
    yield "test-api-key-12345"
    if old_key:
        os.environ["ANTHROPIC_API_KEY"] = old_key
    else:
        os.environ.pop("ANTHROPIC_API_KEY", None)


@pytest.fixture
def temp_manifest_file():
    """Create a temporary manifest file for testing."""
    manifest_data = {
        "name": "test-agent",
        "version": "1.0.0",
        "description": "Test agent",
        "display_name": "Test Agent",
        "tagline": "Testing manifest",
        "system_prompt": "You are a test assistant.",
        "providers": {
            "default": "claude",
            "claude": {
                "model": "claude-3-sonnet-20240229",
            }
        }
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        manifest_path = Path(tmpdir) / "app.yaml"
        with open(manifest_path, "w") as f:
            yaml.dump(manifest_data, f)
        yield manifest_path


class TestAgentAppInitialization:
    """Tests for AgentApp initialization."""

    def test_default_initialization(self, mock_api_key):
        """Test AgentApp initializes with correct defaults."""
        app = AgentApp(name="TestAgent")

        assert app.config.app_name == "TestAgent"
        assert app.config.provider == ProviderType.CLAUDE
        assert app.config.api_key == "test-api-key-12345"
        assert app.config.max_tokens == 4096
        assert app.config.temperature == 0.7
        assert app.config.theme == "catppuccin-mocha"
        assert app._tools == []
        assert app._core is None
        assert app._bridge is None

    def test_custom_initialization(self, mock_api_key):
        """Test AgentApp initializes with custom parameters."""
        app = AgentApp(
            name="CustomAgent",
            provider="openai",
            model="gpt-4",
            api_key="custom-key",
            max_tokens=8192,
            temperature=0.5,
            theme="dracula",
            tagline="Custom Tagline",
            system_prompt="Custom system prompt",
        )

        assert app.config.app_name == "CustomAgent"
        assert app.config.provider == ProviderType.OPENAI
        assert app.config.model == "gpt-4"
        assert app.config.api_key == "custom-key"
        assert app.config.max_tokens == 8192
        assert app.config.temperature == 0.5
        assert app.config.theme == "dracula"
        assert app.config.tagline == "Custom Tagline"
        assert app.config.system_prompt == "Custom system prompt"

    def test_manifest_initialization_from_path(self, temp_manifest_file):
        """Test AgentApp initializes from manifest file."""
        app = AgentApp(manifest=temp_manifest_file)

        assert app.manifest.name == "test-agent"
        assert app.manifest.version == "1.0.0"
        assert app.manifest.display_name == "Test Agent"
        assert app.config.app_name == "Test Agent"
        assert app.config.system_prompt == "You are a test assistant."
        assert app.manifest.model == "claude-3-sonnet-20240229"

    def test_manifest_initialization_from_directory(self, temp_manifest_file):
        """Test AgentApp initializes from directory containing app.yaml."""
        manifest_dir = temp_manifest_file.parent
        app = AgentApp(manifest=manifest_dir)

        assert app.manifest.name == "test-agent"
        assert app.config.app_name == "Test Agent"

    def test_manifest_initialization_from_object(self, mock_api_key):
        """Test AgentApp initializes from AppManifest object."""
        manifest = AppManifest(
            name="object-agent",
            display_name="Object Agent",
            tagline="From object",
        )
        # Must pass tagline as parameter for it to override default
        app = AgentApp(manifest=manifest, tagline="From object")

        assert app.manifest.name == "object-agent"
        assert app.config.app_name == "Object Agent"
        assert app.config.tagline == "From object"

    def test_manifest_not_found_raises_error(self):
        """Test that missing manifest file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Manifest not found"):
            AgentApp(manifest="/nonexistent/path/app.yaml")

    def test_debug_mode_enables_logging(self, mock_api_key):
        """Test that debug=True enables debug logging."""
        with patch("logging.basicConfig") as mock_logging:
            app = AgentApp(name="DebugAgent", debug=True)
            mock_logging.assert_called_once()
            assert app._debug is True


class TestAgentAppApiKeys:
    """Tests for API key retrieval."""

    def test_get_api_key_claude(self):
        """Test API key retrieval for Claude provider."""
        os.environ["ANTHROPIC_API_KEY"] = "test-claude-key"
        app = AgentApp(name="test", provider="claude")
        assert app.config.api_key == "test-claude-key"
        os.environ.pop("ANTHROPIC_API_KEY", None)

    def test_get_api_key_openai(self):
        """Test API key retrieval for OpenAI provider."""
        os.environ["OPENAI_API_KEY"] = "test-openai-key"
        app = AgentApp(name="test", provider="openai")
        assert app.config.api_key == "test-openai-key"
        os.environ.pop("OPENAI_API_KEY", None)

    def test_get_api_key_gemini(self):
        """Test API key retrieval for Gemini provider."""
        os.environ["GOOGLE_API_KEY"] = "test-gemini-key"
        app = AgentApp(name="test", provider="gemini")
        assert app.config.api_key == "test-gemini-key"
        os.environ.pop("GOOGLE_API_KEY", None)

    def test_explicit_api_key_overrides_env(self):
        """Test that explicitly provided API key overrides environment."""
        os.environ["ANTHROPIC_API_KEY"] = "env-key"
        app = AgentApp(name="test", provider="claude", api_key="explicit-key")
        assert app.config.api_key == "explicit-key"
        os.environ.pop("ANTHROPIC_API_KEY", None)


class TestAgentAppToolRegistration:
    """Tests for tool registration via decorators."""

    def test_tool_registration_basic(self, mock_api_key):
        """Test basic tool registration via decorator."""
        app = AgentApp(name="TestAgent")

        @app.tool(
            name="test_tool",
            description="A test tool",
            parameters={
                "type": "object",
                "properties": {
                    "input": {"type": "string"}
                },
            },
        )
        def test_tool(input: str):
            return f"Result: {input}"

        assert len(app._tools) == 1
        tool = app._tools[0]
        assert tool.name == "test_tool"
        assert tool.description == "A test tool"
        assert tool.parameters["type"] == "object"
        assert tool.handler == test_tool
        assert tool.is_ui_tool is False
        assert tool.requires_confirmation is False

    def test_tool_registration_with_ui_flag(self, mock_api_key):
        """Test tool registration with is_ui_tool flag."""
        app = AgentApp(name="TestAgent")

        @app.tool(
            name="ui_tool",
            description="A UI tool",
            parameters={"type": "object"},
            is_ui_tool=True,
        )
        def ui_tool():
            return {"type": "table", "data": []}

        tool = app._tools[0]
        assert tool.is_ui_tool is True

    def test_tool_registration_with_confirmation(self, mock_api_key):
        """Test tool registration with requires_confirmation flag."""
        app = AgentApp(name="TestAgent")

        @app.tool(
            name="dangerous_tool",
            description="A dangerous tool",
            parameters={"type": "object"},
            requires_confirmation=True,
        )
        def dangerous_tool():
            return "Executed"

        tool = app._tools[0]
        assert tool.requires_confirmation is True

    def test_ui_tool_decorator_shorthand(self, mock_api_key):
        """Test ui_tool decorator as shorthand."""
        app = AgentApp(name="TestAgent")

        @app.ui_tool(
            name="shorthand_ui",
            description="UI tool shorthand",
            parameters={"type": "object"},
        )
        def shorthand_ui():
            return {"type": "progress"}

        tool = app._tools[0]
        assert tool.name == "shorthand_ui"
        assert tool.is_ui_tool is True

    def test_multiple_tool_registration(self, mock_api_key):
        """Test registering multiple tools."""
        app = AgentApp(name="TestAgent")

        @app.tool("tool1", "First tool", {"type": "object"})
        def tool1():
            return "one"

        @app.tool("tool2", "Second tool", {"type": "object"})
        def tool2():
            return "two"

        @app.ui_tool("tool3", "Third tool", {"type": "object"})
        def tool3():
            return "three"

        assert len(app._tools) == 3
        assert app._tools[0].name == "tool1"
        assert app._tools[1].name == "tool2"
        assert app._tools[2].name == "tool3"
        assert app._tools[2].is_ui_tool is True

    def test_tool_decorator_returns_original_function(self, mock_api_key):
        """Test that decorator returns the original function."""
        app = AgentApp(name="TestAgent")

        @app.tool("test", "Test", {"type": "object"})
        def original_func(x: int) -> int:
            return x * 2

        # Function should still be callable
        assert original_func(5) == 10
        assert original_func.__name__ == "original_func"


class TestAgentAppChat:
    """Tests for chat functionality."""

    @pytest.mark.asyncio
    async def test_chat_creates_core_on_first_call(self, mock_api_key):
        """Test that chat() creates AgentCore on first call."""
        app = AgentApp(name="TestAgent")
        assert app._core is None

        # Mock the core and its process_message method
        with patch("agentui.app.AgentCore") as MockCore:
            mock_core = MagicMock()
            MockCore.return_value = mock_core

            # Mock process_message to yield chunks
            async def mock_process(message):
                yield MagicMock(content="Hello", is_complete=False)
                yield MagicMock(content=" World", is_complete=True)

            mock_core.process_message = mock_process

            response = await app.chat("Hi")

            assert app._core is not None
            MockCore.assert_called_once()

    @pytest.mark.asyncio
    async def test_chat_reuses_core_on_subsequent_calls(self, mock_api_key):
        """Test that chat() reuses the same core for subsequent calls."""
        app = AgentApp(name="TestAgent")

        with patch("agentui.app.AgentCore") as MockCore:
            mock_core = MagicMock()
            MockCore.return_value = mock_core

            async def mock_process(message):
                yield MagicMock(content="Response", is_complete=True)

            mock_core.process_message = mock_process

            await app.chat("Message 1")
            await app.chat("Message 2")

            # Core should only be created once
            MockCore.assert_called_once()

    @pytest.mark.asyncio
    async def test_chat_registers_tools(self, mock_api_key):
        """Test that chat() registers tools with the core."""
        app = AgentApp(name="TestAgent")

        @app.tool("test_tool", "Test", {"type": "object"})
        def test_tool():
            return "result"

        with patch("agentui.app.AgentCore") as MockCore:
            mock_core = MagicMock()
            MockCore.return_value = mock_core
            mock_core.register_tool = MagicMock()

            async def mock_process(message):
                yield MagicMock(content="Response", is_complete=True)

            mock_core.process_message = mock_process

            await app.chat("Test message")

            # Verify tool was registered
            mock_core.register_tool.assert_called_once()
            registered_tool = mock_core.register_tool.call_args[0][0]
            assert registered_tool.name == "test_tool"

    @pytest.mark.asyncio
    async def test_chat_accumulates_response(self, mock_api_key):
        """Test that chat() correctly accumulates streaming response."""
        app = AgentApp(name="TestAgent")

        with patch("agentui.app.AgentCore") as MockCore:
            mock_core = MagicMock()
            MockCore.return_value = mock_core

            async def mock_process(message):
                yield MagicMock(content="Hello", is_complete=False)
                yield MagicMock(content=" ", is_complete=False)
                yield MagicMock(content="World", is_complete=False)
                yield MagicMock(content="!", is_complete=True)

            mock_core.process_message = mock_process

            response = await app.chat("Hi")

            assert response == "Hello World!"


class TestCreateApp:
    """Tests for create_app convenience function."""

    def test_create_app_without_manifest(self, mock_api_key):
        """Test create_app without manifest."""
        app = create_app(name="TestApp")
        assert isinstance(app, AgentApp)
        assert app.config.app_name == "TestApp"

    def test_create_app_with_manifest(self, temp_manifest_file):
        """Test create_app with manifest path."""
        app = create_app(manifest=temp_manifest_file)
        assert isinstance(app, AgentApp)
        assert app.manifest.name == "test-agent"

    def test_create_app_with_kwargs(self, mock_api_key):
        """Test create_app passes kwargs to AgentApp."""
        app = create_app(
            name="TestApp",
            provider="openai",
            temperature=0.9,
        )
        assert app.config.provider == ProviderType.OPENAI
        assert app.config.temperature == 0.9


class TestQuickChat:
    """Tests for quick_chat convenience function."""

    @pytest.mark.asyncio
    async def test_quick_chat_basic(self, mock_api_key):
        """Test quick_chat creates app and returns response."""
        with patch("agentui.app.AgentCore") as MockCore:
            mock_core = MagicMock()
            MockCore.return_value = mock_core

            async def mock_process(message):
                yield MagicMock(content="Quick response", is_complete=True)

            mock_core.process_message = mock_process

            response = await quick_chat("Test message")
            assert response == "Quick response"

    @pytest.mark.asyncio
    async def test_quick_chat_with_parameters(self, mock_api_key):
        """Test quick_chat accepts provider, model, and system_prompt."""
        with patch("agentui.app.AgentCore") as MockCore:
            mock_core = MagicMock()
            MockCore.return_value = mock_core

            async def mock_process(message):
                yield MagicMock(content="Response", is_complete=True)

            mock_core.process_message = mock_process

            response = await quick_chat(
                "Test",
                provider="openai",
                model="gpt-4",
                system_prompt="Custom prompt",
            )

            assert response == "Response"
