# MCP (Model Context Protocol) Server Architecture

## Overview
The MCP Server is a sophisticated, modular AI-powered platform designed to provide intelligent, context-aware conversational capabilities. It leverages multiple LLM providers (OpenAI, Anthropic, and Google Gemini), FastAPI, and Pyppeteer for web browsing capabilities to deliver nuanced, contextually relevant responses across various business domains.

## Core Architecture Components

### 1. System Architecture
```
                    ┌─────────────┐     ┌─────────────┐
                    │  FastAPI    │     │  OpenAI     │
                    │  Server     │────▶│  API        │
                    │  (MCP)      │     └─────────────┘
                    │             │     ┌─────────────┐
                    │             │────▶│  Anthropic  │
                    │             │     │  API        │
                    │             │     └─────────────┘
                    │             │     ┌─────────────┐
                    │             │────▶│  Google     │
                    │             │     │  Gemini API │
                    │             │     └─────────────┘
                    │             │     ┌─────────────┐
                    │             │────▶│  Pyppeteer  │
                    └─────────────┘     │  Browser    │
                         ▲              └─────────────┘
                         │
                    ┌────┴────────┐
                    │ Any Client  │
                    │ (via REST)  │
                    └─────────────┘
```

**Note:** This repository contains only the MCP server implementation. The diagram shows how any client can interact with the MCP server through its RESTful API.

### 2. Key Architectural Principles
- **Modularity**: Loosely coupled components for easy maintenance and extension
- **Context Awareness**: Advanced memory and vector similarity search
- **Asynchronous Processing**: Non-blocking operations for better performance
- **Type Safety**: Strong typing with Pydantic models
- **Dependency Injection**: Services receive dependencies through constructors

### 3. Technology Stack
- **Backend**: Python with asyncio
- **Web Framework**: FastAPI
- **AI Models**: 
  - OpenAI GPT-4o-mini
  - Anthropic Claude models
  - Google Gemini models
- **Browser Automation**: Pyppeteer (Python port of Puppeteer)
- **Vector Operations**: NumPy for embedding similarity
- **API Documentation**: Swagger UI via FastAPI
- **Frontend Technologies** (for client examples):
  - React
  - TypeScript
  - TailwindCSS
  - shadcn/ui
  - Framer Motion
  - Vite

### 4. Key Modules
- **Routes**: RESTful API endpoint definitions for roles, memories, browser sessions, context switching, multi-modal processing, LLM providers, and domain analysis
- **Services**: Core business logic components:
  - **RoleService**: Manages role definitions and query processing
  - **MemoryService**: Handles memory storage, retrieval, and vector similarity search
  - **BrowserService**: Controls web browsing sessions and interactions
  - **TriggerService**: Analyzes content for domain-specific triggers
  - **ContextSwitchingService**: Manages dynamic role transitions
  - **MultiModalProcessor**: Processes images and other media types
  - **DomainAnalysisService**: Provides domain-specific contextual analysis
  - **LLM Providers**: Modular system for multiple AI model providers
- **Models**: Pydantic data structures for request/response validation
- **AI Processor**: Orchestrates interactions with multiple LLM providers
- **Browser Integration**: Controls headless browser for web interactions
- **Config**: Environment-based configuration management

## Component Interactions

### Standard Query Processing Flow
1. Client sends query to `/roles/process` endpoint
2. RoleService retrieves the specified role
3. Query embedding is generated for memory retrieval
4. Relevant memories are retrieved based on vector similarity
5. Domain-specific analysis is performed based on role's domains of expertise
6. Complete system prompt is generated with role instructions, memories, and domain-specific guidance
7. AIProcessor selects the appropriate LLM provider based on configuration
8. Response is generated and returned to client

### Multi-Modal Processing Flow
1. Client sends query with media (e.g., image) to `/multimodal/process` endpoint
2. MultiModalProcessor validates and processes the media content
3. Role and context information is retrieved
4. Appropriate vision-capable model is selected from available providers
5. Media is encoded and sent along with the query to the LLM provider
6. Response is generated incorporating insights from both text and media
7. Response is returned to client

### Domain Analysis Flow
1. Client sends content to `/domain-analysis/analyze` endpoint with a role ID
2. DomainAnalysisService retrieves the role's domains of expertise
3. Content is analyzed for domain-specific terminology and patterns
4. Relevant metrics and frameworks are identified for each domain
5. Analysis results are returned with domain-specific insights
6. When used internally, this analysis enhances the system prompt with domain-specific guidance

### Context Switching Flow
1. Client sends query to `/context/process` endpoint with session ID
2. ContextSwitchingService retrieves the current session information
3. TriggerService analyzes the query for domain-specific triggers
4. If triggers for a different role are detected above threshold, context switch occurs
5. System prompt is enhanced with context transition information
6. Query is processed using the new role with appropriate context
7. Response is returned with context switching metadata
8. Response is returned to client and stored as a session memory

### Web Browser Integration Flow
1. Client creates a browser session via `/sessions` endpoint
2. BrowserService launches a headless browser instance
3. Client navigates to a URL using `/sessions/{session_id}/navigate`
4. Content is extracted and processed for AI consumption
5. AI can interact with the page through click, fill, and evaluate endpoints

### LLM Provider Selection Flow
1. Client specifies provider preference in the request (optional)
2. If no provider is specified, the default provider from configuration is used
3. AIProcessor validates the requested provider is available
4. Provider-specific parameters and model settings are applied
5. Request is formatted according to the provider's API requirements
6. Response is processed and normalized to a consistent format
7. If streaming is requested, responses are streamed in real-time using SSE

## Design Philosophy
The MCP Server is built on the principle of providing intelligent, adaptive conversational experiences that can understand and respond to complex business contexts with high precision and relevance. It combines role-based advisory capabilities with memory management and web browsing to create a comprehensive AI assistant platform.

## Extensibility
The architecture is designed to be easily extended, allowing for:
- Custom AI advisor roles with specific instructions, tones, and domains of expertise
- Different memory types with configurable importance, expiration, and tagging
- Flexible web browsing capabilities for research and information gathering
- Multi-modal processing for handling images and other media types
- Multiple LLM providers with a consistent interface
- Domain-specific analysis templates for specialized business areas
- Streaming responses for real-time interactions

## Performance Considerations
- Asynchronous processing for non-blocking operations
- Vector similarity search for efficient memory retrieval
- In-memory storage for fast access (with plans for database integration)
- Optimized browser interactions with configurable timeouts
- Provider-specific optimizations for each LLM service
- Streaming responses to reduce perceived latency
- Efficient multi-modal content processing
- Domain-specific pattern extraction for targeted analysis

## Security Principles
- Secure API key management for all LLM providers via environment variables
- Comprehensive input validation with Pydantic models
- Structured error handling with appropriate HTTP status codes
- Secure browser session management and isolation
- Provider-specific security measures for each LLM service
- Safe handling of multi-modal content
- Controlled domain-specific analysis with validation

## Future Roadmap
- Database integration for persistent storage of roles and memories
- Vector database integration (ChromaDB, Supabase) for enhanced semantic search
- JWT-based authentication with Supabase Auth
- Rate limiting for API endpoints
- Client SDK for easier integration
- Comprehensive unit and integration tests
- WebSocket support for bidirectional communication
- Role templates for quick creation
- Role versioning and history
- Support for LangGraph agents and RAG pipelines
- Docker containerization for better deployment and scaling
- Enhanced browser capabilities with session persistence and cookie management
