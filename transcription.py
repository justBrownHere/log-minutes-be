import os
import sys
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)

def transcribe_audio(audio_file: str) -> str:
    try:
        with open(audio_file, "rb") as file:
            transcribe_audio = client.audio.transcription.create(
                model = "whisper-1",
                file = file
            )
        return transcribe_audio.text
    except Exception as e:
        print(f"Error: {e}")
