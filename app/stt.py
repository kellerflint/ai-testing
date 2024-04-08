import whisper

class STT:
    def __init__(self):
        self.model = whisper.load_model("base")

    def transcribe(self, audio_file: str):
        result = self.model.transcribe(audio_file)
        return result["text"]        
