import asyncio
import litellm

async def get_haiku(topic: str):
    """Generates a haiku using a direct LLM call."""

    messages = [{
        "role": "user",
        "content": f"Write a haiku about {topic}."
    }]

    # Direct call to the model
    response = await litellm.acompletion(
        model="gemini/gemini-2.0-flash",
        messages=messages,
        temperature=0.5
    )

    return response.choices[0].message.content

async def main():
    haiku = await get_haiku("a rainy day in Tokyo")
    print(haiku)

if __name__ == "__main__":
    asyncio.run(main())