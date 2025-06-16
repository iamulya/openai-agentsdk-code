import os
from dotenv import load_dotenv

def load_and_check_keys():
    """
    Loads environment variables from a .env file and checks for the presence
    of essential API keys required by the book's examples.

    This function should be called at the beginning of each chapter's main script.

    It expects a .env file in the project's root directory with the following format:

    OPENAI_API_KEY="sk-..."
    GEMINI_API_KEY="AIza..."
    ANTHROPIC_API_KEY="sk-ant-..."

    Raises:
        ValueError: If any of the required API keys are not found in the environment.
    """
    print("Loading environment variables...")
    load_dotenv()

    # Define all keys required by the various chapters
    required_keys = {
        #"OPENAI_API_KEY": "Needed for tracing functionality.",
        "GEMINI_API_KEY": "Needed for Gemini models used in most examples.",
        #"ANTHROPIC_API_KEY": "Needed for the multi-provider chapter (Chapter 9).",
    }

    missing_keys = []
    for key, reason in required_keys.items():
        if not os.getenv(key):
            missing_keys.append(f"  - {key}: {reason}")

    if missing_keys:
        error_message = (
            "ERROR: The following required environment variables are missing.\n"
            "Please create a `.env` file in the project root and add them.\n\n"
        )
        error_message += "\n".join(missing_keys)
        raise ValueError(error_message)

    print("All required API keys are loaded successfully.")
