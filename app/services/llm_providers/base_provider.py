from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def generate_completion(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate a completion using the LLM provider
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            **kwargs: Additional provider-specific parameters
            
        Returns:
            The generated completion
        """
        pass
    
    @abstractmethod
    async def generate_completion_stream(self, system_prompt: str, user_prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Generate a streaming completion using the LLM provider
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            **kwargs: Additional provider-specific parameters
            
        Returns:
            An async generator yielding completion chunks
        """
        pass
    
    @abstractmethod
    async def generate_multimodal_completion(self, system_prompt: str, user_prompt: str, image_urls: List[str], **kwargs) -> str:
        """Generate a completion using the LLM provider with image inputs
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            image_urls: List of image URLs to include in the prompt
            **kwargs: Additional provider-specific parameters
            
        Returns:
            The generated completion
        """
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get the name of the provider"""
        pass
    
    @property
    @abstractmethod
    def default_model(self) -> str:
        """Get the default model for this provider"""
        pass
    
    @property
    @abstractmethod
    def available_models(self) -> List[str]:
        """Get the list of available models for this provider"""
        pass
