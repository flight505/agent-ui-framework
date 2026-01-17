package views

import (
	"github.com/alecthomas/chroma/v2"
	"github.com/charmbracelet/lipgloss"
	"github.com/flight505/agentui/internal/theme"
)

// BuildChromaStyle creates a Chroma style from the current theme colors.
// This ensures code syntax highlighting matches the Charm aesthetic.
func BuildChromaStyle() *chroma.Style {
	colors := theme.Current.Colors

	// Convert lipgloss TerminalColor to hex strings for Chroma
	// For simplicity, we'll use the theme's color scheme

	return chroma.MustNewStyle("charm", chroma.StyleEntries{
		// Background
		chroma.Background:       toChromaColor(colors.Surface),
		chroma.LineNumbers:      toChromaColor(colors.TextDim),
		chroma.LineNumbersTable: toChromaColor(colors.TextDim),

		// Keywords
		chroma.Keyword:            toChromaColor(colors.Primary) + " bold",
		chroma.KeywordConstant:    toChromaColor(colors.Accent2),
		chroma.KeywordDeclaration: toChromaColor(colors.Primary),
		chroma.KeywordNamespace:   toChromaColor(colors.Accent2),
		chroma.KeywordType:        toChromaColor(colors.Accent3),

		// Names
		chroma.Name:             toChromaColor(colors.Text),
		chroma.NameAttribute:    toChromaColor(colors.Accent1),
		chroma.NameBuiltin:      toChromaColor(colors.Accent3),
		chroma.NameClass:        toChromaColor(colors.Accent2) + " bold",
		chroma.NameConstant:     toChromaColor(colors.Accent1),
		chroma.NameDecorator:    toChromaColor(colors.Primary),
		chroma.NameEntity:       toChromaColor(colors.Accent1),
		chroma.NameException:    toChromaColor(colors.Error),
		chroma.NameFunction:     toChromaColor(colors.Accent2),
		chroma.NameLabel:        toChromaColor(colors.Primary),
		chroma.NameNamespace:    toChromaColor(colors.Accent2),
		chroma.NameTag:          toChromaColor(colors.Primary),
		chroma.NameVariable:     toChromaColor(colors.Text),

		// Literals
		chroma.LiteralString:         toChromaColor(colors.Accent3),
		chroma.LiteralStringAffix:    toChromaColor(colors.Accent3),
		chroma.LiteralStringBacktick: toChromaColor(colors.Accent3),
		chroma.LiteralStringChar:     toChromaColor(colors.Accent3),
		chroma.LiteralStringDelimiter: toChromaColor(colors.Accent3),
		chroma.LiteralStringDoc:      toChromaColor(colors.TextMuted),
		chroma.LiteralStringDouble:   toChromaColor(colors.Accent3),
		chroma.LiteralStringEscape:   toChromaColor(colors.Accent1),
		chroma.LiteralStringHeredoc:  toChromaColor(colors.Accent3),
		chroma.LiteralStringInterpol: toChromaColor(colors.Accent1),
		chroma.LiteralStringRegex:    toChromaColor(colors.Accent1),
		chroma.LiteralStringSingle:   toChromaColor(colors.Accent3),

		chroma.LiteralNumber:            toChromaColor(colors.Accent1),
		chroma.LiteralNumberBin:         toChromaColor(colors.Accent1),
		chroma.LiteralNumberFloat:       toChromaColor(colors.Accent1),
		chroma.LiteralNumberHex:         toChromaColor(colors.Accent1),
		chroma.LiteralNumberInteger:     toChromaColor(colors.Accent1),
		chroma.LiteralNumberIntegerLong: toChromaColor(colors.Accent1),
		chroma.LiteralNumberOct:         toChromaColor(colors.Accent1),

		// Operators
		chroma.Operator:     toChromaColor(colors.Primary),
		chroma.OperatorWord: toChromaColor(colors.Primary) + " bold",

		// Punctuation
		chroma.Punctuation: toChromaColor(colors.TextMuted),

		// Comments
		chroma.Comment:         toChromaColor(colors.TextDim) + " italic",
		chroma.CommentHashbang: toChromaColor(colors.TextDim) + " italic",
		chroma.CommentMultiline: toChromaColor(colors.TextDim) + " italic",
		chroma.CommentPreproc:  toChromaColor(colors.TextMuted),
		chroma.CommentSingle:   toChromaColor(colors.TextDim) + " italic",
		chroma.CommentSpecial:  toChromaColor(colors.TextMuted) + " italic bold",

		// Generic
		chroma.Generic:        toChromaColor(colors.Text),
		chroma.GenericDeleted: toChromaColor(colors.Error),
		chroma.GenericEmph:    toChromaColor(colors.Text) + " italic",
		chroma.GenericError:   toChromaColor(colors.Error),
		chroma.GenericHeading: toChromaColor(colors.Primary) + " bold",
		chroma.GenericInserted: toChromaColor(colors.Success),
		chroma.GenericOutput:  toChromaColor(colors.TextMuted),
		chroma.GenericPrompt:  toChromaColor(colors.Primary) + " bold",
		chroma.GenericStrong:  toChromaColor(colors.Text) + " bold",
		chroma.GenericSubheading: toChromaColor(colors.Accent2) + " bold",
		chroma.GenericTraceback: toChromaColor(colors.Error),

		// Errors
		chroma.Error: toChromaColor(colors.Error) + " bold",
	})
}

