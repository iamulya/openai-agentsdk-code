from agents import Agent, Runner, function_tool, RunContextWrapper, ModelSettings


def custom_error_handler(ctx: RunContextWrapper, error: Exception) -> str:
    """A custom function to format error messages for the LLM."""
    print(f"[Error Handler]: Caught a {type(error).__name__}: {error}")
    return f"The tool failed with an error. Please check your inputs. Error: {error}"

@function_tool(failure_error_function=custom_error_handler)
def divide(a: float, b: float) -> float:
    """Divides the first number by the second number."""
    print(f"[Tool Executed]: Dividing {a} by {b}")
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def main():

    error_handling_agent = Agent(
        name="Error Handling Agent",
        instructions="Perform the division using the divide tool. If an error occurs, explain it to the user.",
        model="litellm/gemini/gemini-2.0-flash",
        tools=[divide],
        model_settings=ModelSettings(
            tool_choice="required",            # Must call tools on the first turn
        )
    )

    # This will trigger the failure_error_function
    result = Runner.run_sync(error_handling_agent, "Can you divide 10 by 0?")

    print(f"\nFinal Answer: {result.final_output}")

if __name__ == "__main__":
    main()

# Expected Output:
#
# [Error Handler]: Caught a ValueError: Cannot divide by zero.
#
# Final Answer: I'm sorry, but I cannot perform that calculation. The tool failed with an error because you cannot divide by zero. Please provide a non-zero divisor.