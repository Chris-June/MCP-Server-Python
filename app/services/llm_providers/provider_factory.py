from typing import Dict, Optional, Type
from app.services.llm_providers.base_provider import BaseLLMProvider
from app.services.llm_providers.openai_provider import OpenAIProvider
from app.services.llm_providers.anthropic_provider import AnthropicProvider
from app.services.llm_providers.gemini_provider import GeminiProvider

class LLMProviderFactory:
    """Factory for creating LLM provider instances"""
    
    # Registry of provider classes
    _providers: Dict[str, Type[BaseLLMProvider]] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider
    }
    
    @classmethod
    def create_provider(cls, provider_name: str, api_key: str, model: Optional[str] = None) -> BaseLLMProvider:
        """Create a provider instance
        
        Args:
            provider_name: Name of the provider to create
            api_key: API key for the provider
            model: Optional model name to use
            
        Returns:
            An instance of the requested provider
            
        Raises:
            ValueError: If the provider is not supported
        """
        provider_class = cls._providers.get(provider_name.lower())
        if not provider_class:
            supported = ", ".join(cls._providers.keys())
            raise ValueError(f"Unsupported provider: {provider_name}. Supported providers: {supported}")
        
        return provider_class(api_key=api_key, model=model)
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[BaseLLMProvider]) -> None:
        """Register a new provider class
        
        Args:
            name: Name of the provider
            provider_class: Provider class to register
        """
        cls._providers[name.lower()] = provider_class
    
    @classmethod
    def get_available_providers(cls) -> Dict[str, Type[BaseLLMProvider]]:
        """Get all available providers
        
        Returns:
            Dictionary of provider names to provider classes
        """
        return cls._providers.copy()
