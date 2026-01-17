# AgentUI Charm Aesthetic Implementation Plan

**Date**: 2026-01-17  
**Status**: Active  
**Focus**: Authentic Charm aesthetic with extensible theme system

## Overview

This plan focuses on implementing the authentic Charm aesthetic—the signature pink/purple/teal "vaporwave glamour" look used by Charmbracelet across their tools (Glow, Mods, Huh, etc.)—rather than bundling multiple community themes.

### Philosophy
- **Get one theme right** before adding variety
- **Charm Dark + Charm Light** as the primary themes
- **Extensible architecture** so users can contribute themes via PR
- **Type-safe color system** supporting adaptive colors

---

## Phase 0: Type System Foundation

### 0.1 Refactor Colors to TerminalColor Interface

**Problem Identified**: Current `Colors` struct uses `lipgloss.Color` (a string alias), but adaptive colors require `lipgloss.TerminalColor` interface.

**File**: `internal/theme/theme.go`

```go
// Colors defines the color palette using TerminalColor interface
// for maximum flexibility (simple colors, adaptive, complete, etc.)
type Colors struct {
    // Core colors
    Primary    lipgloss.TerminalColor
    Secondary  lipgloss.TerminalColor
    Background lipgloss.TerminalColor
    Surface    lipgloss.TerminalColor
    Overlay    lipgloss.TerminalColor

    // Text colors  
    Text      lipgloss.TerminalColor
    TextMuted lipgloss.TerminalColor
    TextDim   lipgloss.TerminalColor

    // Semantic colors
    Success lipgloss.TerminalColor
    Warning lipgloss.TerminalColor
    Error   lipgloss.TerminalColor
    Info    lipgloss.TerminalColor

    // Accent colors (Charm signature: pink, purple, teal)
    Accent1 lipgloss.TerminalColor  // Pink
    Accent2 lipgloss.TerminalColor  // Purple  
    Accent3 lipgloss.TerminalColor  // Teal
}
```

**Why TerminalColor interface?**
- `lipgloss.Color` → Simple ANSI/hex colors
- `lipgloss.AdaptiveColor` → Light/dark terminal background detection
- `lipgloss.CompleteColor` → Explicit TrueColor/ANSI256/ANSI fallbacks
- `lipgloss.CompleteAdaptiveColor` → Full control over all scenarios

All implement `TerminalColor`, so our Colors struct accepts any.

### 0.2 Add Theme Registry Pattern

**File**: `internal/theme/registry.go` (new)

```go
package theme

import "sync"

// Registry manages available themes
type Registry struct {
    mu     sync.RWMutex
    themes map[string]*Theme
}

var DefaultRegistry = &Registry{
    themes: make(map[string]*Theme),
}

func (r *Registry) Register(t *Theme) {
    r.mu.Lock()
    defer r.mu.Unlock()
    r.themes[t.ID] = t
}

func (r *Registry) Get(id string) (*Theme, bool) {
    r.mu.RLock()
    defer r.mu.RUnlock()
    t, ok := r.themes[id]
    return t, ok
}

func (r *Registry) List() []string {
    r.mu.RLock()
    defer r.mu.RUnlock()
    names := make([]string, 0, len(r.themes))
    for name := range r.themes {
        names = append(names, name)
    }
    return names
}

// Theme metadata for extensibility
type Theme struct {
    ID          string   // e.g., "charm-dark"
    Name        string   // e.g., "Charm Dark"
    Description string   // e.g., "The signature Charm aesthetic"
    Author      string   // e.g., "AgentUI Team"
    Version     string   // e.g., "1.0.0"
    Colors      Colors
    Styles      Styles
}
```

---

## Phase 1: Charm Aesthetic Implementation

### 1.1 Charm Color Palette Research

From Charmbracelet's official repos and documentation:

| Role | Hex/ANSI | Description |
|------|----------|-------------|
| **Primary Purple** | `#7D56F4` | The signature Charm purple (from lipgloss examples) |
| **Pink** | ANSI `212` / `#ff87d7` | Glamour headings, highlights |
| **Secondary Purple** | ANSI `99` / `#875fff` | Enumerators, accents |
| **Teal** | ANSI `35` / `#04B575` | Success, tree roots |
| **Border Purple** | ANSI `63` / `#5f5fff` | Borders, subtle accents |
| **White** | `#FAFAFA` | Primary text |
| **Dark Background** | `#1a1a2e` | Deep dark with slight blue |
| **Surface** | `#2a2a3e` | Elevated surfaces |

### 1.2 Charm Dark Theme

**File**: `internal/theme/charm.go` (new)

