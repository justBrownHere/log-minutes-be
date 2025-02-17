from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()   
client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

def post_process_transcript(transcript: str, system_prompt: str) -> str:
    response = client.chat.completions.create(
        model = "gpt-4o",
        temperature = 0.1,
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcript
            }
        ]
    )

    return response.choices[0].message.content
    
