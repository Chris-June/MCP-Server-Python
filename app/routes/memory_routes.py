from fastapi import APIRouter, Depends, Request, HTTPException, Query
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

# Define additional response models for new endpoints
from pydantic import BaseModel

class SemanticSearchRequest(BaseModel):
    """Request model for semantic memory search"""
    query: str = Field(..., description="Query to search for")
    role_id: str = Field(..., description="ID of the role to search memories for")
    limit: int = Field(5, description="Maximum number of memories to return")
    category: Optional[str] = Field(None, description="Optional category to filter by")
    tags: Optional[List[str]] = Field(default_factory=list, description="Optional tags to filter by")
    include_shared: bool = Field(True, description="Whether to include memories shared from other roles")
    cross_role: bool = Field(False, description="Whether to search across all roles")
    related_role_ids: Optional[List[str]] = Field(default_factory=list, description="Optional list of specific role IDs to include in the search")

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
    category: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    include_shared: bool = True,
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Get memories for a specific role
    
    Args:
        role_id: ID of the role to get memories for
        memory_type: Optional type of memories to retrieve
        category: Optional category to filter by
        tags: Optional list of tags to filter by
        include_shared: Whether to include memories shared from other roles
    """
    memories = await memory_service.get_memories_by_role_id(
        role_id, 
        memory_type=memory_type,
        category=category,
        tags=tags,
        include_shared=include_shared
    )
    
    return MemoriesResponse(memories=memories)

@router.delete("/{role_id}", response_model=ClearMemoriesResponse, summary="Clear memories for a specific role")
async def clear_memories(
    role_id: str, 
    memory_type: Optional[Literal["session", "user", "knowledge"]] = None,
    category: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    shared_only: bool = False,
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Clear memories for a specific role
    
    Args:
        role_id: ID of the role to clear memories for
        memory_type: Optional type of memories to clear
        category: Optional category of memories to clear
        tags: Optional tags to filter which memories to clear
        shared_only: If True, only clear memories that were shared from other roles
    """
    success = await memory_service.clear_memories_by_role_id(
        role_id, 
        memory_type=memory_type,
        category=category,
        tags=tags,
        shared_only=shared_only
    )
    
    return ClearMemoriesResponse(
        success=success,
        message="Memories cleared successfully"
    )

@router.post("/semantic-search", response_model=MemoriesResponse, summary="Search memories semantically across roles")
async def semantic_search(
    search_request: SemanticSearchRequest,
    memory_service: MemoryService = Depends(get_memory_service),
    ai_processor: AIProcessor = Depends(get_ai_processor)
):
    """Search memories semantically based on query relevance
    
    This endpoint allows for semantic search across memories, optionally spanning multiple roles.
    It uses vector embeddings to find memories that are semantically similar to the query.
    
    Args:
        search_request: The search parameters including query and filters
    """
    # Create embedding for the query
    embedding = await ai_processor.create_embedding(search_request.query)
    
    # Get relevant memories
    memories = await memory_service.get_relevant_memories(
        role_id=search_request.role_id,
        query=search_request.query,
        embedding=embedding,
        limit=search_request.limit,
        category=search_request.category,
        tags=search_request.tags,
        include_shared=search_request.include_shared,
        cross_role=search_request.cross_role,
        related_role_ids=search_request.related_role_ids
    )
    
    return MemoriesResponse(memories=memories)

@router.post("/{role_id}/share", response_model=MemoryResponse, summary="Share a memory with other roles")
async def share_memory(
    role_id: str,
    memory_id: str,
    target_role_ids: List[str],
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Share an existing memory with other roles
    
    Args:
        role_id: ID of the role that owns the memory
        memory_id: ID of the memory to share
        target_role_ids: List of role IDs to share the memory with
    """
    # Get all memories for the role
    memories = await memory_service.get_memories_by_role_id(role_id)
    
    # Find the specific memory
    memory_to_share = next((m for m in memories if m.id == memory_id), None)
    
    if not memory_to_share:
        raise HTTPException(status_code=404, detail="Memory not found")
    
    # Update the memory's shared_with list
    memory_to_share.shared_with.extend([rid for rid in target_role_ids if rid not in memory_to_share.shared_with])
    
    # Re-store the memory to trigger sharing logic
    memory_create = MemoryCreate(
        role_id=memory_to_share.role_id,
        content=memory_to_share.content,
        type=memory_to_share.type,
        importance=memory_to_share.importance,
        tags=memory_to_share.tags,
        category=memory_to_share.category,
        shared_with=memory_to_share.shared_with,
        parent_memory_id=memory_to_share.parent_memory_id
    )
    
    # Store with existing embedding
    updated_memory = await memory_service.store_memory(memory_create, memory_to_share.embedding)
    
    return MemoryResponse(memory=updated_memory)

@router.get("/shared/{role_id}", response_model=MemoriesResponse, summary="Get memories shared with a role")
async def get_shared_memories(
    role_id: str,
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Get memories that have been shared with a specific role
    
    Args:
        role_id: ID of the role to get shared memories for
    """
    # Get all memories for the role
    all_memories = await memory_service.get_memories_by_role_id(role_id)
    
    # Filter to only include shared memories (those with a parent_memory_id)
    shared_memories = [m for m in all_memories if m.parent_memory_id]
    
    return MemoriesResponse(memories=shared_memories)
