from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.routes import role_routes, memory_routes, healthcheck, browser_routes, context_routes, multimodal_routes, provider_routes, domain_routes
from app.services.role_service import RoleService
from app.services.memory_service import MemoryService
from app.services.ai_processor import AIProcessor
from app.services.multimodal_processor import MultiModalProcessor
from app.services.web_browser.browser_service import BrowserService
from app.services.web_browser.browser_integration import BrowserIntegration
from app.services.trigger_service import TriggerService
from app.services.context_switching_service import ContextSwitchingService

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services and cleanup on shutdown"""
    # Initialize services
    browser_service = BrowserService()
    browser_integration = BrowserIntegration(browser_service)
    ai_processor = AIProcessor(browser_integration=browser_integration)
    multimodal_processor = MultiModalProcessor()
    memory_service = MemoryService()
    role_service = RoleService(memory_service, ai_processor)
    
    # Initialize context switching services
    trigger_service = TriggerService()
    context_switching_service = ContextSwitchingService(role_service, trigger_service)
    
    # Initialize browser service
    await browser_service.initialize()
    
    # Initialize triggers for all roles
    await context_switching_service.initialize_roles()
    
    # Add services to app state
    app.state.ai_processor = ai_processor
    app.state.multimodal_processor = multimodal_processor
    app.state.memory_service = memory_service
    app.state.role_service = role_service
    app.state.browser_service = browser_service
    app.state.trigger_service = trigger_service
    app.state.context_switching_service = context_switching_service
    
    yield
    
    # Clean up resources
    await memory_service.close()
    await browser_service.close()

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
app.include_router(browser_routes.router, prefix=settings.api_prefix + "/browser", tags=["Browser"])
app.include_router(context_routes.router, prefix=settings.api_prefix, tags=["Context Switching"])
app.include_router(multimodal_routes.router, prefix=settings.api_prefix, tags=["Multi-Modal"])
app.include_router(provider_routes.router, prefix=settings.api_prefix + "/providers", tags=["LLM Providers"])
app.include_router(domain_routes.router, prefix=settings.api_prefix + "/domain-analysis", tags=["Domain Analysis"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Role-Specific Context MCP Server",
        "version": settings.app_version,
        "documentation": "/docs"
    }
