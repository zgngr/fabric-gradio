from abc import ABC, abstractmethod

class STTProvider(ABC):
    
    @abstractmethod
    def transcribe(self, model:str, audio_file_path: str) -> str:
        pass