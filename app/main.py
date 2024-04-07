from llm import LLM
from tts import TTS


llm_model = LLM()
response = llm_model.query_model("Testing the LLM + TTS engine")

tts_engine = TTS()
tts_engine.speak(response)
