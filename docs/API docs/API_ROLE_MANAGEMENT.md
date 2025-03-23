# Role Management API

This document provides comprehensive documentation for the role management endpoints in the MCP Server, including example requests and responses.

## Table of Contents

- [List All Roles](#list-all-roles)
- [Get Role by ID](#get-role-by-id)
- [Create a New Role](#create-a-new-role)
- [Update a Role](#update-a-role)
- [Delete a Role](#delete-a-role)

## List All Roles

```
GET /api/v1/roles
```

**Description:** Retrieves a list of all available roles.

**Parameters:** None

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/roles' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "roles": [
    {
      "id": "financial-advisor",
      "name": "Financial Advisor",
      "description": "Expert in personal finance, investments, and retirement planning",
      "domains": ["finance", "investing", "retirement"],
      "created_at": "2025-03-20T10:15:30Z",
      "updated_at": "2025-03-20T10:15:30Z"
    },
    {
      "id": "marketing-specialist",
      "name": "Marketing Specialist",
      "description": "Expert in digital marketing, brand strategy, and market analysis",
      "domains": ["marketing", "branding", "social-media"],
      "created_at": "2025-03-20T10:16:45Z",
      "updated_at": "2025-03-21T14:30:22Z"
    }
  ],
  "total": 2
}
```

## Get Role by ID

```
GET /api/v1/roles/{role_id}
```

**Description:** Retrieves detailed information about a specific role.

**Parameters:**
- `role_id` (path parameter): The unique identifier of the role.

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/roles/financial-advisor' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "id": "financial-advisor",
  "name": "Financial Advisor",
  "description": "Expert in personal finance, investments, and retirement planning",
  "instructions": "Provide personalized financial advice. Focus on long-term wealth building strategies. Always consider risk tolerance and time horizon. Explain complex financial concepts in simple terms.",
  "domains": ["finance", "investing", "retirement"],
  "created_at": "2025-03-20T10:15:30Z",
  "updated_at": "2025-03-20T10:15:30Z",
  "memory_count": 3,
  "metadata": {
    "expertise_level": "advanced",
    "certification": "CFP"
  }
}
```

## Create a New Role

```
POST /api/v1/roles
```

**Description:** Creates a new AI advisor role.

**Request Body:**
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "instructions": "string",
  "domains": ["string"],
  "metadata": {}
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/roles' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "tech-writer",
  "name": "Technical Writer",
  "description": "Expert in creating clear technical documentation and tutorials",
  "instructions": "Create clear, concise technical documentation. Use simple language to explain complex concepts. Include examples where helpful.",
  "domains": ["technical-writing", "documentation", "tutorials"],
  "metadata": {
    "expertise_level": "intermediate",
    "specialization": "API documentation"
  }
}'
```

**Example Response:**
```json
{
  "id": "tech-writer",
  "name": "Technical Writer",
  "description": "Expert in creating clear technical documentation and tutorials",
  "instructions": "Create clear, concise technical documentation. Use simple language to explain complex concepts. Include examples where helpful.",
  "domains": ["technical-writing", "documentation", "tutorials"],
  "created_at": "2025-03-23T14:25:10Z",
  "updated_at": "2025-03-23T14:25:10Z",
  "metadata": {
    "expertise_level": "intermediate",
    "specialization": "API documentation"
  }
}
```

## Update a Role

```
PUT /api/v1/roles/{role_id}
```

**Description:** Updates an existing AI advisor role.

**Parameters:**
- `role_id` (path parameter): The unique identifier of the role to update.

**Request Body:**
```json
{
  "name": "string",  // Optional
  "description": "string",  // Optional
  "instructions": "string",  // Optional
  "domains": ["string"],  // Optional
  "metadata": {}  // Optional
}
```

**Example Request:**
```bash
curl -X 'PUT' \
  'http://localhost:8000/api/v1/roles/tech-writer' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Technical Documentation Specialist",
  "description": "Expert in creating clear technical documentation, tutorials, and API references",
  "domains": ["technical-writing", "documentation", "tutorials", "api-reference"],
  "metadata": {
    "expertise_level": "advanced",
    "specialization": "API documentation"
  }
}'
```

**Example Response:**
```json
{
  "id": "tech-writer",
  "name": "Technical Documentation Specialist",
  "description": "Expert in creating clear technical documentation, tutorials, and API references",
  "instructions": "Create clear, concise technical documentation. Use simple language to explain complex concepts. Include examples where helpful.",
  "domains": ["technical-writing", "documentation", "tutorials", "api-reference"],
  "created_at": "2025-03-23T14:25:10Z",
  "updated_at": "2025-03-23T14:30:45Z",
  "metadata": {
    "expertise_level": "advanced",
    "specialization": "API documentation"
  }
}
```

## Delete a Role

```
DELETE /api/v1/roles/{role_id}
```

**Description:** Deletes a specific AI advisor role.

**Parameters:**
- `role_id` (path parameter): The unique identifier of the role to delete.

**Example Request:**
```bash
curl -X 'DELETE' 'http://localhost:8000/api/v1/roles/tech-writer' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "message": "Role tech-writer deleted successfully"
}
```
