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

// toChromaColor converts a lipgloss TerminalColor to a Chroma color string.
// This is a simplified conversion that works for basic Color types.
func toChromaColor(c lipgloss.TerminalColor) string {
	// If it's a simple lipgloss.Color (string), return it
	if color, ok := c.(lipgloss.Color); ok {
		return string(color)
	}

	// For AdaptiveColor, use the dark variant
	if adaptive, ok := c.(lipgloss.AdaptiveColor); ok {
		return adaptive.Dark
	}

	// For CompleteColor, use TrueColor if available, otherwise ANSI256
	if complete, ok := c.(lipgloss.CompleteColor); ok {
		if complete.TrueColor != "" {
			return complete.TrueColor
		}
		if complete.ANSI256 != "" {
			return complete.ANSI256
		}
		return complete.ANSI
	}

	// For CompleteAdaptiveColor, use dark TrueColor
	if completeAdaptive, ok := c.(lipgloss.CompleteAdaptiveColor); ok {
		if completeAdaptive.Dark.TrueColor != "" {
			return completeAdaptive.Dark.TrueColor
		}
		if completeAdaptive.Dark.ANSI256 != "" {
			return completeAdaptive.Dark.ANSI256
		}
		return completeAdaptive.Dark.ANSI
	}

	// Fallback
	return "#FFFFFF"
}
