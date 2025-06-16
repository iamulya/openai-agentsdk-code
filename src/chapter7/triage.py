import asyncio
import os
from agents import Agent, Runner, trace

def main():
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

    # 1. Define the specialist agents
    spanish_agent = Agent(
        name="Spanish Specialist",
        instructions="You are a helpful assistant who communicates only in Spanish.",
        model="litellm/gemini/gemini-1.5-flash-latest"
    )

    english_agent = Agent(
        name="English Specialist",
        instructions="You are a helpful assistant who communicates only in English.",
        model="litellm/gemini/gemini-1.5-flash-latest"
    )

    # 2. Define the Triage Agent with its handoff targets
    triage_agent = Agent(
        name="Triage Agent",
        instructions="You are a language routing agent. Based on the user's language, hand off to the correct specialist. Do not answer the question yourself.",
        model="litellm/gemini/gemini-1.5-flash-latest",
        handoffs=[spanish_agent, english_agent] # List of possible handoff targets
    )

    # 3. Run the workflow with a Spanish query
    with trace("Language Handoff Workflow"):
        result = Runner.run_sync(
            triage_agent,
            "Hola, ¿cuál es la capital de México?"
        )

    print(f"Final Response came from: {result.last_agent.name}")
    print(f"Agent says: {result.final_output}")

if __name__ == "__main__":
    main()

# Expected Output:
#
# Final Response came from: Spanish Specialist
# Agent says: ¡Hola! La capital de México es la Ciudad de México.