```go
package theme

import "github.com/charmbracelet/lipgloss"

// Charm signature colors
var (
    // The iconic Charm purple
    CharmPurple = lipgloss.Color("#7D56F4")
    
    // Pink - the glamour accent (ANSI 212)
    CharmPink = lipgloss.Color("212")
    
    // Secondary purple (ANSI 99)  
    CharmViolet = lipgloss.Color("99")
    
    // Teal accent (ANSI 35)
    CharmTeal = lipgloss.Color("35")
    
    // Border purple (ANSI 63)
    CharmIndigo = lipgloss.Color("63")
)

// CharmDark is the signature Charm aesthetic - dark variant
var CharmDark = Theme{
    ID:          "charm-dark",
    Name:        "Charm Dark",
    Description: "The signature Charm aesthetic - glamorous terminal vibes",
    Author:      "AgentUI Team",
    Version:     "1.0.0",
    Colors: Colors{
        // Core - deep dark with purple undertones
        Primary:    CharmPink,                    // Pink headlines
        Secondary:  CharmPurple,                  // Purple accents
        Background: lipgloss.Color("#1a1a2e"),    // Deep dark blue
        Surface:    lipgloss.Color("#252538"),    // Elevated surface
        Overlay:    lipgloss.Color("#2f2f45"),    // Overlays/modals

        // Text - high contrast
        Text:      lipgloss.Color("#FAFAFA"),     // Bright white
        TextMuted: lipgloss.Color("#a9b1d6"),     // Muted lavender
        TextDim:   lipgloss.Color("#565f89"),     // Dim purple-gray

        // Semantic
        Success: lipgloss.Color("#04B575"),       // Charm teal-green
        Warning: lipgloss.Color("#ffb86c"),       // Warm orange
        Error:   lipgloss.Color("#ff6b6b"),       // Soft red
        Info:    lipgloss.Color("#7dcfff"),       // Cyan

        // Accents - the Charm trinity
        Accent1: CharmPink,                       // Pink
        Accent2: CharmPurple,                     // Purple
        Accent3: CharmTeal,                       // Teal
    },
}

// CharmLight is the signature Charm aesthetic - light variant
var CharmLight = Theme{
    ID:          "charm-light", 
    Name:        "Charm Light",
    Description: "The signature Charm aesthetic - light mode",
    Author:      "AgentUI Team",
    Version:     "1.0.0",
    Colors: Colors{
        // Core - warm light with purple accents
        Primary:    lipgloss.Color("#7D56F4"),    // Purple (darker for light bg)
        Secondary:  lipgloss.Color("#d946ef"),    // Fuchsia
        Background: lipgloss.Color("#faf4ed"),    // Warm off-white
        Surface:    lipgloss.Color("#f2e9e1"),    // Subtle surface
        Overlay:    lipgloss.Color("#e8ddd5"),    // Overlay

        // Text - dark for contrast
        Text:      lipgloss.Color("#1a1a2e"),     // Deep dark
        TextMuted: lipgloss.Color("#6e6a86"),     // Muted purple
        TextDim:   lipgloss.Color("#9893a5"),     // Light muted

        // Semantic  
        Success: lipgloss.Color("#059669"),       // Deeper teal
        Warning: lipgloss.Color("#d97706"),       // Amber
        Error:   lipgloss.Color("#dc2626"),       // Red
        Info:    lipgloss.Color("#0284c7"),       // Blue

        // Accents
        Accent1: lipgloss.Color("#d946ef"),       // Fuchsia
        Accent2: lipgloss.Color("#7D56F4"),       // Purple
        Accent3: lipgloss.Color("#059669"),       // Teal
    },
}

func init() {
    // Build styles from colors
    CharmDark.Styles = BuildStyles(CharmDark.Colors)
    CharmLight.Styles = BuildStyles(CharmLight.Colors)
    
    // Register themes
    DefaultRegistry.Register(&CharmDark)
    DefaultRegistry.Register(&CharmLight)
}
```

### 1.3 Auto-Detection Theme

For terminals that support background detection:

```go
// CharmAuto automatically selects light/dark based on terminal
var CharmAuto = Theme{
    ID:   "charm-auto",
    Name: "Charm Auto",
    Colors: Colors{
        Primary: lipgloss.AdaptiveColor{
            Light: "#7D56F4",  // Purple on light bg
            Dark:  "#ff87d7",  // Pink on dark bg (ANSI 212 equiv)
        },
        Background: lipgloss.AdaptiveColor{
            Light: "#faf4ed",
            Dark:  "#1a1a2e",
        },
        // ... etc
    },
}
```

---

## Phase 2: Style Refinements

### 2.1 Charm-Style Borders

The Charm look uses rounded borders consistently:

```go
// Update BuildStyles to use Charm aesthetic
func BuildStyles(c Colors) Styles {
    // Charm uses rounded borders everywhere
    border := lipgloss.RoundedBorder()
    
    return Styles{
        // Messages with the iconic rounded + pink border
        UserMessage: lipgloss.NewStyle().
            Border(border).
            BorderForeground(c.Primary).
            Padding(1, 2).
            MarginTop(1),
            
        // Charm-style input with subtle border that pops on focus
        InputField: lipgloss.NewStyle().
            Border(border).
            BorderForeground(c.TextDim).
            Padding(0, 1),
            
        InputFieldFocus: lipgloss.NewStyle().
            Border(border).
            BorderForeground(c.Primary).  // Pink/purple pop
            Padding(0, 1),
        
        // ... rest of styles
    }
}
```

### 2.2 Typography Hierarchy

Based on Glamour's markdown styling:

