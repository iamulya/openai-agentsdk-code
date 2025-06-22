#
# Configuring an agent with specific model settings.
#

from agents import Agent, Runner, ModelSettings
from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

def main():

    # Define the Agent with custom ModelSettings
    storyteller_agent = Agent(
        name="Creative Storyteller",
        instructions="You are a master storyteller who writes compelling, short opening paragraphs for fantasy novels.",
        model=DEFAULT_LLM,
        model_settings=ModelSettings(
            temperature=0.8, # Increase creativity
            max_tokens=250   # Limit the length of the response
        )
    )

    # Use the Runner to execute the agent
    result = Runner.run_sync(
        storyteller_agent,
        "A lone knight approaching a dragon's lair."
    )

    print(result.final_output)

if __name__ == "__main__":
    main()