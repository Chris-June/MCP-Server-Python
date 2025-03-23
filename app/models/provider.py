from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field

class LLMProvider(BaseModel):
    """Model for LLM provider information"""
    name: str = Field(..., description="Name of the provider (e.g., 'openai', 'anthropic')")
    model_name: str = Field(..., description="Name of the model (e.g., 'gpt-4o-mini')")
    description: Optional[str] = Field(None, description="Description of the provider/model")
    capabilities: List[str] = Field(default_factory=list, description="List of capabilities (e.g., 'text', 'images', 'audio')")
    max_tokens: int = Field(8192, description="Maximum tokens supported by the model")
    is_default: bool = Field(False, description="Whether this is the default provider")
    config: Dict[str, Any] = Field(default_factory=dict, description="Provider-specific configuration")

class ProviderResponse(BaseModel):
    """Response model for provider information"""
    providers: Dict[str, str] = Field(..., description="Dictionary of provider names to model names")
    default_provider: str = Field(..., description="Name of the default provider")

class ProviderCapabilitiesResponse(BaseModel):
    """Response model for provider capabilities"""
    providers: List[LLMProvider] = Field(..., description="List of provider information")
    default_provider: str = Field(..., description="Name of the default provider")

class ModelParameters(BaseModel):
    """Model for LLM generation parameters"""
    temperature: float = Field(0.7, description="Temperature for response generation (0.0-1.0)")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    top_p: Optional[float] = Field(None, description="Nucleus sampling parameter")
    frequency_penalty: Optional[float] = Field(None, description="Frequency penalty parameter")
    presence_penalty: Optional[float] = Field(None, description="Presence penalty parameter")
    stop_sequences: Optional[List[str]] = Field(None, description="Sequences that will stop generation")

class ProviderGenerateRequest(BaseModel):
    """Extended request model for generating a response with parameters"""
    system_prompt: str = Field(..., description="System prompt for the model")
    user_prompt: str = Field(..., description="User prompt for the model")
    role_id: Optional[str] = Field(None, description="Optional role ID for context")
    provider_name: Optional[str] = Field(None, description="Optional provider name to use")
    parameters: Optional[ModelParameters] = Field(None, description="Optional generation parameters")

class ProviderGenerateResponse(BaseModel):
    """Response model for generated content"""
    response: str = Field(..., description="Generated response")
    provider_name: str = Field(..., description="Provider used for generation")
    model_name: str = Field(..., description="Model used for generation")
    usage: Optional[Dict[str, int]] = Field(None, description="Token usage information if available")
