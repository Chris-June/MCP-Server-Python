# MCP Server Routes

## Overview
Routes in the MCP Server define the API endpoints that enable intelligent, context-aware interactions and business advisory capabilities. The server follows a RESTful architecture with structured endpoint categories for role management, memory operations, and web browsing capabilities.

## Route Categories

### 1. Context Switching
- **`POST /api/context/sessions`**: Create a new session with an initial role
- **`GET /api/context/sessions/{session_id}`**: Get session information
- **`DELETE /api/context/sessions/{session_id}`**: Close a session
- **`POST /api/context/process`**: Process a query with context switching
- **`POST /api/context/process/stream`**: Process a query with context switching and streaming response
- **`POST /api/context/switch`**: Manually switch context to a different role
- **`GET /api/context/sessions/{session_id}/history`**: Get context switch history

### 2. Role Management
- **`GET /roles`**: Get all available roles with optional filtering (search, domains, tone)
- **`GET /roles/{role_id}`**: Get a specific role by ID
- **`POST /roles`**: Create a new custom role
- **`PATCH /roles/{role_id}`**: Update an existing role
- **`DELETE /roles/{role_id}`**: Delete a custom role
- **`POST /roles/process`**: Process a query using a specific role
- **`POST /roles/process/stream`**: Process a query with streaming response
- **`GET /roles/tones`**: Get all available tone profiles
- **`GET /roles/search`**: Search for roles by query text with optional filtering
- **`GET /roles/domains`**: Get all unique domains used across all roles

### 2. Memory Management
- **`POST /memories`**: Store a memory for a specific role
- **`GET /memories/{role_id}`**: Get memories for a specific role
- **`DELETE /memories/{role_id}`**: Clear memories for a specific role

### 3. Web Browser Integration
- **`POST /sessions`**: Create a new browser session
- **`DELETE /sessions/{session_id}`**: Close a browser session
- **`POST /sessions/{session_id}/navigate`**: Navigate to a URL
- **`GET /sessions/{session_id}/content`**: Get the current page content
- **`POST /sessions/{session_id}/screenshot`**: Take a screenshot
- **`POST /sessions/{session_id}/click`**: Click an element on the page
- **`POST /sessions/{session_id}/fill`**: Fill out an input field
- **`POST /sessions/{session_id}/evaluate`**: Execute JavaScript in the browser
- **`GET /sessions/{session_id}/history`**: Get the browsing history

### 4. Health Check
- **`GET /healthcheck`**: Check if the server is running

## Route Design Principles
- **RESTful Architecture**: Follows REST principles for resource management
- **Consistent Response Formats**: Structured JSON responses with appropriate status codes
- **Comprehensive Error Handling**: Detailed error messages with appropriate HTTP status codes
- **Dependency Injection**: Services are injected into route handlers for better testability
- **Async Processing**: All endpoints use async/await for non-blocking operations

## Advanced Routing Features
- **Streaming Responses**: Server-sent events for real-time AI responses
- **Vector Similarity Search**: Memory retrieval based on semantic similarity
- **Web Browser Automation**: Integrated web browsing capabilities
- **Role-based Context Management**: Context-aware processing based on role definitions
- **Automatic Context Switching**: Dynamic role selection based on query content
- **Session-based Conversations**: Maintaining conversation state across context switches
- **Context Transition Notifications**: Real-time notifications of role transitions
- **Role Search and Filtering**: Advanced search capabilities for finding roles by keywords, domains, and tone
- **Multi-Modal Processing**: Support for processing images alongside text queries

## Security Considerations
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Structured error responses with appropriate status codes
- **API Key Management**: Secure OpenAI API key handling via environment variables
- **Future Plans**: JWT-based authentication and role-based access control

## Example Route Handlers

### Process Query
```python
@router.post("/roles/process", response_model=ProcessResponse, summary="Process a query using a specific role")
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
```

### Search Roles
```python
@router.get("/roles/search", response_model=RolesResponse, summary="Search for roles")
async def search_roles(
    query: str,
    domains: Optional[List[str]] = Query(None),
    tone: Optional[str] = None,
    role_service: RoleService = Depends(get_role_service)
):
    """Search for roles based on query text, domains, and tone"""
    roles = await role_service.get_roles(search_query=query, domains=domains, tone=tone)
    return RolesResponse(roles=roles)
```

## Future Enhancements
- **GraphQL Integration**: Alternative query language for more flexible data retrieval
- **WebSocket Support**: Full bidirectional communication for real-time interactions
- **Advanced Semantic Routing**: Context-aware routing based on query intent
- **Multi-modal Input Handling**: Support for image and audio inputs
- **Authentication & Authorization**: JWT-based auth with role-based access control
- **Rate Limiting**: Protect against abuse and ensure fair resource allocation
