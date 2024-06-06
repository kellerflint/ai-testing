import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryBufferMemory
from langchain.prompts.prompt import PromptTemplate

load_dotenv()

class GroqLLM:

    def __init__(self):
        llm = ChatGroq(temperature=1, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")
        
        template = """
            The following is a friendly conversation between a human and an AI. 
            Keep the responses short. 1-2 sentences is best.
                                  
            Current conversation:
            {history}
            Human: {input}
            AI:
        """
        prompt = PromptTemplate(input_variables=["history", "input"], template=template)

        memory = ConversationBufferMemory()
        #memory = ConversationBufferWindowMemory(k=3)
        #memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)
        
        self.conversation = ConversationChain(
            prompt = prompt,
            llm = llm,
            memory = memory,
            verbose = True
        )

    def query_model(self, prompt: str) -> str:
        return self.conversation.predict(input=prompt)
    
