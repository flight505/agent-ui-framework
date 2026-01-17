#!/usr/bin/env python3
"""
LLM Integration Test - Real Claude API testing

This script tests the AgentUI framework with real Claude API calls to verify:
- Streaming responses with Charm aesthetic
- Syntax highlighting in code blocks
- UI primitives (forms, tables, progress bars)
- Spring physics animations
- Full Python↔Go communication

Run:
    python examples/llm_integration_test.py
"""

import asyncio
from agentui import AgentApp, UITable, UICode, UIProgress, UIProgressStep


# Create app with CharmDark theme
app = AgentApp(
    name="llm-test",
    provider="claude",
    model="claude-sonnet-4-5-20250929",
    theme="charm-dark",
    tagline="Testing Charm Aesthetic + Syntax Highlighting",
    system_prompt="""You are a helpful coding assistant testing the AgentUI framework.

When asked to show code, provide syntax-highlighted examples in Python or Go.
When asked about data, return it in table format.
Be concise and showcase the beautiful UI.""",
)


@app.ui_tool(
    name="show_syntax_example",
    description="Show a syntax-highlighted code example in Python or Go",
    parameters={
        "type": "object",
        "properties": {
            "language": {
                "type": "string",
                "enum": ["python", "go"],
                "description": "Programming language"
            },
            "topic": {
                "type": "string",
                "description": "What the code should demonstrate"
            }
        },
        "required": ["language", "topic"]
    }
)
def show_syntax_example(language: str, topic: str) -> UICode:
    """Return a syntax-highlighted code example."""

    if language == "python":
        if "async" in topic.lower():
            code = '''import asyncio
from typing import AsyncIterator

async def stream_data(items: list[str]) -> AsyncIterator[str]:
    """Stream items with delay."""
    for item in items:
        await asyncio.sleep(0.1)
        yield item

async def main():
    """Process streaming data."""
    items = ["alpha", "beta", "gamma"]

    async for item in stream_data(items):
        print(f"Received: {item}")

if __name__ == "__main__":
    asyncio.run(main())'''
        else:
            code = '''def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Optimized with memoization
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_fast(n: int) -> int:
    """Fast Fibonacci with caching."""
    if n <= 1:
        return n
    return fib_fast(n - 1) + fib_fast(n - 2)

# Test
for i in range(10):
    print(f"fib({i}) = {fib_fast(i)}")'''
    else:  # Go
        code = '''package main

import (
    "fmt"
    "sync"
)

// Worker pool pattern
type Task struct {
    ID   int
    Data string
}

func worker(id int, tasks <-chan Task, results chan<- string, wg *sync.WaitGroup) {
    defer wg.Done()

    for task := range tasks {
        result := fmt.Sprintf("Worker %d processed task %d: %s", id, task.ID, task.Data)
        results <- result
    }
}

func main() {
    tasks := make(chan Task, 10)
    results := make(chan string, 10)

    var wg sync.WaitGroup

    // Start workers
    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go worker(i, tasks, results, &wg)
    }

    // Send tasks
    for i := 1; i <= 5; i++ {
        tasks <- Task{ID: i, Data: fmt.Sprintf("data-%d", i)}
    }
    close(tasks)

    // Close results after workers finish
    go func() {
        wg.Wait()
        close(results)
    }()

    // Collect results
    for result := range results {
        fmt.Println(result)
    }
}'''

    return UICode(
        title=f"{language.title()} - {topic}",
        language=language,
        code=code,
    )


@app.ui_tool(
    name="show_benchmark_results",
    description="Show performance benchmark results in a table",
    parameters={
        "type": "object",
        "properties": {
            "framework": {
                "type": "string",
                "description": "Framework being benchmarked"
            }
        }
    }
)
def show_benchmark_results(framework: str = "web") -> UITable:
    """Return benchmark results as a table."""

    if framework == "web":
        return UITable(
            title="Web Framework Benchmarks",
            columns=["Framework", "Language", "Req/sec", "Latency (ms)", "Memory (MB)"],
            rows=[
                ["FastAPI", "Python", "12,400", "8.2", "45"],
                ["Express", "Node.js", "18,200", "5.5", "62"],
                ["Gin", "Go", "47,600", "2.1", "18"],
                ["Actix", "Rust", "52,100", "1.9", "12"],
                ["Spring", "Java", "15,800", "6.3", "180"],
            ],
            footer="Go and Rust show best performance",
        )
    else:
        return UITable(
            title="Database Query Performance",
            columns=["Database", "Query Type", "Time (ms)", "Throughput"],
            rows=[
                ["PostgreSQL", "SELECT", "0.45", "22k/s"],
                ["PostgreSQL", "INSERT", "1.2", "8.3k/s"],
                ["MongoDB", "Find", "0.38", "26k/s"],
                ["Redis", "GET", "0.12", "83k/s"],
                ["MySQL", "SELECT", "0.52", "19k/s"],
            ],
            footer="Redis excels at key-value lookups",
        )


@app.ui_tool(
    name="simulate_deployment",
    description="Simulate a deployment with progress tracking",
    parameters={
        "type": "object",
        "properties": {
            "environment": {
                "type": "string",
                "enum": ["staging", "production"],
                "description": "Deployment environment"
            }
        }
    }
)
def simulate_deployment(environment: str = "staging") -> UIProgress:
    """Return deployment progress."""

    if environment == "production":
        steps = [
            UIProgressStep("Build", "complete", "Compiled in 3.2s"),
            UIProgressStep("Test", "complete", "127 tests passed"),
            UIProgressStep("Security Scan", "complete", "No vulnerabilities"),
            UIProgressStep("Deploy to Canary", "complete", "5% traffic"),
            UIProgressStep("Monitor Metrics", "running", "Watching error rates..."),
            UIProgressStep("Full Rollout", "pending"),
        ]
        percent = 75.0
        message = "Deploying to production..."
    else:
        steps = [
            UIProgressStep("Build", "complete", "Compiled in 2.1s"),
            UIProgressStep("Test", "complete", "127 tests passed"),
            UIProgressStep("Deploy", "running", "Pushing to staging..."),
            UIProgressStep("Smoke Test", "pending"),
        ]
        percent = 50.0
        message = "Deploying to staging..."

    return UIProgress(
        message=message,
        percent=percent,
        steps=steps,
    )


async def main():
    """Run the LLM integration test."""
    print("\n" + "="*60)
    print("🎨 AgentUI - LLM Integration Test")
    print("="*60)
    print("\nTesting with Claude API:")
    print("  • CharmDark theme (pink/purple/teal)")
    print("  • Syntax highlighting with Chroma")
    print("  • Spring physics animations")
    print("  • Real streaming responses")
    print("\n" + "="*60 + "\n")

    # Test prompts that showcase features
    test_prompts = [
        "Show me a Python async example using the show_syntax_example tool",
        "Show benchmark results for web frameworks using show_benchmark_results",
        "Simulate a production deployment using simulate_deployment",
        "Show me a Go concurrency example with the syntax tool",
    ]

    print("Test prompts prepared:")
    for i, prompt in enumerate(test_prompts, 1):
        print(f"  {i}. {prompt}")

    print("\n" + "="*60)
    print("Starting interactive session...")
    print("Type 'test' to run automated tests, or ask your own questions")
    print("="*60 + "\n")

    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user\n")
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        import traceback
        traceback.print_exc()
