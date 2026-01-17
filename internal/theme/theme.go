// Package theme provides theming support for the TUI.
package theme

import (
	"github.com/charmbracelet/lipgloss"
)

// Theme defines the visual appearance of the TUI.
type Theme struct {
	// Metadata
	ID          string
	Name        string
	Description string
	Author      string
	Version     string

	// Visual
	Colors Colors
	Styles Styles
}

// Colors defines the color palette using TerminalColor interface.
// This allows any lipgloss color type: Color, AdaptiveColor, 
// CompleteColor, or CompleteAdaptiveColor.
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
	Accent1 lipgloss.TerminalColor
	Accent2 lipgloss.TerminalColor
	Accent3 lipgloss.TerminalColor
}

// Styles holds pre-configured lipgloss styles.
type Styles struct {
	// App chrome
	Header    lipgloss.Style
	Footer    lipgloss.Style
	StatusBar lipgloss.Style

	// Messages
	UserMessage      lipgloss.Style
	AssistantMessage lipgloss.Style
	SystemMessage    lipgloss.Style

	// Input
	InputField      lipgloss.Style
	InputFieldFocus lipgloss.Style
	InputPrompt     lipgloss.Style

	// Forms
	FormContainer   lipgloss.Style
	FormTitle       lipgloss.Style
	FormLabel       lipgloss.Style
	FormInput       lipgloss.Style
	FormButton      lipgloss.Style
	FormButtonFocus lipgloss.Style

	// Tables
	TableContainer lipgloss.Style
	TableHeader    lipgloss.Style
	TableRow       lipgloss.Style
	TableRowAlt    lipgloss.Style
	TableSelected  lipgloss.Style

	// Code
	CodeContainer lipgloss.Style
	CodeTitle     lipgloss.Style

	// Alerts
	AlertInfo    lipgloss.Style
	AlertSuccess lipgloss.Style
	AlertWarning lipgloss.Style
	AlertError   lipgloss.Style

	// Progress
	ProgressContainer lipgloss.Style
	ProgressBar       lipgloss.Style
	ProgressComplete  lipgloss.Style

	// Misc
	Spinner   lipgloss.Style
	Border    lipgloss.Style
	Highlight lipgloss.Style
	Muted     lipgloss.Style
}

// Current holds the active theme (set to CharmDark by default in charm.go init)
var Current Theme

// Available lists all available themes.
var Available = make(map[string]*Theme)

// SetTheme changes the current theme.
func SetTheme(name string) bool {
	if theme, ok := Available[name]; ok {
		Current = *theme
		return true
	}
	return false
}

// Register adds a theme to the available themes.
func Register(t *Theme) {
	Available[t.ID] = t
}