```go
// Heading styles following Glamour conventions
type HeadingStyles struct {
    H1 lipgloss.Style  // Bold, primary color, with prefix
    H2 lipgloss.Style  // Bold with "▌ " prefix
    H3 lipgloss.Style  // Bold with "┃ " prefix
    H4 lipgloss.Style  // With "│ " prefix
    H5 lipgloss.Style  // With "┆ " prefix
    H6 lipgloss.Style  // With "┊ " prefix
}
```

---

## Phase 3: Theme Extensibility

### 3.1 JSON Theme Loading

Allow users to define themes in JSON (like Glamour):

**File**: `internal/theme/loader.go`

```go
package theme

import (
    "encoding/json"
    "os"
)

// ThemeJSON for loading from files
type ThemeJSON struct {
    ID          string           `json:"id"`
    Name        string           `json:"name"`
    Description string           `json:"description,omitempty"`
    Author      string           `json:"author,omitempty"`
    Colors      ColorsJSON       `json:"colors"`
}

type ColorsJSON struct {
    Primary    string `json:"primary"`
    Secondary  string `json:"secondary"`
    Background string `json:"background"`
    // ... etc
}

// LoadThemeFromFile loads a theme from JSON
func LoadThemeFromFile(path string) (*Theme, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, err
    }
    return LoadThemeFromJSON(data)
}

func LoadThemeFromJSON(data []byte) (*Theme, error) {
    var tj ThemeJSON
    if err := json.Unmarshal(data, &tj); err != nil {
        return nil, err
    }
    return tj.ToTheme(), nil
}
```

### 3.2 Example Custom Theme (for contributors)

**File**: `themes/example-cyberpunk.json`

```json
{
  "id": "cyberpunk",
  "name": "Cyberpunk 2077",
  "description": "Neon-drenched night city vibes",
  "author": "Community",
  "colors": {
    "primary": "#00ffff",
    "secondary": "#ff00ff", 
    "background": "#0a0a12",
    "surface": "#1a1a2e",
    "text": "#ffffff",
    "textMuted": "#8b8ba7",
    "success": "#00ff9f",
    "warning": "#ffff00",
    "error": "#ff0055",
    "info": "#00ffff",
    "accent1": "#ff00ff",
    "accent2": "#00ffff",
    "accent3": "#ffff00"
  }
}
```

### 3.3 Theme Environment Variable

```go
// Allow users to set theme via env
func LoadFromEnv() {
    if themePath := os.Getenv("AGENTUI_THEME"); themePath != "" {
        if theme, err := LoadThemeFromFile(themePath); err == nil {
            DefaultRegistry.Register(theme)
            SetTheme(theme.ID)
        }
    }
}
```

---

## Phase 4: Migration & Cleanup

### 4.1 Remove Bundled Community Themes

The current `themes.go` has Catppuccin, Dracula, Nord, Tokyo Night. These should be:
1. Moved to a `themes/` directory as JSON files
2. Marked as "community themes" in documentation
3. Not loaded by default (users can opt-in)

### 4.2 Update Default Theme

```go
// Default to Charm Dark
var Current = CharmDark

// Available built-in themes
var Available = map[string]*Theme{
    "charm-dark":  &CharmDark,
    "charm-light": &CharmLight,
    "charm-auto":  &CharmAuto,
}
```

---

## Implementation Order

1. **Phase 0.1**: Refactor `Colors` struct to use `TerminalColor` interface ✅ Critical
2. **Phase 0.2**: Add Registry pattern for theme management
3. **Phase 1.2**: Implement `CharmDark` theme
4. **Phase 1.2**: Implement `CharmLight` theme  
5. **Phase 2.1**: Update `BuildStyles` with Charm aesthetic
6. **Phase 3.1**: Add JSON theme loader
7. **Phase 4.1**: Move community themes to opt-in JSON files

---

## Verification

After implementation:

```bash
# Build and test
cd /Users/jesper/Projects/Dev_projects/Claude_SDK/agent-ui-framework
go build ./...
go test ./internal/theme/...

# Visual verification
go run ./cmd/agentui --theme charm-dark
go run ./cmd/agentui --theme charm-light
```

---

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `internal/theme/theme.go` | Modify | Change `lipgloss.Color` → `lipgloss.TerminalColor` |
| `internal/theme/registry.go` | Create | Theme registry with metadata |
| `internal/theme/charm.go` | Create | CharmDark, CharmLight, CharmAuto |
| `internal/theme/loader.go` | Create | JSON theme loading |
| `internal/theme/themes.go` | Delete/Move | Move to themes/*.json |
| `themes/` | Create | Directory for community themes |
| `themes/catppuccin-mocha.json` | Create | Optional community theme |
| `themes/dracula.json` | Create | Optional community theme |
| `CONTRIBUTING.md` | Update | Document how to contribute themes |

---

## Notes

- The Charm aesthetic is intentionally "maximalist minimalism"—bold colors but clean layouts
- Pink (ANSI 212) and purple (#7D56F4) are the signature colors
- Rounded borders (`lipgloss.RoundedBorder()`) are used consistently
- High contrast text (#FAFAFA on dark) for readability
- The goal is to look like it belongs in the Charm ecosystem
