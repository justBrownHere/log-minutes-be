import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

def transcribe_audio(audio_file: str) -> str:
    if not audio_file:
        return ""
    try:
        with open(audio_file, "rb") as file:
            transcribe_audio = client.audio.transcriptions.create(
                model = "whisper-1",
                file = file            
            )
        return transcribe_audio.text
    except Exception as e:
        print(f"Error transcrible: {e}")
        return ""
