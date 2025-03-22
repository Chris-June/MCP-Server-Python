from fastapi import APIRouter, Depends
from app.config import settings

router = APIRouter()

@router.get("/health", summary="Health check endpoint")
async def health_check():
    """Check if the server is running"""
    return {
        "status": "ok",
        "version": settings.app_version
    }
