# AgentUI Aesthetic Requirements

> **Updated 2026-01-17**: Focused on authentic Charm aesthetic as primary design language

## Core Philosophy

**"Charm-Quality Terminal Glamour"**

AgentUI adopts the signature Charmbracelet aesthetic—the vaporwave-inspired pink/purple/teal palette with modern rounded borders that makes terminal tools feel glamorous. Rather than bundling many generic themes, we focus on getting one aesthetic right and making it easy for the community to contribute additional themes.

---

## 1. Primary Design Language: Charm

### The Charm Signature

The Charmbracelet aesthetic (seen in Glow, Mods, Huh, etc.) is characterized by:

| Element | Treatment |
|---------|-----------|
| **Primary Accent** | Pink (ANSI 212 / `#ff87d7`) |
| **Secondary Accent** | Purple (`#7D56F4`) |
| **Tertiary Accent** | Teal (ANSI 35 / `#04B575`) |
| **Backgrounds** | Deep dark with subtle blue undertones |
| **Borders** | Rounded, consistently applied |
| **Text** | High contrast white (`#FAFAFA`) on dark |

### Color Constants (from Charmbracelet repos)

```go
// The iconic Charm colors
CharmPurple = lipgloss.Color("#7D56F4")   // From lipgloss examples
CharmPink   = lipgloss.Color("212")        // ANSI 212 (~#ff87d7)
CharmViolet = lipgloss.Color("99")         // ANSI 99 (~#875fff)
CharmTeal   = lipgloss.Color("35")         // ANSI 35 (~#00af5f)
CharmIndigo = lipgloss.Color("63")         // ANSI 63 (~#5f5fff)
```

### Built-in Themes

| Theme | Description |
|-------|-------------|
| **charm-dark** | Signature dark theme (default) |
| **charm-light** | Light variant for bright terminals |
| **charm-auto** | Adapts to terminal background automatically |

---

## 2. Extensible Theme System

### Design for Contribution

Rather than bundling many themes upfront, AgentUI provides:

1. **TerminalColor Interface**: Colors struct accepts any lipgloss color type
2. **JSON Theme Loading**: Users can create themes without Go code
3. **Theme Registry**: Simple registration pattern for new themes
4. **Environment Variable**: `AGENTUI_THEME` for easy switching

### Creating a Custom Theme

```json
{
  "id": "my-theme",
  "name": "My Theme",
  "description": "A custom theme",
  "author": "Your Name",
  "version": "1.0.0",
  "colors": {
    "primary": "#7D56F4",
    "secondary": "#ff00ff",
    "background": "#1a1a2e",
    "surface": "#252538",
    "overlay": "#2f2f45",
    "text": "#FAFAFA",
    "textMuted": "#a9b1d6",
    "textDim": "#565f89",
    "success": "#04B575",
    "warning": "#ffb86c",
    "error": "#ff6b6b",
    "info": "#7dcfff",
    "accent1": "#ff00ff",
    "accent2": "#00ffff",
    "accent3": "#ffff00"
  }
}
```

### Community Themes (opt-in)

Classic terminal themes available in `internal/theme/community_themes.go`:
- Catppuccin Mocha/Latte
- Dracula
- Nord
- Tokyo Night

Call `RegisterCommunityThemes()` to enable them.

---

## 3. Typography Hierarchy

Following Glamour's markdown styling conventions:

| Level | Use | Style |
|-------|-----|-------|
| H1 | Page titles | Bold + Primary + BlockPrefix |
| H2 | Sections | Bold + "▌ " prefix |
| H3 | Subsections | Bold + "┃ " prefix |
| H4 | Items | "│ " prefix |
| H5 | Sub-items | "┆ " prefix |
| H6 | Minor | "┊ " prefix |

### Text Treatment

```go
// Primary content
Foreground(c.Text)

// Secondary/supporting
Foreground(c.TextMuted).Faint(true)

// Disabled/placeholder
Foreground(c.TextDim).Faint(true)

// Emphasis
Bold(true).Foreground(c.Primary)

// System messages
Italic(true).Foreground(c.TextMuted)
```

---

## 4. Border Philosophy

### Rounded Everywhere (Charm Style)

```go
border := lipgloss.RoundedBorder()
```

