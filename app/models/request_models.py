from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class GenerateRequest(BaseModel):
    """Request model for generating a response"""
    system_prompt: str
    user_prompt: str
    role_id: Optional[str] = None
    provider_name: Optional[str] = None


class StreamGenerateRequest(BaseModel):
    """Request model for generating a streaming response"""
    system_prompt: str
    user_prompt: str
    role_id: Optional[str] = None
    provider_name: Optional[str] = None
