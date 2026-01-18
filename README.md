# AgentUI 🤖✨

> Build beautiful AI agent applications with Charm-quality TUIs

<p align="center">
  <img src="https://img.shields.io/badge/go-1.22+-00ADD8.svg" alt="Go 1.22+">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
</p>

AgentUI combines the beauty of [Charm](https://charm.sh/) terminal UIs with the power of Python's AI ecosystem. Build stunning agent applications that work with Claude, OpenAI, Gemini, and more.

## ✨ Features

- **🎨 Charm-Level Beauty** — Built with Bubbletea, Lip Gloss, and Glamour
- **🔄 Model Agnostic** — Same app works with any LLM provider
- **🎭 Generative UI** — Forms, progress, tables generated at runtime
- **📦 Easy Distribution** — Single binary TUI + pip package
- **🎨 Themes** — Catppuccin, Dracula, Nord, Tokyo Night built-in

## Architecture

```
┌──────────────────────────────────────────────────────┐
│              Terminal (your beautiful TUI)           │
│                   Go + Bubbletea                     │
└──────────────────────────────────────────────────────┘
                         │ JSON protocol
                         ▼
┌──────────────────────────────────────────────────────┐
│                 Python Agent Process                  │
│          Claude / OpenAI / Gemini + Skills           │
└──────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/flight505/agentui
cd agentui

# Install dependencies
uv sync

# Build the TUI binary
make build-tui

# Create a new app
uv run python -m agentui.cli init my-agent

# Run it
cd my-agent
uv run python main.py
```

### Simple Agent

```python
import asyncio
from agentui import AgentApp

app = AgentApp(
    name="my-assistant",
    provider="claude",
)

@app.tool(
    name="get_weather",
    description="Get current weather",
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string"}
        }
    }
)
def get_weather(city: str):
    return {"city": city, "temp": 22, "conditions": "Sunny"}

asyncio.run(app.run())
```

## 🎨 Themes

Built-in themes with Charm aesthetic:
- `charm-dark` (default) — Signature pink/purple/teal on dark
- `charm-light` — Light mode with purple accents
- `charm-auto` — Auto-detect terminal background
- `catppuccin-mocha` — Soothing dark purples
- `catppuccin-latte` — Light mode
- `dracula` — Classic dark
- `nord` — Arctic blues
- `tokyo-night` — Vibrant dark

```bash
# List all themes
uv run python -m agentui.cli themes

# Use a specific theme
uv run python -m agentui.cli run . --theme charm-light
```

## 🎭 Generative UI

The AI can generate beautiful UI elements at runtime:

```python
@app.tool(name="configure_project", is_ui_tool=True)
async def configure_project():
    # This renders as a beautiful form in the TUI
    from agentui.protocol import form_field
    return {
        "type": "form",
        "title": "Project Setup",
        "fields": [
            form_field("name", "Project Name", "text", required=True),
            form_field("stack", "Tech Stack", "select", 
                      options=["Python", "Node.js", "Go"]),
        ]
    }
```

**UI Primitives:**
- Forms with validation
- Progress bars with steps
- Data tables
- Syntax-highlighted code
- Confirmation dialogs
- Selection menus
- Markdown content
- Alerts & notifications

## 📁 Project Structure

```
my-agent/
├── app.yaml              # Configuration
├── skills/               # Agent skills
│   └── research/
│       ├── SKILL.md      # LLM instructions
│       └── skill.yaml    # Tool definitions
└── main.py               # Entry point
```

## 🔧 Development

```bash
# Clone
git clone https://github.com/flight505/agentui
cd agentui

# Install Python dependencies
uv sync

# Build Go TUI
make build-tui

# Run examples
uv run python examples/simple_agent.py
uv run python examples/generative_ui_demo.py
```

### Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run ComponentTester tests (UI component testing)
uv run pytest tests/test_component_tester.py -v

# Test headless mode
echo '{"type":"code","payload":{"language":"python","code":"def hello(): pass","title":"Test"}}' | \
  ./bin/agentui-tui --headless --theme charm-dark
```

### Building from Source

```bash
# Build TUI binary
make build-tui

# Build for all platforms
make build-all-platforms

# Run Go tests
make test-go

# Run Python tests
uv run pytest tests/ -v
```

## 📚 Documentation

- **[CLAUDE.md](./CLAUDE.md)** — Project instructions for Claude Code (architecture, workflows, constraints)
- **[Component Testing](./docs/COMPONENT_TESTING.md)** — ComponentTester API reference for UI testing
- **[Storybook Expansion](./docs/STORYBOOK_ASSISTANT_EXPANSION.md)** — Future plugin integration design

### Status & Verification
- [Component Tester Summary](./COMPONENT_TESTER_SUMMARY.md) — Implementation status
- [Syntax Highlighting Verified](./SYNTAX_HIGHLIGHTING_VERIFIED.md) — Chroma v2 proof

## 🗺️ Roadmap

### ✅ Completed
- [x] Protocol design (JSON Lines communication)
- [x] Go TUI with Bubbletea + Charm libraries
- [x] Python bridge (TUIBridge + CLIBridge fallback)
- [x] Theme system (CharmDark, CharmLight, CharmAuto + community themes)
- [x] Syntax highlighting (Chroma v2 with verified ANSI output)
- [x] ComponentTester framework (Storybook-style testing for TUIs)
- [x] Headless mode for automated testing
- [x] LLM providers (Claude, OpenAI, Gemini)
- [x] UI primitives (Code, Table, Progress, Form, Confirm)
- [x] Skills system

### 🚧 In Progress
- [ ] CI/CD integration for component tests
- [ ] Production examples and demos
- [ ] Package distribution (PyPI)

### 📋 Planned
- [ ] MCP (Model Context Protocol) integration
- [ ] Storybook Assistant plugin expansion
- [ ] Terminal testing agent
- [ ] Plugin marketplace

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md).

## 📄 License

MIT License — see [LICENSE](./LICENSE).

---

<p align="center">
  Built with 💜 using <a href="https://charm.sh">Charm</a>
</p>
