from agents import Agent, Runner, handoff, function_tool
from agents.extensions import handoff_filters

@function_tool
def check_system_status() -> str:
    """Checks the internal system status."""
    return "All systems are operational."

# Specialist agent that should not be concerned with system status checks.
faq_agent = Agent(
    name="FAQ Agent",
    instructions="Answer questions concisely. Do not comment on your tools or previous turns.",
    model="litellm/gemini/gemini-2.0-flash"
)

# Triage agent has a tool and a handoff with a filter
triage_agent = Agent(
    name="Triage Agent",
    instructions="Use your tool to check status, or handoff to the FAQ agent.",
    model="litellm/gemini/gemini-2.0-flash",
    tools=[check_system_status],
    handoffs=[
        handoff(
            agent=faq_agent,
            input_filter=handoff_filters.remove_all_tools # The filter
        )
    ]
)

def main():

    # 1. First, call the tool on the triage agent
    result1 = Runner.run_sync(triage_agent, "First, check the system status.")
    print("--- Turn 1 Complete. Tool call was made. ---\n")

    # 2. Now, ask a question that triggers the handoff
    result2 = Runner.run_sync(
        triage_agent,
        result1.to_input_list() + [{"role": "user", "content": "What is an LLM?"}]
    )

    print(f"FAQ Agent Final Answer: {result2.final_output}")
    print("\n--- Final conversation history for FAQ Agent ---")
    # We inspect the history the final agent saw.
    # The tool call items from turn 1 will be missing.
    for item in result2.to_input_list():
      if item.get("tool_calls") or item.get("type") == "function_call_output":
          assert False, "Tool item was found in history, but should have been filtered!"
    print("History verified: No tool items found.")

if __name__ == "__main__":
    main()