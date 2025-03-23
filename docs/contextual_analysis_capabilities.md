# Contextual Analysis Capabilities for Specialized Domains

## Overview

The MCP Server now includes powerful contextual analysis capabilities for specialized domains, allowing for more targeted and relevant AI responses based on domain-specific expertise. This feature enhances the role-based system by automatically identifying domain terminology, suggesting relevant metrics, and incorporating appropriate analytical frameworks into AI responses.

## Key Features

- **Domain-Specific Templates**: Pre-configured analysis templates for various business domains
- **Pattern Extraction**: Automatic identification of domain-specific terminology in user queries
- **Specialized Metrics**: Domain-relevant KPIs and metrics for each business area
- **Analysis Frameworks**: Suggested analytical approaches for different domains
- **Enhanced Prompts**: Automatic enhancement of system prompts with domain-specific guidance
- **API Endpoints**: Dedicated endpoints for domain template management and content analysis

## Supported Domains

The system currently supports the following specialized domains:

| Domain | Description | Example Metrics | Example Frameworks |
|--------|-------------|-----------------|--------------------|
| Finance | Financial analysis and planning | Profit margin, ROI, Cash flow | Financial ratio analysis, Break-even analysis |
| Marketing | Marketing strategy and campaigns | Conversion rate, CAC, ROAS | Marketing funnel analysis, Customer journey mapping |
| Operations | Process optimization and efficiency | Cycle time, Throughput, OEE | Lean analysis, Process mapping |
| Sales | Pipeline management and revenue growth | Close rate, Sales cycle length | Sales funnel analysis, Win/loss analysis |
| Leadership | Executive strategy and vision | Market share, Growth rate | SWOT analysis, PESTEL analysis |
| Human Resources | Talent management and culture | Turnover rate, Time-to-hire | Talent mapping, Engagement analysis |
| Technology | Tech solutions and architecture | Uptime, Response time, MTTR | Technology stack analysis, Architecture review |
| Legal | Compliance and risk management | Compliance rate, Litigation exposure | Legal risk assessment, Compliance review |

## How It Works

### Domain Analysis Process

1. **Domain Identification**: When a user submits a query, the system identifies the role's domains of expertise.
2. **Pattern Extraction**: The system scans the query for domain-specific terminology and patterns.
3. **Template Selection**: Appropriate domain templates are selected based on the role's expertise areas.
4. **Prompt Enhancement**: The system prompt is enhanced with domain-specific analysis guidance.
5. **Response Generation**: The AI generates a response incorporating domain-specific insights, metrics, and frameworks.

### Integration with Role System

The domain analysis capabilities are deeply integrated with the role system:

- Each role has defined domains of expertise (e.g., "finance", "marketing", "operations")
- The system automatically selects relevant domain templates based on the role's expertise
- Multiple domains can be analyzed simultaneously for roles with cross-functional expertise
- Domain-specific guidance is incorporated into the system prompt for each query

## API Endpoints

### Get All Domain Templates

```
GET /api/v1/domain-analysis/domains
```

Returns all available domain templates with their analysis prompts, extraction patterns, metrics, and frameworks.

#### Response Example

```json
{
  "domains": ["finance", "marketing", "operations", "sales", "leadership", "human resources", "technology", "legal"],
  "templates": {
    "finance": {
      "analysis_prompt": "Analyze the following financial information and provide insights on key metrics, trends, and recommendations:",
      "extraction_patterns": ["revenue", "profit", "cash flow", "ROI", "budget", "investment", "expense"],
      "metrics": ["profit margin", "ROI", "cash flow", "debt-to-equity", "operating margin"],
      "frameworks": ["SWOT analysis", "financial ratio analysis", "cash flow analysis", "break-even analysis"]
    },
    // Other domains...
  }
}
```

### Get Specific Domain Template

```
GET /api/v1/domain-analysis/domains/{domain}
```

Returns a specific domain template by name.

#### Response Example

```json
{
  "domain": "finance",
  "template": {
    "analysis_prompt": "Analyze the following financial information and provide insights on key metrics, trends, and recommendations:",
    "extraction_patterns": ["revenue", "profit", "cash flow", "ROI", "budget", "investment", "expense"],
    "metrics": ["profit margin", "ROI", "cash flow", "debt-to-equity", "operating margin"],
    "frameworks": ["SWOT analysis", "financial ratio analysis", "cash flow analysis", "break-even analysis"]
  }
}
```

### Analyze Content

```
POST /api/v1/domain-analysis/analyze
```

Analyzes content based on a role's domains of expertise.

#### Request Example

```json
{
  "content": "We need to improve our marketing campaign ROI. Our current conversion rate is only 2.3% and our customer acquisition cost is too high at $75 per customer.",
  "role_id": "cmo-advisor"
}
```

#### Response Example

```json
{
  "role_id": "cmo-advisor",
  "role_name": "CMO Advisor",
  "domains": ["marketing", "branding", "customer acquisition", "digital marketing", "content strategy"],
  "domain_analysis": [
    {
      "domain": "marketing",
      "extracted_patterns": ["campaign", "conversion", "customer acquisition"],
      "relevant_metrics": ["conversion rate", "CAC", "CTR", "engagement rate", "ROAS"],
      "suggested_frameworks": ["marketing funnel analysis", "customer journey mapping", "competitive positioning"],
      "analysis_prompt": "Analyze the following marketing information and provide insights on audience, messaging, channels, and campaign effectiveness:"
    }
  ]
}
```

