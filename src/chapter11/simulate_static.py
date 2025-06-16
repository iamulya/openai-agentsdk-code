import asyncio
import os
import numpy as np
import sounddevice as sd
from agents import Agent
from agents.voice import (
    AudioInput,
    VoicePipeline,
    SingleAgentVoiceWorkflow,
)

# --- Agent Definition ---
simple_agent = Agent(
    name="Helpful Assistant",
    instructions="You are a helpful assistant. Be concise.",
    model="litellm/gemini/gemini-1.5-flash-latest"
)

# --- Voice Pipeline Setup ---
# SingleAgentVoiceWorkflow is a simple, pre-built workflow.
workflow = SingleAgentVoiceWorkflow(agent=simple_agent)
pipeline = VoicePipeline(workflow=workflow)

async def main():
    if not os.getenv("GOOGLE_API_KEY") or not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Please set both GOOGLE_API_KEY and OPENAI_API_KEY for STT/TTS.")

    # 1. Simulate a pre-recorded audio input
    # This is a silent audio buffer, but in a real app, it would be a recording.
    # The STT model will transcribe this silence as an empty string.
    # We will manually provide text to the workflow for demonstration.
    print("Simulating audio input...")
    # NOTE: The STT model will transcribe silence as "", so we manually invoke the workflow.
    # To test with real audio, you would record from a microphone.
    # For now, let's just run the workflow with text directly.
    text_input = "What is the speed of light in a vacuum?"

    # The pipeline's workflow can be run directly for text input
    # In a real voice app, the STT stage would produce this text.
    text_stream = workflow.run(text_input)

    # 2. Setup the audio player
    player = sd.OutputStream(samplerate=24000, channels=1, dtype=np.int16)
    player.start()
    print("Agent is generating a response...")

    # 3. Stream the text to the TTS model and play audio chunks
    async for text_chunk in text_stream:
      async for audio_chunk in pipeline._get_tts_model().run(text_chunk, pipeline.config.tts_settings):
          player.write(np.frombuffer(audio_chunk, dtype=np.int16))

    player.stop()
    player.close()
    print("Playback finished.")


if __name__ == "__main__":
    asyncio.run(main())