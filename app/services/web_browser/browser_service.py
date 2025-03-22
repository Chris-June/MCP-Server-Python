import asyncio
import os
import logging
import sys
from typing import Dict, List, Optional, Any, Callable
import json
import time

# Import pyppeteer with error handling
try:
    from pyppeteer import launch
    from pyppeteer.browser import Browser
    from pyppeteer.page import Page
    PYPPETEER_AVAILABLE = True
except ImportError as e:
    logging.error(f"Failed to import pyppeteer: {e}")
    PYPPETEER_AVAILABLE = False
    
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class BrowserService:
    """Service for controlling a headless browser using Pyppeteer (Python port of Puppeteer)"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def initialize(self, headless=True, executable_path=None):
        """Initialize the browser service
        
        Args:
            headless (bool): Whether to run browser in headless mode
            executable_path (str): Optional path to Chrome/Chromium executable
        """
        # Check if pyppeteer is available
        if not PYPPETEER_AVAILABLE:
            logger.error("Pyppeteer is not available. Browser service cannot be initialized.")
            return False
            
        # If browser is already initialized, don't do it again
        if self.browser is not None:
            logger.info("Browser already initialized")
            return True
            
        try:
            # Use more robust launch options
            logger.info(f"Launching browser (headless={headless})...")
            
            # Set environment variables that might help with Chrome launching
            os.environ['PYTHONUNBUFFERED'] = '1'
            
            # Launch with a retry mechanism
            max_retries = 3
            retry_count = 0
            last_error = None
            
            # Prepare launch options
            launch_options = {
                "headless": headless,
                "args": [
                    '--no-sandbox', 
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-features=site-per-process',
                    '--disable-web-security'
                ],
                "handleSIGINT": False,  # Prevent keyboard interrupts from closing browser
                "handleSIGTERM": False, # Prevent termination signals from closing browser
                "handleSIGHUP": False,   # Prevent hangup signals from closing browser
                "ignoreHTTPSErrors": True,
                "dumpio": True  # Output browser process stdout and stderr
            }
            
            # Add executable path if provided
            if executable_path:
                launch_options["executablePath"] = executable_path
                logger.info(f"Using custom Chrome path: {executable_path}")
            
            while retry_count < max_retries:
                try:
                    logger.info(f"Browser launch attempt {retry_count + 1}/{max_retries}")
                    self.browser = await launch(**launch_options)
                    
                    # Verify browser is initialized
                    if self.browser is None:
                        raise Exception("Browser failed to initialize properly")
                        
                    # Test browser by creating a page
                    test_page = await self.browser.newPage()
                    await test_page.close()
                    
                    logger.info("Browser service initialized successfully")
                    return True
                except Exception as e:
                    retry_count += 1
                    last_error = e
                    logger.warning(f"Browser launch attempt {retry_count} failed: {str(e)}")
                    await asyncio.sleep(2)  # Wait before retrying
                    
                    # Try with different options on subsequent attempts
                    if retry_count == 2:
                        # Try with non-headless mode on last attempt if we were using headless
                        if headless:
                            logger.info("Trying with non-headless mode...")
                            launch_options["headless"] = False
            
            # If we get here, all retries failed
            logger.error(f"Failed to initialize browser service after {max_retries} attempts: {str(last_error)}")
            self.browser = None
            return False
        except Exception as e:
            logger.error(f"Failed to initialize browser service: {str(e)}")
            # Reset browser to None to ensure we try again next time
            self.browser = None
            return False
    
    async def close(self):
        """Close the browser and clean up resources"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            logger.info("Browser service closed")
    
    async def create_session(self, session_id: str) -> str:
        """Create a new browser session"""
        if session_id in self.active_sessions:
            return session_id
        
        # Check if browser is initialized, if not, initialize it
        try:
            # First try with headless mode
            if self.browser is None:
                logger.info("Browser not initialized, initializing now with headless mode")
                success = await self.initialize(headless=True)
                
                # If headless mode fails, try with non-headless mode
                if not success:
                    logger.info("Headless mode failed, trying with non-headless mode")
                    success = await self.initialize(headless=False)
                    
                    # If that also fails, try with a specific Chrome path if on Mac
                    if not success and sys.platform == 'darwin':
                        # Try with the default Mac Chrome location
                        mac_chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                        if os.path.exists(mac_chrome_path):
                            logger.info(f"Trying with specific Chrome path: {mac_chrome_path}")
                            success = await self.initialize(headless=False, executable_path=mac_chrome_path)
                
            # Double-check browser is initialized after initialization attempts
            if self.browser is None:
                logger.error("All browser initialization attempts failed")
                # Create a mock response for testing/development
                self.active_sessions[session_id] = {
                    "page": None,  # No actual page
                    "history": [],
                    "mock": True   # Flag to indicate this is a mock session
                }
                logger.warning(f"Created MOCK browser session: {session_id} (browser unavailable)")
                return session_id
                
            # Create a new browser page with retry logic
            max_retries = 3
            retry_count = 0
            last_error = None
            
            while retry_count < max_retries:
                try:
                    # Double-check browser is not None before trying to create a page
                    if self.browser is None:
                        raise Exception("Cannot create page: browser is None")
                        
                    logger.info(f"Attempting to create new page, attempt {retry_count + 1}/{max_retries}")
                    page = await self.browser.newPage()
                    
                    if page is None:
                        raise Exception("Failed to create new page - page is None")
                        
                    logger.info("Setting viewport")
                    await page.setViewport({"width": 1280, "height": 800})
                    
                    # Set default timeout to avoid hanging
                    logger.info("Setting timeouts")
                    await page.setDefaultNavigationTimeout(30000)  # 30 seconds
                    await page.setDefaultTimeout(30000)  # 30 seconds
                    
                    # Disable cache for more reliable results
                    logger.info("Disabling cache")
                    await page.setCacheEnabled(False)
                    
                    self.active_sessions[session_id] = {
                        "page": page,
                        "history": []
                    }
                    
                    logger.info(f"Created new browser session: {session_id}")
                    return session_id
                except Exception as e:
                    retry_count += 1
                    last_error = e
                    logger.warning(f"Attempt {retry_count}/{max_retries} to create session failed: {str(e)}")
                    await asyncio.sleep(1)  # Wait before retrying
                    
                    # Try to reinitialize the browser if we're having issues
                    if retry_count == 2:
                        logger.info("Attempting to reinitialize browser")
                        try:
                            await self.close()  # Close existing browser if any
                            success = await self.initialize(headless=False)  # Try non-headless mode
                            
                            # If reinitialization failed, break out of retry loop
                            if not success or self.browser is None:
                                logger.warning("Browser reinitialization failed, breaking retry loop")
                                break
                        except Exception as reinit_error:
                            logger.error(f"Failed to reinitialize browser: {str(reinit_error)}")
                            # Break out of retry loop if reinitialization failed with exception
                            break
            
            # If we get here, all retries failed
            logger.error(f"Failed to create browser session after {max_retries} attempts: {str(last_error)}")
            
            # Create a mock session as fallback
            self.active_sessions[session_id] = {
                "page": None,  # No actual page
                "history": [],
                "mock": True,  # Flag to indicate this is a mock session
                "error": str(last_error)
            }
            logger.warning(f"Created MOCK browser session as fallback: {session_id}")
            return session_id
        except Exception as e:
            logger.error(f"Failed to create browser session: {str(e)}")
            # Create a mock session as fallback
            self.active_sessions[session_id] = {
                "page": None,  # No actual page
                "history": [],
                "mock": True,  # Flag to indicate this is a mock session
                "error": str(e)
            }
            logger.warning(f"Created MOCK browser session as fallback: {session_id}")
            return session_id
    
    async def close_session(self, session_id: str) -> bool:
        """Close a browser session"""
        if session_id not in self.active_sessions:
            return False
        
        try:
            # Check if this is a mock session
            if self.active_sessions[session_id].get("mock", False):
                # Just clean up the mock session
                del self.active_sessions[session_id]
                logger.info(f"Closed mock browser session: {session_id}")
                return True
                
            # Regular session with a page
            page = self.active_sessions[session_id]["page"]
            try:
                await page.close()
            except Exception as e:
                logger.warning(f"Page may already be closed: {str(e)}")
                # Continue with cleanup even if page.close() fails
            
            # Always clean up the session from active_sessions
            del self.active_sessions[session_id]
            logger.info(f"Closed browser session: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to close browser session: {str(e)}")
            # Try to clean up the session anyway
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
                logger.info(f"Cleaned up session from active_sessions: {session_id}")
            return False
    
    async def navigate(self, session_id: str, url: str) -> Dict[str, Any]:
        """Navigate to a URL"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Make sure the URL is properly formatted
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
            
        # Check if this is a mock session
        if self.active_sessions[session_id].get("mock", False):
            logger.info(f"Using mock navigation for session {session_id} to {url}")
            
            # Extract domain from URL for title
            import re
            domain_match = re.search(r'https?://([^/]+)', url)
            domain = domain_match.group(1) if domain_match else url
            title = f"Mock Page - {domain}"
            
            # Add to history
            self.active_sessions[session_id]["history"].append({
                "url": url,
                "title": title
            })
            
            # Set current URL and title in session
            self.active_sessions[session_id]["current_url"] = url
            self.active_sessions[session_id]["title"] = title
            
            return {
                "success": True,
                "url": url,
                "title": title,
                "status": 200,
                "mock": True
            }
        
        # Regular session with a page
        page = self.active_sessions[session_id]["page"]
        
        try:
            # Use a more reliable navigation approach with multiple wait conditions
            try:
                # First try with networkidle0 (more strict)
                response = await page.goto(url, {
                    "waitUntil": "networkidle0",
                    "timeout": 30000  # 30 seconds timeout
                })
            except Exception as nav_error:
                logger.warning(f"First navigation attempt failed: {str(nav_error)}, trying with less strict conditions")
                # If that fails, try with load event (less strict)
                response = await page.goto(url, {
                    "waitUntil": "load",
                    "timeout": 30000  # 30 seconds timeout
                })
            
            # Wait a bit for any JavaScript to execute
            await asyncio.sleep(1)
            
            # Get page title and URL
            title = await page.title()
            current_url = page.url
            
            # Add to history
            self.active_sessions[session_id]["history"].append({
                "url": current_url,
                "title": title
            })
            
            return {
                "success": True,
                "url": current_url,
                "title": title,
                "status": response.status if response else 200
            }
        except asyncio.CancelledError as ce:
            logger.error(f"Navigation cancelled: {str(ce)}")
            return {
                "success": False,
                "error": "Navigation was cancelled, possibly due to timeout"
            }
        except Exception as e:
            logger.error(f"Navigation error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_page_content(self, session_id: str) -> Dict[str, Any]:
        """Get the current page content"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
            
        # Check if this is a mock session
        if self.active_sessions[session_id].get("mock", False):
            logger.info(f"Using mock page content for session {session_id}")
            
            # Get the current URL and title from the session
            url = self.active_sessions[session_id].get("current_url", "https://example.com")
            title = self.active_sessions[session_id].get("title", "Mock Page")
            
            # Generate mock content based on URL
            import re
            domain_match = re.search(r'https?://([^/]+)', url)
            domain = domain_match.group(1) if domain_match else "example.com"
            
            mock_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
