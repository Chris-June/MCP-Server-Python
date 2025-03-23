from fastapi import APIRouter, Depends, Request, HTTPException, Response, Query
from typing import List, Optional, AsyncGenerator
from fastapi.responses import StreamingResponse
from app.models.role import Role, RoleCreate, RoleUpdate, RoleResponse, RolesResponse, ProcessRequest, ProcessResponse
from app.services.role_service import RoleService
from app.config import TONE_PROFILES

router = APIRouter(prefix="/roles")

async def get_role_service(request: Request) -> RoleService:
    """Dependency for getting the role service"""
    return request.app.state.role_service

@router.get("", response_model=RolesResponse, summary="Get all available roles with optional filtering")
async def get_roles(
    search: Optional[str] = None,
    domains: Optional[List[str]] = Query(None),
    tone: Optional[str] = None,
    role_service: RoleService = Depends(get_role_service)
):
    """Get all available roles with optional filtering
    
    - **search**: Optional text to search in name, description, and instructions
    - **domains**: Optional list of domains to filter by
    - **tone**: Optional tone to filter by
    """
    roles = await role_service.get_roles(search_query=search, domains=domains, tone=tone)
    return RolesResponse(roles=roles)

@router.get("/{role_id}", response_model=RoleResponse, summary="Get a specific role by ID")
async def get_role(role_id: str, role_service: RoleService = Depends(get_role_service)):
    """Get a specific role by ID"""
    role = await role_service.get_role(role_id)
    return RoleResponse(role=role)

@router.post("", response_model=RoleResponse, status_code=201, summary="Create a new custom role")
async def create_role(role_create: RoleCreate, role_service: RoleService = Depends(get_role_service)):
    """Create a new custom role"""
    role = await role_service.create_role(role_create)
    return RoleResponse(role=role)

@router.patch("/{role_id}", response_model=RoleResponse, summary="Update an existing role")
async def update_role(role_id: str, role_update: RoleUpdate, role_service: RoleService = Depends(get_role_service)):
    """Update an existing role"""
    role = await role_service.update_role(role_id, role_update)
    return RoleResponse(role=role)

@router.delete("/{role_id}", summary="Delete a custom role")
async def delete_role(role_id: str, role_service: RoleService = Depends(get_role_service)):
    """Delete a custom role"""
    success = await role_service.delete_role(role_id)
    return {"success": success, "message": "Role deleted successfully"}

@router.post("/process", response_model=ProcessResponse, summary="Process a query using a specific role")
async def process_query(request: ProcessRequest, role_service: RoleService = Depends(get_role_service)):
    """Process a query using a specific role"""
    response = await role_service.process_query(
        request.role_id,
        request.query,
        request.custom_instructions
    )
    
    return ProcessResponse(
        role_id=request.role_id,
        query=request.query,
        response=response
    )

async def generate_stream_response(role_id: str, query: str, custom_instructions: Optional[str], role_service: RoleService) -> AsyncGenerator[str, None]:
    """Generate a streaming response for a query"""
    async for chunk in role_service.process_query_stream(role_id, query, custom_instructions):
        yield f"data: {chunk}\n\n"
    yield "data: [DONE]\n\n"

@router.post("/process/stream", summary="Process a query using a specific role with streaming response")
async def process_query_stream(request: ProcessRequest, role_service: RoleService = Depends(get_role_service)):
    """Process a query using a specific role with streaming response"""
    return StreamingResponse(
        generate_stream_response(
            request.role_id,
            request.query,
            request.custom_instructions,
            role_service
        ),
        media_type="text/event-stream"
    )

@router.get("/tones", summary="Get all available tone profiles")
async def get_tones():
    """Get all available tone profiles"""
    return {"tones": TONE_PROFILES}

@router.get("/search", response_model=RolesResponse, summary="Search for roles")
async def search_roles(
    query: str,
    domains: Optional[List[str]] = Query(None),
    tone: Optional[str] = None,
    role_service: RoleService = Depends(get_role_service)
):
    """Search for roles based on query text, domains, and tone
    
    - **query**: Text to search in name, description, and instructions
    - **domains**: Optional list of domains to filter by
    - **tone**: Optional tone to filter by
    """
    roles = await role_service.get_roles(search_query=query, domains=domains, tone=tone)
    return RolesResponse(roles=roles)

