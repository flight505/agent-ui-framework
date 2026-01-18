# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**IMPORTANT**: This file contains project-specific instructions, architecture details, development workflows, and technical constraints for Claude. Keep this file updated as the project evolves. User-facing documentation (installation, usage examples, API guides) belongs in README.md.

## Project Overview

AgentUI is a hybrid Go/Python framework for building beautiful AI agent applications with Charm-quality TUIs. It uses a split-process architecture where a Go TUI (Bubbletea) handles rendering and a Python process manages LLM interactions.

**Key Architecture Points:**
- **Two-process design**: Go TUI subprocess communicates with Python agent via JSON Lines over stdio
- **Protocol-based communication**: All interaction between Go and Python happens through a JSON protocol (see `src/agentui/protocol.py` and `internal/protocol/`)
- **Model-agnostic**: Same app works with Claude, OpenAI, Gemini via provider abstraction
- **Generative UI**: Python can send UI primitives (forms, tables, progress bars) to Go for rendering

## Technology Stack

- **Python**: 3.11+ (agent runtime, LLM providers, skill system)
- **Go**: 1.22+ (TUI built with Charm libraries)
- **Charm libraries**: Bubbletea (TUI framework), Lip Gloss (styling), Glamour (markdown), Bubbles (components)
- **Chroma v2**: Syntax highlighting engine with 8x output size increase via ANSI codes
- **Testing**: pytest with ComponentTester framework for isolated UI component testing

## Development Commands

### Python Development
```bash
# Install in dev mode (preferred)
uv sync
uv add --dev <package>

# Run tests
uv run pytest tests/ -v

# Run specific test
uv run pytest tests/test_protocol.py::test_name -v

# Run ComponentTester tests (UI component testing)
uv run pytest tests/test_component_tester.py -v

# Lint and format
uv run ruff check src/ tests/ examples/
uv run ruff format src/ tests/ examples/

# Type checking
uv run mypy src/
```

### Go Development
```bash
# Build TUI binary
make build-tui

# Test headless mode (for automated testing)
echo '{"type":"code","payload":{"language":"python","code":"def hello(): pass","title":"Test"}}' | \
  ./bin/agentui-tui --headless --theme charm-dark

# Run Go tests
make test-go
go test ./... -v

# Format Go code
go fmt ./...

# Lint Go code
go vet ./...
```

### Integration Testing
```bash
# Build everything
make build

# Run demo with TUI
make demo

# Run example apps
uv run python examples/simple_agent.py
uv run python examples/generative_ui_demo.py
```

## Code Architecture

### Python Side (`src/agentui/`)

**Core Components:**
- `app.py`: `AgentApp` - High-level API for creating agents with decorator-based tool registration
- `core.py`: `AgentCore` - Agent execution loop, tool calling, context management
- `bridge.py`: `TUIBridge` - Manages subprocess communication with Go TUI
  - Handles async message passing, request/response correlation, reconnection
  - Also includes `CLIBridge` fallback using Rich when TUI binary unavailable
- `protocol.py`: Protocol message types and payload builders
- `providers/`: LLM provider implementations (Claude, OpenAI)
  - Each provider implements streaming, tool calling, context management
- `skills/`: Skill loader and registry for loading SKILL.md files with tool definitions
- `testing/`: ComponentTester framework for isolated UI testing (Storybook-style for TUIs)
  - `component_tester.py`: Main testing class that renders components via headless TUI
  - `snapshot.py`: ANSISnapshotter for regression testing with baseline comparison
  - `assertions.py`: ANSIAsserter with CharmDark theme-specific color assertions

**Key Design Patterns:**
- Bridge manages all stdio communication - never write to TUI stdin/stdout directly
- Use `create_request()` for messages expecting responses (forms, confirms)
- Use `create_message()` for fire-and-forget (text, progress, alerts)
- All blocking UI operations (forms, confirms) use request/response pattern with UUIDs

### Go Side (`cmd/agentui/`, `internal/`)

**Core Components:**
- `cmd/agentui/main.go`: Entry point, CLI argument parsing, headless mode implementation
  - `--headless` flag enables non-interactive rendering for automated testing
  - Headless mode: reads JSON from stdin → renders → outputs ANSI to stdout → exits
