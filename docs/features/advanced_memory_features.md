# Advanced Memory Features

This document provides an overview of the advanced memory features implemented in the Role-Specific Context MCP Server.

## Overview

The Advanced Memory Features enhance the system's ability to store, retrieve, and share contextual information across different AI agents. These features enable more sophisticated collaboration between roles, hierarchical memory access, and semantic search capabilities.

## Key Features

### Memory Tagging and Categorization

Memories can now be tagged and categorized for better organization and retrieval:

- **Tags**: Add multiple tags to memories for flexible filtering and grouping
- **Categories**: Assign a primary category to each memory for high-level organization
- **Filtering**: Retrieve memories by tags, categories, or a combination of both

```typescript
// Example: Creating a memory with tags and category
const response = await fetch('/api/memories', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    role_id: 'financial-advisor',
    content: 'Client prefers low-risk investments',
    type: 'knowledge',
    importance: 'high',
    tags: ['investment', 'preference', 'risk-profile'],
    category: 'client-preferences'
  })
});
```

### Shared Memory Collection

Roles can now share memories with other roles, enabling collaborative knowledge building:

- **Direct Sharing**: Share specific memories with selected roles
- **Reference Tracking**: Shared memories maintain a reference to the original memory
- **Propagation Control**: Control whether shared memories can be further shared

```typescript
// Example: Sharing an existing memory with other roles
const response = await fetch(`/api/memories/${roleId}/share`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    memory_id: 'mem-123',
    target_role_ids: ['financial-analyst', 'investment-manager']
  })
});
```

### Role-based Memory Inheritance

Roles can inherit memories from parent roles, creating a hierarchical knowledge structure:

- **Parent-Child Relationships**: Define inheritance relationships between roles
- **Access Levels**: Control what types of memories are inherited (knowledge, user, session)
- **Category Filtering**: Limit inheritance to specific memory categories

```typescript
// Example: Setting a parent role for inheritance
const response = await fetch(`/api/roles/${roleId}/parent-role/${parentId}`, {
  method: 'PATCH'
});

// Example: Configuring memory access settings
const response = await fetch(`/api/roles/${roleId}/memory-access`, {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    inherit_memories: true,
    memory_access_level: 'elevated',
    memory_categories: ['client-data', 'market-analysis']
  })
});
```

### Hierarchical Memory Access Control

Control access to memories based on role hierarchy and access levels:

- **Access Levels**: Standard, Elevated, Admin
- **Type-Based Access**: Standard access only gets knowledge memories, Elevated adds user memories, Admin gets all
- **Category-Based Access**: Limit access to specific memory categories

### Semantic Search for Cross-role Memory Retrieval

Search for memories across roles based on semantic similarity:

- **Vector Similarity**: Find memories with similar meaning, not just keyword matches
- **Cross-Role Search**: Search across multiple roles' memories
- **Relevance Scoring**: Results are ranked by semantic relevance, importance, and recency

```typescript
// Example: Semantic search across roles
const response = await fetch('/api/memories/semantic-search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'What investment strategies work best in volatile markets?',
    role_id: 'financial-advisor',
    limit: 5,
    cross_role: true,
    related_role_ids: ['market-analyst', 'risk-manager']
  })
});
```

## API Endpoints

### Memory Endpoints

- `POST /memories` - Create a new memory
- `GET /memories/{role_id}` - Get memories for a role
- `DELETE /memories/{role_id}` - Clear memories for a role
- `POST /memories/semantic-search` - Search memories semantically
- `POST /memories/{role_id}/share` - Share a memory with other roles
- `GET /memories/shared/{role_id}` - Get memories shared with a role

### Role Memory Management Endpoints

- `GET /roles/{role_id}/inheritance-chain` - Get the inheritance chain for a role
- `GET /roles/{role_id}/related-roles` - Get roles related to a specific role
- `PATCH /roles/{role_id}/memory-access` - Update memory access settings
- `PATCH /roles/{role_id}/parent-role/{parent_id}` - Set the parent role for inheritance
- `DELETE /roles/{role_id}/parent-role` - Remove the parent role inheritance

## Implementation Details

The advanced memory features are implemented across several components:

1. **Memory Models**: Enhanced with tags, categories, sharing, and inheritance fields
2. **Memory Service**: Updated to support filtering, sharing, and inheritance logic
3. **Role Models**: Extended with parent role, inheritance settings, and access control fields
4. **API Endpoints**: New endpoints for memory sharing, inheritance, and semantic search

## Best Practices

1. **Organize with Tags and Categories**: Use consistent tagging and categorization for better organization
2. **Design Role Hierarchies Carefully**: Plan your role inheritance structure to avoid unnecessary complexity
3. **Set Appropriate Access Levels**: Use the right access level for each role to maintain security
4. **Use Semantic Search for Exploration**: Leverage semantic search to discover relevant memories across roles
5. **Monitor Memory Usage**: Keep track of memory usage and clean up unnecessary memories regularly

## Future Enhancements

- Memory visualization and analytics
- Database persistence for memories
- Memory export/import functionality
- Version history and rollback capabilities
- Memory conflict resolution for shared memories
- Memory access audit logging
