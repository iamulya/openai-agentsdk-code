#
# Configuring an agent with specific model settings.
#

import asyncio
import os
from agents import Agent, Runner, ModelSettings

def main():
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

    # Define the Agent with custom ModelSettings
    storyteller_agent = Agent(
        name="Creative Storyteller",
        instructions="You are a master storyteller who writes compelling, short opening paragraphs for fantasy novels.",
        model="litellm/gemini/gemini-1.5-flash-latest",
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

# Expected Output:
#
# Sir Kaelan’s steel-shod boots crunched on volcanic glass, each step an affront
# to the dead silence of the Obsidian Peaks. The air, thin and sharp with the
# stench of sulfur, tasted of ancient dread. Before him, a chasm yawned in the
# mountainside, a wound in the world that bled a faint, ominous heat. It was the
# maw of the beast, the threshold to Ignis, the Ember-Drake who had scorched
# the memory of summer from the lands below. Kaelan drew the Dragon's Bane,
# its silvered edge gleaming hungrily in the gloom, and took his first step
# into the dragon's shadow.