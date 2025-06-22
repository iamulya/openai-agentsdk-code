import asyncio
import os
import shutil
from agents import Agent, Runner, trace, ModelSettings
from agents.mcp import MCPServerStdio

from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

async def main():
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it.")

    # 1. Define the path to our sample files
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    samples_dir_relative_path = os.path.relpath(
        os.path.join(os.path.dirname(__file__), "sample_files"),
        project_root
    )

    # Dynamically list the files to include in the prompt
    available_files = [f for f in os.listdir(samples_dir_relative_path) if os.path.isfile(os.path.join(samples_dir_relative_path, f))]
    file_list_str = ", ".join(f"`{file}`" for file in available_files)

    # 2. Instantiate and connect to the MCP server
    # We explicitly tell the agent what files it can access.
    PROMPT_WITH_CONTEXT = f"""
    You are a file assistant. Use your tools to answer questions.

    IMPORTANT: The file server's root is the main project directory. To access
    the necessary files, you MUST use the following full relative path prefix:
    `{samples_dir_relative_path}/`

    For example, to read the cities file, you must call the tool with the path:
    `read_file(path="{samples_dir_relative_path}/favorite_cities.txt")`

    The available files are: {file_list_str}.
    """

    # We will run the script from the project root, so '.' is the correct argument.
    async with MCPServerStdio(
        name="Local Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
            "cwd": project_root # Explicitly set the CWD for the server process
        },
    ) as fs_server:
        file_agent = Agent(
            name="File Assistant",
            instructions=PROMPT_WITH_CONTEXT,
            mcp_servers=[fs_server],
            model=DEFAULT_LLM,
            # We force tool use here for a predictable demonstration
            model_settings=ModelSettings(tool_choice="required")
        )

        with trace("MCP Filesystem Example - Corrected"):
            # Now the agent has the full context to make a correct tool call
            result_read = await Runner.run(file_agent, "When do I like to visit Tokyo?")
            print(f"Agent's response: {result_read.final_output}")

if __name__ == "__main__":
    asyncio.run(main())

# Expected Output:
#
# Agent's response (read): Based on the provided text, you might like to visit Tokyo in the winter.