#!/usr/bin/env python3
"""
Smart Assistant Demo

An intelligent agent that understands context, can troubleshoot issues,
and provides dynamic help based on user intent.

This demonstrates:
- Context-aware error handling
- Understanding user intent
- Dynamic troubleshooting
- Project-specific knowledge

Run:
    uv sync --extra all  # Install dependencies first
    uv run python examples/smart_assistant.py
"""

import asyncio
import sys
import logging
import os
import subprocess
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentui import AgentApp

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Create the app with an intelligent system prompt
app = AgentApp(
    name="smart-assistant",
    provider="claude",
    system_prompt="""You are an intelligent AgentUI development assistant with deep knowledge of the project.

## Project Context

This is the AgentUI project - a Python/Go framework for building AI agents with beautiful terminal UIs.

**Tech Stack:**
- Python 3.11+ (agent runtime, LLM providers)
- Go 1.22+ (TUI rendering with Bubbletea)
- Dependencies managed with `uv` (NOT pip)
- Optional LLM providers: anthropic, openai

**Project Structure:**
```
agentui/
├── src/agentui/          # Python framework
│   ├── providers/        # LLM provider implementations
│   │   ├── claude.py     # Requires: anthropic (optional)
│   │   └── openai.py     # Requires: openai (optional)
│   ├── core.py           # Agent runtime
│   └── app.py            # AgentApp API
├── examples/             # Example agents
└── pyproject.toml        # Dependencies
```

**Common Installation Issues:**

1. **"anthropic package not installed" error:**
   - Cause: User ran `uv sync` without optional dependencies
   - Solution: `uv sync --extra all` or `uv sync --extra claude`
   - Note: `anthropic` is in `[project.optional-dependencies]`

2. **"openai package not installed" error:**
   - Cause: User ran `uv sync` without optional dependencies
   - Solution: `uv sync --extra openai` or `uv sync --extra all`

3. **API key errors:**
   - ANTHROPIC_API_KEY must be set for Claude
   - OPENAI_API_KEY must be set for OpenAI

## Your Capabilities

You have tools to:
- `check_environment` - Verify what's installed, check API keys
- `run_command` - Execute shell commands (with user permission)
- `diagnose_error` - Analyze error messages and suggest fixes
- `show_help` - Display context-specific help

## Intelligence Guidelines

1. **Understand User Intent:**
   - "uv sync all dependencies" = they tried installing, but likely missed `--extra`
   - "installed dependencies" but getting errors = optional deps not installed
   - "not working" = ask what error they're seeing

2. **Provide Contextual Help:**
   - Don't just repeat error messages
   - Explain WHY the error happened
   - Give the EXACT command to fix it
   - Offer to run the fix for them

3. **Be Proactive:**
   - If user mentions an error, check their environment first
   - Suggest solutions based on common patterns
   - Ask clarifying questions when needed

4. **Remember Conversation Context:**
   - Track what the user has already tried
   - Don't suggest the same solution twice
   - Build on previous exchanges

Always be helpful, concise, and context-aware.""",
    theme="charm-dark",
    tagline="Your AgentUI Development Assistant",
    debug=False,
)


@app.tool(
    name="check_environment",
    description="Check the current development environment: installed packages, API keys, Python version, etc.",
    parameters={
        "type": "object",
        "properties": {
            "check_type": {
                "type": "string",
                "enum": ["packages", "api_keys", "all"],
                "description": "What to check: 'packages' (installed Python packages), 'api_keys' (environment variables), 'all' (everything)"
            }
        },
        "required": ["check_type"]
    }
)
def check_environment(check_type: str) -> dict:
    """Check the development environment."""
    result = {"check_type": check_type}

    if check_type in ["packages", "all"]:
        # Check if key packages are installed
        packages_status = {}

        for package in ["anthropic", "openai", "rich", "pyyaml"]:
            try:
                __import__(package)
                packages_status[package] = "✅ Installed"
            except ImportError:
                packages_status[package] = "❌ Not installed"

        result["packages"] = packages_status

        # Check Python version
        result["python_version"] = sys.version.split()[0]

    if check_type in ["api_keys", "all"]:
        # Check API keys (without revealing them)
        api_keys_status = {}

        for key_name in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]:
            value = os.environ.get(key_name)
            if value:
                # Show first/last 4 chars only
                masked = f"{value[:7]}...{value[-4:]}" if len(value) > 15 else "sk-***"
                api_keys_status[key_name] = f"✅ Set ({masked})"
            else:
                api_keys_status[key_name] = "❌ Not set"

        result["api_keys"] = api_keys_status

    # Check uv availability
    try:
        uv_version = subprocess.check_output(["uv", "--version"], text=True).strip()
        result["uv"] = f"✅ {uv_version}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        result["uv"] = "❌ Not installed"

    return result


