package theme

import "github.com/charmbracelet/lipgloss"

// Charm signature colors - the iconic pink/purple/teal palette
// These are extracted from Charmbracelet's official repos and documentation
var (
	// The signature Charm purple - used in lipgloss examples
	CharmPurple = lipgloss.Color("#7D56F4")

	// Pink - the glamour accent (ANSI 212 ≈ #ff87d7)
	CharmPink = lipgloss.Color("212")

	// Secondary purple (ANSI 99 ≈ #875fff)
	CharmViolet = lipgloss.Color("99")

	// Teal accent (ANSI 35 ≈ #00af5f)
	CharmTeal = lipgloss.Color("35")

	// Border purple (ANSI 63 ≈ #5f5fff)
	CharmIndigo = lipgloss.Color("63")
)

// CharmDark is the signature Charm aesthetic - dark variant
// This is the primary theme for AgentUI
var CharmDark = Theme{
	ID:          "charm-dark",
	Name:        "Charm Dark",
	Description: "The signature Charm aesthetic - glamorous terminal vibes",
	Author:      "AgentUI Team",
	Version:     "1.0.0",
	Colors: Colors{
		// Core - deep dark with subtle blue undertones
		Primary:    CharmPink,                 // Pink headlines - the signature
		Secondary:  CharmPurple,               // Purple accents
		Background: lipgloss.Color("#1a1a2e"), // Deep dark blue
		Surface:    lipgloss.Color("#252538"), // Elevated surface
		Overlay:    lipgloss.Color("#2f2f45"), // Overlays/modals

		// Text - high contrast for readability
		Text:      lipgloss.Color("#FAFAFA"), // Bright white
		TextMuted: lipgloss.Color("#a9b1d6"), // Muted lavender
		TextDim:   lipgloss.Color("#565f89"), // Dim purple-gray

		// Semantic colors
		Success: lipgloss.Color("#04B575"), // Charm teal-green
		Warning: lipgloss.Color("#ffb86c"), // Warm orange
		Error:   lipgloss.Color("#ff6b6b"), // Soft red
		Info:    lipgloss.Color("#7dcfff"), // Cyan

		// Accents - the Charm trinity: pink, purple, teal
		Accent1: CharmPink,   // Pink
		Accent2: CharmPurple, // Purple
		Accent3: CharmTeal,   // Teal
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
		Primary:    lipgloss.Color("#7D56F4"), // Purple (darker for light bg)
		Secondary:  lipgloss.Color("#d946ef"), // Fuchsia
		Background: lipgloss.Color("#faf4ed"), // Warm off-white
		Surface:    lipgloss.Color("#f2e9e1"), // Subtle surface
		Overlay:    lipgloss.Color("#e8ddd5"), // Overlay

		// Text - dark for contrast on light background
		Text:      lipgloss.Color("#1a1a2e"), // Deep dark
		TextMuted: lipgloss.Color("#6e6a86"), // Muted purple
		TextDim:   lipgloss.Color("#9893a5"), // Light muted

		// Semantic colors - slightly deeper for light backgrounds
		Success: lipgloss.Color("#059669"), // Deeper teal
		Warning: lipgloss.Color("#d97706"), // Amber
		Error:   lipgloss.Color("#dc2626"), // Red
		Info:    lipgloss.Color("#0284c7"), // Blue

		// Accents
		Accent1: lipgloss.Color("#d946ef"), // Fuchsia
		Accent2: lipgloss.Color("#7D56F4"), // Purple
		Accent3: lipgloss.Color("#059669"), // Teal
	},
}

// CharmAuto uses AdaptiveColor to automatically select light/dark
// based on terminal background detection
var CharmAuto = Theme{
	ID:          "charm-auto",
	Name:        "Charm Auto",
	Description: "Automatically adapts to terminal light/dark mode",
	Author:      "AgentUI Team",
	Version:     "1.0.0",
	Colors: Colors{
		Primary: lipgloss.AdaptiveColor{
			Light: "#7D56F4", // Purple on light
			Dark:  "212",     // Pink on dark (ANSI 212)
		},
		Secondary: lipgloss.AdaptiveColor{
			Light: "#d946ef",
			Dark:  "#7D56F4",
		},
		Background: lipgloss.AdaptiveColor{
			Light: "#faf4ed",
			Dark:  "#1a1a2e",
		},
		Surface: lipgloss.AdaptiveColor{
			Light: "#f2e9e1",
			Dark:  "#252538",
		},
		Overlay: lipgloss.AdaptiveColor{
			Light: "#e8ddd5",
			Dark:  "#2f2f45",
		},
		Text: lipgloss.AdaptiveColor{
			Light: "#1a1a2e",
			Dark:  "#FAFAFA",
		},
		TextMuted: lipgloss.AdaptiveColor{
			Light: "#6e6a86",
			Dark:  "#a9b1d6",
		},
		TextDim: lipgloss.AdaptiveColor{
			Light: "#9893a5",
			Dark:  "#565f89",
		},
		Success: lipgloss.AdaptiveColor{
			Light: "#059669",
			Dark:  "#04B575",
		},
		Warning: lipgloss.AdaptiveColor{
			Light: "#d97706",
			Dark:  "#ffb86c",
		},
		Error: lipgloss.AdaptiveColor{
			Light: "#dc2626",
			Dark:  "#ff6b6b",
		},
		Info: lipgloss.AdaptiveColor{
			Light: "#0284c7",
			Dark:  "#7dcfff",
		},
		Accent1: lipgloss.AdaptiveColor{
			Light: "#d946ef",
			Dark:  "212",
		},
		Accent2: lipgloss.AdaptiveColor{
			Light: "#7D56F4",
			Dark:  "#7D56F4",
		},
		Accent3: lipgloss.AdaptiveColor{
			Light: "#059669",
			Dark:  "35",
		},
	},
}

func init() {
	// Build styles from colors
	CharmDark.Styles = BuildStyles(CharmDark.Colors)
	CharmLight.Styles = BuildStyles(CharmLight.Colors)
	CharmAuto.Styles = BuildStyles(CharmAuto.Colors)

	// Register themes
	Register(&CharmDark)
	Register(&CharmLight)
	Register(&CharmAuto)

	// Set default theme
	Current = CharmDark
}
