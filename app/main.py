from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.routes import role_routes, memory_routes, healthcheck
from app.services.role_service import RoleService
from app.services.memory_service import MemoryService
from app.services.ai_processor import AIProcessor

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services and cleanup on shutdown"""
    # Initialize services
    ai_processor = AIProcessor()
    memory_service = MemoryService()
    role_service = RoleService(memory_service, ai_processor)
    
    # Add services to app state
    app.state.ai_processor = ai_processor
    app.state.memory_service = memory_service
    app.state.role_service = role_service
    
    yield
    
    # Clean up resources
    await memory_service.close()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Role-Specific Context MCP Server for AI orchestration",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(healthcheck.router, tags=["Health"])
app.include_router(role_routes.router, prefix=settings.api_prefix, tags=["Roles"])
app.include_router(memory_routes.router, prefix=settings.api_prefix, tags=["Memory"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Role-Specific Context MCP Server",
        "version": settings.app_version,
        "documentation": "/docs"
    }
