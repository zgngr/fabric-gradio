from ai.stt.sttprovider import STTProvider
from openai import OpenAI

class OpenAIProvider(STTProvider):
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        
    def transcribe(self, model:str, audio_file_path: str) -> str:
        audio = open(audio_file_path, "rb")
        transcript = self.client.audio.transcriptions.create(model=model, file=audio, response_format="text")
        return transcript