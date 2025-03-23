from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class BrowserSession(BaseModel):
    """Model for browser session information"""
    session_id: str = Field(..., description="Unique identifier for the browser session")
    created_at: datetime = Field(default_factory=datetime.now, description="When the session was created")
    active: bool = Field(True, description="Whether the session is currently active")
    mock: bool = Field(False, description="Whether this is a mock session")
    error: Optional[str] = Field(None, description="Error message if browser initialization failed")

class BrowserNavigationRequest(BaseModel):
    """Request model for browser navigation"""
    url: HttpUrl = Field(..., description="URL to navigate to")

class BrowserClickRequest(BaseModel):
    """Request model for clicking an element"""
    selector: str = Field(..., description="CSS selector for the element to click")

class BrowserFillRequest(BaseModel):
    """Request model for filling an input field"""
    selector: str = Field(..., description="CSS selector for the input field")
    value: str = Field(..., description="Value to fill in the input field")

class BrowserEvaluateRequest(BaseModel):
    """Request model for evaluating JavaScript"""
    script: str = Field(..., description="JavaScript code to execute")

class BrowserScreenshotRequest(BaseModel):
    """Request model for taking a screenshot"""
    selector: Optional[str] = Field(None, description="CSS selector for element to screenshot")

class BrowserResponse(BaseModel):
    """Base response model for browser operations"""
    success: bool = Field(..., description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if the operation failed")

class BrowserContentResponse(BrowserResponse):
    """Response model for page content"""
    content: str = Field(..., description="HTML content of the page")
    title: str = Field(..., description="Title of the page")
    url: str = Field(..., description="Current URL of the page")

class BrowserScreenshotResponse(BrowserResponse):
    """Response model for screenshots"""
    image_data: str = Field(..., description="Base64-encoded image data")
    mime_type: str = Field("image/png", description="MIME type of the image")

class BrowserEvaluateResponse(BrowserResponse):
    """Response model for JavaScript evaluation"""
    result: Any = Field(..., description="Result of the JavaScript evaluation")

class BrowserHistoryEntry(BaseModel):
    """Model for a browser history entry"""
    url: str = Field(..., description="URL that was visited")
    title: Optional[str] = Field(None, description="Title of the page")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the page was visited")
    actions: List[Dict[str, Any]] = Field(default_factory=list, description="Actions performed on the page")

class BrowserHistoryResponse(BaseModel):
    """Response model for browser history"""
    history: List[BrowserHistoryEntry] = Field(..., description="List of history entries")
