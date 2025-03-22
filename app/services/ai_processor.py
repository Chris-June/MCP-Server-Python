from openai import AsyncOpenAI
import asyncio
import json
from typing import List, Dict, Any, Optional, AsyncGenerator
from app.config import settings
from app.services.web_browser.browser_integration import BrowserIntegration

class AIProcessor:
    """Service for processing AI requests using OpenAI API"""
    
    def __init__(self, browser_integration: Optional[BrowserIntegration] = None):
        """Initialize the AI processor
        
        Args:
            browser_integration: Optional browser integration service
        """
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.browser_integration = browser_integration
    
    async def generate_response(self, system_prompt: str, user_prompt: str, role_id: Optional[str] = None) -> str:
        """Generate a response using the OpenAI API
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            role_id: Optional role ID for browser integration
            
        Returns:
            The generated response
        """
        try:
            # Check if the user prompt contains a web browsing request
            web_result = None
            if self.browser_integration and role_id:
                if "[SEARCH_WEB:" in user_prompt:
                    # Extract search query
                    search_start = user_prompt.find("[SEARCH_WEB:")
                    search_end = user_prompt.find("]", search_start)
                    if search_end > search_start:
                        search_query = user_prompt[search_start + 12:search_end].strip()
                        web_result = await self.browser_integration.search_web(role_id, search_query)
                        # Add the search results to the user prompt
                        web_info = f"\n\n[WEB_SEARCH_RESULTS]\nQuery: {search_query}\n"
                        if web_result["success"]:
                            web_info += f"Title: {web_result['title']}\nURL: {web_result['url']}\n\nResults:\n"
                            for i, result in enumerate(web_result.get('results', []), 1):
                                web_info += f"{i}. {result.get('title', 'No title')}\n   URL: {result.get('url', 'No URL')}\n   {result.get('snippet', 'No snippet')}\n\n"
                        else:
                            web_info += f"Error: {web_result.get('error', 'Unknown error')}\n"
                        web_info += "[/WEB_SEARCH_RESULTS]"
                        user_prompt = user_prompt.replace(user_prompt[search_start:search_end+1], web_info)
                
                elif "[BROWSE_URL:" in user_prompt:
                    # Extract URL
                    url_start = user_prompt.find("[BROWSE_URL:")
                    url_end = user_prompt.find("]", url_start)
                    if url_end > url_start:
                        url = user_prompt[url_start + 12:url_end].strip()
                        web_result = await self.browser_integration.browse_url(role_id, url)
                        # Add the webpage content to the user prompt
                        web_info = f"\n\n[WEB_PAGE_CONTENT]\nURL: {url}\n"
                        if web_result["success"]:
                            web_info += f"Title: {web_result['title']}\n\nContent:\n{web_result.get('content', 'No content extracted')}\n"
                        else:
                            web_info += f"Error: {web_result.get('error', 'Unknown error')}\n"
                        web_info += "[/WEB_PAGE_CONTENT]"
                        user_prompt = user_prompt.replace(user_prompt[url_start:url_end+1], web_info)
            
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
    
    async def generate_response_stream(self, system_prompt: str, user_prompt: str, role_id: Optional[str] = None) -> AsyncGenerator[str, None]:
        """Generate a streaming response using the OpenAI API
        
        Args:
            system_prompt: The system prompt to use
            user_prompt: The user prompt to use
            role_id: Optional role ID for browser integration
            
        Yields:
            Chunks of the generated response
        """
        try:
            # Check if the user prompt contains a web browsing request
            web_result = None
            if self.browser_integration and role_id:
                if "[SEARCH_WEB:" in user_prompt:
                    # Extract search query
                    search_start = user_prompt.find("[SEARCH_WEB:")
                    search_end = user_prompt.find("]", search_start)
                    if search_end > search_start:
                        search_query = user_prompt[search_start + 12:search_end].strip()
                        web_result = await self.browser_integration.search_web(role_id, search_query)
                        # Add the search results to the user prompt
                        web_info = f"\n\n[WEB_SEARCH_RESULTS]\nQuery: {search_query}\n"
                        if web_result["success"]:
                            web_info += f"Title: {web_result['title']}\nURL: {web_result['url']}\n\nResults:\n"
                            for i, result in enumerate(web_result.get('results', []), 1):
                                web_info += f"{i}. {result.get('title', 'No title')}\n   URL: {result.get('url', 'No URL')}\n   {result.get('snippet', 'No snippet')}\n\n"
                        else:
                            web_info += f"Error: {web_result.get('error', 'Unknown error')}\n"
                        web_info += "[/WEB_SEARCH_RESULTS]"
                        user_prompt = user_prompt.replace(user_prompt[search_start:search_end+1], web_info)
                
                elif "[BROWSE_URL:" in user_prompt:
                    # Extract URL
                    url_start = user_prompt.find("[BROWSE_URL:")
                    url_end = user_prompt.find("]", url_start)
                    if url_end > url_start:
                        url = user_prompt[url_start + 12:url_end].strip()
                        web_result = await self.browser_integration.browse_url(role_id, url)
                        # Add the webpage content to the user prompt
                        web_info = f"\n\n[WEB_PAGE_CONTENT]\nURL: {url}\n"
                        if web_result["success"]:
                            web_info += f"Title: {web_result['title']}\n\nContent:\n{web_result.get('content', 'No content extracted')}\n"
                        else:
                            web_info += f"Error: {web_result.get('error', 'Unknown error')}\n"
                        web_info += "[/WEB_PAGE_CONTENT]"
                        user_prompt = user_prompt.replace(user_prompt[url_start:url_end+1], web_info)
            
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
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
            print(f"Error generating streaming response: {e}")
            yield f"I'm sorry, I encountered an error: {str(e)}"
    
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
