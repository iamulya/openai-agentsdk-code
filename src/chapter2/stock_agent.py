#
# An agent that can use a tool to get information.
#

import random
from agents import Agent, Runner, function_tool

# --- Tool Definition ---
@function_tool
def get_stock_price(symbol: str) -> float:
    """
    Gets the current stock price for a given ticker symbol.

    Args:
        symbol: The stock ticker symbol (e.g., "GOOGL", "AAPL").
    """
    print(f"[Tool Executed]: Getting stock price for {symbol}")
    # In a real application, this would call a financial data API.
    # Here, we'll just return a random price for demonstration.
    return round(random.uniform(100, 1000), 2)

# --- Agent Definition ---
def main():

    # Define an agent and provide it with the tool
    financial_agent = Agent(
        name="Financial Assistant",
        instructions="You are a financial assistant. Use your tools to answer questions. Be concise.",
        model="litellm/gemini/gemini-2.0-flash",
        tools=[get_stock_price] # The tool is passed in a list
    )

    # Use the Runner to execute the agent
    result = Runner.run_sync(
        financial_agent,
        "What is the current price of Google's stock?"
    )

    print(f"\nFinal Answer:\n{result.final_output}")

if __name__ == "__main__":
    main()