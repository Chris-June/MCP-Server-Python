import google.generativeai as genai
from typing import List, Dict, Any, Optional, AsyncGenerator
from app.services.llm_providers.base_provider import BaseLLMProvider
import asyncio

class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider implementation"""
    
    def __init__(self, api_key: str, model: str = None):
        """Initialize the Gemini provider
        
        Args:
            api_key: Google API key
            model: Model to use (defaults to gemini-1.5-pro if None)
        """
        genai.configure(api_key=api_key)
        self.model = model or self.default_model
    
    async def generate_completion(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate a completion using Gemini
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The generated completion
        """
        try:
            # Combine system and user prompts for Gemini
            combined_prompt = f"{system_prompt}\n\nUser: {user_prompt}"
            
            # Create the model instance
            model = genai.GenerativeModel(
                model_name=kwargs.get('model', self.model),
                generation_config={
                    "temperature": kwargs.get('temperature', 0.7),
                    "top_p": kwargs.get('top_p', 1.0),
                    "max_output_tokens": kwargs.get('max_tokens', 4000),
                }
            )
            
            # Run in a thread to avoid blocking
            response = await asyncio.to_thread(
                model.generate_content,
                combined_prompt
            )
            
            return response.text
        except Exception as e:
            # Log the error and return a friendly message
            print(f"Gemini API error: {str(e)}")
            return f"I apologize, but I encountered an error while processing your request. Error: {str(e)}"
    
    async def generate_completion_stream(self, system_prompt: str, user_prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Generate a streaming completion using Gemini
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            An async generator yielding completion chunks
        """
        try:
            # Combine system and user prompts for Gemini
            combined_prompt = f"{system_prompt}\n\nUser: {user_prompt}"
            
            # Create the model instance
            model = genai.GenerativeModel(
                model_name=kwargs.get('model', self.model),
                generation_config={
                    "temperature": kwargs.get('temperature', 0.7),
                    "top_p": kwargs.get('top_p', 1.0),
                    "max_output_tokens": kwargs.get('max_tokens', 4000),
                }
            )
            
            # Run in a thread to avoid blocking
            response = await asyncio.to_thread(
                model.generate_content,
                combined_prompt,
                stream=True
            )
            
            # Process the stream
            async for chunk in asyncio.as_completed([asyncio.to_thread(lambda: list(response))]):
                for part in await chunk:
                    if hasattr(part, 'text') and part.text:
                        yield part.text
        except Exception as e:
            # Log the error and yield a friendly message
            print(f"Gemini API error: {str(e)}")
            yield f"I apologize, but I encountered an error while processing your request. Error: {str(e)}"
    
    async def generate_multimodal_completion(self, system_prompt: str, user_prompt: str, image_urls: List[str], **kwargs) -> str:
        """Generate a completion using Gemini with image inputs
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            image_urls: List of image URLs to include in the prompt
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The generated completion
        """
        try:
            # Combine system and user prompts for Gemini
            combined_prompt = f"{system_prompt}\n\nUser: {user_prompt}"
            
            # Create the model instance - use a vision-capable model
            vision_model = kwargs.get('vision_model', 'gemini-1.5-pro-vision')
            model = genai.GenerativeModel(
                model_name=vision_model,
                generation_config={
                    "temperature": kwargs.get('temperature', 0.7),
                    "top_p": kwargs.get('top_p', 1.0),
                    "max_output_tokens": kwargs.get('max_tokens', 4000),
                }
            )
            
            # Create content parts with text and images
            parts = [combined_prompt]
            
            # Add images to the parts
            for image_url in image_urls:
                # Load image from URL
                image_part = await asyncio.to_thread(
                    genai.types.PartDict,
                    inline_data={
                        "mime_type": "image/jpeg",  # Assuming JPEG, adjust as needed
                        "data": image_url
                    }
                )
                parts.append(image_part)
            
            # Run in a thread to avoid blocking
            response = await asyncio.to_thread(
                model.generate_content,
                parts
            )
            
            return response.text
        except Exception as e:
            # Log the error and return a friendly message
            print(f"Gemini API error: {str(e)}")
            return f"I apologize, but I encountered an error while processing your request. Error: {str(e)}"
    
    @property
    def provider_name(self) -> str:
        """Get the name of the provider"""
        return "gemini"
    
    @property
    def default_model(self) -> str:
        """Get the default model for this provider"""
        return "gemini-1.5-pro"
    
    @property
    def available_models(self) -> List[str]:
        """Get the list of available models for this provider"""
        return [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro",
            "gemini-1.5-pro-vision"
        ]
