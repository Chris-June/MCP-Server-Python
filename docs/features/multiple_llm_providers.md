# Multiple LLM Provider Support

## Overview

The MCP server now supports multiple Large Language Model (LLM) providers, allowing you to leverage different AI models based on your specific needs. This modular architecture enables easy integration and switching between providers while maintaining a consistent interface for your application.

Currently supported providers include:

- **OpenAI** (GPT-4o-mini and other models)
- **Anthropic** (Claude models)
- **Google Gemini** (Gemini models)

## Architecture

The multiple LLM provider system is built on a modular architecture that allows for easy addition of new providers:

### Core Components

1. **BaseLLMProvider**: An abstract base class that defines the interface for all LLM providers, ensuring consistent methods across different implementations.

2. **Provider Implementations**:
   - `OpenAIProvider`: Implementation for the OpenAI API
   - `AnthropicProvider`: Implementation for the Anthropic API
   - `GeminiProvider`: Implementation for the Google Gemini API

3. **Provider Factory**: A factory class that creates instances of LLM providers based on configuration.

4. **AIProcessor**: The main service class that manages providers and handles AI requests using the selected provider.

## Configuration

To use multiple LLM providers, you need to configure the appropriate API keys and model names in your `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_VISION_MODEL=gpt-4o

# Anthropic Configuration (Optional)
ANTHROPIC_API_KEY=your_anthropic_api_key
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Google Gemini Configuration (Optional)
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-pro

# Default Provider Configuration
DEFAULT_PROVIDER=openai  # Options: openai, anthropic, gemini
```

You only need to configure the providers you intend to use. The system will automatically initialize providers based on the available API keys.

## Usage

### Basic Usage

By default, the AIProcessor will use the provider specified in the `DEFAULT_PROVIDER` environment variable. If that provider is not available, it will use the first available provider.

```python
# Generate a response using the default provider
response = await ai_processor.generate_response(system_prompt, user_prompt)

# Generate a streaming response using the default provider
async for chunk in ai_processor.generate_response_stream(system_prompt, user_prompt):
    print(chunk, end="", flush=True)
```

### Specifying a Provider

You can specify which provider to use for a particular request:

```python
# Generate a response using a specific provider
response = await ai_processor.generate_response(
    system_prompt, 
    user_prompt, 
    provider_name="anthropic"
)

# Generate a streaming response using a specific provider
async for chunk in ai_processor.generate_response_stream(
    system_prompt, 
    user_prompt, 
    provider_name="gemini"
):
    print(chunk, end="", flush=True)
```

### Getting Available Providers

You can retrieve a list of all available providers and their default models:

```python
available_providers = ai_processor.get_available_providers()
print(available_providers)  # {'openai': 'gpt-4o-mini', 'anthropic': 'claude-3-haiku-20240307', ...}
```

## API Routes

The MCP server includes API routes for interacting with different LLM providers:

### Get Available Providers

```http
GET /api/providers
```

Returns a list of available providers and their default models.

### Generate Response

```http
POST /api/generate
```

Request body:

```json
{
  "system_prompt": "You are a helpful assistant.",
  "user_prompt": "Tell me about multiple LLM providers.",
  "provider_name": "openai"  // Optional, defaults to DEFAULT_PROVIDER
}
```

### Generate Streaming Response

```http
POST /api/generate/stream
```

Request body (same as above):

```json
{
  "system_prompt": "You are a helpful assistant.",
  "user_prompt": "Tell me about multiple LLM providers.",
  "provider_name": "anthropic"  // Optional, defaults to DEFAULT_PROVIDER
}
```

## Provider-Specific Features

### OpenAI Provider

- Supports text completions and streaming
- Supports embeddings for vector search
- Supports vision capabilities with the vision model

### Anthropic Provider

- Supports text completions and streaming
- Supports Claude-specific features like XML tagging

### Gemini Provider

- Supports text completions and streaming
- Supports multi-modal inputs with images

## Extending with New Providers

To add a new LLM provider, follow these steps:

1. Create a new provider class that inherits from `BaseLLMProvider`
2. Implement the required methods (`generate_completion`, `generate_completion_stream`, etc.)
3. Add the provider to the `LLMProviderFactory` class
4. Update the configuration in `config.py` to support the new provider

Example of a new provider implementation:

```python
from app.services.llm_providers.base_provider import BaseLLMProvider
from typing import AsyncGenerator, Dict, Any, List, Optional
import asyncio

class NewProvider(BaseLLMProvider):
    """Implementation of the BaseLLMProvider for a new LLM API"""
    
    def __init__(self, api_key: str, model: Optional[str] = None):
        """Initialize the provider with API key and model"""
        super().__init__()
        self.api_key = api_key
        self.model = model or "default-model-name"
        self.client = YourAPIClient(api_key=api_key)  # Initialize your API client
    
    @property
    def provider_name(self) -> str:
        """Get the name of this provider"""
        return "new_provider"
    
    @property
    def default_model(self) -> str:
        """Get the default model for this provider"""
        return self.model
    
    async def generate_completion(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate a completion using the new provider"""
        # Implement your completion logic here
        pass
    
    async def generate_completion_stream(self, system_prompt: str, user_prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Generate a streaming completion using the new provider"""
        # Implement your streaming logic here
        pass
```

## Best Practices

1. **API Key Management**: Always store API keys in environment variables, never hardcode them in your application.

2. **Error Handling**: Each provider implementation includes error handling to ensure graceful degradation if an API call fails.

3. **Fallback Mechanisms**: Consider implementing fallback mechanisms to try alternative providers if the primary provider fails.

4. **Model Selection**: Choose appropriate models for each provider based on your specific needs and budget constraints.

5. **Monitoring Usage**: Set up monitoring for API usage to track costs and prevent unexpected charges.

## Limitations

- Not all providers support the same features. For example, only OpenAI currently supports embeddings in our implementation.
- Different providers may have different rate limits, token limits, and pricing structures.
- Response formats may vary slightly between providers, though our implementation attempts to normalize these differences.

## Future Enhancements

- Add support for more LLM providers (e.g., Cohere, Mistral AI, etc.)
- Implement provider-specific optimizations for better performance
- Add support for function calling across all providers
- Implement automatic fallback between providers
- Add cost estimation and tracking features