// BuildStyles creates all styles from a color palette.
// Uses Charm aesthetic: rounded borders, clean spacing, high contrast.
func BuildStyles(c Colors) Styles {
	// Charm consistently uses rounded borders
	border := lipgloss.RoundedBorder()

	return Styles{
		// Header/Footer
		Header: lipgloss.NewStyle().
			Background(c.Surface).
			Foreground(c.Primary).
			Padding(0, 2).
			Bold(true),

		Footer: lipgloss.NewStyle().
			Background(c.Surface).
			Foreground(c.TextMuted).
			Padding(0, 2),

		StatusBar: lipgloss.NewStyle().
			Background(c.Surface).
			Foreground(c.TextMuted).
			Padding(0, 1),

		// Messages - Charm style with rounded borders
		UserMessage: lipgloss.NewStyle().
			Background(c.Surface).
			Foreground(c.Text).
			Border(border).
			BorderForeground(c.Primary).
			Padding(1, 2).
			MarginTop(1).
			MarginBottom(1),

		AssistantMessage: lipgloss.NewStyle().
			Foreground(c.Text).
			Padding(1, 2).
			MarginTop(1).
			MarginBottom(1),

		SystemMessage: lipgloss.NewStyle().
			Foreground(c.TextMuted).
			Italic(true).
			Padding(0, 2),

		// Input - subtle border that pops on focus
		InputField: lipgloss.NewStyle().
			Background(c.Surface).
			Foreground(c.Text).
			Border(border).
			BorderForeground(c.TextDim).
			Padding(0, 1),

		InputFieldFocus: lipgloss.NewStyle().
			Background(c.Surface).
			Foreground(c.Text).
			Border(border).
			BorderForeground(c.Primary).
			Padding(0, 1),

		InputPrompt: lipgloss.NewStyle().
			Foreground(c.Primary).
			Bold(true),

		// Forms
		FormContainer: lipgloss.NewStyle().
			Background(c.Surface).
			Border(border).
			BorderForeground(c.Primary).
			Padding(1, 2).
			Margin(1),

		FormTitle: lipgloss.NewStyle().
			Foreground(c.Primary).
			Bold(true).
			MarginBottom(1),

		FormLabel: lipgloss.NewStyle().
			Foreground(c.Text),

		FormInput: lipgloss.NewStyle().
			Background(c.Overlay).
			Foreground(c.Text).
			Padding(0, 1),

		FormButton: lipgloss.NewStyle().
			Background(c.Surface).
			Foreground(c.TextMuted).
			Border(border).
			BorderForeground(c.TextDim).
			Padding(0, 2).
			MarginRight(1),

		FormButtonFocus: lipgloss.NewStyle().
			Background(c.Primary).
			Foreground(c.Background).
			Border(border).
			BorderForeground(c.Primary).
			Padding(0, 2).
			MarginRight(1),

		// Tables
		TableContainer: lipgloss.NewStyle().
			Border(border).
			BorderForeground(c.TextDim).
			Padding(0, 1),

		TableHeader: lipgloss.NewStyle().
			Background(c.Surface).
			Foreground(c.Primary).
			Bold(true).
			Padding(0, 1),

		TableRow: lipgloss.NewStyle().
			Foreground(c.Text).
			Padding(0, 1),

		TableRowAlt: lipgloss.NewStyle().
			Background(c.Surface).
			Foreground(c.Text).
			Padding(0, 1),

		TableSelected: lipgloss.NewStyle().
			Background(c.Primary).
			Foreground(c.Background).
			Padding(0, 1),

		// Code
		CodeContainer: lipgloss.NewStyle().
			Background(c.Surface).
			Border(border).
			BorderForeground(c.TextDim).
			Padding(1),

		CodeTitle: lipgloss.NewStyle().
			Foreground(c.TextMuted).
			Italic(true),

		// Alerts
		AlertInfo: lipgloss.NewStyle().
			Border(border).
			BorderForeground(c.Info).
			Foreground(c.Text).
			Padding(1, 2).
			Margin(1),

		AlertSuccess: lipgloss.NewStyle().
			Border(border).
			BorderForeground(c.Success).
			Foreground(c.Text).
			Padding(1, 2).
			Margin(1),

		AlertWarning: lipgloss.NewStyle().
			Border(border).
			BorderForeground(c.Warning).
			Foreground(c.Text).
			Padding(1, 2).
			Margin(1),

		AlertError: lipgloss.NewStyle().
			Border(border).
			BorderForeground(c.Error).
			Foreground(c.Text).
			Padding(1, 2).
			Margin(1),

		// Progress
		ProgressContainer: lipgloss.NewStyle().
			Padding(1, 2),

		ProgressBar: lipgloss.NewStyle().
			Foreground(c.Primary),

		ProgressComplete: lipgloss.NewStyle().
			Foreground(c.Success),

		// Misc
		Spinner: lipgloss.NewStyle().
			Foreground(c.Primary),

		Border: lipgloss.NewStyle().
			Border(border).
			BorderForeground(c.TextDim),

		Highlight: lipgloss.NewStyle().
			Foreground(c.Primary).
			Bold(true),

		Muted: lipgloss.NewStyle().
			Foreground(c.TextMuted),
	}
}
