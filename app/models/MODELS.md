# MCP Server Models Documentation

This document provides a comprehensive overview of all data models used in the MCP (Model Context Protocol) server. These models define the structure of data exchanged between clients and the server, as well as internal data representations.

## Table of Contents

- [Role Models](#role-models)
- [Memory Models](#memory-models)
- [Request Models](#request-models)
- [Multimodal Models](#multimodal-models)
- [Browser Models](#browser-models)
- [Context Switching Models](#context-switching-models)
- [Domain Analysis Models](#domain-analysis-models)
- [Provider Models](#provider-models)

## Role Models

Role models define the structure of AI advisor roles in the system. These models are defined in `app/models/role.py`.

### Role

Represents a complete role definition with all properties.

```python
class Role(BaseModel):
    id: str                       # Unique identifier for the role
    name: str                     # Human-readable name for the role
    description: str              # Description of the role's purpose
    instructions: str             # Custom instructions for the role
    domains: List[str]            # Areas of expertise
    tone: str                     # Communication tone (strategic, analytical, creative, etc.)
    system_prompt: str            # Base system prompt for this role
    is_default: bool              # Whether this is a default system role
    parent_role_id: Optional[str] # ID of the parent role for inheritance
    inherit_memories: bool        # Whether to inherit memories from parent role
    memory_access_level: str      # Memory access level (standard, elevated, admin)
    memory_categories: List[str]  # Categories of memories this role specializes in
```

### RoleCreate

Used when creating a new role.

```python
class RoleCreate(BaseModel):
    id: str                       # Unique identifier for the role
    name: str                     # Human-readable name for the role
    description: str              # Description of the role's purpose
    instructions: str             # Custom instructions for the role
    domains: List[str]            # Areas of expertise
    tone: str                     # Communication tone (strategic, analytical, creative, etc.)
    system_prompt: str            # Base system prompt for this role
    parent_role_id: Optional[str] # ID of the parent role for inheritance
    inherit_memories: bool        # Whether to inherit memories from parent role
    memory_access_level: str      # Memory access level (standard, elevated, admin)
    memory_categories: List[str]  # Categories of memories this role specializes in
```

### RoleUpdate

Used when updating an existing role. All fields are optional.

```python
class RoleUpdate(BaseModel):
    name: Optional[str]                # Human-readable name for the role
    description: Optional[str]         # Description of the role's purpose
    instructions: Optional[str]        # Custom instructions for the role
    domains: Optional[List[str]]       # Areas of expertise
    tone: Optional[str]                # Communication tone
    system_prompt: Optional[str]       # Base system prompt for this role
    parent_role_id: Optional[str]      # ID of the parent role for inheritance
    inherit_memories: Optional[bool]   # Whether to inherit memories from parent role
    memory_access_level: Optional[str] # Memory access level
    memory_categories: Optional[List[str]] # Categories of memories this role specializes in
```

### RoleResponse and RolesResponse

Response models for role operations.

```python
class RoleResponse(BaseModel):
    role: Role

class RolesResponse(BaseModel):
    roles: List[Role]
```

### ProcessRequest and ProcessResponse

Models for processing queries using a specific role.

```python
class ProcessRequest(BaseModel):
    role_id: str                      # ID of the role to use
    query: str                        # Query to process
    custom_instructions: Optional[str] # Optional custom instructions

class ProcessResponse(BaseModel):
    role_id: str                      # ID of the role used
    query: str                        # The query that was processed
    response: str                     # The processed response
```

## Memory Models

Memory models define the structure of memory entries in the system. These models are defined in `app/models/memory.py`.

### Memory

Represents a complete memory entry with all properties.

```python
class Memory(BaseModel):
    id: str                          # Unique identifier for the memory
    role_id: str                     # ID of the role this memory belongs to
    content: str                     # Content of the memory
    type: Literal["session", "user", "knowledge"] # Type of memory
    importance: Literal["low", "medium", "high"] # Importance of the memory
    embedding: Optional[List[float]] # Vector embedding of the memory content
    created_at: datetime             # When the memory was created
    expires_at: Optional[datetime]   # When the memory expires
    tags: List[str]                  # Tags for categorizing and filtering memories
    category: Optional[str]          # Primary category for the memory
    shared_with: List[str]           # List of role IDs this memory is shared with
    parent_memory_id: Optional[str]  # ID of the parent memory if derived from another memory
```

### MemoryCreate

Used when creating a new memory.

```python
class MemoryCreate(BaseModel):
    role_id: str                     # ID of the role this memory belongs to
    content: str                     # Content of the memory
    type: Literal["session", "user", "knowledge"] # Type of memory
    importance: Literal["low", "medium", "high"] # Importance of the memory
    tags: List[str]                  # Tags for categorizing and filtering memories
    category: Optional[str]          # Primary category for the memory
    shared_with: List[str]           # List of role IDs this memory is shared with
    parent_memory_id: Optional[str]  # ID of the parent memory if derived from another memory
```

### MemoryResponse and MemoriesResponse

Response models for memory operations.

```python
class MemoryResponse(BaseModel):
    success: bool = True
    memory: Memory

class MemoriesResponse(BaseModel):
    memories: List[Memory]
```

### ClearMemoriesResponse

Response model for clearing memories.

```python
class ClearMemoriesResponse(BaseModel):
    success: bool
    message: str
```

### SemanticSearchRequest

Request model for semantic memory search.

```python
class SemanticSearchRequest(BaseModel):
    query: str                       # Query to search for
    role_id: str                     # ID of the role to search memories for
    limit: int                       # Maximum number of memories to return
    category: Optional[str]          # Optional category to filter by
    tags: Optional[List[str]]        # Optional tags to filter by
    include_shared: bool             # Whether to include memories shared from other roles
    cross_role: bool                 # Whether to search across all roles
    related_role_ids: Optional[List[str]] # Optional list of specific role IDs to include
```

## Request Models

Basic request models for generating responses. These models are defined in `app/models/request_models.py`.

### GenerateRequest

Request model for generating a response.

```python
class GenerateRequest(BaseModel):
    system_prompt: str               # System prompt for the model
    user_prompt: str                 # User prompt for the model
    role_id: Optional[str]           # Optional role ID for context
    provider_name: Optional[str]     # Optional provider name to use
```

### StreamGenerateRequest

Request model for generating a streaming response.

```python
class StreamGenerateRequest(BaseModel):
    system_prompt: str               # System prompt for the model
    user_prompt: str                 # User prompt for the model
    role_id: Optional[str]           # Optional role ID for context
    provider_name: Optional[str]     # Optional provider name to use
```

## Multimodal Models

Models for multimodal content processing. These models are defined in `app/models/multimodal.py`.

### ContentType

Enum for content types.

```python
class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    FILE = "file"
```

### MediaContent

Model for media content.

```python
class MediaContent(BaseModel):
    type: ContentType                # Type of media content
    url: Optional[HttpUrl]           # URL to the media content
    base64_data: Optional[str]       # Base64 encoded media data
    mime_type: Optional[str]         # MIME type of the media content
    alt_text: Optional[str]          # Alternative text description of the media
    metadata: Optional[Dict[str, Any]] # Additional metadata for the media
```

### MultiModalContent

Model for multi-modal content.

```python
class MultiModalContent(BaseModel):
    text: Optional[str]              # Text content
    media: Optional[List[MediaContent]] # Media content
```

### MultiModalProcessRequest

Request model for processing a multi-modal query.

```python
class MultiModalProcessRequest(BaseModel):
    role_id: str                     # ID of the role to use
    content: MultiModalContent       # Multi-modal content to process
    custom_instructions: Optional[str] # Optional custom instructions
    provider_name: Optional[str]     # Optional LLM provider to use
```

### MultiModalProcessResponse

Response model for processed multi-modal queries.

```python
class MultiModalProcessResponse(BaseModel):
    role_id: str                     # ID of the role used
    response: str                    # The processed response
    processed_media: List[Dict[str, Any]] # Information about processed media
```

## Browser Models

Models for browser session management and operations. These models are defined in `app/models/browser.py`.

### BrowserSession

Model for browser session information.

```python
class BrowserSession(BaseModel):
    session_id: str                  # Unique identifier for the browser session
    created_at: datetime             # When the session was created
    active: bool                     # Whether the session is currently active
    mock: bool                       # Whether this is a mock session
    error: Optional[str]             # Error message if browser initialization failed
```

### Browser Request Models

Request models for browser operations.

```python
class BrowserNavigationRequest(BaseModel):
    url: HttpUrl                     # URL to navigate to

class BrowserClickRequest(BaseModel):
    selector: str                    # CSS selector for the element to click

class BrowserFillRequest(BaseModel):
    selector: str                    # CSS selector for the input field
    value: str                       # Value to fill in the input field

class BrowserEvaluateRequest(BaseModel):
    script: str                      # JavaScript code to execute

class BrowserScreenshotRequest(BaseModel):
    selector: Optional[str]          # CSS selector for element to screenshot
```

### Browser Response Models

Response models for browser operations.

```python
class BrowserResponse(BaseModel):
    success: bool                    # Whether the operation was successful
    error: Optional[str]             # Error message if the operation failed

class BrowserContentResponse(BrowserResponse):
    content: str                     # HTML content of the page
    title: str                       # Title of the page
    url: str                         # Current URL of the page

class BrowserScreenshotResponse(BrowserResponse):
    image_data: str                  # Base64-encoded image data
    mime_type: str                   # MIME type of the image

class BrowserEvaluateResponse(BrowserResponse):
    result: Any                      # Result of the JavaScript evaluation
```

### BrowserHistoryEntry and BrowserHistoryResponse

Models for browser history.

```python
class BrowserHistoryEntry(BaseModel):
    url: str                         # URL that was visited
    title: Optional[str]             # Title of the page
    timestamp: datetime              # When the page was visited
    actions: List[Dict[str, Any]]    # Actions performed on the page

class BrowserHistoryResponse(BaseModel):
    history: List[BrowserHistoryEntry] # List of history entries
```

## Context Switching Models

Models for context switching functionality. These models are defined in `app/models/context.py`.

### ContextSession

Model for context switching session.

```python
class ContextSession(BaseModel):
    session_id: str                  # Unique identifier for the session
    current_role_id: str             # ID of the current active role
    created_at: datetime             # When the session was created
    last_activity: datetime          # When the session was last active
    last_switch_reason: Optional[str] # Reason for the last context switch
    history: List[Dict[str, Any]]    # History of context switches
```

### ContextSwitchEvent

Model for a context switch event.

```python
class ContextSwitchEvent(BaseModel):
    timestamp: datetime              # When the switch occurred
    from_role_id: str                # ID of the role switched from
    to_role_id: str                  # ID of the role switched to
    reason: str                      # Reason for the switch
    query: Optional[str]             # Query that triggered the switch, if any
    automatic: bool                  # Whether the switch was automatic or manual
```

### Context Request and Response Models

Request and response models for context operations.

```python
class CreateSessionRequest(BaseModel):
    initial_role_id: str             # ID of the initial role to use
    session_id: Optional[str]        # Optional custom session ID

class CreateSessionResponse(BaseModel):
    session_id: str                  # ID of the created session
    current_role_id: str             # ID of the current role
    message: str                     # Status message

class ProcessWithContextRequest(BaseModel):
    session_id: str                  # ID of the session to use
    query: str                       # Query to process
    custom_instructions: Optional[str] # Optional custom instructions
    force_role_id: Optional[str]     # Optional role ID to force using

class ProcessWithContextResponse(BaseModel):
    session_id: str                  # ID of the session
    role_id: str                     # ID of the role used
    query: str                       # The query that was processed
    response: str                    # The processed response
    context_switched: bool           # Whether context was switched
    switch_reason: Optional[str]     # Reason for context switch, if any

class SwitchContextRequest(BaseModel):
    session_id: str                  # ID of the session to switch context for
    new_role_id: str                 # ID of the role to switch to
    reason: Optional[str]            # Reason for the switch

class SwitchContextResponse(BaseModel):
    session_id: str                  # ID of the session
    current_role_id: str             # ID of the current role
    previous_role_id: str            # ID of the previous role
    reason: str                      # Reason for the switch
    message: str                     # Status message
```

### Context Trigger Models

Models for context switching triggers.

```python
class ContextTrigger(BaseModel):
    id: str                          # Unique identifier for the trigger
    role_id: str                     # ID of the role this trigger is for
    pattern: str                     # Regex pattern or keyword to match
    priority: int                    # Priority of the trigger
    description: str                 # Description of what this trigger matches
    is_regex: bool                   # Whether the pattern is a regex pattern
    enabled: bool                    # Whether this trigger is enabled
    created_at: datetime             # When the trigger was created

class CreateTriggerRequest(BaseModel):
    role_id: str                     # ID of the role this trigger is for
    pattern: str                     # Regex pattern or keyword to match
    priority: int                    # Priority of the trigger
    description: str                 # Description of what this trigger matches
    is_regex: bool                   # Whether the pattern is a regex pattern

class UpdateTriggerRequest(BaseModel):
    pattern: Optional[str]           # Regex pattern or keyword to match
    priority: Optional[int]          # Priority of the trigger
    description: Optional[str]       # Description of what this trigger matches
    is_regex: Optional[bool]         # Whether the pattern is a regex pattern
    enabled: Optional[bool]          # Whether this trigger is enabled

class TriggerResponse(BaseModel):
    trigger: ContextTrigger

class TriggersResponse(BaseModel):
    triggers: List[ContextTrigger]
```

## Domain Analysis Models

Models for domain-specific analysis. These models are defined in `app/models/domain.py`.

### DomainTemplate

Model for domain-specific analysis templates.

```python
class DomainTemplate(BaseModel):
    analysis_prompt: str             # Prompt template for domain-specific analysis
    extraction_patterns: List[str]   # Key patterns to extract from content for this domain
    metrics: List[str]               # Key metrics relevant to this domain
    frameworks: List[str]            # Analysis frameworks relevant to this domain
```

### Domain Analysis Request and Response Models

Request and response models for domain analysis.

```python
class DomainAnalysisRequest(BaseModel):
    content: str                     # Content to analyze
    role_id: str                     # ID of the role to use for analysis

class ExtractedPattern(BaseModel):
    pattern: str                     # The pattern that was extracted
    occurrences: int                 # Number of occurrences in the content
    context: Optional[List[str]]     # Surrounding context for the pattern

class DomainSpecificAnalysis(BaseModel):
    domain: str                      # The domain this analysis is for
    extracted_patterns: List[ExtractedPattern] # Patterns extracted from the content
    relevant_metrics: List[str]      # Metrics relevant to this domain
    suggested_frameworks: List[str]  # Analysis frameworks suggested for this domain
    analysis_prompt: str             # The prompt used for analysis

class DomainAnalysisResponse(BaseModel):
    role_id: str                     # ID of the role used for analysis
    role_name: str                   # Name of the role used for analysis
    domains: List[str]               # Domains of the role
    domain_analysis: List[DomainSpecificAnalysis] # Domain-specific analysis results
```

### Domain Template Response Models

Response models for domain templates.

```python
class DomainTemplateResponse(BaseModel):
    domains: List[str]               # Available domain names
    templates: Dict[str, DomainTemplate] # Domain templates

class SpecificDomainTemplateResponse(BaseModel):
    domain: str                      # The domain name
    template: DomainTemplate         # The domain template
```

### Enhanced Prompt Models

Models for enhancing prompts with domain analysis.

```python
class EnhancedPromptRequest(BaseModel):
    system_prompt: str               # Original system prompt
    content: str                     # Content to analyze
    role_id: str                     # ID of the role to use for analysis

class EnhancedPromptResponse(BaseModel):
    original_prompt: str             # The original system prompt
    enhanced_prompt: str             # The enhanced system prompt
    domains_applied: List[str]       # Domains that were applied in the enhancement
```

## Provider Models

Models for LLM provider functionality. These models are defined in `app/models/provider.py`.

### LLMProvider

Model for LLM provider information.

```python
class LLMProvider(BaseModel):
    name: str                        # Name of the provider (e.g., 'openai', 'anthropic')
    model_name: str                  # Name of the model (e.g., 'gpt-4o-mini')
    description: Optional[str]       # Description of the provider/model
    capabilities: List[str]          # List of capabilities (e.g., 'text', 'images', 'audio')
    max_tokens: int                  # Maximum tokens supported by the model
    is_default: bool                 # Whether this is the default provider
    config: Dict[str, Any]           # Provider-specific configuration
```

### Provider Response Models

Response models for provider information.

```python
class ProviderResponse(BaseModel):
    providers: Dict[str, str]        # Dictionary of provider names to model names
    default_provider: str            # Name of the default provider

class ProviderCapabilitiesResponse(BaseModel):
    providers: List[LLMProvider]     # List of provider information
    default_provider: str            # Name of the default provider
```

### Model Parameters

Model for LLM generation parameters.

```python
class ModelParameters(BaseModel):
    temperature: float               # Temperature for response generation (0.0-1.0)
    max_tokens: Optional[int]        # Maximum tokens to generate
    top_p: Optional[float]           # Nucleus sampling parameter
    frequency_penalty: Optional[float] # Frequency penalty parameter
    presence_penalty: Optional[float] # Presence penalty parameter
    stop_sequences: Optional[List[str]] # Sequences that will stop generation
```

### Provider Generate Models

Extended request and response models for generating responses with parameters.

```python
class ProviderGenerateRequest(BaseModel):
    system_prompt: str               # System prompt for the model
    user_prompt: str                 # User prompt for the model
    role_id: Optional[str]           # Optional role ID for context
    provider_name: Optional[str]     # Optional provider name to use
    parameters: Optional[ModelParameters] # Optional generation parameters

class ProviderGenerateResponse(BaseModel):
    response: str                    # Generated response
    provider_name: str               # Provider used for generation
    model_name: str                  # Model used for generation
    usage: Optional[Dict[str, int]]  # Token usage information if available
```
