# AgentUI Themes

This directory contains community-contributed themes for AgentUI.

## Using Custom Themes

### Via Environment Variable

```bash
export AGENTUI_THEME=/path/to/your/theme.json
agentui
```

### Via Theme ID

Built-in themes can be selected by ID:

```bash
export AGENTUI_THEME=charm-dark
```

## Creating a Theme

1. Copy `cyberpunk.json` as a template
2. Modify the colors to your preference
3. Test your theme locally
4. Submit a PR to share with the community

### Color Format

Colors can be specified as:

- **Hex colors**: `"#7D56F4"`, `"#ff00ff"`
- **ANSI 256 colors**: `"212"`, `"99"`, `"35"`
- **Named colors**: `"red"`, `"blue"`, `"cyan"`

### Theme Structure

```json
{
  "id": "my-theme",
  "name": "My Theme",
  "description": "A brief description",
  "author": "Your Name",
  "version": "1.0.0",
  "colors": {
    "primary": "#7D56F4",      // Main accent color (headings, focus)
    "secondary": "#ff00ff",    // Secondary accent
    "background": "#1a1a2e",   // Main background
    "surface": "#252538",      // Cards, elevated surfaces
    "overlay": "#2f2f45",      // Modals, overlays
    "text": "#FAFAFA",         // Primary text
    "textMuted": "#a9b1d6",    // Secondary text
    "textDim": "#565f89",      // Disabled, placeholders
    "success": "#04B575",      // Success states
    "warning": "#ffb86c",      // Warning states
    "error": "#ff6b6b",        // Error states
    "info": "#7dcfff",         // Info states
    "accent1": "#ff00ff",      // Additional accent 1
    "accent2": "#00ffff",      // Additional accent 2
    "accent3": "#ffff00"       // Additional accent 3
  }
}
```

## Built-in Themes

| ID | Name | Description |
|----|------|-------------|
| `charm-dark` | Charm Dark | The signature Charm aesthetic (default) |
| `charm-light` | Charm Light | Light mode Charm aesthetic |
| `charm-auto` | Charm Auto | Automatically adapts to terminal |

## Community Themes

| ID | Name | Author | Description |
|----|------|--------|-------------|
| `cyberpunk` | Cyberpunk | Community | Neon night city vibes |

## Contributing

1. Fork the repository
2. Create your theme JSON file
3. Add it to this directory
4. Update this README with your theme info
5. Submit a Pull Request

### Guidelines

- **Contrast**: Ensure sufficient contrast between text and background
- **Consistency**: Use consistent color relationships
- **Testing**: Test in both TrueColor and 256-color terminals
- **ANSI Fallbacks**: Consider providing ANSI 256 alternatives for important colors

### Testing Your Theme

```bash
# Test with your theme
AGENTUI_THEME=./themes/your-theme.json go run ./cmd/agentui

# Export a built-in theme to study its structure
agentui theme export charm-dark > charm-dark.json
```
