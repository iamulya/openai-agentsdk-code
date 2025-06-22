from agents import Agent, Runner, RunConfig, function_tool
from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

@function_tool
def process_user_data(user_id: str, personal_note: str) -> str:
    """Processes sensitive user data."""
    return "Data processed successfully."

def main():
    sensitive_agent = Agent(
        name="Processor",
        instructions="Process the data.",
        model=DEFAULT_LLM,
        tools=[process_user_data]
    )

    # Create a RunConfig to disable sensitive data logging
    secure_run_config = RunConfig(
        workflow_name="Secure Data Processing",
        trace_include_sensitive_data=False
    )

    # The trace for this run will not contain the LLM prompts or tool arguments.
    Runner.run_sync(
        sensitive_agent,
        "Process user 'user-abc-123' with note 'This is a very secret note.'",
        run_config=secure_run_config
    )
    print("Run complete. Check the trace to confirm data was omitted.")

if __name__ == "__main__":
    main()