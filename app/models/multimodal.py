from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    """Enum for content types"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    FILE = "file"

class MediaContent(BaseModel):
    """Model for media content"""
    type: ContentType = Field(..., description="Type of media content")
    url: Optional[HttpUrl] = Field(None, description="URL to the media content")
    base64_data: Optional[str] = Field(None, description="Base64 encoded media data")
    mime_type: Optional[str] = Field(None, description="MIME type of the media content")
    alt_text: Optional[str] = Field(None, description="Alternative text description of the media")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the media")
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "image",
                "base64_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD...",
                "mime_type": "image/jpeg",
                "alt_text": "A chart showing business growth metrics",
                "metadata": {"width": 800, "height": 600}
            }
        }

class MultiModalContent(BaseModel):
    """Model for multi-modal content"""
    text: Optional[str] = Field(None, description="Text content")
    media: Optional[List[MediaContent]] = Field(None, description="Media content")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Please analyze this chart of our quarterly sales:",
                "media": [{
                    "type": "image",
                    "base64_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD...",
                    "mime_type": "image/jpeg",
                    "alt_text": "Quarterly sales chart for 2024"
                }]
            }
        }

class MultiModalProcessRequest(BaseModel):
    """Request model for processing a multi-modal query"""
    role_id: str = Field(..., description="ID of the role to use")
    content: MultiModalContent = Field(..., description="Multi-modal content to process")
    custom_instructions: Optional[str] = Field(None, description="Optional custom instructions")
    provider_name: Optional[str] = Field(None, description="Optional LLM provider to use (defaults to the configured default provider)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "role_id": "cfo-advisor",
                "content": {
                    "text": "What insights can you provide about our financial performance based on this chart?",
                    "media": [{
                        "type": "image",
                        "base64_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD...",
                        "mime_type": "image/jpeg",
                        "alt_text": "Financial performance chart"
                    }]
                },
                "custom_instructions": "Focus on cash flow implications",
                "provider_name": "openai"
            }
        }

class MultiModalProcessResponse(BaseModel):
    """Response model for processed multi-modal queries"""
    role_id: str
    response: str
    processed_media: List[Dict[str, Any]] = Field(default_factory=list, description="Information about processed media")
