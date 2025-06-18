from agents import Agent, Runner, function_tool, RunConfig

@function_tool
def get_user_city() -> str:
    """Retrieves the user's city from a database."""
    print("[Tool Executed]: get_user_city()")
    return "San Francisco"

def main():

    weather_agent = Agent(
        name="Weather Assistant",
        instructions="You are a helpful assistant. Use your tools to find the user's city and then tell them it's always sunny there.",
        model="litellm/gemini/gemini-2.0-flash",
        tools=[get_user_city]
    )

    # Use RunConfig to give our trace a meaningful name
    run_config = RunConfig(workflow_name="Simple Weather Lookup")
    result = Runner.run_sync(
        weather_agent,
        "What's the weather like where I am?",
        run_config=run_config
    )
    print(f"\nFinal Answer: {result.final_output}")

if __name__ == "__main__":
    main()