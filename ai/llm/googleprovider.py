from typing import List
from ai.llm.llmprovider import LLMProvider
import google.generativeai as genai

class GoogleProvider(LLMProvider):
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        
    def generate_text(self, model: str, messages: List[str], top_p: float, tempreture: float) -> str:
        # Gemini doesn't use the standard OpenAI message format directly in the same way for generate_content mostly.
        # But we need to adapt the messages. The current app sends a list of dicts: {"role": "...", "content": "..."}
        # based on app.py: 
        # messages = [
        #   {"role": "system", "content": system_prompt},
        #   {"role": "user", "content": user_prompt + "\n" + input}
        # ]
        # Gemini Pro supports system instructions in a specific way or just as part of the prompt.
        # For simplicity and compatibility with the current simple usage:
        
        # Flatten messages to a single prompt if needed or use chat history.
        # However, for a single turn "run_prompt" (which app.py seems to do), we can just construct the prompt.
        # app.py's run_prompt just yields the response.
        
        # Let's try to map it to valid Gemini content.
        # System instructions can be set during model creation, but here we select model dynamically.
        # Ideally we should use model.generate_content(prompt)
        
        full_prompt = ""
        for msg in messages:
            full_prompt += f"{msg['role']}: {msg['content']}\n"
            
        generation_config = genai.types.GenerationConfig(
            temperature=tempreture,
            top_p=top_p
        )
        
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(full_prompt, generation_config=generation_config)
        return response.text
    
    async def generate_text_async(self, model: str, messages: List[str], top_p: float, tempreture: float):
        # Construct prompt from messages
        full_prompt = ""
        for msg in messages:
            full_prompt += f"{msg['role']}: {msg['content']}\n"

        generation_config = genai.types.GenerationConfig(
            temperature=tempreture,
            top_p=top_p
        )
        
        model_instance = genai.GenerativeModel(model)
        response = await model_instance.generate_content_async(full_prompt, generation_config=generation_config, stream=True)
        
        async for chunk in response:
            yield chunk.text

    def list_models(self) -> List[str]:
        # List models that support generateContent
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # filter for gemini models mostly
                if 'gemini' in m.name:
                     models.append(m.name.replace("models/", ""))
        models.sort()
        return models
