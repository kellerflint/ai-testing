import boto3
import json
from dotenv import load_dotenv, dotenv_values 

class LLM:
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id='',
            aws_secret_access_key='',
        )
        self.bedrock = self.session.client(service_name='bedrock-runtime', region_name='us-west-2')
        self.base_prompt = open("base_prompt.txt", "r").read()

    def query_model(self, prompt: str) -> str:
        body = json.dumps({
            "prompt": "<s>[INST] " + self.base_prompt + prompt + " [/INST]",
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
        print("Response from LLM:", text)
        return text