# Nano Banana Setup - AgentUI Project

✅ **Status: Fully Configured and Tested**

## Configuration Summary

| Component | Status | Details |
|-----------|--------|---------|
| **OPENROUTER_API_KEY** | ✅ Set | Environment variable configured |
| **Python** | ✅ 3.14.2 | Compatible version |
| **Nano Banana Plugin** | ✅ v1.0.7 | Installed via Claude Code |
| **Dependencies** | ✅ None | Uses Python stdlib only |

## Installation Location

```
~/.claude/plugins/cache/flight505-plugins/nano-banana/1.0.7/
├── skills/
│   ├── diagram/    - Technical diagrams (architecture, flowcharts, etc.)
│   ├── image/      - AI image generation and editing
│   └── mermaid/    - Text-based diagrams
```

## Quick Start Examples

### 1. Generate Architecture Diagrams

```bash
# Create a system architecture diagram
python3 ~/.claude/plugins/cache/flight505-plugins/nano-banana/1.0.7/skills/diagram/scripts/generate_diagram.py \
  "AgentUI architecture: Python agent process communicates with Go TUI via JSON Lines protocol" \
  -o docs/architecture.png \
  --doc-type architecture

# Create a flowchart
python3 ~/.claude/plugins/cache/flight505-plugins/nano-banana/1.0.7/skills/diagram/scripts/generate_diagram.py \
  "User request flow: Input -> AgentCore -> LLM Provider -> Response -> TUI" \
  -o docs/flowchart.png \
  --doc-type presentation
```

### 2. Generate Images

```bash
# Generate project logo/icon
python3 ~/.claude/plugins/cache/flight505-plugins/nano-banana/1.0.7/skills/image/scripts/generate_image.py \
  "Modern minimalist logo for AgentUI: terminal window with AI sparkles, purple and pink gradient" \
  -o assets/logo.png

# Edit existing image
python3 ~/.claude/plugins/cache/flight505-plugins/nano-banana/1.0.7/skills/image/scripts/generate_image.py \
  "Add a subtle glow effect around the edges" \
  --input assets/logo.png \
  -o assets/logo_glow.png
```

### 3. Create Mermaid Diagrams (Text-based)

```bash
# Generate a sequence diagram
python3 ~/.claude/plugins/cache/flight505-plugins/nano-banana/1.0.7/skills/mermaid/scripts/generate_mermaid.py \
  "User authentication flow with JWT tokens" \
  --type sequence \
  -o docs/auth_flow.mmd
```

## Available Diagram Types

**For Technical Documentation** (`--doc-type architecture`):
- System architecture diagrams
- Database schemas
- Network topology
- Component relationships
- Higher quality threshold (8.0/10)

**For Presentations** (`--doc-type presentation`):
- Flowcharts
- Process diagrams
- Concept visualization
- Lower quality threshold (6.5/10)

**For Social Media** (`--doc-type social`):
- Infographics
- Visual storytelling
- Engagement-focused
- Balanced threshold (7.0/10)

## Quality Thresholds

Nano Banana uses AI-powered quality review:

| Document Type | Threshold | Max Iterations |
|--------------|-----------|----------------|
| Architecture | 8.0/10 | 2 |
| Social Media | 7.0/10 | 2 |
| Presentation | 6.5/10 | 2 |

The system auto-regenerates if quality is below threshold.

## API Models Used

- **Diagrams**: `google/gemini-3-pro-image-preview` (Nano Banana Pro)
- **Images**: `google/gemini-3-pro-image-preview` or `black-forest-labs/flux-1.1-pro`
- **Quality Review**: `google/gemini-3-pro-image-preview`

## Test Results

✅ **Diagram Generation Test**
```
Input: "Simple flowchart: Start -> Process -> End"
Output: test_diagram.png (274 KB, 1408x768 JPEG)
Score: 7.5/10 (passed on first iteration)
```

✅ **Image Generation Test**
```
Input: "A simple geometric pattern with blue triangles"
Output: test_image.png (1.8 MB, 1408x768 PNG)
Generated successfully
```

## Integration with AgentUI

Use Nano Banana to create visual assets for the project:

1. **Architecture Diagrams** - Document the Python↔Go architecture
2. **Flowcharts** - Show LLM provider flow, tool calling, etc.
3. **UI Mockups** - Visualize theme concepts (CharmDark aesthetic)
4. **Logo/Branding** - Generate project logos and icons
5. **Documentation Images** - Create visual guides for README.md

## Example: Create Project Architecture Diagram

```bash
python3 ~/.claude/plugins/cache/flight505-plugins/nano-banana/1.0.7/skills/diagram/scripts/generate_diagram.py \
  "AgentUI System Architecture:
   - Top: Terminal UI (Go + Bubbletea)
   - Middle: JSON Lines Protocol Communication
   - Bottom: Python Agent (LLM Providers + Skills)
   - Highlight: CharmDark theme with pink/purple/teal colors" \
  -o docs/images/architecture-overview.png \
  --doc-type architecture
```

## Troubleshooting

### API Errors
- Check OpenRouter credits: https://openrouter.ai/activity
- Verify API key: `echo $OPENROUTER_API_KEY`

### Permission Issues
```bash
chmod +x ~/.claude/plugins/cache/flight505-plugins/nano-banana/1.0.7/skills/*/scripts/*.py
```

### File Not Found
- Use absolute paths for output files
- Ensure output directory exists

## Next Steps

1. Create `docs/images/` directory for project diagrams
2. Generate architecture overview diagram
3. Create CharmDark theme visualization
4. Add visual assets to README.md

## Resources

- OpenRouter Dashboard: https://openrouter.ai/
- Nano Banana Plugin: https://github.com/flight505/nano-banana
- Claude Code Plugins: https://claude.ai/plugins

---

**Setup Date**: 2026-01-18
**Plugin Version**: 1.0.7
**Status**: ✅ Production Ready
