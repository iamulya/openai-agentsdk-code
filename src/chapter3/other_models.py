from agents import Agent, Runner

def main():

    # 1. Define a specialist agent using Google's Gemini
    code_explainer_agent = Agent(
        name="Code Explainer",
        instructions="You are an expert at explaining complex code in simple terms.",
        model="litellm/gemini/gemini-2.0-flash",
        handoff_description="Use for explaining code."
    )

    # 2. Define another specialist using Anthropic's Claude
    poem_writer_agent = Agent(
        name="Poet",
        instructions="You are a poet who writes beautiful poems about any topic.",
        model="litellm/anthropic/claude-3-haiku-20240307",
        handoff_description="Use for writing poetry."
    )

    # 3. The Triage agent can be from any provider
    triage_agent = Agent(
        name="Triage Agent",
        instructions="Analyze the user's request and hand off to the appropriate specialist agent.",
        model="litellm/gemini/gemini-2.0-flash",
        handoffs=[code_explainer_agent, poem_writer_agent]
    )

    print("--- Running Code Explanation Workflow ---")
    code_result = Runner.run_sync(
        triage_agent,
        "Can you explain what this Python list comprehension does: `[x*x for x in range(10)]`?"
    )
    print(f"Final response from: {code_result.last_agent.name}")
    print(f"Response: {code_result.final_output}")

    print("\n--- Running Poetry Workflow ---")
    poem_result = Runner.run_sync(
        triage_agent,
        "Write me a short poem about the moon."
    )
    print(f"Final response from: {poem_result.last_agent.name}")
    print(f"Response: {poem_result.final_output}")


if __name__ == "__main__":
    main()