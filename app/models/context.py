from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4

class ContextSession(BaseModel):
    """Model for context switching session"""
    session_id: str = Field(..., description="Unique identifier for the session")
    current_role_id: str = Field(..., description="ID of the current active role")
    created_at: datetime = Field(default_factory=datetime.now, description="When the session was created")
    last_activity: datetime = Field(default_factory=datetime.now, description="When the session was last active")
    last_switch_reason: Optional[str] = Field(None, description="Reason for the last context switch")
    history: List[Dict[str, Any]] = Field(default_factory=list, description="History of context switches")

class ContextSwitchEvent(BaseModel):
    """Model for a context switch event"""
    timestamp: datetime = Field(default_factory=datetime.now, description="When the switch occurred")
    from_role_id: str = Field(..., description="ID of the role switched from")
    to_role_id: str = Field(..., description="ID of the role switched to")
    reason: str = Field(..., description="Reason for the switch")
    query: Optional[str] = Field(None, description="Query that triggered the switch, if any")
    automatic: bool = Field(False, description="Whether the switch was automatic or manual")

class CreateSessionRequest(BaseModel):
    """Request model for creating a new session"""
    initial_role_id: str = Field(..., description="ID of the initial role to use")
    session_id: Optional[str] = Field(None, description="Optional custom session ID")

class CreateSessionResponse(BaseModel):
    """Response model for session creation"""
    session_id: str = Field(..., description="ID of the created session")
    current_role_id: str = Field(..., description="ID of the current role")
    message: str = Field(..., description="Status message")

class ProcessWithContextRequest(BaseModel):
    """Request model for processing a query with context switching"""
    session_id: str = Field(..., description="ID of the session to use")
    query: str = Field(..., description="Query to process")
    custom_instructions: Optional[str] = Field(None, description="Optional custom instructions")
    force_role_id: Optional[str] = Field(None, description="Optional role ID to force using")

class ProcessWithContextResponse(BaseModel):
    """Response model for processed queries with context switching"""
    session_id: str = Field(..., description="ID of the session")
    role_id: str = Field(..., description="ID of the role used")
    query: str = Field(..., description="The query that was processed")
    response: str = Field(..., description="The processed response")
    context_switched: bool = Field(..., description="Whether context was switched")
    switch_reason: Optional[str] = Field(None, description="Reason for context switch, if any")

class SwitchContextRequest(BaseModel):
    """Request model for manually switching context"""
    session_id: str = Field(..., description="ID of the session to switch context for")
    new_role_id: str = Field(..., description="ID of the role to switch to")
    reason: Optional[str] = Field("Manual switch by user", description="Reason for the switch")

class SwitchContextResponse(BaseModel):
    """Response model for context switching"""
    session_id: str = Field(..., description="ID of the session")
    current_role_id: str = Field(..., description="ID of the current role")
    previous_role_id: str = Field(..., description="ID of the previous role")
    reason: str = Field(..., description="Reason for the switch")
    message: str = Field(..., description="Status message")

class ContextTrigger(BaseModel):
    """Model for context switching triggers"""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the trigger")
    role_id: str = Field(..., description="ID of the role this trigger is for")
    pattern: str = Field(..., description="Regex pattern or keyword to match")
    priority: int = Field(1, description="Priority of the trigger (higher numbers = higher priority)")
    description: str = Field(..., description="Description of what this trigger matches")
    is_regex: bool = Field(False, description="Whether the pattern is a regex pattern")
    enabled: bool = Field(True, description="Whether this trigger is enabled")
    created_at: datetime = Field(default_factory=datetime.now, description="When the trigger was created")

class CreateTriggerRequest(BaseModel):
    """Request model for creating a context trigger"""
    role_id: str = Field(..., description="ID of the role this trigger is for")
    pattern: str = Field(..., description="Regex pattern or keyword to match")
    priority: int = Field(1, description="Priority of the trigger (higher numbers = higher priority)")
    description: str = Field(..., description="Description of what this trigger matches")
    is_regex: bool = Field(False, description="Whether the pattern is a regex pattern")

class UpdateTriggerRequest(BaseModel):
    """Request model for updating a trigger"""
    pattern: Optional[str] = Field(None, description="Regex pattern or keyword to match")
    priority: Optional[int] = Field(None, description="Priority of the trigger")
    description: Optional[str] = Field(None, description="Description of what this trigger matches")
    is_regex: Optional[bool] = Field(None, description="Whether the pattern is a regex pattern")
    enabled: Optional[bool] = Field(None, description="Whether this trigger is enabled")

class TriggerResponse(BaseModel):
    """Response model for trigger operations"""
    trigger: ContextTrigger

class TriggersResponse(BaseModel):
    """Response model for listing triggers"""
    triggers: List[ContextTrigger]
