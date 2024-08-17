from abc import ABC, abstractmethod
from typing import List

class LLMProvider(ABC):
    
    @abstractmethod
    def generate_text(self, model:str, messages: List[str], top_p: float, tempreture: float) -> str:
        pass
    
    @abstractmethod
    def generate_text_async(self, model:str, messages: List[str], top_p: float, tempreture: float):
        pass
    
    @abstractmethod
    def list_models(self) -> List[str]:
        pass
    