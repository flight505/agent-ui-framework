package theme

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/charmbracelet/lipgloss"
)

// ThemeJSON represents a theme definition in JSON format.
// This allows users to create custom themes without writing Go code.
type ThemeJSON struct {
	ID          string     `json:"id"`
	Name        string     `json:"name"`
	Description string     `json:"description,omitempty"`
	Author      string     `json:"author,omitempty"`
	Version     string     `json:"version,omitempty"`
	Colors      ColorsJSON `json:"colors"`
}

// ColorsJSON represents color definitions in JSON format.
// Colors can be specified as:
// - Hex: "#7D56F4"
// - ANSI 256: "212"
// - Named: "red", "blue", etc.
type ColorsJSON struct {
	Primary    string `json:"primary"`
	Secondary  string `json:"secondary"`
	Background string `json:"background"`
	Surface    string `json:"surface"`
	Overlay    string `json:"overlay"`

	Text      string `json:"text"`
	TextMuted string `json:"textMuted"`
	TextDim   string `json:"textDim"`

	Success string `json:"success"`
	Warning string `json:"warning"`
	Error   string `json:"error"`
	Info    string `json:"info"`

	Accent1 string `json:"accent1"`
	Accent2 string `json:"accent2"`
	Accent3 string `json:"accent3"`
}

// LoadThemeFromFile loads a theme from a JSON file.
func LoadThemeFromFile(path string) (*Theme, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read theme file: %w", err)
	}
	return LoadThemeFromJSON(data)
}

// LoadThemeFromJSON loads a theme from JSON data.
func LoadThemeFromJSON(data []byte) (*Theme, error) {
	var tj ThemeJSON
	if err := json.Unmarshal(data, &tj); err != nil {
		return nil, fmt.Errorf("failed to parse theme JSON: %w", err)
	}
	return tj.ToTheme()
}

// ToTheme converts a ThemeJSON to a Theme.
func (tj *ThemeJSON) ToTheme() (*Theme, error) {
	colors := Colors{
		Primary:    parseColor(tj.Colors.Primary),
		Secondary:  parseColor(tj.Colors.Secondary),
		Background: parseColor(tj.Colors.Background),
		Surface:    parseColor(tj.Colors.Surface),
		Overlay:    parseColor(tj.Colors.Overlay),
		Text:       parseColor(tj.Colors.Text),
		TextMuted:  parseColor(tj.Colors.TextMuted),
		TextDim:    parseColor(tj.Colors.TextDim),
		Success:    parseColor(tj.Colors.Success),
		Warning:    parseColor(tj.Colors.Warning),
		Error:      parseColor(tj.Colors.Error),
		Info:       parseColor(tj.Colors.Info),
		Accent1:    parseColor(tj.Colors.Accent1),
		Accent2:    parseColor(tj.Colors.Accent2),
		Accent3:    parseColor(tj.Colors.Accent3),
	}

	return &Theme{
		ID:          tj.ID,
		Name:        tj.Name,
		Description: tj.Description,
		Author:      tj.Author,
		Version:     tj.Version,
		Colors:      colors,
		Styles:      BuildStyles(colors),
	}, nil
}

// parseColor converts a color string to a lipgloss.Color.
// Accepts hex (#7D56F4), ANSI numbers (212), or color names.
func parseColor(s string) lipgloss.TerminalColor {
	if s == "" {
		return lipgloss.Color("")
	}
	return lipgloss.Color(s)
}

// LoadThemesFromDirectory loads all JSON themes from a directory.
// Returns the number of themes loaded and any errors encountered.
func LoadThemesFromDirectory(dir string) (int, []error) {
	var errors []error
	count := 0

	entries, err := os.ReadDir(dir)
	if err != nil {
		return 0, []error{fmt.Errorf("failed to read themes directory: %w", err)}
	}

	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}

		name := entry.Name()
		if !strings.HasSuffix(name, ".json") {
			continue
		}

		path := filepath.Join(dir, name)
		theme, err := LoadThemeFromFile(path)
		if err != nil {
			errors = append(errors, fmt.Errorf("failed to load %s: %w", name, err))
			continue
		}

		Register(theme)
		count++
	}

	return count, errors
}

// LoadThemeFromEnv loads a theme specified by the AGENTUI_THEME environment variable.
// The variable can be:
// - A theme ID: "charm-dark"
// - A file path: "/path/to/theme.json"
func LoadThemeFromEnv() error {
	themePath := os.Getenv("AGENTUI_THEME")
	if themePath == "" {
		return nil
	}

	// Check if it's a registered theme ID
	if _, ok := Available[themePath]; ok {
		SetTheme(themePath)
		return nil
	}

	// Check if it's a file path
	if _, err := os.Stat(themePath); err == nil {
		theme, err := LoadThemeFromFile(themePath)
		if err != nil {
			return fmt.Errorf("failed to load theme from %s: %w", themePath, err)
		}
		Register(theme)
		SetTheme(theme.ID)
		return nil
	}

	return fmt.Errorf("unknown theme: %s", themePath)
}

// ExportThemeToJSON exports a theme to JSON format.
func ExportThemeToJSON(t *Theme) ([]byte, error) {
	tj := ThemeJSON{
		ID:          t.ID,
		Name:        t.Name,
		Description: t.Description,
		Author:      t.Author,
		Version:     t.Version,
		Colors: ColorsJSON{
			Primary:    colorToString(t.Colors.Primary),
			Secondary:  colorToString(t.Colors.Secondary),
			Background: colorToString(t.Colors.Background),
			Surface:    colorToString(t.Colors.Surface),
			Overlay:    colorToString(t.Colors.Overlay),
			Text:       colorToString(t.Colors.Text),
			TextMuted:  colorToString(t.Colors.TextMuted),
			TextDim:    colorToString(t.Colors.TextDim),
			Success:    colorToString(t.Colors.Success),
			Warning:    colorToString(t.Colors.Warning),
			Error:      colorToString(t.Colors.Error),
			Info:       colorToString(t.Colors.Info),
			Accent1:    colorToString(t.Colors.Accent1),
			Accent2:    colorToString(t.Colors.Accent2),
			Accent3:    colorToString(t.Colors.Accent3),
		},
	}

	return json.MarshalIndent(tj, "", "  ")
}

// colorToString converts a TerminalColor back to its string representation.
func colorToString(c lipgloss.TerminalColor) string {
	if c == nil {
		return ""
	}
	// For simple Color types, we can use the string value
	if color, ok := c.(lipgloss.Color); ok {
		return string(color)
	}
	// For adaptive colors, return empty (they need special handling)
	return ""
}
