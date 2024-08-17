from ai.stt.sttprovider import STTProvider


class STTProviderFactory:
    
    def __init__(self):
        self.providers = {}

    def register_provider(self, key: str, provider: STTProvider):
        self.providers[key] = provider

    def get_provider(self, key: str) -> STTProvider:
        provider = self.providers.get(key)
        if not provider:
            raise ValueError(f"Provider not found for key: {key}")
        return provider