from abc import ABC, abstractmethod
import os
import boto3
import json
from dotenv import load_dotenv 
import openai

class LLM(ABC):
    @abstractmethod
    def query_model(self, prompt: str) -> str:
        pass

class BedrockLLM(LLM):
    def __init__(self):
        load_dotenv()
        self.session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_ACCESS_SECRET_KEY'),
        )
        self.bedrock = self.session.client(service_name='bedrock-runtime', region_name='us-west-2')
        self.base_prompt_pre = open("base_prompt_pre.txt", "r").read()
        self.base_prompt_post = open("base_prompt_post.txt", "r").read()

    def query_model(self, prompt: str) -> str:
        body = json.dumps({
            "prompt": "<s>[INST] " + self.base_prompt_pre + "" + self.base_prompt_post + prompt + " [/INST]",
            "max_tokens": 512,
            "temperature": 1,
        })

        modelId = "mistral.mixtral-8x7b-instruct-v0:1"

        accept = "application/json"
        contentType = "application/json"

        response = self.bedrock.invoke_model(
            modelId=modelId,
            body=body,
            accept=accept,
            contentType=contentType
        )

        text = json.loads(response.get('body').read())['outputs'][0]['text']
        return text

class GPTLLM(LLM):
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.model_name = "gpt-3.5-turbo"
        self.base_prompt_pre = open("base_prompt_pre.txt", "r").read()
        self.base_prompt_post = open("base_prompt_post.txt", "r").read()
        self.messages = []

    def query_model(self, prompt: str) -> str:
        request_messages = [
            {"role": "system", "content": self.base_prompt_pre + "" + self.base_prompt_post}
        ]
        request_messages.extend(self.messages[-20:])
        request_messages.append({"role": "user", "content": prompt})
        print('request_messages', request_messages)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=request_messages,
            temperature=1,
            top_p=1
        )

        generated_response = response.choices[0].message.content.strip()

        # really trash code
        generated_response = generated_response.replace("ah,", "")
        generated_response = generated_response.replace("Ah,", "")
        generated_response = generated_response.replace("ah ", "")
        generated_response = generated_response.replace("Ah ", "")

        self.messages.append({"role": "user", "content": prompt})
        self.messages.append({"role": "assistant", "content": generated_response})

        return generated_response
