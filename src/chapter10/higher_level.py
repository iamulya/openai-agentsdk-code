import asyncio
from agents import Agent, Runner, trace, TResponseInputItem

async def main():

    concise_agent = Agent(
        name="Concise Agent",
        instructions="You are extremely concise. Respond in 20 words or less.",
        model="litellm/gemini/gemini-2.0-flash",
    )

    # Wrap multiple Runner calls in a single trace
    with trace(workflow_name="Two-Turn Conversation", group_id="convo-123"):
        print("--- Turn 1 ---")
        # Turn 1
        result1 = await Runner.run(
            concise_agent, "Explain the concept of photosynthesis."
        )
        print(f"Agent: {result1.final_output}")

        # Prepare input for the next turn
        turn2_input: list[TResponseInputItem] = result1.to_input_list()
        turn2_input.append({
            "role": "user",
            "content": "Now explain it as if I were five years old."
        })

        print("\n--- Turn 2 ---")
        # Turn 2
        result2 = await Runner.run(concise_agent, turn2_input)
        print(f"Agent: {result2.final_output}")

if __name__ == "__main__":
    asyncio.run(main())