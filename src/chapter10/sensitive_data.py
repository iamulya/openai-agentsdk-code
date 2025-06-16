from agents import Agent, Runner, RunConfig, function_tool

@function_tool
def process_user_data(user_id: str, personal_note: str) -> str:
    """Processes sensitive user data."""
    return "Data processed successfully."

def main():
    # ... setup ...
    sensitive_agent = Agent(
        name="Processor",
        instructions="Process the data.",
        model="litellm/gemini/gemini-1.5-flash-latest",
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