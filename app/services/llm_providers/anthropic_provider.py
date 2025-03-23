import anthropic
from typing import List, Dict, Any, Optional, AsyncGenerator
from app.services.llm_providers.base_provider import BaseLLMProvider

class AnthropicProvider(BaseLLMProvider):
    """Anthropic LLM provider implementation"""
    
    def __init__(self, api_key: str, model: str = None):
        """Initialize the Anthropic provider
        
        Args:
            api_key: Anthropic API key
            model: Model to use (defaults to claude-3-haiku-20240307 if None)
        """
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = model or self.default_model
    
    async def generate_completion(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate a completion using Anthropic
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The generated completion
        """
        try:
            response = await self.client.messages.create(
                model=kwargs.get('model', self.model),
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 4000),
                top_p=kwargs.get('top_p', 1.0)
            )
            return response.content[0].text
        except Exception as e:
            # Log the error and return a friendly message
            print(f"Anthropic API error: {str(e)}")
            return f"I apologize, but I encountered an error while processing your request. Error: {str(e)}"
    
    async def generate_completion_stream(self, system_prompt: str, user_prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Generate a streaming completion using Anthropic
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            An async generator yielding completion chunks
        """
        try:
            stream = await self.client.messages.create(
                model=kwargs.get('model', self.model),
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 4000),
                top_p=kwargs.get('top_p', 1.0),
                stream=True
            )
            
            async for chunk in stream:
                if chunk.type == "content_block_delta" and chunk.delta.text:
                    yield chunk.delta.text
        except Exception as e:
            # Log the error and yield a friendly message
            print(f"Anthropic API error: {str(e)}")
            yield f"I apologize, but I encountered an error while processing your request. Error: {str(e)}"
    
    async def generate_multimodal_completion(self, system_prompt: str, user_prompt: str, image_urls: List[str], **kwargs) -> str:
        """Generate a completion using Anthropic with image inputs
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            image_urls: List of image URLs to include in the prompt
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The generated completion
        """
        try:
            # Create a list of content items for the user message
            content = []
            
            # Add the text prompt
            content.append({"type": "text", "text": user_prompt})
            
            # Add image URLs to the content
            for image_url in image_urls:
                content.append({
                    "type": "image",
                    "source": {"type": "url", "url": image_url}
                })
            
            # Use a vision-capable model
            vision_model = kwargs.get('vision_model', 'claude-3-opus-20240229')
            
            response = await self.client.messages.create(
                model=vision_model,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": content}
                ],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 4000),
                top_p=kwargs.get('top_p', 1.0)
            )
            return response.content[0].text
        except Exception as e:
            # Log the error and return a friendly message
            print(f"Anthropic API error: {str(e)}")
            return f"I apologize, but I encountered an error while processing your request. Error: {str(e)}"
    
    @property
    def provider_name(self) -> str:
        """Get the name of the provider"""
        return "anthropic"
    
    @property
    def default_model(self) -> str:
        """Get the default model for this provider"""
        return "claude-3-haiku-20240307"
    
    @property
    def available_models(self) -> List[str]:
        """Get the list of available models for this provider"""
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
