# MCP (Model Context Protocol) Server Architecture

## Overview
The MCP Server is a sophisticated, modular AI-powered platform designed to provide intelligent, context-aware conversational capabilities. It leverages OpenAI's GPT-4o-mini model, FastAPI, and Pyppeteer for web browsing capabilities to deliver nuanced, contextually relevant responses across various business domains.

## Core Architecture Components

### 1. System Architecture
```
                    ┌─────────────┐     ┌─────────────┐
                    │  FastAPI    │     │  OpenAI     │
                    │  Server     │────▶│  API        │
                    │  (MCP)      │     └─────────────┘
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
- **AI Model**: OpenAI GPT-4o-mini
- **Browser Automation**: Pyppeteer (Python port of Puppeteer)
- **Vector Operations**: NumPy for embedding similarity
- **API Documentation**: Swagger UI via FastAPI

### 4. Key Modules
- **Routes**: RESTful API endpoint definitions for roles, memories, browser sessions, and context switching
- **Services**: Core business logic including RoleService, MemoryService, BrowserService, TriggerService, and ContextSwitchingService
- **Models**: Pydantic data structures for request/response validation
- **AI Processor**: Handles interactions with OpenAI API
- **Browser Integration**: Controls headless browser for web interactions
- **Context Switching**: Manages dynamic role transitions based on conversation content

## Component Interactions

### Standard Query Processing Flow
1. Client sends query to `/roles/process` endpoint
2. RoleService retrieves the specified role
3. Query embedding is generated for memory retrieval
4. Relevant memories are retrieved based on vector similarity
5. Complete system prompt is generated with role instructions and memories
6. AIProcessor sends request to OpenAI API

### Context Switching Flow
1. Client sends query to `/context/process` endpoint with session ID
2. ContextSwitchingService retrieves the current session information
3. TriggerService analyzes the query for domain-specific triggers
4. If triggers for a different role are detected above threshold, context switch occurs
5. System prompt is enhanced with context transition information
6. Query is processed using the new role with appropriate context
7. Response is returned with context switching metadata
7. Response is returned to client and stored as a session memory

### Web Browser Integration Flow
1. Client creates a browser session via `/sessions` endpoint
2. BrowserService launches a headless browser instance
3. Client navigates to a URL using `/sessions/{session_id}/navigate`
4. Content is extracted and processed for AI consumption
5. AI can interact with the page through click, fill, and evaluate endpoints

## Design Philosophy
The MCP Server is built on the principle of providing intelligent, adaptive conversational experiences that can understand and respond to complex business contexts with high precision and relevance. It combines role-based advisory capabilities with memory management and web browsing to create a comprehensive AI assistant platform.

## Extensibility
The architecture is designed to be easily extended, allowing for:
- Custom AI advisor roles with specific instructions and tones
- Different memory types with configurable importance and expiration
- Flexible web browsing capabilities for research and information gathering
- Streaming responses for real-time interactions

## Performance Considerations
- Asynchronous processing for non-blocking operations
- Vector similarity search for efficient memory retrieval
- In-memory storage for fast access (with plans for database integration)
- Optimized browser interactions with configurable timeouts

## Security Principles
- Secure OpenAI API key management via environment variables
- Comprehensive input validation with Pydantic models
- Structured error handling with appropriate HTTP status codes
- Secure browser session management and isolation

## Future Roadmap
- Database integration for persistent storage of roles and memories
- Vector database for enhanced semantic search capabilities
- JWT-based authentication with role-based access control
- Multi-modal support for handling image and audio inputs
- Docker containerization for better deployment and scaling
- Enhanced browser capabilities with session persistence and cookie management
