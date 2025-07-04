import asyncio
from agents import Agent, Runner

from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

async def main():
    # Define an Agent: an LLM configured with instructions
    haiku_agent = Agent(
        name="Haiku Poet",
        instructions="You are a poetic assistant who only responds in haikus (5-7-5 syllables).",
        model=DEFAULT_LLM # Using the 'litellm/' prefix
    )

    # Use the Runner to execute the agent
    result = await Runner.run(
      starting_agent=haiku_agent,
      input="Write a haiku about a rainy day in Tokyo."
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())