## Implementation Details

### Domain Analysis Service

The `DomainAnalysisService` class provides the core functionality for domain-specific analysis:

```python
class DomainAnalysisService:
    """Service for domain-specific contextual analysis
    
    This service provides specialized analysis capabilities for different domains,
    allowing for more targeted and relevant insights based on the role's expertise.
    """
    
    # Domain-specific analysis templates with specialized prompts and extraction patterns
    DOMAIN_TEMPLATES = {
        "finance": { ... },
        "marketing": { ... },
        # Other domains...
    }
    
    def get_domain_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get all available domain templates"""
        ...
    
    def get_domain_template(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get a specific domain template"""
        ...
    
    def get_relevant_domains(self, role: Role) -> List[Dict[str, Any]]:
        """Get relevant domain templates for a role"""
        ...
    
    def analyze_content(self, content: str, role: Role) -> Dict[str, Any]:
        """Analyze content based on role domains"""
        ...
    
    def enhance_prompt_with_domain_analysis(self, system_prompt: str, content: str, role: Role) -> str:
        """Enhance system prompt with domain-specific analysis guidance"""
        ...
```

### Integration with Role Service

The domain analysis capabilities are integrated with the `RoleService` class to enhance query processing:

```python
async def process_query(self, role_id: str, query: str, custom_instructions: Optional[str] = None) -> str:
    # Get the role
    role = await self.get_role(role_id)
    
    # Generate the system prompt
    system_prompt = await self.generate_complete_prompt(role_id, custom_instructions)
    
    # Enhance prompt with domain-specific analysis
    system_prompt = self.domain_analysis_service.enhance_prompt_with_domain_analysis(system_prompt, query, role)
    
    # Generate the response
    response = await self.ai_processor.generate_response(system_prompt, query, role_id=role_id)
    
    # Return the response
    return response
```

## Example Usage

### Example 1: Financial Analysis

**User Query to CFO Advisor:**
```
Our revenue increased by 15% last quarter, but our profit margin decreased from 22% to 18%. What might be causing this and what should we do?
```

**System Analysis:**
- Role domains: finance, accounting, cash flow, budgeting, investment
- Extracted patterns: revenue, profit margin
- Relevant metrics: profit margin, operating margin
- Suggested frameworks: financial ratio analysis

**Enhanced Prompt Guidance:**
```
Analyze the following financial information and provide insights on key metrics, trends, and recommendations:

Relevant terms identified: revenue, profit margin

Key metrics to consider: profit margin, ROI, cash flow, debt-to-equity, operating margin

Recommended frameworks: SWOT analysis, financial ratio analysis, cash flow analysis, break-even analysis
```

### Example 2: Marketing Strategy

**User Query to CMO Advisor:**
```
Our social media engagement is down 12% this month despite increasing our posting frequency. What should we change in our content strategy?
```

**System Analysis:**
- Role domains: marketing, branding, customer acquisition, digital marketing, content strategy
- Extracted patterns: social media, engagement, content
- Relevant metrics: engagement rate
- Suggested frameworks: content strategy analysis

**Enhanced Prompt Guidance:**
```
Analyze the following marketing information and provide insights on audience, messaging, channels, and campaign effectiveness:

Relevant terms identified: social media, engagement, content

Key metrics to consider: conversion rate, CAC, CTR, engagement rate, ROAS

Recommended frameworks: marketing funnel analysis, customer journey mapping, competitive positioning
```

## Extending Domain Capabilities

To add support for new domains or enhance existing ones:

1. Update the `DOMAIN_TEMPLATES` dictionary in the `DomainAnalysisService` class
2. Add appropriate extraction patterns, metrics, and frameworks for the new domain
3. Create an analysis prompt that guides the AI in providing domain-specific insights

Example of adding a new domain:

```python
"sustainability": {
    "analysis_prompt": "Analyze the following sustainability information and provide insights on environmental impact, resource efficiency, and ESG considerations:",
    "extraction_patterns": [
        "carbon footprint", "emissions", "renewable", "sustainable", "ESG", 
        "environmental", "green", "recycling", "waste reduction"
    ],
    "metrics": ["carbon emissions", "energy efficiency", "waste reduction", "water usage"],
    "frameworks": ["ESG analysis", "sustainability scorecard", "circular economy model"]
}
```

## Best Practices

1. **Define Clear Domains**: When creating roles, define clear and specific domains of expertise
2. **Use Domain-Specific Terminology**: Include relevant domain terminology in user queries to trigger pattern extraction
3. **Combine Domains**: For cross-functional advice, create roles with multiple domains (e.g., "finance" and "operations")
4. **Review Analysis Results**: Use the `/analyze` endpoint to review how the system is interpreting queries
5. **Extend Templates**: Add new extraction patterns, metrics, and frameworks as needed for your specific use cases
