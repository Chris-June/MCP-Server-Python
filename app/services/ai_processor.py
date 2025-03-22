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
                # Handle search web command
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
                
                # Handle browse URL command with different extraction modes
                elif "[BROWSE_URL:" in user_prompt:
                    # Extract URL and optional extraction mode
                    url_start = user_prompt.find("[BROWSE_URL:")
                    url_end = user_prompt.find("]", url_start)
                    if url_end > url_start:
                        url_params = user_prompt[url_start + 12:url_end].strip()
                        
                        # Check if extraction mode is specified
                        extract_mode = 'auto'  # default
                        if '|' in url_params:
                            url, extract_mode = url_params.split('|', 1)
                            url = url.strip()
                            extract_mode = extract_mode.strip().lower()
                            # Validate extract_mode
                            if extract_mode not in ['auto', 'article', 'full', 'structured']:
                                extract_mode = 'auto'
                        else:
                            url = url_params
                        
                        web_result = await self.browser_integration.browse_url(role_id, url, extract_mode)
                        
                        # Add the webpage content to the user prompt
                        web_info = f"\n\n[WEB_PAGE_CONTENT]\nURL: {url}\n"
                        if web_result["success"]:
                            web_info += f"Title: {web_result['title']}\n"
                            
                            # Add metadata if available
                            if web_result.get('metadata') and extract_mode in ['structured', 'full']:
                                meta = web_result['metadata']
                                if meta.get('description'):
                                    web_info += f"Description: {meta.get('description')}\n"
                                if meta.get('keywords'):
                                    web_info += f"Keywords: {meta.get('keywords')}\n"
                            
                            # Add summary if available
                            if web_result.get('summary'):
                                web_info += f"\nSummary:\n{web_result.get('summary')}\n\n"
                            
                            # Add content
                            web_info += f"\nContent:\n{web_result.get('content', 'No content extracted')}\n"
                        else:
                            web_info += f"Error: {web_result.get('error', 'Unknown error')}\n"
                        web_info += "[/WEB_PAGE_CONTENT]"
                        user_prompt = user_prompt.replace(user_prompt[url_start:url_end+1], web_info)
                
                # Handle click element command
                elif "[CLICK_ELEMENT:" in user_prompt:
                    selector_start = user_prompt.find("[CLICK_ELEMENT:")
                    selector_end = user_prompt.find("]", selector_start)
                    if selector_end > selector_start:
                        selector = user_prompt[selector_start + 15:selector_end].strip()
                        click_result = await self.browser_integration.click_element(role_id, selector)
                        
                        # Add the click result to the user prompt
                        click_info = f"\n\n[ELEMENT_INTERACTION]\n"
                        if click_result["success"]:
                            click_info += f"Successfully clicked element: {selector}\n"
                        else:
                            click_info += f"Failed to click element: {selector}\nError: {click_result.get('error', 'Unknown error')}\n"
                        click_info += "[/ELEMENT_INTERACTION]"
                        user_prompt = user_prompt.replace(user_prompt[selector_start:selector_end+1], click_info)
                
                # Handle extract element text command
                elif "[EXTRACT_ELEMENT:" in user_prompt:
                    selector_start = user_prompt.find("[EXTRACT_ELEMENT:")
                    selector_end = user_prompt.find("]", selector_start)
                    if selector_end > selector_start:
                        selector = user_prompt[selector_start + 17:selector_end].strip()
                        extract_result = await self.browser_integration.extract_element_text(role_id, selector)
                        
                        # Add the extraction result to the user prompt
                        extract_info = f"\n\n[ELEMENT_CONTENT]\nSelector: {selector}\n"
                        if extract_result["success"]:
                            extract_info += f"Content:\n{extract_result.get('text', 'No content')}\n"
                        else:
                            extract_info += f"Error: {extract_result.get('error', 'Element not found')}\n"
                        extract_info += "[/ELEMENT_CONTENT]"
                        user_prompt = user_prompt.replace(user_prompt[selector_start:selector_end+1], extract_info)
                
                # Handle fill form command
                elif "[FILL_FORM:" in user_prompt:
                    form_start = user_prompt.find("[FILL_FORM:")
                    form_end = user_prompt.find("]", form_start)
                    if form_end > form_start:
                        form_data_str = user_prompt[form_start + 11:form_end].strip()
                        try:
                            # Parse form data in format: selector1=value1,selector2=value2
                            form_data = {}
                            for item in form_data_str.split(','):
                                if '=' in item:
                                    selector, value = item.split('=', 1)
                                    form_data[selector.strip()] = value.strip()
                            
                            if form_data:
                                fill_result = await self.browser_integration.fill_form(role_id, form_data)
                                
                                # Add the form fill result to the user prompt
                                form_info = f"\n\n[FORM_INTERACTION]\n"
                                if fill_result["success"]:
                                    form_info += f"Successfully filled form with {len(form_data)} fields\n"
                                else:
                                    form_info += f"Partially filled form with {len(form_data)} fields\n"
                                    for result in fill_result.get('results', []):
                                        if not result["success"]:
                                            form_info += f"- Failed to fill {result['selector']}: {result.get('error', 'Unknown error')}\n"
                                form_info += "[/FORM_INTERACTION]"
                                user_prompt = user_prompt.replace(user_prompt[form_start:form_end+1], form_info)
                        except Exception as e:
                            # Handle parsing errors
                            form_info = f"\n\n[FORM_INTERACTION]\nFailed to parse form data: {str(e)}\n[/FORM_INTERACTION]"
                            user_prompt = user_prompt.replace(user_prompt[form_start:form_end+1], form_info)
            
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
            # Process the user prompt with browser commands
            # This code is duplicated from generate_response to ensure consistency
            # In a production environment, refactor this into a shared method
            if self.browser_integration and role_id:
                # Handle search web command
                if "[SEARCH_WEB:" in user_prompt:
                    search_start = user_prompt.find("[SEARCH_WEB:")
                    search_end = user_prompt.find("]", search_start)
                    if search_end > search_start:
                        search_query = user_prompt[search_start + 12:search_end].strip()
                        web_result = await self.browser_integration.search_web(role_id, search_query)
                        web_info = f"\n\n[WEB_SEARCH_RESULTS]\nQuery: {search_query}\n"
                        if web_result["success"]:
                            web_info += f"Title: {web_result['title']}\nURL: {web_result['url']}\n\nResults:\n"
                            for i, result in enumerate(web_result.get('results', []), 1):
                                web_info += f"{i}. {result.get('title', 'No title')}\n   URL: {result.get('url', 'No URL')}\n   {result.get('snippet', 'No snippet')}\n\n"
                        else:
                            web_info += f"Error: {web_result.get('error', 'Unknown error')}\n"
                        web_info += "[/WEB_SEARCH_RESULTS]"
                        user_prompt = user_prompt.replace(user_prompt[search_start:search_end+1], web_info)
                
                # Handle browse URL command with different extraction modes
                elif "[BROWSE_URL:" in user_prompt:
                    url_start = user_prompt.find("[BROWSE_URL:")
                    url_end = user_prompt.find("]", url_start)
                    if url_end > url_start:
                        url_params = user_prompt[url_start + 12:url_end].strip()
                        
                        # Check if extraction mode is specified
                        extract_mode = 'auto'  # default
                        if '|' in url_params:
                            url, extract_mode = url_params.split('|', 1)
                            url = url.strip()
                            extract_mode = extract_mode.strip().lower()
                            if extract_mode not in ['auto', 'article', 'full', 'structured']:
                                extract_mode = 'auto'
                        else:
                            url = url_params
                        
                        web_result = await self.browser_integration.browse_url(role_id, url, extract_mode)
                        
                        web_info = f"\n\n[WEB_PAGE_CONTENT]\nURL: {url}\n"
                        if web_result["success"]:
                            web_info += f"Title: {web_result['title']}\n"
                            
                            # Add metadata if available
                            if web_result.get('metadata') and extract_mode in ['structured', 'full']:
                                meta = web_result['metadata']
                                if meta.get('description'):
                                    web_info += f"Description: {meta.get('description')}\n"
                                if meta.get('keywords'):
                                    web_info += f"Keywords: {meta.get('keywords')}\n"
                            
                            # Add summary if available
                            if web_result.get('summary'):
                                web_info += f"\nSummary:\n{web_result.get('summary')}\n\n"
                            
                            # Add content
                            web_info += f"\nContent:\n{web_result.get('content', 'No content extracted')}\n"
                        else:
                            web_info += f"Error: {web_result.get('error', 'Unknown error')}\n"
                        web_info += "[/WEB_PAGE_CONTENT]"
                        user_prompt = user_prompt.replace(user_prompt[url_start:url_end+1], web_info)
                
                # Handle click element command
                elif "[CLICK_ELEMENT:" in user_prompt:
                    selector_start = user_prompt.find("[CLICK_ELEMENT:")
                    selector_end = user_prompt.find("]", selector_start)
                    if selector_end > selector_start:
                        selector = user_prompt[selector_start + 15:selector_end].strip()
                        click_result = await self.browser_integration.click_element(role_id, selector)
                        
                        click_info = f"\n\n[ELEMENT_INTERACTION]\n"
                        if click_result["success"]:
                            click_info += f"Successfully clicked element: {selector}\n"
                        else:
                            click_info += f"Failed to click element: {selector}\nError: {click_result.get('error', 'Unknown error')}\n"
                        click_info += "[/ELEMENT_INTERACTION]"
                        user_prompt = user_prompt.replace(user_prompt[selector_start:selector_end+1], click_info)
                
                # Handle extract element text command
                elif "[EXTRACT_ELEMENT:" in user_prompt:
                    selector_start = user_prompt.find("[EXTRACT_ELEMENT:")
                    selector_end = user_prompt.find("]", selector_start)
                    if selector_end > selector_start:
                        selector = user_prompt[selector_start + 17:selector_end].strip()
                        extract_result = await self.browser_integration.extract_element_text(role_id, selector)
                        
                        extract_info = f"\n\n[ELEMENT_CONTENT]\nSelector: {selector}\n"
                        if extract_result["success"]:
                            extract_info += f"Content:\n{extract_result.get('text', 'No content')}\n"
                        else:
                            extract_info += f"Error: {extract_result.get('error', 'Element not found')}\n"
                        extract_info += "[/ELEMENT_CONTENT]"
                        user_prompt = user_prompt.replace(user_prompt[selector_start:selector_end+1], extract_info)
                
                # Handle fill form command
                elif "[FILL_FORM:" in user_prompt:
                    form_start = user_prompt.find("[FILL_FORM:")
                    form_end = user_prompt.find("]", form_start)
                    if form_end > form_start:
                        form_data_str = user_prompt[form_start + 11:form_end].strip()
                        try:
                            # Parse form data in format: selector1=value1,selector2=value2
                            form_data = {}
                            for item in form_data_str.split(','):
                                if '=' in item:
                                    selector, value = item.split('=', 1)
                                    form_data[selector.strip()] = value.strip()
                            
                            if form_data:
                                fill_result = await self.browser_integration.fill_form(role_id, form_data)
                                
                                form_info = f"\n\n[FORM_INTERACTION]\n"
                                if fill_result["success"]:
                                    form_info += f"Successfully filled form with {len(form_data)} fields\n"
                                else:
                                    form_info += f"Partially filled form with {len(form_data)} fields\n"
                                    for result in fill_result.get('results', []):
                                        if not result["success"]:
                                            form_info += f"- Failed to fill {result['selector']}: {result.get('error', 'Unknown error')}\n"
                                form_info += "[/FORM_INTERACTION]"
                                user_prompt = user_prompt.replace(user_prompt[form_start:form_end+1], form_info)
                        except Exception as e:
                            # Handle parsing errors
                            form_info = f"\n\n[FORM_INTERACTION]\nFailed to parse form data: {str(e)}\n[/FORM_INTERACTION]"
                            user_prompt = user_prompt.replace(user_prompt[form_start:form_end+1], form_info)
            
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
