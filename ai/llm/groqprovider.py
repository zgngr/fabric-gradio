from typing import List
from ai.llm.llmprovider import LLMProvider
from groq import Groq, AsyncGroq

class GroqProvider(LLMProvider):
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.async_client = AsyncGroq(api_key=api_key)
        
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
        models = [model.id.strip() for model in self.client.models.list().data]
        return [model for model in models if "whisper" not in model]
