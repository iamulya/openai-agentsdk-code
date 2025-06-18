#
# Forcing JSON via prompt when structured output is not supported.
#
import json
from pydantic import BaseModel, ValidationError
from agents import Agent, Runner

class UserProfile(BaseModel):
    name: str
    age: int

def main():
    # Note: We do NOT set output_type on the agent
    json_agent = Agent(
        name="JSON Extractor",
        # We bake the schema and instructions into the prompt itself
        instructions=f"""
        You are a JSON extraction expert. Extract the user's name and age from their message.
        You MUST respond with only a single, valid JSON object that conforms to this Pydantic schema:

        ```json
        {json.dumps(UserProfile.model_json_schema(), indent=2)}
        ```
        """,
        model="litellm/gemini/gemini-2.0-flash"
    )

    # After running, you would need to manually parse the `result.final_output` string
    result = Runner.run_sync(json_agent, "Hi, I'm Bob and I'm 32 years old.")
    try:
        # Sanitize the output to extract only the JSON part
        final_result = result.final_output

        # Find the start and end indices of the JSON object
        json_start = final_result.find('{')
        json_end = final_result.rfind('}') + 1

        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON object found in the LLM output.")

        clean_json_str = final_result[json_start:json_end]

        print(f"Cleaned JSON String for Parsing:\n{clean_json_str}\n")

        # Now parse the cleaned string
        profile = UserProfile.model_validate_json(clean_json_str)

        print("Successfully parsed UserProfile!")
        print(f"Name: {profile.name}, Age: {profile.age}")
    except (ValidationError, ValueError, json.JSONDecodeError) as e:
        print(f"Failed to parse LLM output: {e}")

if __name__ == "__main__":
    main()

