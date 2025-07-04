from agents import Agent, Runner, function_tool
from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

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

    # 2. Create an agent and give it the tool
    calculator_agent = Agent(
        name="Calculator Agent",
        instructions="You are a calculator. Use your tools to perform calculations.",
        model=DEFAULT_LLM,
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