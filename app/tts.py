import os
import datetime
import re
import azure.cognitiveservices.speech as speechsdk 
from dotenv import load_dotenv 

class TTS:
    def __init__(self):
        load_dotenv()
        self.speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv("AZURE_SPEECH_SERVICE_KEY"), 
            region=os.getenv("AZURE_SPEECH_SERVICE_REGION")
        )
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        self.voice_name='en-US-AshleyNeural'

    def speak(self, text: str):

        emotion_map = {
            "angry": "angry",
            "cheerful": "cheerful",
            "excited": "excited",
            "friendly": "friendly",
            "hopeful": "hopeful",
            "sad": "sad",
            "shouting": "shouting",
            "terrified": "terrified",
            "unfriendly": "unfriendly",
            "whispering": "whispering"
        }

        for emotion, style in emotion_map.items():
            text = text.replace(f"<{emotion}>", f'<mstts:express-as style="{style}">')
            text = text.replace(f"</{emotion}>", "</mstts:express-as>")

        print('test', text)

        ssml_string = f"""<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="en-US-SaraNeural"><prosody rate="+10.00%" pitch="+20.00%">{text}</prosody></voice></speak>"""

        print('ssml_string', ssml_string)

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
        
        speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        print(speech_synthesis_result.cancellation_details.error_details if speech_synthesis_result.cancellation_details else "Speech synthesized successfully.")
