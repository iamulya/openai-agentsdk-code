import asyncio
import os
from agents import Agent, Runner, trace

def main():
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

    # 1. Define Specialist Agents
    spanish_translator = Agent(
        name="Spanish Translator",
        instructions="You are an expert translator. Translate the user's text into Spanish.",
        model="litellm/gemini/gemini-1.5-flash-latest",
    )

    french_translator = Agent(
        name="French Translator",
        instructions="You are an expert translator. Translate the user's text into French.",
        model="litellm/gemini/gemini-1.5-flash-latest",
    )

    # 2. Define the Orchestrator and provide the specialists as tools
    orchestrator = Agent(
        name="Translation Orchestrator",
        instructions="You are a project manager for translations. Use your tools to fulfill the user's request. Call all relevant tools.",
        model="litellm/gemini/gemini-1.5-flash-latest",
        tools=[
            spanish_translator.as_tool(
                tool_name="translate_to_spanish",
                tool_description="Use this to translate a given text into Spanish."
            ),
            french_translator.as_tool(
                tool_name="translate_to_french",
                tool_description="Use this to translate a given text into French."
            ),
        ]
    )

    # 3. Run the orchestration
    with trace("Multi-language Translation Trace"):
        result = Runner.run_sync(
            orchestrator,
            "Please translate the phrase 'hello world' into Spanish and French."
        )

    print(f"Orchestrator's Final Report:\n{result.final_output}")


if __name__ == "__main__":
    main()

# Expected Output:
#
# Orchestrator's Final Report:
# The translation of "hello world" into Spanish is "hola mundo" and into French is "bonjour le monde".