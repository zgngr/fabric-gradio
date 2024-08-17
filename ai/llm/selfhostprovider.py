from typing import List
from ai.llm.llmprovider import LLMProvider
import ollama

class SelfHostProvider(LLMProvider):
    
    def __init__(self, url: str):
        self.client = ollama.Client(host=url)
        self.client_async = ollama.AsyncClient(host=url)
        
    def generate_text(self, model: str, messages: List[str], top_p: float, tempreture: float) -> str:
        prompt = "\n".join([f"{message['role'].upper()}: {message['content']}" for message in messages])
        response = self.client.generate(model=model, prompt=prompt, stream=False)
        return response['response']
    
    async def generate_text_async(self, model: str, messages: List[str], top_p: float, tempreture: float):
        prompt = "\n".join([f"{message['role'].upper()}: {message['content']}" for message in messages])
        async for response in await self.client_async.generate(model=model, prompt=prompt, stream=True):
            yield response['response']
    
    def list_models(self) -> List[str]:
        models = []
        for model in self.client.list()["models"]:
            models.append(model["name"])
     
        return models
  
    