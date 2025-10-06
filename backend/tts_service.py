import requests
import tempfile
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
async def synthesize_speech(text: str) -> str:
    
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 1,
            "similarity_boost": 1
        }
    }
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"TTS failed: {response.text}")

    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    with open(output_file, "wb") as f:
        f.write(response.content)

    return output_file
