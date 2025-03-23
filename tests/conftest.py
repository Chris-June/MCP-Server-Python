import os
import sys
import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi.testclient import TestClient

# Add the parent directory to the Python path so that 'app' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the FastAPI app
from app.main import app

# Set asyncio default fixture loop scope to function
pytest_plugins = ["asyncio"]
pytest_asyncio_default_fixture_loop_scope = "function"

@pytest.fixture
def client():
    """Return a TestClient for testing the API endpoints"""
    # Create mock services
    app.state.role_service = MagicMock()
    app.state.memory_service = MagicMock()
    app.state.browser_service = MagicMock()
    app.state.ai_processor = MagicMock()
    app.state.context_service = MagicMock()
    app.state.multimodal_service = MagicMock()
    app.state.provider_factory = MagicMock()
    app.state.domain_service = MagicMock()
    
    # Set up async methods as AsyncMock
    for service_name in ['role_service', 'memory_service', 'browser_service', 'ai_processor', 
                       'context_service', 'multimodal_service', 'provider_factory', 'domain_service']:
        service = getattr(app.state, service_name)
        for method_name in dir(service):
            if not method_name.startswith('_') and callable(getattr(service, method_name)):
                setattr(service, method_name, AsyncMock())
    
    return TestClient(app)