// toChromaColor converts a lipgloss TerminalColor to a Chroma-compatible hex color string.
// Chroma requires hex colors (e.g., "#FF00FF"), not ANSI codes.
func toChromaColor(c lipgloss.TerminalColor) string {
	// If it's a simple lipgloss.Color (string), check if it's hex or ANSI
	if color, ok := c.(lipgloss.Color); ok {
		colorStr := string(color)
		// If it starts with #, it's already hex
		if len(colorStr) > 0 && colorStr[0] == '#' {
			return colorStr
		}
		// Otherwise it's an ANSI code, convert to hex
		return ansi256ToHex(colorStr)
	}

	// For AdaptiveColor, use the dark variant
	if adaptive, ok := c.(lipgloss.AdaptiveColor); ok {
		if len(adaptive.Dark) > 0 && adaptive.Dark[0] == '#' {
			return adaptive.Dark
		}
		return ansi256ToHex(adaptive.Dark)
	}

	// For CompleteColor, prefer TrueColor
	if complete, ok := c.(lipgloss.CompleteColor); ok {
		if complete.TrueColor != "" {
			return complete.TrueColor
		}
		if complete.ANSI256 != "" {
			return ansi256ToHex(complete.ANSI256)
		}
		return ansi256ToHex(complete.ANSI)
	}

	// For CompleteAdaptiveColor, use dark TrueColor
	if completeAdaptive, ok := c.(lipgloss.CompleteAdaptiveColor); ok {
		if completeAdaptive.Dark.TrueColor != "" {
			return completeAdaptive.Dark.TrueColor
		}
		if completeAdaptive.Dark.ANSI256 != "" {
			return ansi256ToHex(completeAdaptive.Dark.ANSI256)
		}
		return ansi256ToHex(completeAdaptive.Dark.ANSI)
	}

	// Fallback
	return "#FFFFFF"
}

// ansi256ToHex converts ANSI 256 color codes to approximate hex values.
// This is a simplified mapping for common CharmDark colors.
func ansi256ToHex(ansiCode string) string {
	// Map of common ANSI codes to hex colors
	ansiMap := map[string]string{
		"212": "#FF87D7", // Pink (CharmPink)
		"35":  "#00AF5F", // Teal (CharmTeal)
		"99":  "#875FFF", // Violet (CharmViolet)
		"63":  "#5F5FFF", // Indigo (CharmIndigo)
		"8":   "#808080", // Gray
		"7":   "#C0C0C0", // Light gray
		"0":   "#000000", // Black
		"15":  "#FFFFFF", // White
	}

	if hex, ok := ansiMap[ansiCode]; ok {
		return hex
	}

	// If no mapping, return a neutral gray
	return "#888888"
}
