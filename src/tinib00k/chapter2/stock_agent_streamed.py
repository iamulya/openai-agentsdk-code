#
# An agent that can use a tool to get information.
#

import asyncio
import random
from agents import Agent, Runner, function_tool

from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

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
async def stream_example():

    # Define an agent and provide it with the tool
    financial_agent = Agent(
        name="Financial Assistant",
        instructions="You are a financial assistant. Use your tools to answer questions. Be concise.",
        model=DEFAULT_LLM,
        tools=[get_stock_price] # The tool is passed in a list
    )

    # Use the Runner to execute the agent
    result = Runner.run_streamed(
        financial_agent,
        "What is the current price of Google's stock?"
    )

    print("Agent's Final Answer: ", end="")
    # The stream_events() iterator yields different event types.
    # We filter for text deltas to print the response token-by-token.
    async for event in result.stream_events():
        if event.type == "raw_response_event" and event.data.type =="response.output_text.delta":
            print(event.data.delta, end="", flush=True)

    print() # for a final newline

if __name__ == "__main__":
    asyncio.run(stream_example())