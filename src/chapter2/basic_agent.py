#
# A basic agent that responds to a prompt.
#

from agents import Agent, Runner

def main():
    # 1. Define the Agent
    polite_agent = Agent(
        name="Polite Assistant",
        instructions="You are a helpful and polite assistant. You always answer in a clear and friendly tone.",
        model="litellm/gemini/gemini-1.5-flash-latest"
    )

    # 2. Define the input
    user_input = "What is the primary function of a CPU in a computer?"

    # 3. Use the Runner to execute the agent
    print(f"User: {user_input}")
    result = Runner.run_sync(polite_agent, user_input)

    # 4. Print the final output
    print(f"\nAgent: {result.final_output}")

if __name__ == "__main__":
    main()