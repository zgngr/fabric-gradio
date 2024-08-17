from ai.llm.llmprovider import LLMProvider


class LLMProviderFactory:
    
    def __init__(self):
        self.providers = {}

    def register_provider(self, key: str, provider: LLMProvider):
        self.providers[key] = provider

    def get_provider(self, key: str) -> LLMProvider:
        provider = self.providers.get(key)
        if not provider:
            raise ValueError(f"Provider not found for key: {key}")
        return provider
    
    def get_registered_providers(self):
        return self.providers.keys()