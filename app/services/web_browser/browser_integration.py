import logging
import json
from typing import Dict, List, Optional, Any
from app.services.web_browser.browser_service import BrowserService

logger = logging.getLogger(__name__)

class BrowserIntegration:
    """Integration between AI processing and web browser functionality"""
    
    def __init__(self, browser_service: BrowserService):
        self.browser_service = browser_service
        self.active_sessions: Dict[str, str] = {}  # Maps role_id to session_id
    
    async def get_or_create_session(self, role_id: str) -> str:
        """Get an existing browser session for a role or create a new one"""
        if role_id in self.active_sessions:
            # Check if the session is still valid
            session_id = self.active_sessions[role_id]
            try:
                # Try to get history to verify session is active
                await self.browser_service.get_session_history(session_id)
                return session_id
            except ValueError:
                # Session no longer exists, remove it
                del self.active_sessions[role_id]
        
        # Create a new session
        session_id = await self.browser_service.create_session(role_id)
        self.active_sessions[role_id] = session_id
        return session_id
    
    async def search_web(self, role_id: str, query: str) -> Dict[str, Any]:
        """Search the web for information"""
        session_id = await self.get_or_create_session(role_id)
        
        # Navigate to a search engine
        search_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
        result = await self.browser_service.navigate(session_id, search_url)
        
        if not result["success"]:
            return {
                "success": False,
                "error": result.get("error", "Failed to navigate to search engine")
            }
        
        # Take a screenshot of the search results
        screenshot = await self.browser_service.screenshot(session_id)
        
        # Get the page content
        content = await self.browser_service.get_page_content(session_id)
        
        # Extract search results using JavaScript
        extract_script = """
        function extractSearchResults() {
            const results = [];
            const resultElements = document.querySelectorAll('.result');
            
            resultElements.forEach((el, index) => {
                if (index < 5) {  // Limit to top 5 results
                    const titleEl = el.querySelector('.result__title');
                    const linkEl = el.querySelector('.result__url');
                    const snippetEl = el.querySelector('.result__snippet');
                    
                    if (titleEl && snippetEl) {
                        results.push({
                            title: titleEl.textContent.trim(),
                            url: linkEl ? linkEl.textContent.trim() : '',
                            snippet: snippetEl.textContent.trim()
                        });
                    }
                }
            });
            
            return results;
        }
        
        return extractSearchResults();
        """
        
        js_result = await self.browser_service.evaluate(session_id, extract_script)
        
        return {
            "success": True,
            "query": query,
            "url": result["url"],
            "title": result["title"],
            "results": js_result.get("result", []),
            "screenshot": screenshot.get("data") if screenshot["success"] else None
        }
    
    async def browse_url(self, role_id: str, url: str) -> Dict[str, Any]:
        """Browse a specific URL and extract content"""
        session_id = await self.get_or_create_session(role_id)
        
        # Navigate to the URL
        result = await self.browser_service.navigate(session_id, url)
        
        if not result["success"]:
            return {
                "success": False,
                "error": result.get("error", "Failed to navigate to URL")
            }
        
        # Take a screenshot
        screenshot = await self.browser_service.screenshot(session_id)
        
        # Get the page content
        content = await self.browser_service.get_page_content(session_id)
        
        # Extract main content using JavaScript
        extract_script = """
        function extractMainContent() {
            // Try to find the main content
            const mainElement = document.querySelector('main') || 
                               document.querySelector('article') || 
                               document.querySelector('#content') || 
                               document.querySelector('.content');
            
            if (mainElement) {
                return mainElement.textContent.trim();
            }
            
            // Fallback: get all paragraphs
            const paragraphs = Array.from(document.querySelectorAll('p'));
            return paragraphs.map(p => p.textContent.trim()).join('\n\n');
        }
        
        return extractMainContent();
        """
        
        js_result = await self.browser_service.evaluate(session_id, extract_script)
        
        return {
            "success": True,
            "url": result["url"],
            "title": result["title"],
            "content": js_result.get("result", ""),
            "screenshot": screenshot.get("data") if screenshot["success"] else None
        }
    
    async def close_role_session(self, role_id: str) -> bool:
        """Close the browser session for a role"""
        if role_id not in self.active_sessions:
            return True
        
        session_id = self.active_sessions[role_id]
        success = await self.browser_service.close_session(session_id)
        
        if success:
            del self.active_sessions[role_id]
        
        return success
