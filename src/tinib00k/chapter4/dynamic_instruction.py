from dataclasses import dataclass
from typing import Literal
from agents import Agent, Runner, RunContextWrapper

from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

# 1. Define a context class to hold our state
@dataclass
class AgentContext:
    mood: Literal["happy", "grumpy", "poetic"]

# 2. Define the dynamic instructions function
def get_moody_instructions(
    run_context: RunContextWrapper[AgentContext],
    agent: Agent[AgentContext]
) -> str:
    """Generates instructions based on the mood in the context."""
    mood = run_context.context.mood
    if mood == "happy":
        return "You are a cheerful and optimistic assistant. Use lots of exclamation points!"
    elif mood == "grumpy":
        return "You are a grumpy assistant who answers questions reluctantly. Keep it short."
    else: # poetic
        return "You answer all questions in the form of a rhyming couplet."

# 3. Create the agent with the dynamic instructions function
moody_agent = Agent[AgentContext](
    name="Moody Assistant",
    instructions=get_moody_instructions, # Pass the function, not its result
    model=DEFAULT_LLM
)

def main():

    # Run the agent with different moods
    for mood in ["happy", "grumpy", "poetic"]:
        print(f"--- Running agent in a {mood.upper()} mood ---")
        context = AgentContext(mood=mood)
        result = Runner.run_sync(
            moody_agent,
            "What is the capital of France?",
            context=context # Pass the context to the runner
        )
        print(f"Agent: {result.final_output}\n")

if __name__ == "__main__":
    main()