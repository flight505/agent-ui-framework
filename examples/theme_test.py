#!/usr/bin/env python3
"""
Theme Test - Visual test of all themes without requiring LLM API

Tests the new Charm themes:
- charm-dark
- charm-light
- charm-auto

Run:
    python examples/theme_test.py [theme-name]
"""

import asyncio
import sys


async def test_theme(theme_name: str):
    """Test a theme by showing various UI elements."""

    print(f"\n{'='*60}")
    print(f"Testing theme: {theme_name}")
    print(f"{'='*60}\n")

    # Import bridge utilities
    from agentui.bridge import TUIConfig, managed_bridge

    # Create TUI config
    tui_config = TUIConfig(
        theme=theme_name,
        app_name="Theme Test",
        tagline=f"Testing {theme_name}",
        debug=False,
    )

    # Use managed bridge context
    async with managed_bridge(tui_config, fallback=True) as bridge:
        # Test 1: Text message
        print("→ Sending text message...")
        await bridge.send_text("Welcome to AgentUI Theme Test!", done=False)
        await asyncio.sleep(0.5)

        # Test 2: Markdown
        print("→ Showing markdown...")
        await bridge.send_markdown("""
# AgentUI Theme Test

Testing the **{theme}** theme with various UI components.

## Features
- Beautiful terminal rendering
- Charm-quality aesthetics
- Multiple theme support

> This is a blockquote to test styling
""".format(theme=theme_name), title="Theme Documentation")
        await asyncio.sleep(1.5)

        # Test 3: Table
        print("→ Showing table...")
        await bridge.send_table(
            title="Cloud Costs",
            columns=["Service", "Tier", "Monthly Cost"],
            rows=[
                ["EC2", "t3.medium", "$30.00"],
                ["RDS", "db.t3.small", "$25.00"],
                ["S3", "Standard", "$5.00"],
                ["Lambda", "1M reqs", "$2.00"],
            ],
            footer="Total: $60/month",
        )
        await asyncio.sleep(1.5)

        # Test 4: Progress
        print("→ Showing progress...")
        await bridge.send_progress(
            message="Deploying application...",
            percent=65.0,
            steps=[
                {"label": "Build", "status": "complete", "detail": "Compiled in 2.3s"},
                {"label": "Test", "status": "complete", "detail": "42 tests passed"},
                {"label": "Deploy", "status": "running", "detail": "Uploading..."},
                {"label": "Verify", "status": "pending"},
            ],
        )
        await asyncio.sleep(1.5)

        # Test 5: Code
        print("→ Showing code block...")
        await bridge.send_code(
            code='''def hello_world():
    """A simple function."""
    print("Hello, World!")
    return 42

if __name__ == "__main__":
    result = hello_world()
    print(f"Result: {result}")''',
            language="python",
            title="Python Example",
        )
        await asyncio.sleep(1.5)

        # Test 6: Final message
        print("→ Sending completion message...")
        await bridge.send_text(f"✨ Theme test complete for {theme_name}!", done=True)
        await asyncio.sleep(2)

    print(f"\n✓ Theme {theme_name} tested successfully!\n")


async def main():
    """Run theme tests."""
    themes = ["charm-dark", "charm-light", "charm-auto"]

    if len(sys.argv) > 1:
        # Test specific theme
        theme = sys.argv[1]
        await test_theme(theme)
    else:
        # Test all Charm themes
        print("\n🎨 AgentUI - Charm Theme Test Suite")
        print("Testing all Charm themes...\n")

        for theme in themes:
            try:
                await test_theme(theme)
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n\n⚠ Test interrupted by user")
                break
            except Exception as e:
                print(f"\n✗ Error testing {theme}: {e}\n")

        print("\n" + "="*60)
        print("All theme tests complete!")
        print("="*60 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user\n")
