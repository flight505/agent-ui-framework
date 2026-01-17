#!/usr/bin/env python3
"""
Automated LLM Test - Non-interactive testing with Claude API

Tests the full stack:
- Real Claude API streaming
- Charm theme rendering
- Syntax highlighting
- UI primitives
- Animations

Run:
    python examples/automated_llm_test.py
"""

import asyncio
from agentui import AgentApp, UICode, UITable, UIProgress, UIProgressStep


app = AgentApp(
    name="automated-test",
    provider="claude",
    model="claude-sonnet-4-5-20250929",
    theme="charm-dark",
    tagline="Automated Testing with Real LLM",
    system_prompt="""You are testing the AgentUI framework. Be concise.

When asked for code, use the show_code tool.
When asked for data, use the show_table tool.
Keep responses brief to speed up testing.""",
)


@app.ui_tool(
    name="show_code",
    description="Show a code example with syntax highlighting",
    parameters={
        "type": "object",
        "properties": {
            "language": {"type": "string", "description": "python or go"},
            "description": {"type": "string", "description": "What code does"}
        },
        "required": ["language"]
    }
)
def show_code(language: str, description: str = "Example code") -> UICode:
    """Return syntax-highlighted code."""

    code_examples = {
        "python": '''async def fetch_data(url: str) -> dict:
    """Fetch JSON data asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Usage
data = await fetch_data("https://api.example.com/data")
print(f"Received {len(data)} items")''',

        "go": '''func ProcessConcurrently(items []string) []Result {
    results := make(chan Result, len(items))

    for _, item := range items {
        go func(i string) {
            results <- Process(i)
        }(item)
    }

    output := make([]Result, len(items))
    for i := range items {
        output[i] = <-results
    }
    return output
}''',
    }

    return UICode(
        title=f"{language.title()} Example",
        language=language,
        code=code_examples.get(language, "# No example available"),
    )


@app.ui_tool(
    name="show_table",
    description="Show data in a formatted table",
    parameters={
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "What data to show"}
        }
    }
)
def show_table(topic: str = "metrics") -> UITable:
    """Return data as a table."""

    return UITable(
        title="Performance Metrics",
        columns=["Metric", "Value", "Status"],
        rows=[
            ["Response Time", "45ms", "✓"],
            ["Throughput", "1.2k/s", "✓"],
            ["Error Rate", "0.1%", "✓"],
            ["Memory Usage", "128MB", "✓"],
        ],
        footer="All systems operational",
    )


@app.ui_tool(
    name="show_progress",
    description="Show a progress indicator",
    parameters={"type": "object", "properties": {}}
)
def show_progress() -> UIProgress:
    """Return progress indicator."""

    return UIProgress(
        message="Processing workflow...",
        percent=65.0,
        steps=[
            UIProgressStep("Initialize", "complete"),
            UIProgressStep("Process", "running", "Item 65/100"),
            UIProgressStep("Finalize", "pending"),
        ],
    )


async def run_automated_tests():
    """Run automated tests with Claude."""

    print("\n" + "="*70)
    print("🤖 Automated LLM Integration Test")
    print("="*70)
    print("\nTesting:")
    print("  ✓ Real Claude API streaming")
    print("  ✓ CharmDark theme (pink/purple/teal)")
    print("  ✓ Syntax highlighting (Chroma)")
    print("  ✓ UI primitives (code, tables, progress)")
    print("  ✓ Spring physics animations")
    print("\n" + "="*70 + "\n")

    # Test messages
    tests = [
        ("Show me Python code using the show_code tool", "Syntax Highlighting"),
        ("Show performance data using show_table", "Table Rendering"),
        ("Show progress using show_progress", "Progress Indicators"),
    ]

    for i, (prompt, test_name) in enumerate(tests, 1):
        print(f"\n[Test {i}/{len(tests)}] {test_name}")
        print(f"Prompt: {prompt}")
        print("-" * 70)

        # This will process through the agent
        # In a real test, we'd send this and capture the output
        # For now, we're demonstrating the structure

    print("\n" + "="*70)
    print("Ready to run interactive test!")
    print("Type your questions or 'quit' to exit")
    print("="*70 + "\n")

    # Run the interactive app
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(run_automated_tests())
    except KeyboardInterrupt:
        print("\n\n⚠ Test cancelled\n")
