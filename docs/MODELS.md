# MCP Server Models

## Overview
The models in the MCP Server define the data structures, type definitions, and core schemas that enable intelligent, context-aware interactions. These Pydantic models provide strict type validation and structured data representation throughout the application.

## Purpose
- Provide strict type definitions for API requests and responses
- Ensure data integrity through validation
- Support complex business logic with well-defined structures
- Enable advanced context management with semantic memory
- Facilitate serialization and deserialization of data

## Key Model Categories

### 1. Role Models
- **Role**: Core model defining an AI advisor role with properties like ID, name, description, instructions, domains, tone, and system prompt
- **RoleCreate**: Model for creating a new role with required fields
- **RoleUpdate**: Model for updating an existing role with optional fields
- **RoleResponse**: Response model wrapping a Role object
- **RolesResponse**: Response model containing a list of Role objects
- **ProcessRequest**: Request model for processing a query with a specific role
- **ProcessResponse**: Response model for processed queries

### 2. Memory Models
- **Memory**: Core model for memory entries with properties like ID, role_id, content, type, importance, embedding, and expiration
- **MemoryCreate**: Model for creating a new memory with required fields
- **MemoryResponse**: Response model wrapping a Memory object
- **MemoriesResponse**: Response model containing a list of Memory objects
- **ClearMemoriesResponse**: Response model for memory clearing operations

## Model Design Principles
- **Immutability**: Models are designed to be immutable to prevent unexpected changes
- **Type Safety**: Strict typing with Pydantic ensures data integrity
- **Extensibility**: Models can be extended with additional fields as needed
- **Validation**: Built-in validation ensures data consistency
- **Documentation**: Models include field descriptions for better API documentation

## Advanced Features
- **Vector Embeddings**: Memory models support vector embeddings for semantic search
- **Memory Types**: Different memory types (session, user, knowledge) with configurable TTL
- **Importance Levels**: Memory importance levels (low, medium, high) affecting relevance scoring
- **Tone Profiles**: Role models support different communication tones
- **Custom Instructions**: Support for additional instructions during query processing

## Example Model Structure
```python
class Memory(BaseModel):
    """Model for memory entries"""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the memory")
    role_id: str = Field(..., description="ID of the role this memory belongs to")
    content: str = Field(..., description="Content of the memory")
    type: Literal["session", "user", "knowledge"] = Field(..., description="Type of memory")
    importance: Literal["low", "medium", "high"] = Field("medium", description="Importance of the memory")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding of the memory content")
    created_at: datetime = Field(default_factory=datetime.now, description="When the memory was created")
    expires_at: Optional[datetime] = Field(None, description="When the memory expires")
```

## Future Enhancements
- **Database Integration**: Persistent storage for models in a database
- **Advanced Vector Embeddings**: Enhanced semantic representation capabilities
- **Cross-role Memory Sharing**: Ability to share memories between roles
- **Hierarchical Memory Structure**: Organized memory storage with parent-child relationships
- **Role Templates**: Pre-defined role templates for common use cases
- **Memory Tagging**: Enhanced categorization of memories for better retrieval
