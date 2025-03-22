import logging
import json
import re
from typing import Dict, List, Optional, Any, Tuple
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
    
    async def browse_url(self, role_id: str, url: str, extract_mode: str = 'auto') -> Dict[str, Any]:
        """Browse a specific URL and extract content
        
        Args:
            role_id: The ID of the role
            url: The URL to browse
            extract_mode: The extraction mode ('auto', 'article', 'full', 'structured')
            
        Returns:
            Dictionary with browsing results
        """
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
        
        # Get the page content based on extraction mode
        content = ""
        metadata = {}
        
        if extract_mode == 'full':
            # Get the full page content
            page_content = await self.browser_service.get_page_content(session_id)
            content = page_content.get("content", "")
        elif extract_mode == 'structured':
            # Extract structured data from the page
            structured_data = await self._extract_structured_data(session_id)
            content = json.dumps(structured_data, indent=2)
            metadata = structured_data
        else:  # 'auto' or 'article'
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
            content = js_result.get("result", "")
        
        # Get page metadata
        meta_script = """
        function getPageMetadata() {
            const metadata = {
                title: document.title,
                description: "",
                keywords: "",
                author: "",
                canonicalUrl: "",
                ogTags: {}
            };
            
            // Get meta tags
            const metaTags = document.querySelectorAll('meta');
            metaTags.forEach(tag => {
                const name = tag.getAttribute('name') || tag.getAttribute('property');
                const content = tag.getAttribute('content');
                
                if (name && content) {
                    if (name === 'description') metadata.description = content;
                    if (name === 'keywords') metadata.keywords = content;
                    if (name === 'author') metadata.author = content;
                    if (name.startsWith('og:')) metadata.ogTags[name] = content;
                }
            });
            
            // Get canonical URL
            const canonicalLink = document.querySelector('link[rel="canonical"]');
            if (canonicalLink) metadata.canonicalUrl = canonicalLink.getAttribute('href');
            
            return metadata;
        }
        
        return getPageMetadata();
        """
        
        meta_result = await self.browser_service.evaluate(session_id, meta_script)
        if meta_result["success"]:
            metadata.update(meta_result.get("result", {}))
        
        # Generate a summary if content is long
        summary = ""
        if len(content) > 1000:
            summary = await self._generate_content_summary(content[:5000])  # Limit to first 5000 chars for summary
        
        return {
            "success": True,
            "url": result["url"],
            "title": result["title"],
            "content": content,
            "summary": summary,
            "metadata": metadata,
            "screenshot": screenshot.get("data") if screenshot["success"] else None
        }
    
    async def _extract_structured_data(self, session_id: str) -> Dict[str, Any]:
        """Extract structured data from the page
        
        Args:
            session_id: The browser session ID
            
        Returns:
            Dictionary with structured data
        """
        # Extract structured data using JavaScript
        extract_script = """
        function extractStructuredData() {
            const result = {
                headings: [],
                links: [],
                images: [],
                lists: [],
                tables: [],
                forms: []
            };
            
            // Extract headings
            const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
            headings.forEach(h => {
                result.headings.push({
                    level: parseInt(h.tagName.substring(1)),
                    text: h.textContent.trim()
                });
            });
            
            // Extract links (limit to 20)
            const links = document.querySelectorAll('a[href]');
            let linkCount = 0;
            links.forEach(link => {
                if (linkCount < 20) {
                    const href = link.getAttribute('href');
                    if (href && !href.startsWith('#') && !href.startsWith('javascript:')) {
                        result.links.push({
                            text: link.textContent.trim(),
                            url: href
                        });
                        linkCount++;
                    }
                }
            });
            
            // Extract images (limit to 10)
            const images = document.querySelectorAll('img[src]');
            let imageCount = 0;
            images.forEach(img => {
                if (imageCount < 10) {
                    result.images.push({
                        alt: img.getAttribute('alt') || '',
                        src: img.getAttribute('src')
                    });
                    imageCount++;
                }
            });
            
            // Extract lists (limit to 5)
            const lists = document.querySelectorAll('ul, ol');
            let listCount = 0;
            lists.forEach(list => {
                if (listCount < 5) {
                    const items = Array.from(list.querySelectorAll('li')).map(li => li.textContent.trim());
                    result.lists.push({
                        type: list.tagName.toLowerCase(),
                        items: items
                    });
                    listCount++;
                }
            });
            
            // Extract tables (limit to 3)
            const tables = document.querySelectorAll('table');
            let tableCount = 0;
            tables.forEach(table => {
                if (tableCount < 3) {
                    const tableData = {
                        headers: [],
                        rows: []
                    };
                    
                    // Extract headers
                    const headerCells = table.querySelectorAll('th');
                    headerCells.forEach(cell => {
                        tableData.headers.push(cell.textContent.trim());
                    });
                    
                    // Extract rows
                    const rows = table.querySelectorAll('tr');
                    rows.forEach(row => {
                        const cells = row.querySelectorAll('td');
                        if (cells.length > 0) {
                            const rowData = [];
                            cells.forEach(cell => {
                                rowData.push(cell.textContent.trim());
                            });
                            tableData.rows.push(rowData);
                        }
                    });
                    
                    result.tables.push(tableData);
                    tableCount++;
                }
            });
            
            // Extract forms
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                const formData = {
                    id: form.getAttribute('id') || '',
                    action: form.getAttribute('action') || '',
                    method: form.getAttribute('method') || 'get',
                    fields: []
                };
                
                const inputs = form.querySelectorAll('input, select, textarea');
                inputs.forEach(input => {
                    formData.fields.push({
                        type: input.tagName.toLowerCase() === 'input' ? input.getAttribute('type') || 'text' : input.tagName.toLowerCase(),
                        name: input.getAttribute('name') || '',
                        id: input.getAttribute('id') || '',
                        placeholder: input.getAttribute('placeholder') || ''
                    });
                });
                
                result.forms.push(formData);
            });
            
            return result;
        }
        
        return extractStructuredData();
        """
        
        js_result = await self.browser_service.evaluate(session_id, extract_script)
        return js_result.get("result", {})
    
    async def _generate_content_summary(self, content: str) -> str:
        """Generate a summary of the content
        
        This is a simple rule-based summarization. In a production environment,
        you would use a more sophisticated approach, possibly using AI.
        
        Args:
            content: The content to summarize
            
        Returns:
            Summary of the content
        """
        # Simple rule-based summarization
        # In a real implementation, you might call an AI model here
        
        # Split into sentences and paragraphs
        sentences = re.split(r'(?<=[.!?])\s+', content)
        paragraphs = content.split('\n\n')
        
        # Get first few sentences (up to 5)
        first_sentences = sentences[:min(5, len(sentences))]
        
        # Get first paragraph
        first_paragraph = paragraphs[0] if paragraphs else ''
        
        # Combine for summary
        if len(first_paragraph) < 200 and len(paragraphs) > 1:
            summary = first_paragraph + '\n\n' + paragraphs[1][:200] + '...'
        else:
            summary = ' '.join(first_sentences) + '...'
        
        return summary[:500]  # Limit to 500 chars
    
    async def fill_form(self, role_id: str, form_data: Dict[str, str]) -> Dict[str, Any]:
        """Fill a form on the current page
        
        Args:
            role_id: The ID of the role
            form_data: Dictionary mapping selectors to values
            
        Returns:
            Dictionary with form filling results
        """
        session_id = await self.get_or_create_session(role_id)
        results = []
        
        for selector, value in form_data.items():
            result = await self.browser_service.fill(session_id, selector, value)
            results.append({
                "selector": selector,
                "success": result["success"],
                "error": result.get("error", "")
            })
        
        return {
            "success": all(r["success"] for r in results),
            "results": results
        }
    
    async def click_element(self, role_id: str, selector: str) -> Dict[str, Any]:
        """Click an element on the current page
        
        Args:
            role_id: The ID of the role
            selector: CSS selector for the element to click
            
        Returns:
            Dictionary with click results
        """
        session_id = await self.get_or_create_session(role_id)
        result = await self.browser_service.click(session_id, selector)
        
        # Take a screenshot after clicking
        if result["success"]:
            await self.browser_service.screenshot(session_id)
        
        return result
    
    async def extract_element_text(self, role_id: str, selector: str) -> Dict[str, Any]:
        """Extract text from an element on the current page
        
        Args:
            role_id: The ID of the role
            selector: CSS selector for the element
            
        Returns:
            Dictionary with extraction results
        """
        session_id = await self.get_or_create_session(role_id)
        
        # Extract text using JavaScript
        extract_script = f"""
        function extractElementText() {{
            const element = document.querySelector('{selector}');
            if (!element) return null;
            return element.textContent.trim();
        }}
        
        return extractElementText();
        """
        
        js_result = await self.browser_service.evaluate(session_id, extract_script)
        
        if not js_result["success"] or js_result.get("result") is None:
            return {
                "success": False,
                "error": f"Element not found: {selector}"
            }
        
        return {
            "success": True,
            "text": js_result.get("result", "")
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
