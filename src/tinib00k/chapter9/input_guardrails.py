from agents import Agent, Runner, InputGuardrailTripwireTriggered
from agents import input_guardrail, GuardrailFunctionOutput, RunContextWrapper, TResponseInputItem

from pydantic import BaseModel, Field
from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

class IntentClassification(BaseModel):
    is_coding_question: bool = Field(description="Is the user asking a question related to programming, code, or software development?")
    reasoning: str = Field(description="A brief justification for the classification.")

# This agent is small and fast, perfect for a guardrail.
guardrail_agent = Agent(
    name="Intent Classifier",
    instructions="Classify the user's request. Is it a coding-related question?",
    model=DEFAULT_LLM,
    output_type=IntentClassification
)

@input_guardrail
async def topic_check_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """This guardrail checks if the input is a coding question."""
    print("[Guardrail]: Checking if the request is on-topic...")

    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    classification: IntentClassification = result.final_output

    # The tripwire is triggered if the topic is NOT a coding question.
    should_trip = not classification.is_coding_question

    if should_trip:
        print("[Guardrail]: Tripwire triggered! Request is off-topic.")

    return GuardrailFunctionOutput(
        output_info=classification.reasoning, # We can pass along info for logging
        tripwire_triggered=should_trip
    )

def main():

    # Main agent is more powerful and specialized.
    coding_agent = Agent(
        name="Python Expert",
        instructions="You are an expert Python developer who provides concise, accurate code solutions.",
        model=DEFAULT_LLM,
        input_guardrails=[topic_check_guardrail] # Attach the guardrail
    )

    print("--- Test Case 1: On-topic request ---")
    try:
        on_topic_result = Runner.run_sync(
            coding_agent,
            "How do I sort a dictionary by its values in Python?"
        )
        print(f"Agent Response: {on_topic_result.final_output}")
    except InputGuardrailTripwireTriggered as e:
        print(f"This should not happen. Guardrail tripped unexpectedly: {e.guardrail_result.output.output_info}")


    print("\n--- Test Case 2: Off-topic request ---")
    try:
        Runner.run_sync(
            coding_agent,
            "What was the main cause of the fall of the Roman Empire?"
        )
    except InputGuardrailTripwireTriggered as e:
        print("Guardrail correctly tripped!")
        print(f"Reason from guardrail: {e.guardrail_result.output.output_info}")
        print("Main agent was never called, saving time and resources.")

if __name__ == "__main__":
    main()