Charm tools use rounded borders consistently. This creates a cohesive, modern feel without visual noise from mixed border styles.

### Border Hierarchy

| State | Treatment |
|-------|-----------|
| **Default** | Border with TextDim foreground |
| **Focused** | Border with Primary foreground |
| **Active** | Border with Primary + Background surface |
| **Error** | Border with Error foreground |

```go
// Default input
InputField: lipgloss.NewStyle().
    Border(lipgloss.RoundedBorder()).
    BorderForeground(c.TextDim).
    Padding(0, 1),

// Focused input  
InputFieldFocus: lipgloss.NewStyle().
    Border(lipgloss.RoundedBorder()).
    BorderForeground(c.Primary).
    Padding(0, 1),
```

---

## 5. Animation Standards

### Timing Guidelines

| Duration | Use |
|----------|-----|
| 100ms | Micro-interactions (button clicks, toggles) |
| 200-300ms | State transitions (modal open, form reveals) |
| 300-500ms | Layout changes (multi-element reveals) |

### Spinner Selection by Urgency

```go
// Fast operations (API calls)
spinner.Dot     // 10 FPS

// Standard operations (file processing)
spinner.Points  // 7 FPS

// Background operations (sync)
spinner.Globe   // 4 FPS
```

### Harmonica Spring Physics

For smooth modal/dialog positioning:

```go
import "github.com/charmbracelet/harmonica"

spring := harmonica.NewSpring(harmonica.FPS(60), 7.0, 0.15)
```

---

## 6. Component Styling

### User Messages

```go
UserMessage: lipgloss.NewStyle().
    Border(lipgloss.RoundedBorder()).
    BorderForeground(c.Primary).  // Pink/purple accent
    Padding(1, 2).
    MarginTop(1),
```

### Assistant Messages

```go
AssistantMessage: lipgloss.NewStyle().
    Foreground(c.Text).
    Padding(1, 2).
    MarginTop(1),
```

### Forms

```go
FormContainer: lipgloss.NewStyle().
    Border(lipgloss.RoundedBorder()).
    BorderForeground(c.Primary).
    Padding(1, 2).
    Margin(1),

FormButtonFocus: lipgloss.NewStyle().
    Background(c.Primary).
    Foreground(c.Background).
    Border(lipgloss.RoundedBorder()).
    BorderForeground(c.Primary).
    Padding(0, 2),
```

### Alerts

```go
// Consistent border treatment with semantic colors
AlertSuccess: lipgloss.NewStyle().
    Border(lipgloss.RoundedBorder()).
    BorderForeground(c.Success).
    Foreground(c.Text).
    Padding(1, 2),
```

---

## 7. Implementation Status

### Completed ✅

- [x] TerminalColor interface in Colors struct
- [x] CharmDark theme implementation
- [x] CharmLight theme implementation
- [x] CharmAuto adaptive theme
- [x] JSON theme loader
- [x] Theme registry pattern
- [x] Community themes (opt-in)
- [x] Example cyberpunk theme

### Pending

- [ ] Harmonica animation integration
- [ ] Syntax highlighting (Chroma)
- [ ] Staggered reveal animations
- [ ] Progress bar smoothing

---

## 8. Quality Criteria

### Visual Tests

- [ ] 16-color terminal (ANSI fallbacks work)
- [ ] 256-color terminal (ANSI256 mapping correct)
- [ ] TrueColor terminal (hex colors render)
- [ ] Light background (CharmLight contrast)
- [ ] Dark background (CharmDark contrast)

### Aesthetic Checklist

- [x] **Charm Identity**: Looks like a Charmbracelet tool
- [x] **Consistency**: Rounded borders everywhere
- [x] **Hierarchy**: Clear text levels without color overload
- [x] **Extensibility**: Easy to add new themes
- [ ] **Animation**: Smooth, responsive (100-300ms)

---

## Summary

AgentUI's aesthetic is defined by the Charm design language:

1. **Pink/Purple/Teal** accent palette
2. **Rounded borders** consistently applied
3. **High contrast** text on dark backgrounds
4. **Extensible** theme system for community contributions

This creates a TUI that feels like a natural part of the Charmbracelet ecosystem while remaining unique and professional.
