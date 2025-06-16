import asyncio
import litellm

# --- Setup ---
# Ensure you have litellm installed: pip install litellm
# Set your Google API key: export GOOGLE_API_KEY="your-key-here"
# ----------------

async def get_haiku(topic: str):
    """Generates a haiku using a direct LLM call."""

    messages = [{
        "role": "user",
        "content": f"Write a haiku about {topic}."
    }]

    # Direct call to the model
    response = await litellm.acompletion(
        model="gemini/gemini-1.5-flash-latest",
        messages=messages,
        temperature=0.5
    )

    return response.choices[0].message.content

async def main():
    haiku = await get_haiku("a rainy day in Tokyo")
    print(haiku)

if __name__ == "__main__":
    asyncio.run(main())