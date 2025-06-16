import asyncio
import os
from collections.abc import AsyncIterator
from agents import Agent, Runner, TResponseInputItem
from agents.voice import (
    VoiceWorkflowBase,
    VoiceWorkflowHelper,
    VoicePipeline,
    StreamedAudioInput
)

# --- A custom workflow class ---
class SecretWordWorkflow(VoiceWorkflowBase):
    def __init__(self, secret_word: str):
        self._secret_word = secret_word.lower()
        self._agent = Agent(name="Chatter", instructions="Make small talk.", model="litellm/gemini/gemini-1.5-flash-latest")
        self._history: list[TResponseInputItem] = []

    async def run(self, transcription: str) -> AsyncIterator[str]:
        print(f"[Workflow]: Received transcription: '{transcription}'")
        self._history.append({"role": "user", "content": transcription})

        # Custom logic: check for the secret word
        if self._secret_word in transcription.lower():
            print(f"[Workflow]: Secret word '{self._secret_word}' detected! Bypassing agent.")
            yield "You said the secret word! You win!"
            return # End the workflow for this turn

        # Default logic: run the agent
        print("[Workflow]: Running default agent...")
        result_stream = Runner.run_streamed(self._agent, self._history)

        full_response = ""
        # Use a helper to stream text from the agent run
        async for text_chunk in VoiceWorkflowHelper.stream_text_from(result_stream):
            full_response += text_chunk
            yield text_chunk

        # Update history for the next turn
        self._history.append({"role": "assistant", "content": full_response})

async def main():
    if not os.getenv("GOOGLE_API_KEY") or not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Please set both GOOGLE_API_KEY and OPENAI_API_KEY for STT/TTS.")

    # Instantiate the pipeline with our custom workflow
    custom_workflow = SecretWordWorkflow(secret_word="banana")
    pipeline = VoicePipeline(workflow=custom_workflow)

    # ... simulation and playback logic would go here ...
    # Try prompting it with "hello there" and then "is the secret word banana?"
    # to see the two different logic paths execute.
    print("Custom workflow is set up. Try saying 'banana'!")

if __name__ == "__main__":
    asyncio.run(main())