- `internal/app/app.go`: Main Bubbletea model (Elm architecture)
- `internal/protocol/`: JSON protocol reading/writing, message dispatch
- `internal/ui/views/`: UI component renderers (forms, tables, chat, progress)
  - `code_view.go`: Syntax highlighting with Chroma v2 (8x size increase proves ANSI codes work)
- `internal/theme/`: Theme system with Charm aesthetic (CharmDark/CharmLight/CharmAuto as default)

**Key Design Patterns:**
- Everything is a Bubbletea model with Update/View pattern
- Protocol messages arrive as Bubbletea messages via stdin reader
- UI state is immutable - Update returns new model
- Views are pure functions that render lipgloss.Styles

### Communication Flow

```
Python Agent → bridge.send() → JSON → TUI stdin → protocol.handler → Bubbletea Update → View render
User Input → Bubbletea Update → protocol.writer → JSON → bridge.events() → Agent Loop
```

**Critical Points:**
- TUI must respond to requests (forms, confirms) by echoing the request ID
- Python awaits responses using Future pattern in `_pending_requests`
- If TUI crashes, bridge attempts reconnection (configurable retries)

## Common Development Tasks

### Adding a New UI Primitive

1. Define message type in `src/agentui/protocol.py` (MessageType enum)
2. Create payload builder function (e.g., `new_primitive_payload()`)
3. Add convenience method to TUIBridge (e.g., `send_new_primitive()`)
4. Implement Go renderer in `internal/ui/views/`
5. Wire up in `internal/protocol/handler.go` dispatch
6. Add to main Bubbletea model's View() in `internal/app/app.go`

### Adding a New LLM Provider

1. Create `src/agentui/providers/new_provider.py`
2. Implement async streaming and tool calling
3. Match interface used by Claude provider (see `providers/claude.py`)
4. Add provider type to `types.py` ProviderType enum
5. Update `AgentApp._get_api_key()` for environment variable mapping
6. Add to `pyproject.toml` optional dependencies

### Adding Built-in Tools

1. Add tool definition to `src/agentui/skills/builtins.py`
2. Tool handler should be async and return dict or UI primitive
3. Register in core or expose via decorator pattern

### Testing UI Components with ComponentTester

1. Create test in `tests/test_component_tester.py` or new test file
2. Initialize ComponentTester with desired theme: `tester = ComponentTester(theme="charm-dark")`
3. Render component: `result = tester.render_code("python", "def hello(): pass")`
4. Add assertions:
   - Basic: `assert result.success` and `assert result.has_ansi_codes()`
   - Colors: `asserter.assert_has_pink_keywords(result.output)` (CharmDark theme)
   - Content: `asserter.assert_contains_text(result.output, "hello")`
5. Optional: Create snapshot baseline: `snapshotter.save_baseline("test-name", result.output)`
6. Run tests: `uv run pytest tests/test_component_tester.py -v`

**Headless mode troubleshooting:**
- If tests fail with "could not open TTY": Rebuild with `make build-tui`
- Headless mode was added in commit a66aa94
- Test headless directly: `echo '{"type":"code",...}' | ./bin/agentui-tui --headless`

## Testing Strategy

- **Python**: pytest with async support (`pytest-asyncio`)
- **Go**: standard `go test` with table-driven tests
- **ComponentTester**: Isolated UI component testing (like Storybook for TUIs)
  - Test components without full app or LLM integration
  - Uses headless mode for automated rendering
  - Snapshot testing with ANSISnapshotter for regression detection
  - Color/style assertions with ANSIAsserter (CharmDark theme verification)
  - See `docs/COMPONENT_TESTING.md` for full API reference
- **Integration**: Run examples/ scripts that exercise full Python↔Go flow
- **Protocol**: Test message serialization/deserialization independently
- **Syntax highlighting**: Verified via 8x output size increase (92→737 bytes with ANSI codes)

## Environment Variables

- `ANTHROPIC_API_KEY`: For Claude provider
- `OPENAI_API_KEY`: For OpenAI provider
- `GOOGLE_API_KEY`: For Gemini provider

## Binary Distribution

- Go binary built for multiple platforms via `make build-all-platforms`
- Python package includes pre-built binaries in `src/agentui/bin/`
- Bridge searches: dev location `../../../bin/`, package `src/agentui/bin/`, system PATH
- Falls back to Rich CLI rendering if binary not found

