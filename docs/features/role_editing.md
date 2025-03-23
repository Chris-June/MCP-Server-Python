# Role Editing Functionality

## Overview

The MCP server includes comprehensive role editing capabilities, allowing users to modify existing custom roles. This feature enables dynamic adjustment of AI advisor behaviors, instructions, domains of expertise, and communication tones to better suit evolving requirements.

## Features

- **Update Role Properties**: Modify name, description, and instructions
- **Adjust Domains**: Update areas of expertise for the role
- **Change Tone**: Modify the communication style (strategic, analytical, creative, etc.)
- **Revise System Prompt**: Update the base system prompt for the role
- **Validation**: Ensure updates meet system requirements
- **Default Role Protection**: Prevent modification of system-defined default roles

## How to Use

### API Endpoint

The role editing functionality is accessible through the following API endpoint:

```
PATCH /api/v1/roles/{role_id}
```

Parameters:
- `role_id`: The unique identifier of the role to update

Request body should contain a JSON object with the fields to update. All fields are optional:

```json
{
  "name": "Updated Role Name",
  "description": "Updated role description",
  "instructions": "New instructions for the role",
  "domains": ["finance", "marketing", "operations"],
  "tone": "analytical",
  "system_prompt": "You are an updated AI advisor..."
}
```

Response:

```json
{
  "role": {
    "id": "role-id",
    "name": "Updated Role Name",
    "description": "Updated role description",
    "instructions": "New instructions for the role",
    "domains": ["finance", "marketing", "operations"],
    "tone": "analytical",
    "system_prompt": "You are an updated AI advisor...",
    "is_default": false
  }
}
```

## Example Code

### Python Example

```python
import httpx
import asyncio

async def update_role():
    role_id = "custom-advisor"
    update_data = {
        "name": "Updated Custom Advisor",
        "description": "A more specialized business advisor",
        "domains": ["strategic planning", "market analysis", "competitive intelligence"],
        "tone": "analytical"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"http://localhost:8000/api/v1/roles/{role_id}",
            json=update_data
        )
        
        if response.status_code == 200:
            updated_role = response.json()["role"]
            print(f"Role updated successfully: {updated_role['name']}")
        else:
            print(f"Error updating role: {response.text}")

# Run the example
asyncio.run(update_role())
```

### JavaScript/Fetch Example

```javascript
async function updateRole() {
  const roleId = 'custom-advisor';
  const updateData = {
    name: 'Updated Custom Advisor',
    description: 'A more specialized business advisor',
    domains: ['strategic planning', 'market analysis', 'competitive intelligence'],
    tone: 'analytical'
  };
  
  try {
    const response = await fetch(`/api/v1/roles/${roleId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updateData)
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('Role updated successfully:', data.role);
      return data.role;
    } else {
      const errorData = await response.json();
      console.error('Error updating role:', errorData);
      throw new Error(errorData.detail || 'Failed to update role');
    }
  } catch (error) {
    console.error('Request failed:', error);
    throw error;
  }
}
```

## Implementation Details

### Backend Service

The role editing functionality is implemented in the `RoleService` class, which handles the following:

1. **Validation**: Ensures the role exists and is not a default role
2. **Tone Verification**: Validates that the provided tone is supported
3. **Partial Updates**: Only updates the fields provided in the request
4. **Response Generation**: Returns the complete updated role object

### Data Model

The `RoleUpdate` model defines the structure for role updates:

```python
class RoleUpdate(BaseModel):
    """Model for updating an existing role"""
    name: Optional[str] = Field(None, description="Human-readable name for the role")
    description: Optional[str] = Field(None, description="Description of the role's purpose")
    instructions: Optional[str] = Field(None, description="Custom instructions for the role")
    domains: Optional[List[str]] = Field(None, description="Areas of expertise")
    tone: Optional[str] = Field(None, description="Communication tone (strategic, analytical, creative, etc.)")
    system_prompt: Optional[str] = Field(None, description="Base system prompt for this role")
```

## Best Practices

### When to Update Roles

- **Refining Expertise**: When you need to adjust the role's domain knowledge
- **Changing Communication Style**: When a different tone would better serve your users
- **Improving Instructions**: When you discover better prompting techniques
- **Expanding Capabilities**: When adding new functionalities to a role

### Tips for Effective Role Updates

1. **Be Specific**: Provide clear, detailed instructions in the role definition
2. **Test Changes**: Validate role updates with sample queries
3. **Incremental Updates**: Make small, focused changes rather than completely redefining a role
4. **Document Changes**: Keep track of role modifications for future reference
5. **Consider Context**: Ensure updated roles maintain compatibility with existing memories

## Limitations

- Default system roles cannot be modified
- Role IDs cannot be changed after creation
- Changes to a role will affect all future interactions but won't retroactively modify past responses

## Troubleshooting

- If you receive a 404 error, verify that the role ID exists
- If you receive a 403 error, you may be attempting to modify a default role
- If you receive a 400 error when updating the tone, check that you're using a supported tone value
