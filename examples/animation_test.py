#!/usr/bin/env python3
"""
Animation Test - Tests smooth spring physics animations

Demonstrates:
- Fade-in animations for modals
- Spring physics for smooth positioning
- Charm aesthetic timing (200-300ms)

Run:
    python examples/animation_test.py
"""

import asyncio
from agentui.bridge import TUIConfig, managed_bridge
from agentui import UIForm
from agentui.primitives import text_field, checkbox_field


async def test_animations():
    """Test smooth animations with forms and confirms."""

    print("\n🎨 AgentUI - Animation Test")
    print("Testing spring physics animations...\n")

    # Create TUI config
    tui_config = TUIConfig(
        theme="charm-dark",
        app_name="Animation Test",
        tagline="Spring Physics Demo",
        debug=False,
    )

    async with managed_bridge(tui_config, fallback=True) as bridge:
        # Test 1: Show text message
        print("→ Sending welcome message...")
        await bridge.send_text("Welcome! Watch for smooth animations when forms appear.", done=False)
        await asyncio.sleep(2)

        # Test 2: Show form (should animate in smoothly)
        print("→ Showing form with animation...")
        await bridge.send_text("Here comes a form with smooth fade-in animation!")
        await asyncio.sleep(0.5)

        # Create and send form
        form = UIForm(
            title="Profile Setup",
            description="Watch the smooth animation as this form appears",
            fields=[
                text_field("name", "Your Name", required=True, placeholder="John Doe"),
                text_field("email", "Email", required=True, placeholder="john@example.com"),
                checkbox_field("subscribe", "Subscribe to updates", default=True),
            ],
            submit_label="Save",
            cancel_label="Cancel",
        )

        # Send the form (request_form waits for user response)
        try:
            response = await bridge.request_form(form.to_dict())
            print(f"→ Form response: {response}")
        except Exception as e:
            print(f"→ Form cancelled or error: {e}")

        # Test 3: Show another message
        print("→ Sending completion message...")
        await bridge.send_text("Animation test complete! Notice the smooth transitions.", done=True)
        await asyncio.sleep(2)

    print("\n✓ Animation test completed!\n")


async def main():
    """Run animation test."""
    try:
        await test_animations()
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user\n")
    except Exception as e:
        print(f"\n✗ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
