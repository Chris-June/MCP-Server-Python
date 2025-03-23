from fastapi import APIRouter, Depends, Request, HTTPException, Response
from typing import List, Dict, Any, Optional, AsyncGenerator
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from uuid import uuid4
from app.services.context_switching_service import ContextSwitchingService

router = APIRouter(prefix="/context")

async def get_context_switching_service(request: Request) -> ContextSwitchingService:
    """Dependency for getting the context switching service"""
    return request.app.state.context_switching_service

# Models for context switching API
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

@router.post("/sessions", response_model=CreateSessionResponse, status_code=201, summary="Create a new session")
async def create_session(
    request: CreateSessionRequest, 
    context_switching_service: ContextSwitchingService = Depends(get_context_switching_service)
):
    """Create a new session"""
    # Generate a session ID if not provided
    session_id = request.session_id or str(uuid4())
    
    # Create the session
    session = await context_switching_service.create_session(session_id, request.initial_role_id)
    
    return CreateSessionResponse(
        session_id=session_id,
        current_role_id=session["current_role_id"],
        message="Session created successfully"
    )

@router.post("/process", response_model=ProcessWithContextResponse, summary="Process a query with context switching")
async def process_with_context(
    request: ProcessWithContextRequest, 
    context_switching_service: ContextSwitchingService = Depends(get_context_switching_service)
):
    """Process a query with context switching"""
    try:
        result = await context_switching_service.process_query_with_context_switching(
            request.session_id,
            request.query,
            request.custom_instructions,
            request.force_role_id
        )
        
        return ProcessWithContextResponse(
            session_id=request.session_id,
            role_id=result["role_id"],
            query=result["query"],
            response=result["response"],
            context_switched=result["context_switched"],
            switch_reason=result["switch_reason"]
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

async def generate_stream_response_with_context(
    session_id: str, 
    query: str, 
    custom_instructions: Optional[str],
    force_role_id: Optional[str],
    context_switching_service: ContextSwitchingService
) -> AsyncGenerator[str, None]:
    """Generate a streaming response for a query with context switching"""
    try:
        async for chunk in context_switching_service.process_query_stream_with_context_switching(
            session_id,
            query,
            custom_instructions,
            force_role_id
        ):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"
    except ValueError as e:
        yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
        yield "data: [DONE]\n\n"

@router.post("/process/stream", summary="Process a query with context switching and streaming response")
async def process_with_context_stream(
    request: ProcessWithContextRequest, 
    context_switching_service: ContextSwitchingService = Depends(get_context_switching_service)
):
    """Process a query with context switching and streaming response"""
    return StreamingResponse(
        generate_stream_response_with_context(
            request.session_id,
            request.query,
            request.custom_instructions,
            request.force_role_id,
            context_switching_service
        ),
        media_type="text/event-stream"
    )

@router.post("/switch", response_model=SwitchContextResponse, summary="Manually switch context")
async def switch_context(
    request: SwitchContextRequest, 
    context_switching_service: ContextSwitchingService = Depends(get_context_switching_service)
):
    """Manually switch context to a different role"""
    try:
        # Get the current role ID before switching
        session = await context_switching_service.get_session(request.session_id)
        if not session:
            raise ValueError(f"Session {request.session_id} does not exist")
        
        previous_role_id = session["current_role_id"]
        
        # Switch the context
        updated_session = await context_switching_service.manually_switch_context(
            request.session_id,
            request.new_role_id,
            request.reason
        )
        
        return SwitchContextResponse(
            session_id=request.session_id,
            current_role_id=updated_session["current_role_id"],
            previous_role_id=previous_role_id,
            reason=request.reason,
            message="Context switched successfully"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/sessions/{session_id}", summary="Get session information")
async def get_session(
    session_id: str, 
    context_switching_service: ContextSwitchingService = Depends(get_context_switching_service)
):
    """Get information about a session"""
    session = await context_switching_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    return {
        "session_id": session_id,
        "current_role_id": session["current_role_id"],
        "last_switch_reason": session.get("last_switch_reason"),
        "switch_count": len(session["history"])
    }

@router.get("/sessions/{session_id}/history", summary="Get context switch history")
async def get_context_switch_history(
    session_id: str, 
    context_switching_service: ContextSwitchingService = Depends(get_context_switching_service)
):
    """Get the context switch history for a session"""
    try:
        history = await context_switching_service.get_context_switch_history(session_id)
        return {"history": history}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/sessions/{session_id}", summary="Close a session")
async def close_session(
    session_id: str, 
    context_switching_service: ContextSwitchingService = Depends(get_context_switching_service)
):
    """Close a session"""
    success = await context_switching_service.close_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    return {"message": "Session closed successfully"}
