# Context Switching

This document describes the real-time context switching feature in the MCP (Model Context Protocol) system.

## Overview

Context switching allows the AI to dynamically adapt to different roles based on the content of user queries. This feature enables more natural conversations as the AI can seamlessly transition between different areas of expertise without requiring explicit role selection from the user.

## How It Works

The context switching system consists of three main components:

1. **Trigger Detection**: Analyzes user queries for specific patterns that indicate a particular domain or role would be more appropriate.
2. **Role Matching**: Determines the best role to handle the query based on detected triggers and scoring.
3. **Context Transition**: Manages the smooth transition between roles, including providing context about the switch to the AI.

## Key Components

### TriggerService

The `TriggerService` is responsible for detecting triggers in user queries and determining which role is most appropriate for handling a given query.

```python
class TriggerService:
    # Registers triggers for roles based on domains and custom patterns
    async def register_role_triggers(self, role: Role, custom_triggers: Optional[List[str]] = None) -> None:
        # ...
    
    # Detects triggers in a query and returns matching roles with scores
    async def detect_triggers(self, query: str) -> List[Tuple[str, int]]:
        # ...
    
    # Gets the best role for a query, with hysteresis to prevent unnecessary switching
    async def get_best_role_for_query(self, query: str, current_role_id: Optional[str] = None) -> Optional[str]:
        # ...
```

### ContextSwitchingService

The `ContextSwitchingService` manages sessions and handles the process of switching between roles based on detected triggers.

```python
class ContextSwitchingService:
    # Creates a new session with an initial role
    async def create_session(self, session_id: str, initial_role_id: str) -> Dict[str, Any]:
        # ...
    
    # Processes a query with context switching
    async def process_query_with_context_switching(
        self, 
        session_id: str, 
        query: str,
        custom_instructions: Optional[str] = None,
        force_role_id: Optional[str] = None
    ) -> Dict[str, Any]:
        # ...
    
    # Manually switches context to a different role
    async def manually_switch_context(
        self, 
        session_id: str, 
        new_role_id: str,
        reason: str = "Manual switch by user"
    ) -> Dict[str, Any]:
        # ...
```

## API Endpoints

The context switching feature is exposed through the following API endpoints:

- `POST /api/context/sessions`: Create a new session with an initial role
- `POST /api/context/process`: Process a query with context switching
- `POST /api/context/process/stream`: Process a query with context switching and streaming response
- `POST /api/context/switch`: Manually switch context to a different role
- `GET /api/context/sessions/{session_id}`: Get session information
- `GET /api/context/sessions/{session_id}/history`: Get context switch history
- `DELETE /api/context/sessions/{session_id}`: Close a session

## Trigger Patterns

The system includes default trigger patterns for common domains:

- **Finance**: Terms related to money, budgets, investments, markets, etc.
- **Technology**: Terms related to software, hardware, programming, etc.
- **Healthcare**: Terms related to health, medicine, treatment, etc.
- **Marketing**: Terms related to advertising, campaigns, branding, etc.
- **Legal**: Terms related to law, contracts, compliance, etc.
- **Education**: Terms related to teaching, learning, curriculum, etc.
- **Creative**: Terms related to design, art, writing, etc.

Custom triggers can also be added for specific roles.

## Context Switching Logic

The system uses a scoring mechanism to determine when to switch contexts:

1. Each trigger pattern has a priority level (higher = more important)
2. When a query matches multiple triggers for a role, the scores are summed
3. A diversity bonus is added for matching different types of triggers
4. To prevent unnecessary switching, the current role is maintained if its score is at least 80% of the top score

## Usage Example

### Creating a Session

```http
POST /api/context/sessions
Content-Type: application/json

{
  "initial_role_id": "tech-expert"
}
```

### Processing a Query with Context Switching

```http
POST /api/context/process
Content-Type: application/json

{
  "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "query": "What are the best investment strategies for tech startups?"
}
```

In this example, the query contains triggers for both finance and technology domains, and the system will determine the most appropriate role to handle it.

## Benefits

- **Seamless User Experience**: Users don't need to explicitly switch between different AI roles
- **Contextual Continuity**: The system maintains session history across role transitions
- **Dynamic Adaptation**: The AI can adapt to changing conversation topics
- **Specialized Expertise**: Each query is handled by the most appropriate role

## Implementation Considerations

- **Hysteresis**: The system includes hysteresis to prevent rapid switching between roles
- **Explicit Overrides**: Users can still explicitly force a specific role when needed
- **Transition Context**: When switching roles, the AI is provided with context about the previous role
