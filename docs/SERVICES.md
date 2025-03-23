# MCP Server Services

## Overview
Services in the MCP Server implement the core business logic, AI interactions, and advanced computational capabilities that power the intelligent conversational platform. These services handle role management, memory operations, AI processing, and web browser integration.

## Service Categories

### 1. Context Switching Services
- **TriggerService**: Detects triggers in user queries to determine appropriate roles
- Registers and manages trigger patterns for different domains and roles
- Implements scoring mechanism for role matching based on query content
- Supports custom triggers with configurable priorities
- Prevents unnecessary context switching with hysteresis logic

- **ContextSwitchingService**: Manages context switching between different roles
- Maintains session state for tracking current roles and switch history
- Processes queries with automatic context detection and switching
- Provides streaming response support with context switch notifications
- Enables manual context switching when needed

### 2. Role Service
- **RoleService**: Manages role creation, retrieval, updating, and deletion
- Processes queries using specific roles
- Generates complete system prompts with role instructions, tone, and relevant memories
- Supports streaming responses for real-time interactions
- Handles role-specific context management

### 2. Memory Service
- **MemoryService**: Manages memory storage and retrieval
- Stores memories with configurable expiration based on memory type
- Retrieves memories by role ID and memory type
- Implements vector similarity search for finding relevant memories
- Supports memory importance levels affecting relevance scoring

### 3. AI Processor
- **AIProcessor**: Handles interactions with the OpenAI API
- Generates responses using role-specific system prompts
- Creates embeddings for semantic memory operations
- Supports streaming responses for real-time interactions
- Integrates with web browser functionality for research capabilities

### 4. Web Browser Integration
- **BrowserService**: Controls headless browser using Pyppeteer
- Manages browser sessions for different roles
- Supports navigation, content extraction, and interaction with web pages
- Provides screenshot capabilities for visual context
- Enables JavaScript execution for advanced web interactions
- **BrowserIntegration**: Connects AI processing with browser functionality
- Implements web search, content browsing, and element interaction
- Extracts structured data from web pages

## Core Service Design Principles
- **Modularity**: Services are designed as independent components with clear responsibilities
- **Dependency Injection**: Services receive their dependencies through constructors
- **Asynchronous Processing**: All service methods use async/await for non-blocking operations
- **Stateless Design**: Services maintain minimal state for better scalability
- **Error Handling**: Comprehensive error handling with appropriate error responses

## Advanced Capabilities

### AI Processing
- **Context-Aware Responses**: Generates responses based on role, instructions, and relevant memories
- **Vector Similarity Search**: Finds memories relevant to the current query using embeddings
- **Streaming Responses**: Real-time response generation using server-sent events

### Context Switching
- **Automatic Role Detection**: Identifies the most appropriate role based on query content
- **Trigger Pattern Matching**: Uses regex patterns to detect domain-specific terminology
- **Seamless Transitions**: Provides context about role transitions to maintain conversation coherence
- **Session Management**: Maintains conversation history across role transitions
- **Prioritized Matching**: Assigns different priorities to triggers for more accurate role selection
- **Memory Management**: Intelligent memory storage and retrieval with importance scoring

### Web Browser Capabilities
- **Web Search**: AI-assisted web research using search engines
- **Content Extraction**: Multiple extraction modes (auto, article, full, structured)
- **Element Interaction**: Click, fill, and extract content from web page elements
- **JavaScript Execution**: Run custom scripts for advanced web interactions
- **Form Filling**: Automated form filling for web interactions

## Example Service Implementation
```python
async def process_query(self, role_id: str, query: str, custom_instructions: Optional[str] = None) -> str:
    """Process a query using a specific role
    
    Args:
        role_id: The ID of the role to use
        query: The query to process
        custom_instructions: Optional custom instructions
        
    Returns:
        The processed response
    """
    # Generate query embedding for memory retrieval
    embedding = await self.ai_processor.create_embedding(query)
    
    # Get relevant memories
    relevant_memories = await self.memory_service.get_relevant_memories(
        role_id, query, embedding, limit=5
    )
    
    # Generate complete system prompt
    system_prompt = await self.generate_complete_prompt(role_id, custom_instructions)
    
    # Add relevant memories to the prompt if available
    if relevant_memories:
        memory_text = "\n\nRelevant memories:\n" + "\n".join(
            [f"- {memory.content}" for memory in relevant_memories]
        )
        system_prompt += memory_text
    
    # Process the query with the AI processor
    response = await self.ai_processor.generate_response(system_prompt, query, role_id)
    
    # Store the query and response as a session memory
    memory_content = f"User: {query}\nAssistant: {response}"
    await self.memory_service.store_memory(
        MemoryCreate(
            role_id=role_id,
            content=memory_content,
            type="session",
            importance="medium"
        )
    )
    
    return response
```

## Security and Compliance
- **Secure API Key Management**: OpenAI API key handled via environment variables
- **Input Validation**: Request validation using Pydantic models
- **Error Handling**: Structured error responses with appropriate status codes
- **Browser Security**: Secure browser session management and isolation

## Future Roadmap
- **Database Integration**: Persistent storage for roles and memories
- **Vector Database**: Enhanced semantic search with dedicated vector database
- **Authentication & Authorization**: JWT-based auth with role-based access control
- **Advanced Memory Features**: Memory sharing, tagging, and hierarchical structure
- **Browser Enhancements**: Session persistence, cookie management, and proxy support
- **Multi-modal Support**: Handling image and audio inputs for more versatile interactions
