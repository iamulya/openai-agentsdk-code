from agents import Agent, Runner, handoff, RunContextWrapper

# 1. Define the on_handoff callback
def log_billing_transfer(ctx: RunContextWrapper) -> None:
    """This function will be called when the handoff occurs."""
    print("[AUDIT LOG]: Transferring user to the billing department.")

# 2. Define the target agent
billing_agent = Agent(
    name="Billing Department",
    instructions="You help users with their billing inquiries.",
    model="litellm/gemini/gemini-2.0-flash",
    # We can add a description that the orchestrator will see
    handoff_description="Use for questions about invoices, payments, or subscriptions."
)

# 3. Create the handoff using the helper
custom_handoff = handoff(
    agent=billing_agent,
    on_handoff=log_billing_transfer,
    tool_name_override="goto_billing_specialist",
    tool_description_override="Transfer the user to the billing department for any questions related to payments."
)

# 4. Configure the triage agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="You are a support router.",
    model="litellm/gemini/gemini-2.0-flash",
    handoffs=[custom_handoff]
)

def main():
    Runner.run_sync(triage_agent, "I have a question about my last invoice.")

if __name__ == "__main__":
    main()

# Expected Output:
#
# [AUDIT LOG]: Transferring user to the billing department.
# (Followed by the billing agent's response)