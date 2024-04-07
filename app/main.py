from llm import LLM
from tts import TTS


llm_model = LLM()
#response = llm_model.query_model("Testing the LLM + TTS engine")

tts_engine = TTS()
#tts_engine.speak(response)


import pyaudio
import webrtcvad

SAMPLE_RATE = 16000
FRAME_DURATION = 30  # Duration of each frame in ms
PADDING_DURATION = 300  # Duration of padding in ms

vad = webrtcvad.Vad()
vad.set_mode(3)  # Set the VAD aggressiveness (0-3)

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=int(SAMPLE_RATE * FRAME_DURATION / 1000))

def is_speech(frame):
    return vad.is_speech(frame, SAMPLE_RATE)

def main():
    print("Listening for speech...")
    while True:
        frames = []
        while True:
            frame = stream.read(int(SAMPLE_RATE * FRAME_DURATION / 1000))
            frames.append(frame)
            if len(frames) > PADDING_DURATION / FRAME_DURATION:
                frames.pop(0)
            if is_speech(frame):
                break

        speech_frames = []
        for frame in frames:
            if is_speech(frame):
                speech_frames.append(frame)
            else:
                break

        while True:
            frame = stream.read(int(SAMPLE_RATE * FRAME_DURATION / 1000))
            if is_speech(frame):
                speech_frames.append(frame)
            else:
                if len(speech_frames) > PADDING_DURATION / FRAME_DURATION:
                    print("Speech detected!")
                    # Process the speech frames here
                break

if __name__ == "__main__":
    main()