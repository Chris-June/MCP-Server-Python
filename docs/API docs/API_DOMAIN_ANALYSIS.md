# Domain Analysis API

This document provides comprehensive documentation for the domain analysis endpoints in the MCP Server, including example requests and responses.

## Table of Contents

- [Get All Domain Templates](#get-all-domain-templates)
- [Get a Specific Domain Template](#get-a-specific-domain-template)
- [Analyze Content](#analyze-content)

## Get All Domain Templates

```
GET /api/v1/domain-analysis/domains
```

**Description:** Retrieves all available domain templates for analysis.

**Parameters:** None

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/domain-analysis/domains' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "domains": ["finance", "marketing", "operations", "sales", "hr", "technology", "legal"],
  "templates": {
    "finance": {
      "key_metrics": ["ROI", "NPV", "IRR", "Payback Period", "Debt-to-Equity Ratio"],
      "frameworks": ["CAPM", "DCF Analysis", "Financial Ratio Analysis"],
      "terminology": ["assets", "liabilities", "equity", "cash flow", "depreciation"],
      "patterns": ["\\b(?:ROI|ROE|EBITDA)\\b", "\\b(?:cash flow|balance sheet|income statement)\\b"]
    },
    "marketing": {
      "key_metrics": ["CAC", "LTV", "Conversion Rate", "Churn Rate", "ROAS"],
      "frameworks": ["4Ps", "SWOT Analysis", "Customer Journey Mapping"],
      "terminology": ["brand", "campaign", "conversion", "funnel", "engagement"],
      "patterns": ["\\b(?:CAC|LTV|ROAS)\\b", "\\b(?:brand|campaign|conversion|funnel)\\b"]
    }
  }
}
```

## Get a Specific Domain Template

```
GET /api/v1/domain-analysis/domains/{domain}
```

**Description:** Retrieves a specific domain template by name.

**Parameters:**
- `domain` (path parameter): The name of the domain template to retrieve.

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/domain-analysis/domains/finance' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "domain": "finance",
  "template": {
    "key_metrics": ["ROI", "NPV", "IRR", "Payback Period", "Debt-to-Equity Ratio"],
    "frameworks": ["CAPM", "DCF Analysis", "Financial Ratio Analysis"],
    "terminology": ["assets", "liabilities", "equity", "cash flow", "depreciation"],
    "patterns": ["\\b(?:ROI|ROE|EBITDA)\\b", "\\b(?:cash flow|balance sheet|income statement)\\b"]
  }
}
```

## Analyze Content

```
POST /api/v1/domain-analysis/analyze
```

**Description:** Analyzes content based on role domains and provides domain-specific insights.

**Request Body:**
```json
{
  "content": "string",
  "role_id": "string"
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/domain-analysis/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "We need to improve our marketing ROI and reduce our customer acquisition costs. Our current CAC is $150 and our LTV is $450.",
  "role_id": "marketing-specialist"
}'
```

**Example Response:**
```json
{
  "role_id": "marketing-specialist",
  "role_name": "Marketing Specialist",
  "domains": ["marketing", "branding", "social-media"],
  "domain_analysis": [
    {
      "domain": "marketing",
      "detected_terms": {
        "metrics": ["ROI", "CAC", "LTV"],
        "terminology": ["customer acquisition"]
      },
      "insights": [
        "The LTV:CAC ratio is 3:1, which is generally considered healthy (ideal is 3:1 or higher)",
        "Focus on improving ROI could involve optimizing marketing channels or improving conversion rates",
        "Consider strategies to increase LTV through customer retention and upselling"
      ],
      "relevant_frameworks": ["Customer Acquisition Framework", "LTV Optimization"]
    }
  ]
}
```
