"""brew install ffmpeg"""

import base64
import json
import os
from io import BytesIO

import requests
from pydub import AudioSegment
from pydub.playback import play


def get_audio_from_text(text, save_to_file=None):
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

        if save_to_file:
            with open(save_to_file, "wb") as out_file:
                out_file.write(audio_data)
            print(f"Audio saved to {save_to_file}")

    else:
        raise Exception(f"Error in text-to-speech request: {response.text}")


if __name__ == "__main__":
    get_audio_from_text(
        "Hello, this is a test of the text to speech system.", save_to_file="data/test.mp3"
    )
