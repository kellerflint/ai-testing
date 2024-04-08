import os
import datetime
import pyaudio
import webrtcvad
import wave
from dotenv import load_dotenv

from llm import LLM, BedrockLLM, GPTLLM
from tts import TTS
from stt import STT

load_dotenv()

stt_engine = STT()
llm_model: LLM = GPTLLM()
tts_engine = TTS()

CHUNK_SIZE = 480
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_DURATION = 1

def record_audio(p, stream, vad):
    print("Waiting for speech...")

    frames = []
    silence_frames = 0
    speech_started = False

    while True:
        data = stream.read(CHUNK_SIZE)

        if not speech_started:
            if vad.is_speech(data, RATE):
                speech_started = True
                print("Recording started.")
            else:
                continue

        frames.append(data)

        if vad.is_speech(data, RATE):
            silence_frames = 0
        else:
            silence_frames += CHUNK_SIZE

        if silence_frames >= RATE * SILENCE_DURATION:
            break

    print("Recording finished at ", datetime.datetime.now())

    wf = wave.open(os.getenv('AUDIO_OUT_PATH'), "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

    print(f"Audio saved as {os.getenv('AUDIO_OUT_PATH')}")

    transcription = stt_engine.transcribe(os.getenv('AUDIO_OUT_PATH'))
    print('Transcription completed at', datetime.datetime.now(), 'Text:', transcription)

    response = llm_model.query_model(transcription)
    print('LLM response received at', datetime.datetime.now(), 'Response:', response)

    tts_engine.speak(response)

def main():
    p = pyaudio.PyAudio()
    vad = webrtcvad.Vad()
    vad.set_mode(3)  # Set VAD aggressiveness (0-3)

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE, input_device_index=2)

    try:
        while True:
            record_audio(p, stream, vad)
    except KeyboardInterrupt:
        print("Stopping...")

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    main()