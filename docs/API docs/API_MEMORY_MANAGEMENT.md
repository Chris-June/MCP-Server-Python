# Memory Management API

This document provides comprehensive documentation for the memory management endpoints in the MCP Server, including example requests and responses.

## Table of Contents

- [List All Memories](#list-all-memories)
- [Get Memory by ID](#get-memory-by-id)
- [Create a New Memory](#create-a-new-memory)
- [Update a Memory](#update-a-memory)
- [Delete a Memory](#delete-a-memory)
- [List Memories for a Role](#list-memories-for-a-role)
- [Clear All Memories for a Role](#clear-all-memories-for-a-role)

## List All Memories

```
GET /api/v1/memories
```

**Description:** Retrieves a list of all memories across all roles.

**Parameters:**
- `limit` (query parameter, optional): Maximum number of memories to return (default: 50).
- `offset` (query parameter, optional): Number of memories to skip (for pagination).
- `type` (query parameter, optional): Filter by memory type (e.g., "preference", "fact", "context").

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/memories?limit=10&type=preference' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "memories": [
    {
      "id": "mem-001",
      "role_id": "financial-advisor",
      "content": "The user prefers low-risk investments.",
      "type": "preference",
      "importance": 0.8,
      "created_at": "2025-03-20T11:30:15Z",
      "updated_at": "2025-03-20T11:30:15Z"
    },
    {
      "id": "mem-002",
      "role_id": "marketing-specialist",
      "content": "The user prefers data-driven marketing approaches.",
      "type": "preference",
      "importance": 0.9,
      "created_at": "2025-03-21T09:45:30Z",
      "updated_at": "2025-03-21T09:45:30Z"
    }
  ],
  "total": 2,
  "limit": 10,
  "offset": 0
}
```

## Get Memory by ID

```
GET /api/v1/memories/{memory_id}
```

**Description:** Retrieves detailed information about a specific memory.

**Parameters:**
- `memory_id` (path parameter): The unique identifier of the memory.

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/memories/mem-001' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "id": "mem-001",
  "role_id": "financial-advisor",
  "content": "The user prefers low-risk investments.",
  "type": "preference",
  "importance": 0.8,
  "created_at": "2025-03-20T11:30:15Z",
  "updated_at": "2025-03-20T11:30:15Z",
  "metadata": {
    "source": "user-conversation",
    "confidence": "high"
  }
}
```

## Create a New Memory

```
POST /api/v1/memories
```

**Description:** Creates a new memory for a specific role.

**Request Body:**
```json
{
  "role_id": "string",
  "content": "string",
  "type": "string",
  "importance": number,  // Optional, 0.0 to 1.0, default: 0.5
  "metadata": {}  // Optional
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/memories' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "role_id": "financial-advisor",
  "content": "The user is interested in sustainable investing options.",
  "type": "preference",
  "importance": 0.7
}'
```

**Example Response:**
```json
{
  "id": "mem-003",
  "role_id": "financial-advisor",
  "content": "The user is interested in sustainable investing options.",
  "type": "preference",
  "importance": 0.7,
  "created_at": "2025-03-23T14:20:15Z",
  "updated_at": "2025-03-23T14:20:15Z",
  "metadata": {}
}
```

## Update a Memory

```
PUT /api/v1/memories/{memory_id}
```

**Description:** Updates an existing memory.

**Parameters:**
- `memory_id` (path parameter): The unique identifier of the memory to update.

**Request Body:**
```json
{
  "content": "string",  // Optional
  "type": "string",  // Optional
  "importance": number,  // Optional, 0.0 to 1.0
  "metadata": {}  // Optional
}
```

**Example Request:**
```bash
curl -X 'PUT' \
  'http://localhost:8000/api/v1/memories/mem-003' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "The user is very interested in ESG and sustainable investing options.",
  "importance": 0.9
}'
```

**Example Response:**
```json
{
  "id": "mem-003",
  "role_id": "financial-advisor",
  "content": "The user is very interested in ESG and sustainable investing options.",
  "type": "preference",
  "importance": 0.9,
  "created_at": "2025-03-23T14:20:15Z",
  "updated_at": "2025-03-23T14:35:22Z",
  "metadata": {}
}
```

## Delete a Memory

```
DELETE /api/v1/memories/{memory_id}
```

**Description:** Deletes a specific memory.

**Parameters:**
- `memory_id` (path parameter): The unique identifier of the memory to delete.

**Example Request:**
```bash
curl -X 'DELETE' 'http://localhost:8000/api/v1/memories/mem-003' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "message": "Memory mem-003 deleted successfully"
}
```

## List Memories for a Role

```
GET /api/v1/memories/role/{role_id}
```

**Description:** Retrieves all memories associated with a specific role.

**Parameters:**
- `role_id` (path parameter): The unique identifier of the role.
- `limit` (query parameter, optional): Maximum number of memories to return (default: 50).
- `offset` (query parameter, optional): Number of memories to skip (for pagination).
- `type` (query parameter, optional): Filter by memory type.

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/memories/role/financial-advisor' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "role_id": "financial-advisor",
  "memories": [
    {
      "id": "mem-001",
      "content": "The user prefers low-risk investments.",
      "type": "preference",
      "importance": 0.8,
      "created_at": "2025-03-20T11:30:15Z"
    },
    {
      "id": "mem-003",
      "content": "The user is very interested in ESG and sustainable investing options.",
      "type": "preference",
      "importance": 0.9,
      "created_at": "2025-03-23T14:20:15Z"
    }
  ],
  "total": 2,
  "limit": 50,
  "offset": 0
}
```

## Clear All Memories for a Role

```
DELETE /api/v1/memories/{role_id}
```

**Description:** Deletes all memories associated with a specific role.

**Parameters:**
- `role_id` (path parameter): The unique identifier of the role.

**Example Request:**
```bash
curl -X 'DELETE' 'http://localhost:8000/api/v1/memories/financial-advisor' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "message": "All memories for role financial-advisor deleted successfully"
}
```
