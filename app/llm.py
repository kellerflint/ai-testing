import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class GroqLLM:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.message_history = []

    def query_model(self, prompt: str) -> str:
        self.message_history.append({
            "role": "user",
            "content": prompt,
        })

        chat_completion = self.client.chat.completions.create(
            messages=self.message_history,
            model="llama3-8b-8192",
        )

        response = chat_completion.choices[0].message.content
        print("Response from LLM:", response)
        self.message_history.append({
            "role": "assistant",
            "content": response,
        })

        return response

