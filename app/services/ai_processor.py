from openai import AsyncOpenAI
import asyncio
from typing import List, Dict, Any, Optional
from app.config import settings

class AIProcessor:
    """Service for processing AI requests using OpenAI API"""
    
    def __init__(self):
        """Initialize the AI processor"""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using the OpenAI API
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            
        Returns:
            The generated response
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            # In a production environment, add proper error handling and logging
            print(f"Error generating response: {e}")
            return f"I'm sorry, I encountered an error: {str(e)}"
    
    async def create_embedding(self, text: str) -> List[float]:
        """Create an embedding vector for the given text
        
        Args:
            text: The text to embed
            
        Returns:
            The embedding vector
        """
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            
            return response.data[0].embedding
        except Exception as e:
            # In a production environment, add proper error handling and logging
            print(f"Error creating embedding: {e}")
            return []
