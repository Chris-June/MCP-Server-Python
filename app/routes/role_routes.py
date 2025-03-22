from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List, Optional
from app.models.role import Role, RoleCreate, RoleUpdate, RoleResponse, RolesResponse, ProcessRequest, ProcessResponse
from app.services.role_service import RoleService
from app.config import TONE_PROFILES

router = APIRouter(prefix="/roles")

async def get_role_service(request: Request) -> RoleService:
    """Dependency for getting the role service"""
    return request.app.state.role_service

@router.get("", response_model=RolesResponse, summary="Get all available roles")
async def get_roles(role_service: RoleService = Depends(get_role_service)):
    """Get all available roles"""
    roles = await role_service.get_roles()
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

@router.get("/tones", summary="Get all available tone profiles")
async def get_tones():
    """Get all available tone profiles"""
    return {"tones": TONE_PROFILES}
