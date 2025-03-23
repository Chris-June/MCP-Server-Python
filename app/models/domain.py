from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

class DomainTemplate(BaseModel):
    """Model for domain-specific analysis templates"""
    analysis_prompt: str = Field(..., description="Prompt template for domain-specific analysis")
    extraction_patterns: List[str] = Field(..., description="Key patterns to extract from content for this domain")
    metrics: List[str] = Field(..., description="Key metrics relevant to this domain")
    frameworks: List[str] = Field(..., description="Analysis frameworks relevant to this domain")

class DomainAnalysisRequest(BaseModel):
    """Request model for domain analysis"""
    content: str = Field(..., description="Content to analyze")
    role_id: str = Field(..., description="ID of the role to use for analysis")

class ExtractedPattern(BaseModel):
    """Model for extracted patterns from content"""
    pattern: str = Field(..., description="The pattern that was extracted")
    occurrences: int = Field(1, description="Number of occurrences in the content")
    context: Optional[List[str]] = Field(None, description="Surrounding context for the pattern")

class DomainSpecificAnalysis(BaseModel):
    """Model for domain-specific analysis results"""
    domain: str = Field(..., description="The domain this analysis is for")
    extracted_patterns: List[ExtractedPattern] = Field(..., description="Patterns extracted from the content")
    relevant_metrics: List[str] = Field(..., description="Metrics relevant to this domain")
    suggested_frameworks: List[str] = Field(..., description="Analysis frameworks suggested for this domain")
    analysis_prompt: str = Field(..., description="The prompt used for analysis")

class DomainAnalysisResponse(BaseModel):
    """Response model for domain analysis"""
    role_id: str = Field(..., description="ID of the role used for analysis")
    role_name: str = Field(..., description="Name of the role used for analysis")
    domains: List[str] = Field(..., description="Domains of the role")
    domain_analysis: List[DomainSpecificAnalysis] = Field(..., description="Domain-specific analysis results")

class DomainTemplateResponse(BaseModel):
    """Response model for domain templates"""
    domains: List[str] = Field(..., description="Available domain names")
    templates: Dict[str, DomainTemplate] = Field(..., description="Domain templates")

class SpecificDomainTemplateResponse(BaseModel):
    """Response model for a specific domain template"""
    domain: str = Field(..., description="The domain name")
    template: DomainTemplate = Field(..., description="The domain template")

class EnhancedPromptRequest(BaseModel):
    """Request model for enhancing a prompt with domain analysis"""
    system_prompt: str = Field(..., description="Original system prompt")
    content: str = Field(..., description="Content to analyze")
    role_id: str = Field(..., description="ID of the role to use for analysis")

class EnhancedPromptResponse(BaseModel):
    """Response model for an enhanced prompt"""
    original_prompt: str = Field(..., description="The original system prompt")
    enhanced_prompt: str = Field(..., description="The enhanced system prompt")
    domains_applied: List[str] = Field(..., description="Domains that were applied in the enhancement")
