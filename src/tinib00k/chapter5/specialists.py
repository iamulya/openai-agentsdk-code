from agents import Agent, Runner, trace

from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

def main():

    # 1. Define Specialist Agents
    spanish_translator = Agent(
        name="Spanish Translator",
        instructions="You are an expert translator. Translate the user's text into Spanish.",
        model=DEFAULT_LLM,
    )

    french_translator = Agent(
        name="French Translator",
        instructions="You are an expert translator. Translate the user's text into French.",
        model=DEFAULT_LLM,
    )

    # 2. Define the Orchestrator and provide the specialists as tools
    orchestrator = Agent(
        name="Translation Orchestrator",
        instructions="You are a project manager for translations. Use your tools to fulfill the user's request. Call all relevant tools.",
        model=DEFAULT_LLM,
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