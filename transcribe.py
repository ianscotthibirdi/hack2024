import io
import os

import pyaudio
import simpleaudio as sa
from google.cloud import speech_v1 as speech
from pydub import AudioSegment


def get_text_from_audio(audio_in):
    api_key = os.getenv("GOOGLE_API_KEY")

    client = speech.SpeechClient(client_options={"api_key": api_key})

    audio = speech.RecognitionAudio(content=audio_in)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return transcripts


def capture_audio_to_bytes(duration=5, sample_rate=16000, channels=1):
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=1024,
    )

    print("Recording...")
    frames = []

    # Record audio for the given duration
    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert to audio segment
    audio_segment = AudioSegment(
        data=b"".join(frames),
        sample_width=p.get_sample_size(pyaudio.paInt16),
        frame_rate=sample_rate,
        channels=channels,
    )

    # Export to raw audio in memory
    raw_audio_io = io.BytesIO()
    audio_segment.export(raw_audio_io, format="raw")
    raw_audio_io.seek(0)

    return raw_audio_io.read()


def play_audio_bytes(audio_bytes, sample_rate=16000, channels=1):
    # Convert bytes to an audio segment
    audio_segment = AudioSegment(
        data=audio_bytes,
        sample_width=2,  # Assuming 16-bit audio (2 bytes per sample)
        frame_rate=sample_rate,
        channels=channels,
    )

    # Export the audio segment to a WAV format in memory
    wav_io = io.BytesIO()
    audio_segment.export(wav_io, format="wav")
    wav_io.seek(0)

    # Play the audio
    play_obj = sa.WaveObject(
        wav_io.read(), num_channels=channels, bytes_per_sample=2, sample_rate=sample_rate
    ).play()
    play_obj.wait_done()


def audio_to_text(duration=5, play_audio=False):
    audio_bytes = capture_audio_to_bytes(duration=duration)
    transcripts = get_text_from_audio(audio_bytes)
    if play_audio:
        play_audio_bytes(audio_bytes)
    return transcripts


if __name__ == "__main__":
    transcripts = audio_to_text(duration=5, play_audio=True)
    print(transcripts)