@app.tool(
    name="diagnose_error",
    description="Analyze an error message and provide a diagnosis with fix suggestions.",
    parameters={
        "type": "object",
        "properties": {
            "error_message": {
                "type": "string",
                "description": "The error message to diagnose"
            }
        },
        "required": ["error_message"]
    }
)
def diagnose_error(error_message: str) -> dict:
    """Diagnose an error and suggest fixes."""
    error_lower = error_message.lower()

    diagnoses = []

    # Check for common errors
    if "anthropic" in error_lower and ("not installed" in error_lower or "no module" in error_lower):
        diagnoses.append({
            "issue": "Anthropic package not installed",
            "cause": "The anthropic package is an optional dependency. Running 'uv sync' only installs core dependencies.",
            "fix": "uv sync --extra claude",
            "alternative": "uv sync --extra all",
            "explanation": "The --extra flag installs optional dependency groups defined in pyproject.toml"
        })

    elif "openai" in error_lower and ("not installed" in error_lower or "no module" in error_lower):
        diagnoses.append({
            "issue": "OpenAI package not installed",
            "cause": "The openai package is an optional dependency.",
            "fix": "uv sync --extra openai",
            "alternative": "uv sync --extra all",
            "explanation": "The --extra flag installs optional dependency groups"
        })

    elif "api key" in error_lower or "anthropic_api_key" in error_lower:
        diagnoses.append({
            "issue": "Missing Anthropic API key",
            "cause": "The ANTHROPIC_API_KEY environment variable is not set",
            "fix": "export ANTHROPIC_API_KEY='sk-ant-...'",
            "explanation": "Get your API key from: https://console.anthropic.com/settings/keys",
            "persistent": "Add to ~/.zshrc or ~/.bashrc to make it permanent"
        })

    elif "openai_api_key" in error_lower:
        diagnoses.append({
            "issue": "Missing OpenAI API key",
            "cause": "The OPENAI_API_KEY environment variable is not set",
            "fix": "export OPENAI_API_KEY='sk-...'",
            "explanation": "Get your API key from: https://platform.openai.com/api-keys"
        })

    if not diagnoses:
        # Generic diagnosis
        return {
            "error": error_message,
            "diagnosis": "Unable to automatically diagnose this error. Please share more details.",
            "suggestion": "Try: check_environment('all') to see what's installed"
        }

    return {
        "error": error_message,
        "diagnoses": diagnoses,
        "recommended_action": diagnoses[0]["fix"] if diagnoses else None
    }


@app.tool(
    name="run_command",
    description="Execute a shell command. Use this to install packages, check versions, etc. Ask user for permission first for destructive operations.",
    parameters={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The shell command to execute (e.g., 'uv sync --extra all', 'echo $ANTHROPIC_API_KEY')"
            },
            "description": {
                "type": "string",
                "description": "Human-readable description of what this command does"
            }
        },
        "required": ["command", "description"]
    }
)
def run_command(command: str, description: str) -> dict:
    """Execute a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "command": command,
            "description": description,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip() if result.stdout else "",
            "stderr": result.stderr.strip() if result.stderr else "",
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            "command": command,
            "description": description,
            "error": "Command timed out after 30 seconds",
            "success": False
        }
    except Exception as e:
        return {
            "command": command,
            "description": description,
            "error": str(e),
            "success": False
        }


@app.tool(
    name="show_installation_guide",
    description="Show installation instructions for AgentUI and its dependencies.",
    parameters={
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "enum": ["quick_start", "providers", "troubleshooting", "all"],
                "description": "Which guide to show"
            }
        },
        "required": ["topic"]
    }
)
def show_installation_guide(topic: str) -> dict:
    """Return installation guide content."""
    guides = {
        "quick_start": """
# Quick Start Installation

1. Install all dependencies:
   ```bash
   uv sync --extra all
   ```

2. Set API key:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

3. Run an example:
   ```bash
   uv run python examples/simple_agent.py
   ```
""",
        "providers": """
# Installing LLM Providers

AgentUI uses optional dependencies for different providers:

**Claude (Anthropic):**
```bash
uv sync --extra claude
export ANTHROPIC_API_KEY="sk-ant-..."
```

**OpenAI (GPT):**
```bash
uv sync --extra openai
export OPENAI_API_KEY="sk-..."
```

**All Providers:**
```bash
uv sync --extra all
```
""",
        "troubleshooting": """
# Common Issues

**"anthropic package not installed":**
- You ran `uv sync` without --extra flag
- Fix: `uv sync --extra claude` or `uv sync --extra all`

**"API key not found":**
- Environment variable not set
- Fix: `export ANTHROPIC_API_KEY="your-key"`
- Make permanent: Add to ~/.zshrc

**"uv command not found":**
- uv not installed
- Fix: `curl -LsSf https://astral.sh/uv/install.sh | sh`
"""
    }

    if topic == "all":
        return {
            "topic": topic,
            "content": "\n\n".join(guides.values())
        }

    return {
        "topic": topic,
        "content": guides.get(topic, "Unknown topic")
    }


async def main():
    """Run the smart assistant."""
    print()
    print("=" * 60)
    print("🤖 AgentUI Smart Assistant")
    print("=" * 60)
    print()
    print("I'm your intelligent development assistant for AgentUI.")
    print()
    print("I can help you:")
    print("  • Troubleshoot installation issues")
    print("  • Check your environment setup")
    print("  • Diagnose error messages")
    print("  • Run commands to fix problems")
    print("  • Answer questions about the project")
    print()
    print("Try saying:")
    print('  • "I\'m getting an error about anthropic not installed"')
    print('  • "Check my environment"')
    print('  • "Help me install dependencies"')
    print('  • "I ran uv sync but examples don\'t work"')
    print()
    print("Type 'quit' or press Ctrl+C to exit.")
    print("=" * 60)
    print()

    try:
        await app.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")


if __name__ == "__main__":
    asyncio.run(main())
