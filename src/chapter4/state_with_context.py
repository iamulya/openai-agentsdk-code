from dataclasses import dataclass, field
from agents import Agent, Runner, RunContextWrapper, function_tool

# 1. Define a context class to hold session data
@dataclass
class UserSession:
    user_id: str
    items_in_cart: list[str] = field(default_factory=list)

# 2. Define a tool that interacts with the context
@function_tool
def add_to_cart(
    ctx: RunContextWrapper[UserSession], # Receives the context wrapper
    item_name: str
) -> str:
    """Adds an item to the user's shopping cart."""
    ctx.context.items_in_cart.append(item_name)
    return f"Successfully added '{item_name}' to the cart."

# 3. Define the agent, specifying its context type
shopping_agent = Agent[UserSession](
    name="Shopping Assistant",
    instructions="Help the user with their shopping. Use your tools to manage the cart.",
    model="litellm/gemini/gemini-2.0-flash",
    tools=[add_to_cart]
)

def main():
    session_context = UserSession(user_id="alex-123")
    Runner.run_sync(
        shopping_agent,
        "Please add a 'laptop' to my cart.",
        context=session_context
    )
    print(f"Cart contents from context: {session_context.items_in_cart}")

if __name__ == "__main__":
    main()