# Testing AgentUI with Real LLM

This guide explains how to test the complete AgentUI framework with real Claude API calls.

---

## Prerequisites

### 1. API Key

You need an Anthropic API key:

```bash
export ANTHROPIC_API_KEY='your-key-here'
```

To verify it's set:

```bash
echo $ANTHROPIC_API_KEY
```

### 2. Dependencies

Ensure all dependencies are installed:

```bash
uv sync
make build-tui
```

---

## Quick Demo

The fastest way to test real LLM integration:

```bash
python examples/quick_llm_demo.py
```

### What This Tests

- ✅ **Real streaming responses** from Claude Sonnet 4.5
- ✅ **CharmDark theme** with pink/purple/teal aesthetic
- ✅ **Syntax highlighting** (Chroma) for Python, Go, TypeScript, Rust
- ✅ **Spring physics animations** when tools are called
- ✅ **Full Python↔Go communication** over JSON protocol

### Example Prompts

Try these to see all features:

```
Show me Python code using show_code_example
```
→ Triggers syntax-highlighted code block with CharmDark colors

```
Show me Go code
```
→ Tests Go syntax highlighting with Chroma lexer

```
Show me TypeScript code
```
→ Demonstrates TypeScript highlighting

```
Explain async/await in Python
```
→ Tests streaming response rendering with Charm aesthetic

---

## Comprehensive Test

For testing all UI primitives:

```bash
python examples/llm_integration_test.py
```

### Features Tested

| Feature | Tool | Test |
|---------|------|------|
| **Syntax Highlighting** | `show_syntax_example` | Python/Go code with Chroma |
| **Tables** | `show_benchmark_results` | Performance data in table format |
| **Progress Indicators** | `simulate_deployment` | Multi-step progress with icons |
| **Streaming Text** | Native | Real-time token streaming |
| **Animations** | All UI tools | Spring physics modal fade-in |

### Test Prompts

```bash
# Syntax highlighting
Show me a Python async example using the show_syntax_example tool

# Tables
Show benchmark results for web frameworks using show_benchmark_results

# Progress bars
Simulate a production deployment using simulate_deployment

# Go code
Show me a Go concurrency example with the syntax tool
```

---

## What to Look For

### 1. CharmDark Theme

When the TUI launches, you should see:

- **Background**: Deep dark blue (#1a1a2e)
- **Primary text**: Bright white (#FAFAFA)
- **Accents**: Pink (ANSI 212), Purple (#7D56F4), Teal (ANSI 35)
- **Borders**: Rounded everywhere
- **Header**: Pink/purple gradient

### 2. Syntax Highlighting

When code is displayed:

- **Keywords**: Pink (bold) - `def`, `async`, `if`, `for`
- **Strings**: Teal - `"hello"`, `'world'`
- **Numbers**: Pink - `42`, `3.14`
- **Comments**: Dim gray (italic) - `# comment`
- **Functions**: Purple - `function_name()`
- **Types**: Teal - `int`, `str`, `bool`

### 3. Streaming Responses

Text should appear character-by-character:
- Smooth scrolling
- No blocking
- Progress indicator (spinner) while streaming

### 4. Animations

When forms/tools appear:
- **Fade in**: ~250ms smooth opacity transition
- **Slide down**: Gentle spring physics from top
- **No jumpiness**: Smooth motion throughout

### 5. UI Primitives

**Tables**:
- Rounded borders
- Pink header
- Alternating row colors
- Aligned columns

**Code Blocks**:
- Rounded container
- Title bar with pink accent
- Line numbers (gray)
- Syntax-colored code

**Progress Bars**:
- Pink filled portion
- Gray empty portion
- Step icons: ✓ (complete), ● (running), ○ (pending)

---

## Testing Different Themes

### CharmLight (Light Mode)

```bash
# Edit examples/quick_llm_demo.py
# Change: theme="charm-dark"
# To: theme="charm-light"

python examples/quick_llm_demo.py
```

Look for:
- Light background (#faf4ed)
- Dark text (#1a1a2e)
- Purple accents
- Readable in bright terminals

### CharmAuto (Adaptive)

```bash
# Change: theme="charm-auto"

python examples/quick_llm_demo.py
```

Should adapt to your terminal's background automatically.

### Custom Theme (JSON)

```bash
AGENTUI_THEME=themes/cyberpunk.json python examples/quick_llm_demo.py
```

Tests the JSON theme loader.

---

## Troubleshooting

### "API key not found"

```bash
# Make sure it's exported
export ANTHROPIC_API_KEY='sk-ant-...'

# Verify
echo $ANTHROPIC_API_KEY
```

### "TUI binary not found"

```bash
# Build the Go TUI
make build-tui

# Verify it exists
ls -la bin/agentui-tui
```

### "Connection refused" or protocol errors

```bash
# Rebuild both sides
make build
uv sync

# Check Go compilation
go build ./...
```

### Streaming looks choppy

This is normal if:
- Running on slow connection
- Claude API is rate-limiting
- Terminal emulator is slow

Try:
- Use a faster terminal (iTerm2, Warp, Alacritty)
- Reduce response length
- Check network connection

---

## Performance Testing

### Measure Streaming Latency

Watch how fast tokens appear. Should see:
- **First token**: ~500-800ms (network + Claude processing)
- **Subsequent tokens**: Real-time as they arrive
- **Tool calls**: Appear immediately when streamed

### Animation Smoothness

Forms/modals should:
- **Fade in**: Smooth opacity 0→1 over ~250ms
- **Slide**: Natural spring motion, slight overshoot
- **Settle**: Stop smoothly without abrupt end

### Memory Usage

```bash
# Check Python process
ps aux | grep python

# Check Go TUI
ps aux | grep agentui-tui
```

Expected:
- Python: 50-150 MB (depends on provider libraries)
- Go TUI: 10-30 MB (lightweight)

---

## Automated Testing

For CI/CD or headless testing:

```bash
# Test without API calls (unit tests)
go test ./internal/theme/... -v
uv run pytest tests/ -v

# Test protocol without LLM
uv run python examples/theme_test.py charm-dark
```

---

## Reporting Issues

If you find problems, provide:

1. **Go version**: `go version`
2. **Python version**: `python --version`
3. **Terminal**: Name and version
4. **Theme**: Which theme you were using
5. **Error message**: Full traceback
6. **Steps to reproduce**: Exact prompts used

---

## Success Criteria

✅ **Theme Rendering**
- CharmDark colors visible
- Rounded borders everywhere
- Pink/purple/teal accents

✅ **Syntax Highlighting**
- Keywords are pink
- Strings are teal
- Comments are gray/italic
- Line numbers visible

✅ **Animations**
- Modals fade in smoothly
- Spring motion feels natural
- No visual glitches

✅ **Streaming**
- Text appears in real-time
- No blocking or freezing
- Spinner shows during processing

✅ **Tools**
- Code blocks render correctly
- Tables are formatted properly
- Progress bars update smoothly

---

## Next Steps

After verifying LLM integration works:

1. **Build your own agent**: See `examples/simple_agent.py`
2. **Create custom themes**: See `CONTRIBUTING.md`
3. **Add tools**: See agent docs in `src/agentui/`
4. **Optimize prompts**: See Claude docs

---

## Resources

- **Claude API**: https://docs.anthropic.com/
- **AgentUI Docs**: `/docs/`
- **Charm Libraries**: https://github.com/charmbracelet
- **Examples**: `/examples/`

---

Happy testing! 🎨✨
