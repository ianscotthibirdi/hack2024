import base64
import json
import os
from pathlib import Path

import requests


def get_mp3_from_text(text):
    api_key = os.getenv("GOOGLE_API_KEY")

    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"

    headers = {"Content-Type": "application/json"}

    data = {
        "input": {"text": text},
        "voice": {"languageCode": "en-US", "name": "en-US-Journey-F"},
        "audioConfig": {"audioEncoding": "MP3"},
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        audio_content = response.json()["audioContent"]
        path = Path("output.mp3")
        with open(path, "wb") as audio_file:
            audio_file.write(base64.b64decode(audio_content))
        return path
