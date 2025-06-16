import asyncio
import os
from pydantic import BaseModel, Field
from agents import Agent, Runner, handoff, RunContextWrapper

# 1. Define the data schema for the handoff
class EscalationData(BaseModel):
    reason: str = Field(description="A brief explanation for why the escalation is necessary.")
    ticket_id: str = Field(description="The customer's support ticket ID.")

# 2. The on_handoff callback now accepts the validated data
def process_escalation(ctx: RunContextWrapper, data: EscalationData) -> None:
    print("\n--- Escalation Protocol Initiated ---")
    print(f"Escalating ticket {data.ticket_id}")
    print(f"Reason: {data.reason}")
    print("------------------------------------")
    # In a real app, you might now create a Jira ticket or alert a human.

# 3. Define the agents and the typed handoff
human_support_agent = Agent(name="Human Support Team", instructions="...")
triage_agent = Agent(
    name="Triage Agent",
    instructions="You are an AI assistant. If you cannot resolve the issue, escalate to a human.",
    model="litellm/gemini/gemini-1.5-flash-latest",
    handoffs=[
        handoff(
            agent=human_support_agent,
            on_handoff=process_escalation,
            input_type=EscalationData # Specify the input schema
        )
    ]
)

def main():
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

    Runner.run_sync(triage_agent, "My ticket is T-12345. I'm really frustrated, I've asked three times about my refund and the issue is still not solved. I need to speak to a person.")

if __name__ == "__main__":
    main()