#
# A fan-out/fan-in pattern for parallel execution.
#
import asyncio
from agents import Agent, Runner, trace

async def main():

    # 1. Define the parallel specialist agents (the "Fan-Out")
    optimist_agent = Agent(
        name="Optimist",
        instructions="You are an eternal optimist. You see the best in every situation and focus only on the positive outcomes.",
        model="litellm/gemini/gemini-2.0-flash"
    )
    pessimist_agent = Agent(
        name="Pessimist",
        instructions="You are a deep pessimist. You see the worst in every situation and focus only on the risks and negative outcomes.",
        model="litellm/gemini/gemini-2.0-flash"
    )
    realist_agent = Agent(
        name="Realist",
        instructions="You are a balanced realist. You weigh the pros and cons objectively.",
        model="litellm/gemini/gemini-2.0-flash"
    )

    # 2. Define the synthesizer agent (the "Fan-In")
    synthesizer_agent = Agent(
        name="Synthesizer",
        instructions="You have been given three perspectives on a topic: one optimistic, one pessimistic, and one realistic. Your job is to synthesize these into a single, balanced, final answer.",
        model="litellm/gemini/gemini-2.0-flash"
    )

    # --- Orchestration ---
    topic = "the impact of AI on the job market for software developers."
    with trace("Parallel Perspective Analysis"):
        print(f"Analyzing topic: {topic}\n")

        # Step A: Fan-Out - Run all three persona agents in parallel
        optimist_task = Runner.run(optimist_agent, topic)
        pessimist_task = Runner.run(pessimist_agent, topic)
        realist_task = Runner.run(realist_agent, topic)

        results = await asyncio.gather(optimist_task, pessimist_task, realist_task)
        optimist_view, pessimist_view, realist_view = [res.final_output for res in results]

        print("--- Perspectives Gathered ---")
        print(f"Optimist says: {optimist_view}\n")
        print(f"Pessimist says: {pessimist_view}\n")
        print(f"Realist says: {realist_view}\n")

        # Step B: Fan-In - Feed the parallel results into the synthesizer
        synthesis_input = f"""
        Topic: {topic}

        Optimistic Perspective:
        {optimist_view}

        Pessimistic Perspective:
        {pessimist_view}

        Realistic Perspective:
        {realist_view}

        Please synthesize these into a final, balanced analysis.
        """
        final_result = await Runner.run(synthesizer_agent, synthesis_input)

        print("--- Final Synthesized Report ---")
        print(final_result.final_output)

if __name__ == "__main__":
    asyncio.run(main())