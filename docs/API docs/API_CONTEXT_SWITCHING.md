# Context Switching API

This document provides comprehensive documentation for the context switching endpoints in the MCP Server, including example requests and responses.

## Table of Contents

- [Create a New Session](#create-a-new-session)
- [Get Session Information](#get-session-information)
- [Process Query with Context](#process-query-with-context)
- [Get Session History](#get-session-history)
- [Delete a Session](#delete-a-session)

## Create a New Session

```
POST /api/v1/context/sessions
```

**Description:** Creates a new context session with an optional initial role and system prompt.

**Request Body:**
```json
{
  "role_id": "string",  // Optional
  "system_prompt": "string",  // Optional
  "metadata": {  // Optional
    "user_id": "string",
    "session_name": "string",
    "tags": ["string"]
  }
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/context/sessions' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "role_id": "financial-advisor",
  "metadata": {
    "user_id": "user-123",
    "session_name": "Retirement Planning",
    "tags": ["finance", "retirement", "planning"]
  }
}'
```

**Example Response:**
```json
{
  "session_id": "sess-8f7e6d5c",
  "role_id": "financial-advisor",
  "metadata": {
    "user_id": "user-123",
    "session_name": "Retirement Planning",
    "tags": ["finance", "retirement", "planning"]
  },
  "created_at": "2025-03-24T10:15:30Z"
}
```

## Get Session Information

```
GET /api/v1/context/sessions/{session_id}
```

**Description:** Retrieves information about a specific context session.

**Parameters:**
- `session_id` (path parameter): The unique identifier of the session.

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/context/sessions/sess-8f7e6d5c' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "session_id": "sess-8f7e6d5c",
  "role_id": "financial-advisor",
  "metadata": {
    "user_id": "user-123",
    "session_name": "Retirement Planning",
    "tags": ["finance", "retirement", "planning"]
  },
  "created_at": "2025-03-24T10:15:30Z",
  "last_active": "2025-03-24T10:15:30Z",
  "message_count": 0
}
```

## Process Query with Context

```
POST /api/v1/context/sessions/{session_id}/query
```

**Description:** Processes a query within the context of a specific session, maintaining conversation history.

**Parameters:**
- `session_id` (path parameter): The unique identifier of the session.

**Request Body:**
```json
{
  "query": "string",
  "custom_instructions": "string",  // Optional
  "provider": "string"  // Optional (openai, anthropic, gemini)
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/context/sessions/sess-8f7e6d5c/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "I\'m 35 years old and want to start planning for retirement. What should I consider?",
  "custom_instructions": "Provide practical, actionable advice."
}'
```

**Example Response:**
```json
{
  "session_id": "sess-8f7e6d5c",
  "query": "I'm 35 years old and want to start planning for retirement. What should I consider?",
  "response": "# Retirement Planning at 35: Key Considerations\n\n## Current Position Assessment\n\n Before diving into specific strategies, let's establish what you should evaluate about your current financial situation:\n\n* **Current savings rate**: What percentage of your income are you currently saving?\n* **Existing retirement accounts**: Do you have a 401(k), IRA, or other retirement vehicles already?\n* **Debt situation**: High-interest debt should typically be addressed before aggressive retirement saving\n* **Emergency fund status**: Ideally 3-6 months of expenses in liquid savings\n\n## Key Action Items\n\n### 1. Maximize Employer Matching\n\nIf your employer offers a 401(k) match, this should be your first priority - it's essentially free money:\n\n* Contribute at least enough to get the full employer match\n* Typical matches range from 3-6% of your salary\n* This has an immediate 100% return on investment\n\n### 2. Establish Retirement Goals\n\n* Calculate your retirement number (typically 25-30x your expected annual expenses)\n* At 35, you likely have 30+ years until traditional retirement age\n* Consider whether you want to retire early or work longer\n\n### 3. Optimize Account Types\n\n* **401(k)/403(b)**: Pre-tax contributions, tax-deferred growth\n* **Roth IRA**: After-tax contributions, tax-free growth and withdrawals\n* **HSA**: If eligible, triple tax advantage for healthcare expenses\n* **Taxable brokerage accounts**: For additional investments beyond tax-advantaged limits\n\n### 4. Asset Allocation Strategy\n\nAt 35, you have a long time horizon, which typically suggests:\n\n* 80-90% stocks (mix of domestic and international)\n* 10-20% bonds\n* Regular rebalancing to maintain your target allocation\n\n### 5. Practical Next Steps\n\n1. Increase your savings rate by 1-2% every year\n2. Set up automatic contributions to retirement accounts\n3. Review your investment choices for appropriate diversification\n4. Consider working with a fee-only financial advisor for personalized guidance\n\nRemember that consistency is key - starting at 35 gives you significant time to benefit from compound growth."
}
```

## Get Session History

```
GET /api/v1/context/sessions/{session_id}/history
```

**Description:** Retrieves the conversation history for a specific session.

**Parameters:**
- `session_id` (path parameter): The unique identifier of the session.
- `limit` (query parameter, optional): Maximum number of messages to return (default: 50).
- `before` (query parameter, optional): Timestamp to get messages before this time.

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/context/sessions/sess-8f7e6d5c/history?limit=10' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "session_id": "sess-8f7e6d5c",
  "messages": [
    {
      "id": "msg-1a2b3c4d",
      "role": "user",
      "content": "I'm 35 years old and want to start planning for retirement. What should I consider?",
      "timestamp": "2025-03-24T10:16:45Z"
    },
    {
      "id": "msg-5e6f7g8h",
      "role": "assistant",
      "content": "# Retirement Planning at 35: Key Considerations\n\n## Current Position Assessment\n\n Before diving into specific strategies...",
      "timestamp": "2025-03-24T10:16:50Z"
    },
    {
      "id": "msg-9i0j1k2l",
      "role": "user",
      "content": "How much should I be saving each month?",
      "timestamp": "2025-03-24T10:18:30Z"
    },
    {
      "id": "msg-3m4n5o6p",
      "role": "assistant",
      "content": "# Monthly Savings Recommendations\n\nThe general guideline is to save 15-20% of your pre-tax income for retirement...",
      "timestamp": "2025-03-24T10:18:35Z"
    }
  ],
  "has_more": false,
  "total_count": 4
}
```

## Delete a Session

```
DELETE /api/v1/context/sessions/{session_id}
```

**Description:** Deletes a specific context session and all associated messages.

**Parameters:**
- `session_id` (path parameter): The unique identifier of the session.

**Example Request:**
```bash
curl -X 'DELETE' 'http://localhost:8000/api/v1/context/sessions/sess-8f7e6d5c' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "message": "Session sess-8f7e6d5c deleted successfully"
}
```
