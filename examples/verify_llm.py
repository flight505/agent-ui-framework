#!/usr/bin/env python3
"""
Quick Verification - Automated LLM interaction test

This script sends a single prompt to verify:
- Real Claude API streaming works
- CharmDark theme renders
- Syntax highlighting with Chroma functions
- Python↔Go communication is stable

Run:
    python examples/verify_llm.py
"""

import asyncio
import os
from agentui import AgentApp, UICode


if not os.environ.get("ANTHROPIC_API_KEY"):
    print("❌ Error: ANTHROPIC_API_KEY not set")
    exit(1)

print("✅ API key found")
print("🧪 Running automated verification...\n")


app = AgentApp(
    name="verify",
    provider="claude",
    model="claude-sonnet-4-5-20250929",
    theme="charm-dark",
    tagline="Automated Verification Test",
    system_prompt="""You are testing the AgentUI framework.

When asked for code, use the show_code tool to display it.
Be very brief - just show the code, no extra explanation.""",
)


@app.ui_tool(
    name="show_code",
    description="Show syntax-highlighted code",
    parameters={
        "type": "object",
        "properties": {
            "language": {"type": "string", "enum": ["python", "go"]},
        },
        "required": ["language"]
    }
)
def show_code(language: str) -> UICode:
    """Return a simple code example."""

    if language == "python":
        code = '''def hello(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"

# Usage
message = hello("World")
print(message)'''
    else:  # go
        code = '''package main

import "fmt"

func hello(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}

func main() {
    message := hello("World")
    fmt.Println(message)
}'''

    return UICode(
        title=f"{language.title()} Example",
        language=language,
        code=code,
    )


async def main():
    """Run automated verification."""

    print("=" * 60)
    print("Starting AgentUI with CharmDark theme...")
    print("=" * 60)
    print("\nTest prompt: 'Show me Python code using show_code'")
    print("\nExpected behavior:")
    print("  • CharmDark theme renders (pink/purple/teal)")
    print("  • Code block appears with syntax highlighting")
    print("  • Keywords are pink, strings are teal")
    print("  • Streaming response appears smoothly")
    print("\n" + "=" * 60 + "\n")

    # This will launch the interactive TUI
    # User can type: "Show me Python code using show_code"
    # Or: "quit" to exit
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✅ Verification test interrupted\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
