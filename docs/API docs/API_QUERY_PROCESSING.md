# Query Processing API

This document provides comprehensive documentation for the query processing endpoints in the MCP Server, including example requests and responses.

## Table of Contents

- [Process a Query](#process-a-query)
- [Process a Query with Streaming Response](#process-a-query-with-streaming-response)

## Process a Query

```
POST /api/v1/roles/process
```

**Description:** Processes a query using a specific role's context and returns a response.

**Request Body:**
```json
{
  "role_id": "string",
  "query": "string",
  "custom_instructions": "string" // Optional
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/roles/process' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "role_id": "financial-advisor",
  "query": "What are some good retirement investment options for someone in their 30s?",
  "custom_instructions": "Focus on long-term growth strategies."
}'
```

**Example Response:**
```json
{
  "role_id": "financial-advisor",
  "query": "What are some good retirement investment options for someone in their 30s?",
  "response": "# Retirement Investment Options for Your 30s\n\n## Long-Term Growth Strategies\n\nSince you're in your 30s, you have a significant time horizon before retirement, which allows you to focus on growth-oriented investments. Here are some excellent options to consider:\n\n### 1. Index Funds\n* **Total Market Index Funds**: Provide broad market exposure with low fees\n* **S&P 500 Index Funds**: Track the performance of the 500 largest U.S. companies\n* **Historical returns**: ~10% annually over long periods (though past performance doesn't guarantee future results)\n\n### 2. Target Date Funds\n* Automatically adjust asset allocation as you approach retirement\n* Become more conservative over time\n* Require minimal management on your part\n\n### 3. Roth IRA\n* Tax-free growth and withdrawals in retirement\n* 2025 contribution limit: $7,000 ($8,000 if over 50)\n* Income limits apply, but backdoor Roth conversions are an option\n\n### 4. 401(k) with Employer Match\n* Always contribute at least enough to get the full employer match\n* This is essentially free money and an immediate return on investment\n\n### 5. Growth-Oriented ETFs\n* Technology, healthcare, and emerging markets ETFs offer higher growth potential\n* Higher volatility but potentially higher returns over decades\n\n## Asset Allocation Recommendation\n\nIn your 30s, a growth-oriented portfolio might look like:\n* 80-90% stocks (mix of domestic and international)\n* 10-20% bonds\n* Small allocation to alternative investments if desired\n\nRemember to regularly rebalance your portfolio and increase contributions as your income grows."
}
```

## Process a Query with Streaming Response

```
POST /api/v1/roles/process-stream
```

**Description:** Processes a query using a specific role's context and returns a streaming response.

**Request Body:**
```json
{
  "role_id": "string",
  "query": "string",
  "custom_instructions": "string" // Optional
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/roles/process-stream' \
  -H 'accept: text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{
  "role_id": "financial-advisor",
  "query": "What are some good retirement investment options for someone in their 30s?",
  "custom_instructions": "Focus on long-term growth strategies."
}'
```

**Example Response:**
The response is a text/event-stream with data chunks that can be processed in real-time:

```
data: # Retirement Investment Options for Your 30s

data: ## Long-Term Growth Strategies

data: Since you're in your 30s, you have a significant time horizon before retirement, which allows you to focus on growth-oriented investments. Here are some excellent options to consider:

...

data: [DONE]
```
