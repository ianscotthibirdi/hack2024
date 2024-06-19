import os

from google.cloud import speech_v1 as speech

from speak import get_audio_from_text


def get_text_from_audio(audio_in):
    api_key = os.getenv("GOOGLE_API_KEY")

    client = speech.SpeechClient(client_options={"api_key": api_key})

    audio = speech.RecognitionAudio(content=audio_in)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return transcripts


if __name__ == "__main__":
    audio_file_path = "data/test.mp3"
    get_audio_from_text(
        "Hello, this is a test of the text to speech system.", save_to_file=audio_file_path
    )
    with open(audio_file_path, "rb") as audio_file:
        audio = audio_file.read()

    print(get_text_from_audio(audio))
