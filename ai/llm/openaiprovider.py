from typing import List
from ai.llm.llmprovider import LLMProvider
from openai import OpenAI, AsyncOpenAI

class OpenAIProvider(LLMProvider):
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)
        
    def generate_text(self, model: str, messages: List[str], top_p: float, tempreture: float) -> str:
        response = self.client.chat.completions.create(model=model, messages=messages, top_p=top_p, temperature=tempreture)
        return response.choices[0].message.content
    
    async def generate_text_async(self, model: str, messages: List[str], top_p: float, tempreture: float):
        stream = await self.async_client.chat.completions.create(
            model=model, 
            messages=messages, 
            top_p=top_p, 
            temperature=tempreture, 
            stream=True
        )
        
        async for chunk in stream:
            yield chunk.choices[0].delta.content or ""
                
    def list_models(self) -> List[str]:
        gptlist = []
        models = [model.id.strip() for model in self.client.models.list().data]
        if "/" in models[0] or "\\" in models[0]:
            gptlist = [
                item[item.rfind("/") + 1 :]
                if "/" in item
                else item[item.rfind("\\") + 1 :]
                for item in models
            ]
        else:
            gptlist = [
                item.strip() for item in models if item.startswith("gpt")
            ]
        gptlist.sort()
        
        return gptlist
  
    