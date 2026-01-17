package views

import (
	"strings"
	"testing"

	"github.com/flight505/agentui/internal/theme"
)

func TestBuildChromaStyle(t *testing.T) {
	// Set a theme first
	theme.SetTheme("charm-dark")

	style := BuildChromaStyle()

	if style == nil {
		t.Fatal("BuildChromaStyle() returned nil")
	}

	// Verify the style has the expected name
	if style.Name != "charm" {
		t.Errorf("Expected style name 'charm', got '%s'", style.Name)
	}
}

func TestCodeView_Render(t *testing.T) {
	// Set CharmDark theme
	theme.SetTheme("charm-dark")

	tests := []struct {
		name     string
		language string
		code     string
		wantErr  bool
	}{
		{
			name:     "Python code",
			language: "python",
			code:     "def hello():\n    print('world')",
			wantErr:  false,
		},
		{
			name:     "Go code",
			language: "go",
			code:     "package main\n\nfunc main() {\n    println(\"hello\")\n}",
			wantErr:  false,
		},
		{
			name:     "TypeScript code",
			language: "typescript",
			code:     "function hello(): void {\n    console.log('world');\n}",
			wantErr:  false,
		},
		{
			name:     "Rust code",
			language: "rust",
			code:     "fn main() {\n    println!(\"hello\");\n}",
			wantErr:  false,
		},
		{
			name:     "Unknown language fallback",
			language: "unknown",
			code:     "some code",
			wantErr:  false, // Should fallback gracefully
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			view := NewCodeView()

			if view == nil {
				t.Fatal("NewCodeView() returned nil")
			}

			// Set properties
			view.SetTitle("Test Code")
			view.SetLanguage(tt.language)
			view.SetCode(tt.code)
			view.SetLineNumbers(true)
			view.SetWidth(80)

			// Render the view
			output := view.View()

			if output == "" {
				t.Error("View() produced empty output")
			}

			// Check that the title appears in output
			if !strings.Contains(output, "Test Code") {
				t.Error("View() output missing title")
			}

			// For valid languages, check that highlighting was attempted
			// (code should be different from plain input after highlighting)
			if tt.language != "unknown" {
				highlighted := view.highlightCode()

				// If highlighting worked, output should contain ANSI codes
				// or be different from plain code
				if highlighted == tt.code && !strings.Contains(highlighted, "\x1b[") {
					t.Logf("Warning: No highlighting detected for %s (may fallback to plain text)", tt.language)
				}
			}
		})
	}
}

func TestCodeView_HighlightCode(t *testing.T) {
	theme.SetTheme("charm-dark")

	pythonCode := `def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)`

	view := NewCodeView()
	view.SetTitle("Fibonacci")
	view.SetLanguage("python")
	view.SetCode(pythonCode)

	highlighted := view.highlightCode()

	// Highlighted code should not be empty
	if highlighted == "" {
		t.Error("highlightCode() returned empty string")
	}

	// Should contain some content from the original code
	if !strings.Contains(highlighted, "fibonacci") {
		t.Error("highlightCode() missing function name from source")
	}

	t.Logf("Highlighted Python code length: %d bytes", len(highlighted))
	t.Logf("Original code length: %d bytes", len(pythonCode))

	// Typically highlighted code is longer due to ANSI codes
	// But if highlighting fails, it should at least equal original length
	if len(highlighted) < len(pythonCode) {
		t.Error("Highlighted code is shorter than original (unexpected)")
	}
}