</head>
<body>
    <h1>Mock Content for {domain}</h1>
    <p>This is a mock page generated because the browser service is running in fallback mode.</p>
    <p>URL: {url}</p>
</body>
</html>"""
            
            return {
                "success": True,
                "url": url,
                "title": title,
                "content": mock_content,
                "mock": True
            }
        
        # Regular session with a page
        page = self.active_sessions[session_id]["page"]
        try:
            content = await page.content()
            title = await page.title()
            current_url = page.url
            
            return {
                "success": True,
                "url": current_url,
                "title": title,
                "content": content
            }
        except Exception as e:
            logger.error(f"Error getting page content: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def screenshot(self, session_id: str, selector: Optional[str] = None) -> Dict[str, Any]:
        """Take a screenshot of the current page or a specific element"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
            
        # Check if this is a mock session
        if self.active_sessions[session_id].get("mock", False):
            logger.info(f"Using mock screenshot for session {session_id}")
            
            # Generate a simple mock screenshot (1x1 transparent PNG)
            # This is the base64 representation of a 1x1 transparent PNG
            mock_screenshot = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
            
            return {
                "success": True,
                "data": mock_screenshot,
                "mock": True
            }
        
        # Regular session with a page
        page = self.active_sessions[session_id]["page"]
        try:
            if selector:
                element = await page.querySelector(selector)
                if not element:
                    return {"success": False, "error": f"Element not found: {selector}"}
                screenshot = await element.screenshot({"encoding": "base64"})
            else:
                screenshot = await page.screenshot({"encoding": "base64"})
            
            return {
                "success": True,
                "data": screenshot
            }
        except Exception as e:
            logger.error(f"Screenshot error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def click(self, session_id: str, selector: str) -> Dict[str, Any]:
        """Click an element on the page"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Check if this is a mock session
        if self.active_sessions[session_id].get("mock", False):
            logger.info(f"Using mock click for session {session_id} on selector {selector}")
            return {
                "success": True,
                "mock": True,
                "selector": selector
            }
        
        # Regular session with a page
        page = self.active_sessions[session_id]["page"]
        try:
            await page.waitForSelector(selector, {"visible": True, "timeout": 5000})
            await page.click(selector)
            return {"success": True}
        except Exception as e:
            logger.error(f"Click error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def fill(self, session_id: str, selector: str, value: str) -> Dict[str, Any]:
        """Fill out an input field"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Check if this is a mock session
        if self.active_sessions[session_id].get("mock", False):
            logger.info(f"Using mock fill for session {session_id} on selector {selector} with value {value}")
            return {
                "success": True,
                "mock": True,
                "selector": selector,
                "value": value
            }
        
        # Regular session with a page
        page = self.active_sessions[session_id]["page"]
        try:
            await page.waitForSelector(selector, {"visible": True, "timeout": 5000})
            await page.type(selector, value)
            return {"success": True}
        except Exception as e:
            logger.error(f"Fill error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def evaluate(self, session_id: str, script: str) -> Dict[str, Any]:
        """Execute JavaScript in the browser"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Check if this is a mock session
        if self.active_sessions[session_id].get("mock", False):
            logger.info(f"Using mock evaluate for session {session_id} with script: {script[:100]}...")
            # Return a simple mock result
            return {
                "success": True,
                "result": None,  # Most JS evaluations return null for simple operations
                "mock": True,
                "script": script[:100] + ("..." if len(script) > 100 else "")
            }
        
        # Regular session with a page
        page = self.active_sessions[session_id]["page"]
        try:
            result = await page.evaluate(script)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            logger.error(f"Evaluation error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_session_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get the browsing history for a session"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Return history regardless of whether it's a mock session or not
        # Both types of sessions maintain history in the same way
        history = self.active_sessions[session_id]["history"]
        
        # Add a flag if this is a mock session
        if self.active_sessions[session_id].get("mock", False):
            logger.info(f"Returning mock session history for {session_id}")
            return [{**item, "mock": True} for item in history]
        
        return history
