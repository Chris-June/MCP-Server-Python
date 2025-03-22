from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, UUID4
from uuid import uuid4
from datetime import datetime

class Memory(BaseModel):
    """Model for memory entries"""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the memory")
    role_id: str = Field(..., description="ID of the role this memory belongs to")
    content: str = Field(..., description="Content of the memory")
    type: Literal["session", "user", "knowledge"] = Field(..., description="Type of memory")
    importance: Literal["low", "medium", "high"] = Field("medium", description="Importance of the memory")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding of the memory content")
    created_at: datetime = Field(default_factory=datetime.now, description="When the memory was created")
    expires_at: Optional[datetime] = Field(None, description="When the memory expires")

class MemoryCreate(BaseModel):
    """Model for creating a new memory"""
    role_id: str = Field(..., description="ID of the role this memory belongs to")
    content: str = Field(..., description="Content of the memory")
    type: Literal["session", "user", "knowledge"] = Field(..., description="Type of memory")
    importance: Literal["low", "medium", "high"] = Field("medium", description="Importance of the memory")

class MemoryResponse(BaseModel):
    """Response model for memory operations"""
    success: bool = True
    memory: Memory

class MemoriesResponse(BaseModel):
    """Response model for listing memories"""
    memories: List[Memory]

class ClearMemoriesResponse(BaseModel):
    """Response model for clearing memories"""
    success: bool
    message: str
