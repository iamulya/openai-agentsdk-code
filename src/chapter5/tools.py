import asyncio
import os
from agents import Agent, Runner, function_tool

# 1. Define a regular Python function and decorate it
@function_tool
def add(a: int, b: int) -> int:
    """
    Calculates the sum of two integers.

    Args:
        a: The first integer.
        b: The second integer.
    """
    print(f"[Tool Executed]: add(a={a}, b={b})")
    return a + b

def main():
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

    # 2. Create an agent and give it the tool
    calculator_agent = Agent(
        name="Calculator Agent",
        instructions="You are a calculator. Use your tools to perform calculations.",
        model="litellm/gemini/gemini-1.5-flash-latest",
        tools=[add] # Pass the decorated function directly
    )

    # 3. Run the agent with a prompt that requires the tool
    result = Runner.run_sync(
        calculator_agent,
        "What is 115 plus 237?"
    )

    print(f"\nFinal Answer: {result.final_output}")


if __name__ == "__main__":
    main()

# Expected Output:
#
# [Tool Executed]: add(a=115, b=237)
#
# Final Answer: The sum of 115 and 237 is 352.