## Skills System

Skills are directories with:
- `SKILL.md`: Instructions for LLM (loaded into context)
- `skill.yaml`: Tool definitions (name, parameters, description)

Skills auto-load from manifest `skills:` list. See `examples/skills/weather/` for reference.

## Important Constraints

- **Never block Python event loop**: All subprocess I/O uses `run_in_executor()`
- **TUI binary must be stateless**: All state lives in Python, TUI just renders
- **Protocol is line-delimited**: Each message must be single line JSON
- **IDs are required for requests**: Use `create_request()` which auto-generates UUID
- **Type hints required**: Project uses mypy strict mode (`disallow_untyped_defs = true`)

## Theme & Aesthetic Direction

**IMPORTANT**: The aesthetic goal is to match the Charmbracelet style (Glow, Mods, Huh, etc.).

**Primary Themes (built-in):**
- `CharmDark` - Signature pink/purple/teal on dark (DEFAULT)
- `CharmLight` - Purple-focused light variant
- `CharmAuto` - Auto-detects terminal background

**Charm Signature Colors:**
```go
CharmPurple = "#7D56F4"   // The iconic Charm purple
CharmPink   = "212"       // ANSI 212 (~#ff87d7)
CharmTeal   = "35"        // ANSI 35 (~#00af5f)
```

**DO NOT:**
- Implement Sage, Obsidian, Zephyr, Ember themes (archived direction)
- Bundle many community themes by default
- Use `CompleteAdaptiveColor` everywhere (simple `lipgloss.Color` is fine)

**Theme System:**
- `internal/theme/theme.go`: Core types with `TerminalColor` interface
- `internal/theme/charm.go`: CharmDark, CharmLight, CharmAuto
- `internal/theme/community_themes.go`: Opt-in Catppuccin, Dracula, Nord, Tokyo Night
- `internal/theme/loader.go`: JSON theme loading for extensibility
- Users create themes via JSON in `themes/` directory

**For Implementation Plans**: See `docs/plans/README.md` - only follow the ACTIVE plan.

---

## Current Implementation Status

### ✅ Completed Features

- **Core Framework**: Two-process Python/Go architecture with JSON Lines protocol
- **LLM Providers**: Claude (Anthropic), OpenAI, Gemini support
- **Theme System**: CharmDark (default), CharmLight, CharmAuto with Charm aesthetic
- **Syntax Highlighting**: Chroma v2 integration with verified 8x ANSI output increase
- **UI Primitives**: UICode, UITable, UIProgress, UIForm, UIConfirm
- **ComponentTester Framework** (commit 3496340, a66aa94):
  - Isolated component testing without full app
  - Headless mode (`--headless` flag) for automated testing
  - ANSISnapshotter for snapshot regression testing
  - ANSIAsserter with CharmDark theme color verification
  - All 12 tests passing (0.24s execution time)
  - Complete documentation in `docs/COMPONENT_TESTING.md`
- **Skills System**: SKILL.md loader with tool definitions
- **Bridge Patterns**: TUIBridge (Go subprocess) and CLIBridge (Rich fallback)

### 📚 Documentation

- `CLAUDE.md` - Project instructions for Claude Code (this file)
- `docs/COMPONENT_TESTING.md` - ComponentTester API reference (600+ lines)
- `docs/STORYBOOK_ASSISTANT_EXPANSION.md` - Future plugin integration design (1,000+ lines)
- `COMPONENT_TESTER_SUMMARY.md` - Implementation summary with status
- `SYNTAX_HIGHLIGHTING_VERIFIED.md` - Syntax highlighting proof

### 🚧 In Development

- CI/CD integration for ComponentTester tests
- Additional snapshot baselines for regression testing
- Production examples and demos

### 📋 Future Enhancements (Documented, Not Implemented)

- Storybook Assistant plugin integration (see `docs/STORYBOOK_ASSISTANT_EXPANSION.md`)
- Terminal testing agent with `/test-tui-component` command
- Interactive testing wizards
- Cross-theme testing matrix
- Visual regression HTML reports

**When working on this project**: Always check implementation status above before proposing changes. Prefer extending existing patterns over creating new ones.
