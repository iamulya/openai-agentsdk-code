import asyncio
from agents import Agent, Runner, function_tool, ModelSettings

from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

# --- Tool Definitions ---
@function_tool
async def setup_database(user_id: str) -> str:
    """Prepares the user's database."""
    print(f"[Tool]: Setting up database for {user_id}...")
    await asyncio.sleep(1) # Simulate network latency
    print(f"[Tool]: Database ready for {user_id}.")
    return "Database connection is ready."

@function_tool
async def authenticate_user(user_id: str) -> str:
    """Authenticates the user and retrieves their permissions."""
    print(f"[Tool]: Authenticating {user_id}...")
    await asyncio.sleep(0.5) # Simulate authentication call
    print(f"[Tool]: {user_id} is authenticated as 'admin'.")
    return "User is authenticated with 'admin' role."

# --- Agent Definition ---
async def main():

    orchestrator_agent = Agent(
        name="Workflow Orchestrator",
        instructions="You are a system orchestrator. Your job is to prepare the system for the user by calling all necessary setup tools.",
        model=DEFAULT_LLM, # A model that supports parallel calls
        tools=[setup_database, authenticate_user],
        model_settings=ModelSettings(
            tool_choice="required",            # Must call tools on the first turn
            parallel_tool_calls=True,          # Encourage concurrent tool calls
        )
    )

    # --- Run the Orchestration ---
    result = await Runner.run(
        orchestrator_agent,
        "Prepare the system for user 'alex-456'."
    )

    print("\n--- Final Output ---")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())