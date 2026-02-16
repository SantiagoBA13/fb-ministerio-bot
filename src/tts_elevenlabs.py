# src/tts_elevenlabs.py
import os
import requests

ELEVEN_BASE = "https://api.elevenlabs.io/v1"

def synthesize_to_mp3(text: str, out_path: str) -> None:
    api_key = os.environ["ELEVENLABS_API_KEY"]
    voice_id = os.environ["ELEVENLABS_VOICE_ID"]
    model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")

    url = f"{ELEVEN_BASE}/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.8,
            "style": 0.35,
            "use_speaker_boost": True
        }
    }
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)
