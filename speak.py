"""brew install ffmpeg"""

import base64
import html
import json
import os
from io import BytesIO

import requests
from pydub import AudioSegment
from pydub.playback import play


def get_audio_from_text(text, save_to_file=None):
    ssml = text_to_ssml(text)
    api_key = os.getenv("GOOGLE_API_KEY")

    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"

    headers = {"Content-Type": "application/json"}

    data = {
        "input": {"ssml": ssml},
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


def text_to_ssml(input_text):
    # Generates SSML text from plaintext.
    # Given an input filename, this function converts the contents of the text
    # file into a string of formatted SSML text. This function formats the SSML
    # string so that, when synthesized, the synthetic audio will pause for two
    # seconds between each line of the text file. This function also handles
    # special text characters which might interfere with SSML commands.
    #
    # Args:
    # inputfile: string name of plaintext file
    #
    # Returns:
    # A string of SSML text based on plaintext input

    # Replace special characters with HTML Ampersand Character Codes
    # These Codes prevent the API from confusing text with
    # SSML commands
    # For example, '<' --> '&lt;' and '&' --> '&amp;'

    escaped_lines = html.escape(input_text)

    # Convert plaintext to SSML
    # Wait two seconds between each address
    ssml = "<speak>{}</speak>".format(escaped_lines.replace("\n", '\n<break time="2s"/>'))

    # Return the concatenated string of ssml script
    return ssml


def list_en_us_female_voices():
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://texttospeech.googleapis.com/v1/voices?key={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        voices = response.json()["voices"]
        for voice in voices:
            if voice["languageCodes"][0] == "en-US" and voice["ssmlGender"] == "FEMALE":
                print(f"Name: {voice['name']}, SSML Support: {voice.get('ssmlGender', 'Unknown')}")
    else:
        raise Exception(f"Error in fetching voices: {response.text}")


if __name__ == "__main__":
    # get_audio_from_text(
    #     "Hello, this is a test of the text to speech system.", save_to_file="data/test.mp3"
    # )
    list_en_us_female_voices()
