from agents import Agent, Runner, trace
from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

def main():

    # 1. Define the specialist agents
    spanish_agent = Agent(
        name="Spanish Specialist",
        instructions="You are a helpful assistant who communicates only in Spanish.",
        model=DEFAULT_LLM
    )

    english_agent = Agent(
        name="English Specialist",
        instructions="You are a helpful assistant who communicates only in English.",
        model=DEFAULT_LLM
    )

    # 2. Define the Triage Agent with its handoff targets
    triage_agent = Agent(
        name="Triage Agent",
        instructions="You are a language routing agent. Based on the user's language, hand off to the correct specialist. Do not answer the question yourself.",
        model=DEFAULT_LLM,
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