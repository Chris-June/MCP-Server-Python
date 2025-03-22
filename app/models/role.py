from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, UUID4
from uuid import uuid4
from datetime import datetime

class Role(BaseModel):
    """Model for role definitions"""
    id: str = Field(..., description="Unique identifier for the role")
    name: str = Field(..., description="Human-readable name for the role")
    description: str = Field(..., description="Description of the role's purpose")
    instructions: str = Field(..., description="Custom instructions for the role")
    domains: List[str] = Field(default_factory=list, description="Areas of expertise")
    tone: str = Field("strategic", description="Communication tone (strategic, analytical, creative, etc.)")
    system_prompt: str = Field(..., description="Base system prompt for this role")
    is_default: bool = Field(False, description="Whether this is a default system role")

class RoleCreate(BaseModel):
    """Model for creating a new role"""
    id: str = Field(..., description="Unique identifier for the role")
    name: str = Field(..., description="Human-readable name for the role")
    description: str = Field(..., description="Description of the role's purpose")
    instructions: str = Field(..., description="Custom instructions for the role")
    domains: List[str] = Field(default_factory=list, description="Areas of expertise")
    tone: str = Field("strategic", description="Communication tone (strategic, analytical, creative, etc.)")
    system_prompt: str = Field(..., description="Base system prompt for this role")

class RoleUpdate(BaseModel):
    """Model for updating an existing role"""
    name: Optional[str] = Field(None, description="Human-readable name for the role")
    description: Optional[str] = Field(None, description="Description of the role's purpose")
    instructions: Optional[str] = Field(None, description="Custom instructions for the role")
    domains: Optional[List[str]] = Field(None, description="Areas of expertise")
    tone: Optional[str] = Field(None, description="Communication tone (strategic, analytical, creative, etc.)")
    system_prompt: Optional[str] = Field(None, description="Base system prompt for this role")

class RoleResponse(BaseModel):
    """Response model for role operations"""
    role: Role

class RolesResponse(BaseModel):
    """Response model for listing roles"""
    roles: List[Role]

class ProcessRequest(BaseModel):
    """Request model for processing a query"""
    role_id: str = Field(..., description="ID of the role to use")
    query: str = Field(..., description="Query to process")
    custom_instructions: Optional[str] = Field(None, description="Optional custom instructions")

class ProcessResponse(BaseModel):
    """Response model for processed queries"""
    role_id: str
    query: str
    response: str
