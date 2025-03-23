# MCP Server API Documentation

This document serves as an index for all API endpoints available in the MCP Server. Each API category has its own dedicated documentation file with comprehensive details, example requests, and responses.

## Documentation Structure

The API documentation is organized into multiple files for easier navigation:

- **API_DOCUMENTATION.md** (this file): Index of all API documentation
- **[API_ROLE_MANAGEMENT.md](API_ROLE_MANAGEMENT.md)**: Role Management endpoints
- **[API_MEMORY_MANAGEMENT.md](API_MEMORY_MANAGEMENT.md)**: Memory Management endpoints
- **[API_QUERY_PROCESSING.md](API_QUERY_PROCESSING.md)**: Query Processing endpoints
- **[API_DOMAIN_ANALYSIS.md](API_DOMAIN_ANALYSIS.md)**: Domain Analysis endpoints
- **[API_MULTIMODAL.md](API_MULTIMODAL.md)**: Multi-Modal Processing endpoints
- **[API_LLM_PROVIDERS.md](API_LLM_PROVIDERS.md)**: LLM Provider Management endpoints
- **[API_CONTEXT_SWITCHING.md](API_CONTEXT_SWITCHING.md)**: Context Switching endpoints
- **[API_WEB_BROWSER.md](API_WEB_BROWSER.md)**: Web Browser Automation endpoints

## API Categories

### [Role Management](API_ROLE_MANAGEMENT.md)

Endpoints for creating, retrieving, updating, and deleting AI advisor roles.

- `GET /api/v1/roles` - List all roles
- `GET /api/v1/roles/{role_id}` - Get role by ID
- `POST /api/v1/roles` - Create a new role
- `PUT /api/v1/roles/{role_id}` - Update a role
- `DELETE /api/v1/roles/{role_id}` - Delete a role

### [Memory Management](API_MEMORY_MANAGEMENT.md)

Endpoints for managing role-specific memories.

- `GET /api/v1/memories` - List all memories
- `GET /api/v1/memories/{memory_id}` - Get memory by ID
- `POST /api/v1/memories` - Create a new memory
- `PUT /api/v1/memories/{memory_id}` - Update a memory
- `DELETE /api/v1/memories/{memory_id}` - Delete a memory
- `GET /api/v1/memories/role/{role_id}` - List memories for a role
- `DELETE /api/v1/memories/{role_id}` - Clear all memories for a role

### [Query Processing](API_QUERY_PROCESSING.md)

Endpoints for processing queries with role-specific context.

- `POST /api/v1/roles/process` - Process a query
- `POST /api/v1/roles/process-stream` - Process a query with streaming response

### [Domain Analysis](API_DOMAIN_ANALYSIS.md)

Endpoints for domain-specific analysis capabilities.

- `GET /api/v1/domain-analysis/domains` - Get all domain templates
- `GET /api/v1/domain-analysis/domains/{domain}` - Get a specific domain template
- `POST /api/v1/domain-analysis/analyze` - Analyze content

### [Multi-Modal Processing](API_MULTIMODAL.md)

Endpoints for processing multi-modal content (text + images).

- `POST /api/v1/multimodal/process` - Process multi-modal content
- `POST /api/v1/multimodal/process-stream` - Process multi-modal content with streaming response

### [LLM Provider Management](API_LLM_PROVIDERS.md)

Endpoints for managing LLM providers and their configurations.

- `GET /api/v1/llm-providers` - Get available LLM providers
- `PUT /api/v1/llm-providers/default` - Set default LLM provider
- `GET /api/v1/llm-providers/{provider_id}/config` - Get LLM provider configuration
- `PUT /api/v1/llm-providers/{provider_id}/config` - Update LLM provider configuration

### [Context Switching](API_CONTEXT_SWITCHING.md)

Endpoints for managing conversation context and sessions.

- `POST /api/v1/context/sessions` - Create a new session
- `GET /api/v1/context/sessions/{session_id}` - Get session information
- `POST /api/v1/context/sessions/{session_id}/query` - Process query with context
- `GET /api/v1/context/sessions/{session_id}/history` - Get session history
- `DELETE /api/v1/context/sessions/{session_id}` - Delete a session

### [Web Browser](API_WEB_BROWSER.md)

Endpoints for web browser automation.

- `POST /api/v1/browser/sessions` - Create browser session
- `DELETE /api/v1/browser/sessions/{session_id}` - Close browser session
- `POST /api/v1/browser/sessions/{session_id}/navigate` - Navigate to URL
- `GET /api/v1/browser/sessions/{session_id}/content` - Get current page content
- `POST /api/v1/browser/sessions/{session_id}/screenshot` - Take screenshot
- `POST /api/v1/browser/sessions/{session_id}/click` - Click element
- `POST /api/v1/browser/sessions/{session_id}/fill` - Fill form field
- `POST /api/v1/browser/sessions/{session_id}/execute` - Execute JavaScript
