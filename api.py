"""brew install ffmpeg"""

import base64
import json
import os
from io import BytesIO

import requests
from pydub import AudioSegment
from pydub.playback import play


def get_audio_from_text(text):
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
        audio_data = base64.b64decode(audio_content)

        audio = AudioSegment.from_file(BytesIO(audio_data), format="mp3")
        play(audio)
    else:
        raise Exception(f"Error in text-to-speech request: {response.text}")


if __name__ == "__main__":
    get_audio_from_text("Hello, this is a test of the text to speech system.")
