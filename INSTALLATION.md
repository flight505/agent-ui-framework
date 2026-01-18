# Installation Guide

## Quick Start

### 1. Clone and Install Core Dependencies

```bash
git clone https://github.com/flight505/agentui.git
cd agentui

# Install core dependencies only (Rich, PyYAML)
uv sync
```

### 2. Install LLM Provider Dependencies

AgentUI uses **optional dependencies** for different LLM providers. You need to explicitly install them:

#### Option A: Install All Providers (Recommended)

```bash
uv sync --extra all
```

This installs:
- ✅ `anthropic` (for Claude)
- ✅ `openai` (for GPT models)

#### Option B: Install Specific Providers

```bash
# For Claude (Anthropic) only
uv sync --extra claude

# For OpenAI/GPT only
uv sync --extra openai
```

#### Option C: Add Dependencies Manually

```bash
# Add Anthropic Claude support
uv add anthropic

# Add OpenAI support
uv add openai
```

### 3. Set Up API Keys

```bash
# For Claude (required for examples)
export ANTHROPIC_API_KEY="your-key-here"

# For OpenAI (optional)
export OPENAI_API_KEY="your-key-here"
```

Add these to your shell profile (`~/.zshrc`, `~/.bashrc`) to make them permanent.

### 4. Verify Installation

```bash
# Run a simple example
uv run python examples/simple_agent.py

# Or use the alias (if configured)
py examples/simple_agent.py
```

---

## Development Installation

For development work (includes testing tools):

```bash
# Install dev dependencies (includes all providers + pytest, ruff, mypy)
uv sync --extra dev

# Or install dev dependencies as a group
uv sync --group dev
```

---

## Understanding Optional Dependencies

### Why Optional?

AgentUI supports multiple LLM providers (Claude, OpenAI, Gemini), but you may only need one. Optional dependencies keep the installation lightweight.

### Where Are They Defined?

See `pyproject.toml`:

```toml
[project.optional-dependencies]
claude = ["anthropic>=0.40.0"]
openai = ["openai>=1.50.0"]
all = ["anthropic>=0.40.0", "openai>=1.50.0"]
```

### Common Errors

#### "anthropic package not installed"

**Error:**
```
ImportError: anthropic package not installed.
Install with: uv sync --extra claude  (or: uv add anthropic)
```

**Fix:**
```bash
uv sync --extra claude
# or
uv sync --extra all
```

#### "openai package not installed"

**Error:**
```
ImportError: openai package not installed.
Install with: uv sync --extra openai  (or: uv add openai)
```

**Fix:**
```bash
uv sync --extra openai
# or
uv sync --extra all
```

---

## Troubleshooting

### Issue: Examples don't run after `uv sync`

**Cause:** You only installed core dependencies, not provider extras.

**Solution:**
```bash
uv sync --extra all
```

### Issue: API key errors

**Cause:** Environment variable not set.

**Solution:**
```bash
# Check if key is set
echo $ANTHROPIC_API_KEY

# Set it (temporary)
export ANTHROPIC_API_KEY="sk-ant-..."

# Set it permanently (add to ~/.zshrc or ~/.bashrc)
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc
```

### Issue: "command not found: uv"

**Cause:** uv is not installed.

**Solution:**
```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Verify installation
uv --version
```

---

## Project Structure

```
agentui/
├── src/agentui/           # Core framework
│   ├── providers/         # LLM provider implementations
│   │   ├── claude.py      # Requires: anthropic
│   │   └── openai.py      # Requires: openai
│   ├── core.py            # Agent runtime
│   ├── bridge.py          # TUI communication
│   └── protocol.py        # Message protocol
├── examples/              # Example applications
│   ├── simple_agent.py    # Basic agent demo
│   └── generative_ui_demo.py  # Advanced UI demo
└── pyproject.toml         # Dependencies configuration
```

---

## Next Steps

1. ✅ Install dependencies: `uv sync --extra all`
2. ✅ Set API key: `export ANTHROPIC_API_KEY="..."`
3. ✅ Run an example: `uv run python examples/simple_agent.py`
4. 📖 Read the [README](./README.md) for architecture details
5. 🚀 Build your own agent!

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `uv sync` | Install core dependencies only |
| `uv sync --extra all` | Install all providers |
| `uv sync --extra claude` | Install Claude provider |
| `uv sync --extra openai` | Install OpenAI provider |
| `uv sync --extra dev` | Install dev tools |
| `uv add <package>` | Add a new dependency |
| `uv run python <file>` | Run a Python file in the environment |

---

**Last Updated:** 2026-01-18