@router.get("/domains", summary="Get all unique domains across roles")
async def get_domains(role_service: RoleService = Depends(get_role_service)):
    """Get all unique domains used across all roles"""
    roles = await role_service.get_roles()
    # Extract all domains from all roles and create a unique set
    all_domains = set()
    for role in roles:
        all_domains.update(role.domains)
    return {"domains": sorted(list(all_domains))}

@router.get("/{role_id}/inheritance-chain", response_model=RolesResponse, summary="Get the inheritance chain for a role")
async def get_inheritance_chain(
    role_id: str, 
    role_service: RoleService = Depends(get_role_service)
):
    """Get the inheritance chain for a role
    
    Returns all roles in the inheritance chain, starting with the specified role
    and following parent relationships.
    """
    # Get the memory service from the role service
    memory_service = role_service.memory_service
    
    # Get the inheritance chain
    roles = await memory_service.get_role_inheritance_chain(role_id, role_service)
    
    return RolesResponse(roles=roles)

@router.get("/{role_id}/related-roles", response_model=RolesResponse, summary="Get roles related to a specific role")
async def get_related_roles(
    role_id: str, 
    role_service: RoleService = Depends(get_role_service)
):
    """Get roles related to a specific role
    
    Returns roles that share memories with the specified role or have inheritance relationships.
    """
    # Get the memory service from the role service
    memory_service = role_service.memory_service
    
    # Get related role IDs
    related_role_ids = await memory_service.get_related_roles(role_id, role_service)
    
    # Get the actual role objects
    related_roles = []
    for related_id in related_role_ids:
        role = await role_service.get_role(related_id)
        if role:
            related_roles.append(role)
    
    return RolesResponse(roles=related_roles)

@router.patch("/{role_id}/memory-access", response_model=RoleResponse, summary="Update memory access settings for a role")
async def update_memory_access(
    role_id: str,
    inherit_memories: Optional[bool] = None,
    memory_access_level: Optional[str] = None,
    memory_categories: Optional[List[str]] = Query(None),
    role_service: RoleService = Depends(get_role_service)
):
    """Update memory access settings for a role
    
    Args:
        role_id: ID of the role to update
        inherit_memories: Whether the role should inherit memories from its parent
        memory_access_level: Memory access level (standard, elevated, admin)
        memory_categories: Categories of memories this role specializes in
    """
    # Create a partial update object with only the provided fields
    update_data = {}
    if inherit_memories is not None:
        update_data["inherit_memories"] = inherit_memories
    if memory_access_level is not None:
        update_data["memory_access_level"] = memory_access_level
    if memory_categories is not None:
        update_data["memory_categories"] = memory_categories
    
    # Create a RoleUpdate object with the update data
    role_update = RoleUpdate(**update_data)
    
    # Update the role
    role = await role_service.update_role(role_id, role_update)
    
    return RoleResponse(role=role)

@router.patch("/{role_id}/parent-role/{parent_id}", response_model=RoleResponse, summary="Set the parent role for inheritance")
async def set_parent_role(
    role_id: str,
    parent_id: str,
    role_service: RoleService = Depends(get_role_service)
):
    """Set the parent role for inheritance
    
    Args:
        role_id: ID of the role to update
        parent_id: ID of the parent role
    """
    # Check if the parent role exists
    parent_role = await role_service.get_role(parent_id)
    if not parent_role:
        raise HTTPException(status_code=404, detail="Parent role not found")
    
    # Check for circular inheritance
    memory_service = role_service.memory_service
    inheritance_chain = await memory_service.get_role_inheritance_chain(parent_id, role_service)
    if any(role.id == role_id for role in inheritance_chain):
        raise HTTPException(status_code=400, detail="Circular inheritance detected")
    
    # Create a RoleUpdate object with the parent role ID
    role_update = RoleUpdate(parent_role_id=parent_id)
    
    # Update the role
    role = await role_service.update_role(role_id, role_update)
    
    return RoleResponse(role=role)

@router.delete("/{role_id}/parent-role", response_model=RoleResponse, summary="Remove the parent role inheritance")
async def remove_parent_role(
    role_id: str,
    role_service: RoleService = Depends(get_role_service)
):
    """Remove the parent role inheritance
    
    Args:
        role_id: ID of the role to update
    """
    # Create a RoleUpdate object with null parent role ID
    role_update = RoleUpdate(parent_role_id=None, inherit_memories=False)
    
    # Update the role
    role = await role_service.update_role(role_id, role_update)
    
    return RoleResponse(role=role)
