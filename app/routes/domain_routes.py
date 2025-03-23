from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict, List, Any, Optional
from app.models.role import Role
from app.services.role_service import RoleService
from app.services.domain_analysis_service import DomainAnalysisService

router = APIRouter()

# Dependency to get the role service
async def get_role_service():
    from app.main import app
    return app.state.role_service

# Dependency to get the domain analysis service
def get_domain_analysis_service():
    return DomainAnalysisService()

@router.get("/domains")
async def get_domain_templates(domain_analysis_service: DomainAnalysisService = Depends(get_domain_analysis_service)):
    """Get all available domain templates"""
    return {
        "domains": list(domain_analysis_service.get_domain_templates().keys()),
        "templates": domain_analysis_service.get_domain_templates()
    }

@router.get("/domains/{domain}")
async def get_domain_template(domain: str, domain_analysis_service: DomainAnalysisService = Depends(get_domain_analysis_service)):
    """Get a specific domain template"""
    template = domain_analysis_service.get_domain_template(domain)
    if not template:
        raise HTTPException(status_code=404, detail=f"Domain template not found for: {domain}")
    
    return {
        "domain": domain,
        "template": template
    }

@router.post("/analyze")
async def analyze_content(
    content: str = Body(..., embed=True),
    role_id: str = Body(..., embed=True),
    role_service: RoleService = Depends(get_role_service),
    domain_analysis_service: DomainAnalysisService = Depends(get_domain_analysis_service)
):
    """Analyze content based on role domains"""
    try:
        # Get the role
        role = await role_service.get_role(role_id)
        
        # Analyze content
        analysis = domain_analysis_service.analyze_content(content, role)
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
