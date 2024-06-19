import os

from google.cloud import speech_v1 as speech

from speak import get_audio_from_text

api_key = os.getenv("GOOGLE_API_KEY")


client = speech.SpeechClient(client_options={"api_key": api_key})


audio_file_path = "data/test.mp3"

# Load the audio into memory
with open(audio_file_path, "rb") as audio_file:
    content = audio_file.read()

# Configure the request
audio = speech.RecognitionAudio(content=content)
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.MP3,
    sample_rate_hertz=16000,
    language_code="en-US",
)

# Make the request to the API
response = client.recognize(config=config, audio=audio)

# Print the results
for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))
