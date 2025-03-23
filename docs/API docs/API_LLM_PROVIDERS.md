# LLM Provider Management API

This document provides comprehensive documentation for the LLM provider management endpoints in the MCP Server, including example requests and responses.

## Table of Contents

- [Get Available LLM Providers](#get-available-llm-providers)
- [Set Default LLM Provider](#set-default-llm-provider)
- [Get LLM Provider Configuration](#get-llm-provider-configuration)
- [Update LLM Provider Configuration](#update-llm-provider-configuration)

## Get Available LLM Providers

```
GET /api/v1/llm-providers
```

**Description:** Retrieves a list of all available LLM providers and their current status.

**Parameters:** None

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/llm-providers' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "providers": [
    {
      "id": "openai",
      "name": "OpenAI",
      "status": "active",
      "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
      "features": ["text", "images", "streaming", "function-calling"],
      "is_default": true
    },
    {
      "id": "anthropic",
      "name": "Anthropic",
      "status": "active",
      "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
      "features": ["text", "images", "streaming"],
      "is_default": false
    },
    {
      "id": "gemini",
      "name": "Google Gemini",
      "status": "active",
      "models": ["gemini-pro", "gemini-ultra"],
      "features": ["text", "images"],
      "is_default": false
    }
  ],
  "default_provider": "openai"
}
```

## Set Default LLM Provider

```
PUT /api/v1/llm-providers/default
```

**Description:** Sets the default LLM provider to use when no specific provider is requested.

**Request Body:**
```json
{
  "provider_id": "string"
}
```

**Example Request:**
```bash
curl -X 'PUT' \
  'http://localhost:8000/api/v1/llm-providers/default' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "provider_id": "anthropic"
}'
```

**Example Response:**
```json
{
  "message": "Default provider updated successfully",
  "provider_id": "anthropic"
}
```

## Get LLM Provider Configuration

```
GET /api/v1/llm-providers/{provider_id}/config
```

**Description:** Retrieves the configuration for a specific LLM provider.

**Parameters:**
- `provider_id` (path parameter): The ID of the LLM provider (e.g., "openai", "anthropic", "gemini").

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/llm-providers/openai/config' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "provider_id": "openai",
  "config": {
    "api_key": "sk-***************************",
    "organization_id": "org-***************************",
    "default_model": "gpt-4o",
    "temperature": 0.7,
    "max_tokens": 4000,
    "timeout_seconds": 60
  }
}
```

## Update LLM Provider Configuration

```
PUT /api/v1/llm-providers/{provider_id}/config
```

**Description:** Updates the configuration for a specific LLM provider.

**Parameters:**
- `provider_id` (path parameter): The ID of the LLM provider (e.g., "openai", "anthropic", "gemini").

**Request Body:**
```json
{
  "config": {
    "api_key": "string",
    "organization_id": "string",  // Optional
    "default_model": "string",    // Optional
    "temperature": number,         // Optional
    "max_tokens": number,         // Optional
    "timeout_seconds": number     // Optional
  }
}
```

**Example Request:**
```bash
curl -X 'PUT' \
  'http://localhost:8000/api/v1/llm-providers/openai/config' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "config": {
    "api_key": "sk-new-api-key",
    "default_model": "gpt-4-turbo",
    "temperature": 0.5
  }
}'
```

**Example Response:**
```json
{
  "message": "Provider configuration updated successfully",
  "provider_id": "openai",
  "updated_fields": ["api_key", "default_model", "temperature"]
}
```
