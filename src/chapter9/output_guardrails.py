#
# An output guardrail to check for sensitive words.
#
import asyncio
import os
from pydantic import BaseModel
from agents import Agent, Runner, output_guardrail, GuardrailFunctionOutput, RunContextWrapper, OutputGuardrailTripwireTriggered

# 1. Main agent's output type
class AgentResponse(BaseModel):
    response: str

# 2. Guardrail's output type
class PIIAnalysis(BaseModel):
    contains_pii: bool
    reasoning: str

# 3. Guardrail agent
pii_checker_agent = Agent(
    name="PII Checker",
    instructions="Analyze the text. Does it contain the secret project codename 'Bluebird'?",
    output_type=PIIAnalysis,
    model="litellm/gemini/gemini-1.5-flash-latest"
)

# 4. The output guardrail function. Note the type hint for `output`.
@output_guardrail
async def pii_check_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: AgentResponse # Type hint matches main agent's output_type
) -> GuardrailFunctionOutput:
    """Checks the agent's final response for the sensitive codename."""
    print("[Guardrail]: Checking final output for sensitive data...")
    result = await Runner.run(pii_checker_agent, output.response, context=ctx.context)
    analysis: PIIAnalysis = result.final_output

    should_trip = analysis.contains_pii
    if should_trip:
        print("[Guardrail]: Tripwire triggered! Sensitive data detected.")

    return GuardrailFunctionOutput(
        output_info=analysis.reasoning,
        tripwire_triggered=should_trip
    )

# 5. The main agent, with the output guardrail attached
main_agent = Agent(
    name="Internal Comms Agent",
    instructions="You are writing an internal company update. The secret project is codenamed 'Project Bluebird'. Announce that its launch has been successful.",
    output_type=AgentResponse,
    output_guardrails=[pii_check_guardrail]
)

def main():
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

    try:
        Runner.run_sync(main_agent, "Write the internal announcement.")
    except OutputGuardrailTripwireTriggered as e:
        print("\nOutput guardrail successfully caught the sensitive information.")
        print("The response was blocked before it could be sent to the user.")
        print(f"Reason: {e.guardrail_result.output.output_info}")

if __name__ == "__main__":
    main()