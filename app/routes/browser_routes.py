from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
import uuid
import json

from app.services.web_browser.browser_service import BrowserService

router = APIRouter()

# Browser session endpoints
@router.post("/sessions")
async def create_browser_session(request: Request):
    """Create a new browser session"""
    browser_service = request.app.state.browser_service
    session_id = str(uuid.uuid4())
    
    try:
        # Create the session
        await browser_service.create_session(session_id)
        
        # Check if this is a mock session
        is_mock = False
        if session_id in browser_service.active_sessions:
            is_mock = browser_service.active_sessions[session_id].get("mock", False)
        
        # Return session info
        response = {"session_id": session_id}
        
        # Add mock flag if applicable
        if is_mock:
            response["mock"] = True
            response["warning"] = "Using mock browser session. Browser initialization failed."
            
            # Add error message if available
            if "error" in browser_service.active_sessions[session_id]:
                response["error"] = browser_service.active_sessions[session_id]["error"]
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create browser session: {str(e)}")

@router.delete("/sessions/{session_id}")
async def close_browser_session(session_id: str, request: Request):
    """Close a browser session"""
    browser_service = request.app.state.browser_service
    
    try:
        success = await browser_service.close_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        return {"success": True}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to close browser session: {str(e)}")

# Browser navigation and interaction endpoints
@router.post("/sessions/{session_id}/navigate")
async def navigate(session_id: str, data: Dict[str, str], request: Request):
    """Navigate to a URL"""
    browser_service = request.app.state.browser_service
    
    if "url" not in data:
        raise HTTPException(status_code=400, detail="URL is required")
    
    try:
        result = await browser_service.navigate(session_id, data["url"])
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Navigation error: {str(e)}")

@router.get("/sessions/{session_id}/content")
async def get_page_content(session_id: str, request: Request):
    """Get the current page content"""
    browser_service = request.app.state.browser_service
    
    try:
        result = await browser_service.get_page_content(session_id)
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting page content: {str(e)}")

@router.post("/sessions/{session_id}/screenshot")
async def take_screenshot(session_id: str, data: Dict[str, Optional[str]], request: Request):
    """Take a screenshot of the current page or a specific element"""
    browser_service = request.app.state.browser_service
    selector = data.get("selector")
    
    try:
        result = await browser_service.screenshot(session_id, selector)
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Screenshot error: {str(e)}")

@router.post("/sessions/{session_id}/click")
async def click_element(session_id: str, data: Dict[str, str], request: Request):
    """Click an element on the page"""
    browser_service = request.app.state.browser_service
    
    if "selector" not in data:
        raise HTTPException(status_code=400, detail="Selector is required")
    
    try:
        result = await browser_service.click(session_id, data["selector"])
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Click error: {str(e)}")

@router.post("/sessions/{session_id}/fill")
async def fill_input(session_id: str, data: Dict[str, str], request: Request):
    """Fill out an input field"""
    browser_service = request.app.state.browser_service
    
    if "selector" not in data or "value" not in data:
        raise HTTPException(status_code=400, detail="Selector and value are required")
    
    try:
        result = await browser_service.fill(session_id, data["selector"], data["value"])
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fill error: {str(e)}")

@router.post("/sessions/{session_id}/evaluate")
async def evaluate_script(session_id: str, data: Dict[str, str], request: Request):
    """Execute JavaScript in the browser"""
    browser_service = request.app.state.browser_service
    
    if "script" not in data:
        raise HTTPException(status_code=400, detail="Script is required")
    
    try:
        result = await browser_service.evaluate(session_id, data["script"])
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation error: {str(e)}")

@router.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str, request: Request):
    """Get the browsing history for a session"""
    browser_service = request.app.state.browser_service
    
    try:
        history = await browser_service.get_session_history(session_id)
        return {"history": history}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting session history: {str(e)}")
