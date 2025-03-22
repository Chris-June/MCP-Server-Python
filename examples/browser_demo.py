#!/usr/bin/env python3
"""
Web Browser MCP Demo Script

This script demonstrates how to use the web browsing capabilities of the MCP server.
It creates a browser session, navigates to a website, takes a screenshot, and performs
basic interactions with web elements.
"""

import asyncio
import json
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import httpx

# API base URL
API_BASE = "http://localhost:8000/api/v1/browser"

async def create_session():
    """Create a new browser session"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_BASE}/sessions")
        response.raise_for_status()
        return response.json()["session_id"]

async def navigate(session_id, url):
    """Navigate to a URL"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE}/sessions/{session_id}/navigate",
            json={"url": url}
        )
        response.raise_for_status()
        return response.json()

async def take_screenshot(session_id, selector=None):
    """Take a screenshot of the current page or a specific element"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE}/sessions/{session_id}/screenshot",
            json={"selector": selector}
        )
        response.raise_for_status()
        return response.json()

async def click_element(session_id, selector):
    """Click an element on the page"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE}/sessions/{session_id}/click",
            json={"selector": selector}
        )
        response.raise_for_status()
        return response.json()

async def fill_input(session_id, selector, value):
    """Fill out an input field"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE}/sessions/{session_id}/fill",
            json={"selector": selector, "value": value}
        )
        response.raise_for_status()
        return response.json()

async def evaluate_script(session_id, script):
    """Execute JavaScript in the browser"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE}/sessions/{session_id}/evaluate",
            json={"script": script}
        )
        response.raise_for_status()
        return response.json()

async def get_history(session_id):
    """Get the browsing history for a session"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/sessions/{session_id}/history")
        response.raise_for_status()
        return response.json()["history"]

async def close_session(session_id):
    """Close a browser session"""
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{API_BASE}/sessions/{session_id}")
        response.raise_for_status()
        return response.json()

async def main():
    print("Web Browser MCP Demo")
    print("====================")
    
    try:
        # Create a new browser session
        print("\nCreating browser session...")
        session_id = await create_session()
        print(f"Session created: {session_id}")
        
        # Navigate to a website
        print("\nNavigating to example.com...")
        try:
            result = await navigate(session_id, "https://example.com")
            print(f"Navigation successful: {result['title']}")
        except Exception as e:
            print(f"Navigation error: {e}")
            import traceback
            traceback.print_exc()
        
        # Take a screenshot
        print("\nTaking screenshot...")
        try:
            screenshot = await take_screenshot(session_id)
            screenshot_file = f"example_screenshot.png"
            
            # Save the screenshot
            import base64
            with open(screenshot_file, "wb") as f:
                f.write(base64.b64decode(screenshot["data"]))
            print(f"Screenshot saved to {screenshot_file}")
        except Exception as e:
            print(f"Screenshot error: {e}")
            import traceback
            traceback.print_exc()
        
        # Navigate to a search engine
        print("\nNavigating to search engine...")
        try:
            result = await navigate(session_id, "https://duckduckgo.com")
            print(f"Navigation successful: {result['title']}")
        except Exception as e:
            print(f"Navigation error: {e}")
            import traceback
            traceback.print_exc()
        
        # Fill the search box
        print("\nFilling search box...")
        await fill_input(session_id, "input[name=q]", "Small Business Executive Advisors")
        
        # Click the search button
        print("\nClicking search button...")
        await click_element(session_id, "button[type=submit]")
        
        # Wait for results to load
        print("\nWaiting for search results...")
        await asyncio.sleep(2)
        
        # Take a screenshot of the search results
        print("\nTaking screenshot of search results...")
        screenshot = await take_screenshot(session_id)
        screenshot_file = f"search_results_screenshot.png"
        
        # Save the screenshot
        with open(screenshot_file, "wb") as f:
            f.write(base64.b64decode(screenshot["data"]))
        print(f"Screenshot saved to {screenshot_file}")
        
        # Get browsing history
        print("\nGetting browsing history...")
        history = await get_history(session_id)
        print("Browsing history:")
        for i, entry in enumerate(history, 1):
            print(f"  {i}. {entry['title']} - {entry['url']}")
        
        # Close the session
        print("\nClosing browser session...")
        await close_session(session_id)
        print("Session closed successfully")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nDemo completed")

if __name__ == "__main__":
    asyncio.run(main())
