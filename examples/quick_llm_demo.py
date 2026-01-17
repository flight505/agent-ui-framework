#!/usr/bin/env python3
"""
Quick LLM Demo - Fast demonstration of real Claude integration

Shows:
- Streaming Claude responses
- CharmDark theme
- Syntax highlighting
- Tool calls with UI primitives

Run:
    python examples/quick_llm_demo.py
"""

import asyncio
import os
from agentui import AgentApp, UICode


# Check for API key
if not os.environ.get("ANTHROPIC_API_KEY"):
    print("❌ Error: ANTHROPIC_API_KEY not set")
    print("\nSet it with:")
    print("  export ANTHROPIC_API_KEY='your-key-here'")
    exit(1)

print("\n✅ API key found - starting demo...\n")


# Create app with CharmDark theme
app = AgentApp(
    name="quick-demo",
    provider="claude",
    model="claude-sonnet-4-5-20250929",
    theme="charm-dark",  # Test CharmDark theme
    tagline="Quick Demo - Charm Aesthetic + Syntax Highlighting",
    system_prompt="""You are demonstrating the AgentUI framework.

When asked for code, use the show_code_example tool to display it with beautiful syntax highlighting.

Be enthusiastic and concise. Showcase the Charm aesthetic!""",
)


@app.ui_tool(
    name="show_code_example",
    description="Show a beautiful syntax-highlighted code example",
    parameters={
        "type": "object",
        "properties": {
            "language": {
                "type": "string",
                "enum": ["python", "go", "typescript", "rust"],
                "description": "Programming language for syntax highlighting"
            }
        },
        "required": ["language"]
    }
)
def show_code_example(language: str) -> UICode:
    """Return a syntax-highlighted code example."""

    examples = {
        "python": '''import asyncio
from dataclasses import dataclass

@dataclass
class User:
    """User model with validation."""
    name: str
    email: str
    age: int

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age must be positive")

async def fetch_users() -> list[User]:
    """Fetch users asynchronously."""
    # Simulate API call
    await asyncio.sleep(0.1)

    return [
        User("Alice", "alice@example.com", 28),
        User("Bob", "bob@example.com", 35),
    ]

# Usage
users = await fetch_users()
for user in users:
    print(f"{user.name}: {user.email}")''',

        "go": '''package main

import (
    "context"
    "fmt"
    "time"
)

type User struct {
    Name  string
    Email string
    Age   int
}

func FetchUsers(ctx context.Context) ([]User, error) {
    // Simulate API call with context
    select {
    case <-time.After(100 * time.Millisecond):
        return []User{
            {Name: "Alice", Email: "alice@example.com", Age: 28},
            {Name: "Bob", Email: "bob@example.com", Age: 35},
        }, nil
    case <-ctx.Done():
        return nil, ctx.Err()
    }
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    users, err := FetchUsers(ctx)
    if err != nil {
        fmt.Printf("Error: %v\\n", err)
        return
    }

    for _, user := range users {
        fmt.Printf("%s: %s\\n", user.Name, user.Email)
    }
}''',

        "typescript": '''interface User {
  name: string;
  email: string;
  age: number;
}

async function fetchUsers(): Promise<User[]> {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 100));

  return [
    { name: "Alice", email: "alice@example.com", age: 28 },
    { name: "Bob", email: "bob@example.com", age: 35 },
  ];
}

// Usage with error handling
try {
  const users = await fetchUsers();
  users.forEach(user => {
    console.log(`${user.name}: ${user.email}`);
  });
} catch (error) {
  console.error("Failed to fetch users:", error);
}''',

        "rust": '''use std::time::Duration;
use tokio::time::sleep;

#[derive(Debug)]
struct User {
    name: String,
    email: String,
    age: u32,
}

async fn fetch_users() -> Result<Vec<User>, Box<dyn std::error::Error>> {
    // Simulate API call
    sleep(Duration::from_millis(100)).await;

    Ok(vec![
        User {
            name: "Alice".to_string(),
            email: "alice@example.com".to_string(),
            age: 28,
        },
        User {
            name: "Bob".to_string(),
            email: "bob@example.com".to_string(),
            age: 35,
        },
    ])
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let users = fetch_users().await?;

    for user in users {
        println!("{}: {}", user.name, user.email);
    }

    Ok(())
}''',
    }

    return UICode(
        title=f"Beautiful {language.title()} Code",
        language=language,
        code=examples.get(language, "# Example not found"),
    )


async def main():
    """Run the quick demo."""

    print("="*70)
    print("🎨 AgentUI Quick Demo - Real Claude Integration")
    print("="*70)
    print("\nFeatures being tested:")
    print("  • Real streaming responses from Claude Sonnet 4.5")
    print("  • CharmDark theme (pink/purple/teal aesthetic)")
    print("  • Syntax highlighting with Chroma")
    print("  • Spring physics animations")
    print("  • Full Python↔Go TUI communication")
    print("\n" + "="*70)
    print("\nTry asking:")
    print("  'Show me Python code using show_code_example'")
    print("  'Show me Go code'")
    print("  'Show me TypeScript code'")
    print("  'Explain async/await in Python'")
    print("\n" + "="*70 + "\n")

    # Run the interactive app
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠ Demo cancelled by user\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
