import azure.cognitiveservices.speech as speechsdk 
from dotenv import load_dotenv, dotenv_values 

class TTS:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(subscription="", region="")
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        self.voice_name='en-US-AshleyNeural'

    def speak(self, text: str):
        ssml_string = f"""
            <speak xmlns="http://www.w3.org/2001/10/synthesis" 
                xmlns:mstts="http://www.w3.org/2001/mstts" 
                xmlns:emo="http://www.w3.org/2009/10/emotionml" 
                version="1.0" 
                xml:lang="en-US">
                <voice name="en-US-SaraNeural">
                    <prosody rate="+10.00%" pitch="+20.00%">{text}</prosody>
                </voice>
            </speak>
        """

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

        speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_string).get()
