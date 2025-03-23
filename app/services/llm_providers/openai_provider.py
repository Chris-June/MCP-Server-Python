from openai import AsyncOpenAI
from typing import List, Dict, Any, Optional, AsyncGenerator
from app.services.llm_providers.base_provider import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider implementation"""
    
    def __init__(self, api_key: str, model: str = None):
        """Initialize the OpenAI provider
        
        Args:
            api_key: OpenAI API key
            model: Model to use (defaults to gpt-4o-mini if None)
        """
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model or self.default_model
    
    async def generate_completion(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate a completion using OpenAI
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The generated completion
        """
        try:
            response = await self.client.chat.completions.create(
                model=kwargs.get('model', self.model),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 4000),
                top_p=kwargs.get('top_p', 1.0),
                frequency_penalty=kwargs.get('frequency_penalty', 0.0),
                presence_penalty=kwargs.get('presence_penalty', 0.0)
            )
            return response.choices[0].message.content
        except Exception as e:
            # Log the error and return a friendly message
            print(f"OpenAI API error: {str(e)}")
            return f"I apologize, but I encountered an error while processing your request. Error: {str(e)}"
    
    async def generate_completion_stream(self, system_prompt: str, user_prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Generate a streaming completion using OpenAI
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            An async generator yielding completion chunks
        """
        try:
            stream = await self.client.chat.completions.create(
                model=kwargs.get('model', self.model),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 4000),
                top_p=kwargs.get('top_p', 1.0),
                frequency_penalty=kwargs.get('frequency_penalty', 0.0),
                presence_penalty=kwargs.get('presence_penalty', 0.0),
                stream=True
            )
            
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content is not None:
                    yield content
        except Exception as e:
            # Log the error and yield a friendly message
            print(f"OpenAI API error: {str(e)}")
            yield f"I apologize, but I encountered an error while processing your request. Error: {str(e)}"
    
    async def generate_multimodal_completion(self, system_prompt: str, user_prompt: str, image_urls: List[str], **kwargs) -> str:
        """Generate a completion using OpenAI with image inputs
        
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
            content = [{"type": "text", "text": user_prompt}]
            
            # Add image URLs to the content
            for image_url in image_urls:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": image_url}
                })
            
            # Use a vision-capable model
            vision_model = kwargs.get('vision_model', 'gpt-4o')
            
            response = await self.client.chat.completions.create(
                model=vision_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 4000),
                top_p=kwargs.get('top_p', 1.0),
                frequency_penalty=kwargs.get('frequency_penalty', 0.0),
                presence_penalty=kwargs.get('presence_penalty', 0.0)
            )
            return response.choices[0].message.content
        except Exception as e:
            # Log the error and return a friendly message
            print(f"OpenAI API error: {str(e)}")
            return f"I apologize, but I encountered an error while processing your request. Error: {str(e)}"
    
    @property
    def provider_name(self) -> str:
        """Get the name of the provider"""
        return "openai"
    
    @property
    def default_model(self) -> str:
        """Get the default model for this provider"""
        return "gpt-4o-mini"
    
    @property
    def available_models(self) -> List[str]:
        """Get the list of available models for this provider"""
        return [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo"
        ]
