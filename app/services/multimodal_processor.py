import base64
import os
import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator, Tuple
from openai import AsyncOpenAI
from app.config import settings
from app.models.multimodal import ContentType, MediaContent, MultiModalContent

class MultiModalProcessor:
    """Service for processing multi-modal content using OpenAI API"""
    
    def __init__(self):
        """Initialize the multi-modal processor"""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.vision_model = settings.openai_vision_model
    
    async def process_multimodal_content(self, system_prompt: str, content: MultiModalContent) -> str:
        """Process multi-modal content and generate a response
        
        Args:
            system_prompt: The system prompt to use
            content: The multi-modal content to process
            
        Returns:
            The generated response
        """
        try:
            # Prepare messages for the API call
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Process text and media content
            user_message = self._prepare_user_message(content)
            messages.append(user_message)
            
            # Call the OpenAI API with the appropriate model based on content type
            if self._contains_media(content):
                response = await self.client.chat.completions.create(
                    model=self.vision_model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
            else:
                # If it's just text, use the standard model
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            # In a production environment, add proper error handling and logging
            print(f"Error processing multi-modal content: {e}")
            return f"I'm sorry, I encountered an error processing the multi-modal content: {str(e)}"
    
    async def process_multimodal_content_stream(self, system_prompt: str, content: MultiModalContent) -> AsyncGenerator[str, None]:
        """Process multi-modal content and generate a streaming response
        
        Args:
            system_prompt: The system prompt to use
            content: The multi-modal content to process
            
        Yields:
            Chunks of the generated response
        """
        try:
            # Prepare messages for the API call
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Process text and media content
            user_message = self._prepare_user_message(content)
            messages.append(user_message)
            
            # Call the OpenAI API with the appropriate model based on content type
            if self._contains_media(content):
                stream = await self.client.chat.completions.create(
                    model=self.vision_model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    stream=True
                )
            else:
                # If it's just text, use the standard model
                stream = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    stream=True
                )
            
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        yield content
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
    
    async def analyze_image(self, image_data: str, prompt: str) -> str:
        """Analyze an image using the vision model
        
        Args:
            image_data: The image data (URL or base64)
            prompt: The prompt to use for analysis
            
        Returns:
            The analysis result
        """
        try:
            # Prepare the image URL (either a web URL or base64 data)
            image_url = image_data
            if not image_data.startswith("http") and not image_data.startswith("data:"):
                # Assume it's base64 data without the prefix
                image_url = f"data:image/jpeg;base64,{image_data}"
            
            response = await self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image", "image_url": {"url": image_url}}
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return f"I'm sorry, I encountered an error analyzing the image: {str(e)}"
