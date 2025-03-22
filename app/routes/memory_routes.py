from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List, Optional, Literal
from app.models.memory import Memory, MemoryCreate, MemoryResponse, MemoriesResponse, ClearMemoriesResponse
from app.services.memory_service import MemoryService
from app.services.ai_processor import AIProcessor

router = APIRouter(prefix="/memories")

async def get_memory_service(request: Request) -> MemoryService:
    """Dependency for getting the memory service"""
    return request.app.state.memory_service

async def get_ai_processor(request: Request) -> AIProcessor:
    """Dependency for getting the AI processor"""
    return request.app.state.ai_processor

@router.post("", response_model=MemoryResponse, status_code=201, summary="Store a memory for a specific role")
async def store_memory(
    memory_create: MemoryCreate, 
    memory_service: MemoryService = Depends(get_memory_service),
    ai_processor: AIProcessor = Depends(get_ai_processor)
):
    """Store a memory for a specific role"""
    # Create embedding for the memory content
    embedding = await ai_processor.create_embedding(memory_create.content)
    
    # Store the memory
    memory = await memory_service.store_memory(memory_create, embedding)
    
    return MemoryResponse(memory=memory)

@router.get("/{role_id}", response_model=MemoriesResponse, summary="Get memories for a specific role")
async def get_memories(
    role_id: str, 
    memory_type: Optional[Literal["session", "user", "knowledge"]] = None,
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Get memories for a specific role"""
    memories = await memory_service.get_memories_by_role_id(role_id, memory_type)
    
    return MemoriesResponse(memories=memories)

@router.delete("/{role_id}", response_model=ClearMemoriesResponse, summary="Clear memories for a specific role")
async def clear_memories(
    role_id: str, 
    memory_type: Optional[Literal["session", "user", "knowledge"]] = None,
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Clear memories for a specific role"""
    success = await memory_service.clear_memories_by_role_id(role_id, memory_type)
    
    return ClearMemoriesResponse(
        success=success,
        message="Memories cleared successfully"
    )
