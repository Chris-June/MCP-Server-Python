import base64
import os
import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator, Tuple
from app.config import settings
from app.models.multimodal import ContentType, MediaContent, MultiModalContent
from app.services.llm_providers.provider_factory import LLMProviderFactory
from app.services.llm_providers.base_provider import BaseLLMProvider

class MultiModalProcessor:
    """Service for processing multi-modal content using multiple LLM providers"""
    
    def __init__(self):
        """Initialize the multi-modal processor"""
        # Initialize providers based on available API keys
        self.providers = {}
        
        # Initialize OpenAI provider if API key is available
        if settings.openai_api_key:
            self.providers["openai"] = LLMProviderFactory.create_provider(
                "openai", 
                settings.openai_api_key, 
                settings.openai_model
            )
        
        # Initialize Anthropic provider if API key is available
        if settings.anthropic_api_key:
            self.providers["anthropic"] = LLMProviderFactory.create_provider(
                "anthropic", 
                settings.anthropic_api_key, 
                settings.anthropic_model
            )
        
        # Initialize Gemini provider if API key is available
        if settings.gemini_api_key:
            self.providers["gemini"] = LLMProviderFactory.create_provider(
                "gemini", 
                settings.gemini_api_key, 
                settings.gemini_model
            )
        
        # Ensure we have at least one provider available
        if not self.providers:
            raise ValueError("No LLM providers available. Please configure at least one provider API key.")
        
        # Use the default provider if available, otherwise use the first available provider
        self.default_provider_name = settings.default_provider
        if self.default_provider_name in self.providers:
            self.default_provider = self.providers[self.default_provider_name]
        else:
            self.default_provider_name = next(iter(self.providers.keys()))
            self.default_provider = self.providers[self.default_provider_name]
    
    async def process_multimodal_content(self, system_prompt: str, content: MultiModalContent, provider_name: Optional[str] = None) -> str:
        """Process multi-modal content and generate a response
        
        Args:
            system_prompt: The system prompt to use
            content: The multi-modal content to process
            provider_name: Optional provider name to use (defaults to the default provider)
            
        Returns:
            The generated response
        """
        try:
            # Get the appropriate provider
            provider = self.get_provider(provider_name)
            
            # Process text and media content
            user_message = self._prepare_user_message(content)
            
            # Check if the content contains media
            if self._contains_media(content):
                # For multi-modal content, we need to use a provider that supports it
                if provider.provider_name == "openai":
                    # Use OpenAI's vision capabilities
                    return await provider.generate_multimodal_completion(
                        system_prompt,
                        user_message["content"],
                        [media["image_url"] for media in self._extract_media_urls(content)]
                    )
                elif provider.provider_name == "anthropic":
                    # Use Anthropic's vision capabilities
                    return await provider.generate_multimodal_completion(
                        system_prompt,
                        user_message["content"],
                        [media["image_url"] for media in self._extract_media_urls(content)]
                    )
                elif provider.provider_name == "gemini":
                    # Use Gemini's vision capabilities
                    return await provider.generate_multimodal_completion(
                        system_prompt,
                        user_message["content"],
                        [media["image_url"] for media in self._extract_media_urls(content)]
                    )
                else:
                    # Fall back to OpenAI if the provider doesn't support multi-modal
                    fallback_provider = self.providers.get("openai")
                    if not fallback_provider:
                        raise ValueError("No provider with multi-modal capabilities is available")
                    
                    return await fallback_provider.generate_multimodal_completion(
                        system_prompt,
                        user_message["content"],
                        [media["image_url"] for media in self._extract_media_urls(content)]
                    )
            else:
                # For text-only content, use the standard completion method
                return await provider.generate_completion(system_prompt, user_message["content"])
        except Exception as e:
            # In a production environment, add proper error handling and logging
            print(f"Error processing multi-modal content: {e}")
            return f"I'm sorry, I encountered an error processing the multi-modal content: {str(e)}"
    
    async def process_multimodal_content_stream(self, system_prompt: str, content: MultiModalContent, provider_name: Optional[str] = None) -> AsyncGenerator[str, None]:
        """Process multi-modal content and generate a streaming response
        
        Args:
            system_prompt: The system prompt to use
            content: The multi-modal content to process
            provider_name: Optional provider name to use (defaults to the default provider)
            
        Yields:
            Chunks of the generated response
        """
        try:
            # Get the appropriate provider
            provider = self.get_provider(provider_name)
            
            # Process text and media content
            user_message = self._prepare_user_message(content)
            
            # Check if the content contains media
            if self._contains_media(content):
                # Currently, streaming with multi-modal content is not well supported by all providers
                # So we'll generate the full response and yield it as a single chunk
                full_response = await self.process_multimodal_content(system_prompt, content, provider_name)
                yield full_response
            else:
                # For text-only content, use the standard streaming method
                async for chunk in provider.generate_completion_stream(system_prompt, user_message["content"]):
                    yield chunk
        except Exception as e:
            # In a production environment, add proper error handling and logging
            print(f"Error processing multi-modal content stream: {e}")
            yield f"I'm sorry, I encountered an error processing the multi-modal content: {str(e)}"
    
    def _prepare_user_message(self, content: MultiModalContent) -> Dict[str, Any]:
        """Prepare the user message for the API call
        
        Args:
            content: The multi-modal content
            
        Returns:
            The formatted user message
        """
        message = {"role": "user"}
        
        # If there's no media, just return the text content
        if not self._contains_media(content):
            message["content"] = content.text or ""
            return message
        
        # For multi-modal content, format as a list of content parts
        message_content = []
        
        # Add text if available
        if content.text:
            message_content.append({"type": "text", "text": content.text})
        
        # Add media content
        if content.media:
            for media in content.media:
                if media.type == ContentType.IMAGE:
                    # Handle image content
                    image_content = {"type": "image"}
                    
                    # Use URL if provided, otherwise use base64 data
                    if media.url:
                        image_content["image_url"] = {"url": str(media.url)}
                    elif media.base64_data:
                        # Ensure the base64 data has the correct format
                        if not media.base64_data.startswith("data:"):
                            mime_type = media.mime_type or "image/jpeg"
                            image_content["image_url"] = {
                                "url": f"data:{mime_type};base64,{media.base64_data}"
                            }
                        else:
                            image_content["image_url"] = {"url": media.base64_data}
                    
                    # Add detail level if specified in metadata
                    if media.metadata and "detail" in media.metadata:
                        image_content["image_url"]["detail"] = media.metadata["detail"]
                    
                    message_content.append(image_content)
                
                # Future: Add support for other media types as OpenAI adds them
        
        message["content"] = message_content
        return message
    
    def _contains_media(self, content: MultiModalContent) -> bool:
        """Check if the content contains media
        
        Args:
            content: The multi-modal content
            
        Returns:
            True if the content contains media, False otherwise
        """
        return content.media is not None and len(content.media) > 0
    
    def get_provider(self, provider_name: Optional[str] = None) -> BaseLLMProvider:
        """Get a provider by name
        
        Args:
            provider_name: Name of the provider to get (defaults to the default provider)
            
        Returns:
            The requested provider
            
        Raises:
            ValueError: If the provider is not available
        """
        # Use the default provider if none specified
        if not provider_name:
            return self.default_provider
        
        # Get the requested provider
        provider = self.providers.get(provider_name.lower())
        if not provider:
            available = ", ".join(self.providers.keys())
            raise ValueError(f"Provider '{provider_name}' not available. Available providers: {available}")
        
        return provider
    
    def get_available_providers(self) -> Dict[str, str]:
        """Get all available providers
        
        Returns:
            Dictionary of provider names to model names
        """
        return {name: provider.default_model for name, provider in self.providers.items()}
    
    async def analyze_image(self, image_data: str, prompt: str, provider_name: Optional[str] = None) -> str:
        """Analyze an image using the vision model
        
        Args:
            image_data: The image data (URL or base64)
            prompt: The prompt to use for analysis
            provider_name: Optional provider name to use (defaults to the default provider)
            
        Returns:
            The analysis result
        """
        try:
            # Get the appropriate provider
            provider = self.get_provider(provider_name)
            
            # Prepare the image URL (either a web URL or base64 data)
            image_url = image_data
            if not image_data.startswith("http") and not image_data.startswith("data:"):
                # Assume it's base64 data without the prefix
                image_url = f"data:image/jpeg;base64,{image_data}"
            
            # Create a simple multimodal content with the image
            media_urls = [{
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            }]
            
            # Use the provider's multimodal completion method
            if provider.provider_name == "openai" or provider.provider_name == "anthropic" or provider.provider_name == "gemini":
                return await provider.generate_multimodal_completion("You are a helpful assistant.", prompt, media_urls)
            else:
                # Fall back to OpenAI if the provider doesn't support multi-modal
                fallback_provider = self.providers.get("openai")
                if not fallback_provider:
                    raise ValueError("No provider with multi-modal capabilities is available")
                
                return await fallback_provider.generate_multimodal_completion("You are a helpful assistant.", prompt, media_urls)
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return f"I'm sorry, I encountered an error analyzing the image: {str(e)}"
