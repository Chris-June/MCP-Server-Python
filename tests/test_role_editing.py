import pytest
import json
from unittest.mock import AsyncMock

from app.config import settings

from app.models.role import RoleCreate, RoleUpdate

# Test data for roles
test_role = {
    "id": "financial-analyst",
    "name": "Financial Analyst",
    "description": "Analyzes financial data and provides insights",
    "instructions": "Analyze financial statements and market trends",
    "domains": ["finance", "investment", "economics"],
    "tone": "analytical",
    "system_prompt": "You are a financial analyst with expertise in market analysis and financial forecasting."
}

@pytest.fixture(autouse=True)
def setup_test_role(client):
    """Setup test role before each test"""
    from app.main import app
    role_service = app.state.role_service
    
    # Mock the get_role method to return test_role when called with test_role["id"]
    async def mock_get_role(role_id):
        if role_id == test_role["id"]:
            return test_role
        return None
    
    role_service.get_role = AsyncMock(side_effect=mock_get_role)
    
    # Mock other methods
    role_service.create_role = AsyncMock(return_value=test_role)
    role_service.update_role = AsyncMock(return_value=test_role)
    role_service.delete_role = AsyncMock(return_value=True)
    role_service.clone_role = AsyncMock(return_value=test_role)
    role_service.validate_system_prompt = AsyncMock(return_value={"valid": True})
    role_service.export_role = AsyncMock(return_value=test_role)
    role_service.import_role = AsyncMock(return_value=test_role)
    role_service.get_all_roles = AsyncMock(return_value=[test_role])
    
    yield


def test_create_role(client):
    """Test creating a new role"""
    new_role = {
        "id": "marketing-specialist",
        "name": "Marketing Specialist",
        "description": "Specializes in marketing strategy and campaign analysis",
        "instructions": "Develop marketing strategies and analyze campaign performance",
        "domains": ["marketing", "advertising", "branding"],
        "tone": "creative",
        "system_prompt": "You are a marketing specialist with expertise in digital marketing and brand development."
    }
    
    # Mock the response for create_role
    from app.main import app
    app.state.role_service.create_role.return_value = new_role
    
    response = client.post(f"{settings.api_prefix}/roles", json=new_role)
    assert response.status_code == 201
    
    # Verify create_role was called with the correct parameters
    app.state.role_service.create_role.assert_called_once()

def test_update_role(client):
    """Test updating an existing role"""
    role_id = test_role["id"]
    updated_data = {
        "name": "Senior Financial Analyst",
        "description": "Senior analyst specializing in complex financial data",
        "instructions": "Provide in-depth analysis of financial statements and market trends",
        "domains": ["finance", "investment", "economics", "risk-management"],
        "tone": "professional",
        "system_prompt": "You are a senior financial analyst with extensive experience in market analysis and financial forecasting."
    }
    
    # Mock the response for update_role
    from app.main import app
    updated_role = test_role.copy()
    updated_role.update(updated_data)
    app.state.role_service.update_role.return_value = updated_role
    
    response = client.patch(f"{settings.api_prefix}/roles/{role_id}", json=updated_data)
    assert response.status_code == 200
    
    # Verify the update_role method was called
    app.state.role_service.update_role.assert_called_once()


def test_partial_update_role(client):
    """Test partially updating a role"""
    role_id = test_role["id"]
    partial_update = {
        "name": "Updated Financial Analyst",
        "domains": ["finance", "investment", "economics", "banking"]
    }
    
    # Mock the response for partial update
    from app.main import app
    updated_role = test_role.copy()
    updated_role.update(partial_update)
    app.state.role_service.update_role.return_value = updated_role
    
    response = client.patch(f"{settings.api_prefix}/roles/{role_id}", json=partial_update)
    assert response.status_code == 200
    
    # Verify update_role was called with the correct parameters
    app.state.role_service.update_role.assert_called_once()


def test_delete_role(client):
    """Test deleting a role"""
    # Create a temporary role to delete
    temp_role = {
        "id": "temp-role",
        "name": "Temporary Role",
        "description": "Role for deletion test",
        "instructions": "This role will be deleted",
        "domains": ["test"],
        "tone": "neutral",
        "system_prompt": "You are a temporary test role."
    }
    
    # Mock the responses
    from app.main import app
    app.state.role_service.create_role.return_value = temp_role
    app.state.role_service.get_role.side_effect = lambda role_id: temp_role if role_id == temp_role["id"] else None
    app.state.role_service.delete_role.return_value = True
    
    # Add the temporary role
    response = client.post(f"{settings.api_prefix}/roles", json=temp_role)
    assert response.status_code == 201
    
    # Delete the role
    response = client.delete(f"{settings.api_prefix}/roles/{temp_role['id']}")
    assert response.status_code == 200
    
    # Verify delete_role was called
    app.state.role_service.delete_role.assert_called_once_with(temp_role["id"])


def test_clone_role(client):
    """Test cloning a role"""
    # Skip this test as the clone endpoint is not implemented yet
    pytest.skip("Clone endpoint not implemented yet")


def test_validate_role_system_prompt(client):
    """Test validating a role's system prompt"""
    # Skip this test as the validate system prompt endpoint is not implemented yet
    pytest.skip("Validate system prompt endpoint not implemented yet")


def test_export_role(client):
    """Test exporting a role"""
    # Skip this test as the export role endpoint is not implemented yet
    pytest.skip("Export role endpoint not implemented yet")


def test_import_role(client):
    """Test importing a role"""
    # Skip this test as the import role endpoint is not implemented yet
    pytest.skip("Import role endpoint not implemented yet")
