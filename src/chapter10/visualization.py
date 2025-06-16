from agents import Agent, function_tool, handoff
from agents.extensions.visualization import draw_graph

# --- Define a complex agent architecture ---
@function_tool
def general_knowledge_qa(question: str) -> str:
    """Answers general knowledge questions."""
    return "The answer is 42."

billing_agent = Agent(name="Billing Agent", instructions="...")
shipping_agent = Agent(name="Shipping Agent", instructions="...")

support_agent = Agent(
    name="Support Agent",
    instructions="I help with support tickets.",
    tools=[general_knowledge_qa],
    handoffs=[shipping_agent]
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="I route users to the correct department.",
    handoffs=[support_agent, billing_agent]
)

# --- Generate and save the visualization ---
graph = draw_graph(triage_agent, filename="triage_system_architecture")
print("Graph saved to triage_system_architecture.png")