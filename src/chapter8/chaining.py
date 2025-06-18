#
# A deterministic chain: Brainstormer -> Writer
#

from pydantic import BaseModel, Field
from agents import Agent, Runner, trace

class BlogIdeas(BaseModel):
    ideas: list[str] = Field(description="A list of three creative blog post titles.")

def main():

    # 1. Define the first agent in the chain
    brainstormer_agent = Agent(
        name="Brainstormer",
        instructions="You are an expert idea generator. Generate creative blog post titles based on the user's topic.",
        model="litellm/gemini/gemini-2.0-flash",
        output_type=BlogIdeas # We use a structured output
    )

    # 2. Define the second agent in the chain
    writer_agent = Agent(
        name="Writer",
        instructions="You are a professional writer. Write a short, engaging blog post (2-3 paragraphs) based on the provided title.",
        model="litellm/gemini/gemini-2.0-flash" 
    )

    # --- Code-driven Orchestration ---
    with trace("Chained Blog Writing Workflow"):
        # Step 1: Run the brainstormer
        print("--- Running Brainstormer Agent ---")
        topic = "the future of renewable energy"
        brainstorm_result = Runner.run_sync(brainstormer_agent, f"Topic: {topic}")

        # Extract the structured output
        ideas_output: BlogIdeas = brainstorm_result.final_output
        print(f"Generated Ideas: {ideas_output.ideas}")

        # Choose an idea (can be done by user or logic)
        chosen_title = ideas_output.ideas[0]
        print(f"\nSelected Title: '{chosen_title}'")

        # Step 2: Run the writer with the output of the first agent
        print("\n--- Running Writer Agent ---")
        write_result = Runner.run_sync(
            writer_agent,
            f"Please write a blog post titled: '{chosen_title}'"
        )

        print("\n--- Final Blog Post ---")
        print(write_result.final_output)

if __name__ == "__main__":
    main()