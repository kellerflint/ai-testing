import os
import datetime
from dotenv import load_dotenv

from llm import GroqLLM
from tts import TTS
from stt import STT
from speechDetector import SpeechDetector

load_dotenv()

AUDIO_DEVICE_INDEX = 2

stt_engine = STT()
llm_model = GroqLLM()
tts_engine = TTS()
speech_detector = SpeechDetector(os.getenv('AUDIO_OUT_PATH'), AUDIO_DEVICE_INDEX)

def main():
    try:
        while True:
            speech_detector.record_audio()
            transcription = stt_engine.transcribe(os.getenv('AUDIO_OUT_PATH'))
            print('Transcription completed at', datetime.datetime.now(), 'Text:', transcription)

            response = llm_model.query_model(transcription)
            print('LLM response received at', datetime.datetime.now(), 'Response:', response)

            tts_engine.speak(response)
    except KeyboardInterrupt:
        print("Stopping...")

    speech_detector.terminate()

if __name__ == "__main__":
    main()