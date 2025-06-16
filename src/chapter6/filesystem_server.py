import asyncio
import os
import shutil
from agents import Agent, Runner, trace, ModelSettings
from agents.mcp import MCPServerStdio

async def main():
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Please set the GOOGLE_API_KEY environment variable.")
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it.")

    # 1. Define the path to our sample files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")

    # 2. Instantiate and connect to the MCP server
    async with MCPServerStdio(
        name="Local Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        },
    ) as fs_server:
        # 3. Define an agent that uses the server
        file_agent = Agent(
            name="File Assistant",
            instructions="Use your tools to read files and answer questions based on their content.",
            mcp_servers=[fs_server],
            model="litellm/gemini/gemini-1.5-flash-latest",
            # We force tool use here for a predictable demonstration
            model_settings=ModelSettings(tool_choice="required")
        )

        # 4. Run the agent
        with trace("MCP Filesystem Example"):
            # First, ask the agent to list the files it sees
            result_list = await Runner.run(file_agent, "What files can you see?")
            print(f"Agent's response (list): {result_list.final_output}")

            # Now, ask a question that requires reading a file
            result_read = await Runner.run(file_agent, "When do I like to visit Tokyo?")
            print(f"Agent's response (read): {result_read.final_output}")

if __name__ == "__main__":
    asyncio.run(main())

# Expected Output:
#
# Agent's response (list): I can see the file `favorite_cities.txt`.
# Agent's response (read): You like to visit Tokyo in the winter.