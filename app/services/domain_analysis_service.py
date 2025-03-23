import json
from typing import Dict, List, Any, Optional
from app.models.role import Role
from app.services.llm_providers.base_provider import BaseLLMProvider

class DomainAnalysisService:
    """Service for domain-specific contextual analysis
    
    This service provides specialized analysis capabilities for different domains,
    allowing for more targeted and relevant insights based on the role's expertise.
    """
    
    # Domain-specific analysis templates with specialized prompts and extraction patterns
    DOMAIN_TEMPLATES = {
        "finance": {
            "analysis_prompt": "Analyze the following financial information and provide insights on key metrics, trends, and recommendations:",
            "extraction_patterns": [
                "revenue", "profit", "cash flow", "ROI", "budget", "investment", "expense", 
                "financial statement", "balance sheet", "income statement", "cash flow statement"
            ],
            "metrics": ["profit margin", "ROI", "cash flow", "debt-to-equity", "operating margin"],
            "frameworks": ["SWOT analysis", "financial ratio analysis", "cash flow analysis", "break-even analysis"]
        },
        "marketing": {
            "analysis_prompt": "Analyze the following marketing information and provide insights on audience, messaging, channels, and campaign effectiveness:",
            "extraction_patterns": [
                "campaign", "audience", "conversion", "engagement", "brand", "messaging", 
                "social media", "content", "SEO", "PPC", "email marketing"
            ],
            "metrics": ["conversion rate", "CAC", "CTR", "engagement rate", "ROAS"],
            "frameworks": ["marketing funnel analysis", "customer journey mapping", "competitive positioning"]
        },
        "operations": {
            "analysis_prompt": "Analyze the following operational information and provide insights on processes, efficiency, and optimization opportunities:",
            "extraction_patterns": [
                "process", "workflow", "efficiency", "productivity", "supply chain", 
                "inventory", "logistics", "quality control", "throughput"
            ],
            "metrics": ["cycle time", "throughput", "defect rate", "inventory turnover", "OEE"],
            "frameworks": ["lean analysis", "six sigma", "process mapping", "value stream mapping"]
        },
        "sales": {
            "analysis_prompt": "Analyze the following sales information and provide insights on pipeline, conversion, and revenue opportunities:",
            "extraction_patterns": [
                "pipeline", "lead", "opportunity", "close rate", "revenue", "sales cycle", 
                "customer acquisition", "upsell", "cross-sell", "churn"
            ],
            "metrics": ["close rate", "sales cycle length", "average deal size", "pipeline velocity"],
            "frameworks": ["sales funnel analysis", "win/loss analysis", "territory analysis"]
        },
        "leadership": {
            "analysis_prompt": "Analyze the following leadership and strategy information and provide executive-level insights and recommendations:",
            "extraction_patterns": [
                "strategy", "vision", "mission", "leadership", "team", "culture", 
                "growth", "market", "competition", "innovation"
            ],
            "metrics": ["market share", "growth rate", "employee satisfaction", "innovation index"],
            "frameworks": ["SWOT analysis", "PESTEL analysis", "Porter's Five Forces", "OKR framework"]
        },
        "human resources": {
            "analysis_prompt": "Analyze the following HR and talent information and provide insights on team development, culture, and talent management:",
            "extraction_patterns": [
                "hiring", "talent", "recruitment", "retention", "performance", 
                "culture", "engagement", "development", "training", "compensation"
            ],
            "metrics": ["turnover rate", "time-to-hire", "employee satisfaction", "training ROI"],
            "frameworks": ["talent mapping", "performance matrix", "engagement analysis"]
        },
        "technology": {
            "analysis_prompt": "Analyze the following technology information and provide insights on solutions, architecture, and implementation strategies:",
            "extraction_patterns": [
                "software", "hardware", "cloud", "infrastructure", "architecture", 
                "development", "security", "data", "integration", "API"
            ],
            "metrics": ["uptime", "response time", "error rate", "deployment frequency", "MTTR"],
            "frameworks": ["technology stack analysis", "architecture review", "security assessment"]
        },
        "legal": {
            "analysis_prompt": "Analyze the following legal information and provide insights on compliance, risk, and legal strategy:",
            "extraction_patterns": [
                "contract", "compliance", "regulation", "risk", "liability", 
                "intellectual property", "privacy", "terms", "agreement"
            ],
            "metrics": ["compliance rate", "contract review time", "litigation exposure"],
            "frameworks": ["legal risk assessment", "contract analysis", "compliance review"]
        }
    }
    
    def __init__(self):
        """Initialize the domain analysis service"""
        pass
    
    def get_domain_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get all available domain templates
        
        Returns:
            Dictionary of domain templates
        """
        return self.DOMAIN_TEMPLATES
    
    def get_domain_template(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get a specific domain template
        
        Args:
            domain: The domain to get template for
            
        Returns:
            The domain template or None if not found
        """
        # Normalize domain name for matching
        domain_lower = domain.lower()
        
        # Direct match
        if domain_lower in self.DOMAIN_TEMPLATES:
            return self.DOMAIN_TEMPLATES[domain_lower]
        
        # Partial match
        for template_domain, template in self.DOMAIN_TEMPLATES.items():
            if template_domain in domain_lower or domain_lower in template_domain:
                return template
        
        return None
    
    def get_relevant_domains(self, role: Role) -> List[Dict[str, Any]]:
        """Get relevant domain templates for a role
        
        Args:
            role: The role to get domain templates for
            
        Returns:
            List of relevant domain templates
        """
        relevant_templates = []
        
        for domain in role.domains:
            template = self.get_domain_template(domain)
            if template:
                relevant_templates.append({
                    "domain": domain,
                    "template": template
                })
        
        return relevant_templates
    
    def analyze_content(self, content: str, role: Role) -> Dict[str, Any]:
        """Analyze content based on role domains
        
        Args:
            content: The content to analyze
            role: The role to use for analysis
            
        Returns:
            Analysis results with domain-specific insights
        """
        results = {
            "role_id": role.id,
            "role_name": role.name,
            "domains": role.domains,
            "domain_analysis": []
        }
        
        # Get relevant domain templates
        relevant_domains = self.get_relevant_domains(role)
        
        for domain_info in relevant_domains:
            domain = domain_info["domain"]
            template = domain_info["template"]
            
            # Extract domain-specific patterns
            extracted_patterns = self._extract_patterns(content, template["extraction_patterns"])
            
            # Add domain analysis
            if extracted_patterns:
                results["domain_analysis"].append({
                    "domain": domain,
                    "extracted_patterns": extracted_patterns,
                    "relevant_metrics": template["metrics"],
                    "suggested_frameworks": template["frameworks"],
                    "analysis_prompt": template["analysis_prompt"]
                })
        
        return results
    
    def enhance_prompt_with_domain_analysis(self, system_prompt: str, content: str, role: Role) -> str:
        """Enhance system prompt with domain-specific analysis guidance
        
        Args:
            system_prompt: The original system prompt
            content: The content to analyze
            role: The role to use for analysis
            
        Returns:
            Enhanced system prompt with domain-specific guidance
        """
        # Analyze content for domain-specific patterns
        analysis = self.analyze_content(content, role)
        
        # If no domain analysis, return original prompt
        if not analysis["domain_analysis"]:
            return system_prompt
        
        # Build domain-specific guidance
        domain_guidance = ["\n\n## Domain-Specific Analysis Guidance:"]
        
        for domain_analysis in analysis["domain_analysis"]:
            domain = domain_analysis["domain"]
            guidance = f"\n### {domain.title()} Analysis:\n"
            guidance += f"{domain_analysis['analysis_prompt']}\n"
            
            if domain_analysis["extracted_patterns"]:
                guidance += "\nRelevant terms identified: " + ", ".join(domain_analysis["extracted_patterns"]) + "\n"
            
            guidance += "\nKey metrics to consider: " + ", ".join(domain_analysis["relevant_metrics"]) + "\n"
            guidance += "\nRecommended frameworks: " + ", ".join(domain_analysis["suggested_frameworks"]) + "\n"
            
            domain_guidance.append(guidance)
        
        # Add domain guidance to system prompt
        enhanced_prompt = system_prompt + "\n" + "\n".join(domain_guidance)
        return enhanced_prompt
    
    def _extract_patterns(self, content: str, patterns: List[str]) -> List[str]:
        """Extract domain-specific patterns from content
        
        Args:
            content: The content to extract patterns from
            patterns: List of patterns to extract
            
        Returns:
            List of extracted patterns
        """
        extracted = []
        content_lower = content.lower()
        
        for pattern in patterns:
            if pattern.lower() in content_lower:
                extracted.append(pattern)
        
        return extracted
