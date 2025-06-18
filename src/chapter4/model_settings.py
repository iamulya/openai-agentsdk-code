#
# Configuring an agent with specific model settings.
#

from agents import Agent, Runner, ModelSettings

def main():

    # Define the Agent with custom ModelSettings
    storyteller_agent = Agent(
        name="Creative Storyteller",
        instructions="You are a master storyteller who writes compelling, short opening paragraphs for fantasy novels.",
        model="litellm/gemini/gemini-2.0-flash",
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