import re
from typing import List, Dict, Any, Optional, Tuple
from app.models.role import Role

class TriggerService:
    """Service for detecting triggers and managing context switching"""
    
    def __init__(self):
        """Initialize the trigger service"""
        # Dictionary to store role triggers
        # Format: {role_id: [{"pattern": regex_pattern, "priority": int}]}
        self.role_triggers: Dict[str, List[Dict[str, Any]]] = {}
        
        # Default trigger patterns for common domains
        self.default_domain_triggers = {
            "finance": [
                r"\b(?:finance|financial|money|budget|invest|stock|market|economy)\b",
                r"\b(?:roi|revenue|profit|loss|balance sheet|income statement)\b"
            ],
            "technology": [
                r"\b(?:tech|technology|software|hardware|code|program|app|application)\b",
                r"\b(?:algorithm|database|server|cloud|api|interface|frontend|backend)\b"
            ],
            "healthcare": [
                r"\b(?:health|medical|doctor|patient|disease|treatment|medicine|drug)\b",
                r"\b(?:symptom|diagnosis|therapy|hospital|clinic|prescription)\b"
            ],
            "marketing": [
                r"\b(?:marketing|advertise|campaign|brand|customer|audience|market)\b",
                r"\b(?:seo|ppc|conversion|lead|funnel|engagement|retention)\b"
            ],
            "legal": [
                r"\b(?:legal|law|contract|agreement|compliance|regulation|policy)\b",
                r"\b(?:liability|lawsuit|attorney|court|judge|plaintiff|defendant)\b"
            ],
            "education": [
                r"\b(?:education|school|teach|learn|student|course|curriculum)\b",
                r"\b(?:lesson|assignment|exam|test|grade|professor|instructor)\b"
            ],
            "creative": [
                r"\b(?:creative|design|art|artist|write|writer|create|craft)\b",
                r"\b(?:story|novel|poem|script|character|plot|theme|setting)\b"
            ]
        }
    
    async def register_role_triggers(self, role: Role, custom_triggers: Optional[List[str]] = None) -> None:
        """Register triggers for a role
        
        Args:
            role: The role to register triggers for
            custom_triggers: Optional list of custom trigger patterns
        """
        # Initialize triggers list for this role
        self.role_triggers[role.id] = []
        
        # Add domain-based triggers
        for domain in role.domains:
            domain_lower = domain.lower()
            # Check if we have default triggers for this domain
            if domain_lower in self.default_domain_triggers:
                for pattern in self.default_domain_triggers[domain_lower]:
                    self.role_triggers[role.id].append({
                        "pattern": pattern,
                        "priority": 1,  # Default priority
                        "source": f"domain:{domain_lower}"
                    })
        
        # Add name-based trigger
        self.role_triggers[role.id].append({
            "pattern": f"\\b{re.escape(role.name.lower())}\\b",
            "priority": 2,  # Higher priority than domain triggers
            "source": "name"
        })
        
        # Add custom triggers if provided
        if custom_triggers:
            for i, trigger in enumerate(custom_triggers):
                self.role_triggers[role.id].append({
                    "pattern": trigger,
                    "priority": 3 + i,  # Highest priority, preserve order
                    "source": "custom"
                })
    
    async def unregister_role_triggers(self, role_id: str) -> None:
        """Unregister triggers for a role
        
        Args:
            role_id: The ID of the role to unregister triggers for
        """
        if role_id in self.role_triggers:
            del self.role_triggers[role_id]
    
    async def detect_triggers(self, query: str) -> List[Tuple[str, int]]:
        """Detect triggers in a query
        
        Args:
            query: The query to detect triggers in
            
        Returns:
            List of tuples containing role_id and match score
        """
        query_lower = query.lower()
        matches = []
        
        # Check each role's triggers
        for role_id, triggers in self.role_triggers.items():
            role_score = 0
            matched_priorities = set()
            
            for trigger in triggers:
                pattern = trigger["pattern"]
                priority = trigger["priority"]
                
                # Check if the pattern matches the query
                if re.search(pattern, query_lower, re.IGNORECASE):
                    # Add the priority to the score
                    role_score += priority
                    matched_priorities.add(priority)
            
            # Only consider roles with at least one match
            if role_score > 0:
                # Bonus for matching multiple trigger types (diversity bonus)
                diversity_bonus = len(matched_priorities) * 2
                final_score = role_score + diversity_bonus
                
                matches.append((role_id, final_score))
        
        # Sort by score in descending order
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches
    
    async def get_best_role_for_query(self, query: str, current_role_id: Optional[str] = None) -> Optional[str]:
        """Get the best role for a query
        
        Args:
            query: The query to find the best role for
            current_role_id: The current role ID, if any
            
        Returns:
            The ID of the best role, or None if no triggers matched
        """
        matches = await self.detect_triggers(query)
        
        if not matches:
            return None
        
        # If we have a current role and it's in the top matches with a decent score,
        # prefer to stay with it to avoid unnecessary switching
        if current_role_id:
            # Find the current role in matches
            current_role_score = next((score for role_id, score in matches if role_id == current_role_id), 0)
            
            # Find the top score
            top_role_id, top_score = matches[0]
            
            # If the current role has a score at least 80% of the top score, stick with it
            if current_role_score >= top_score * 0.8:
                return current_role_id
        
        # Otherwise, return the top match
        return matches[0][0] if matches else None
    
    async def add_custom_trigger(self, role_id: str, trigger_pattern: str, priority: int = 3) -> bool:
        """Add a custom trigger for a role
        
        Args:
            role_id: The ID of the role to add the trigger for
            trigger_pattern: The regex pattern for the trigger
            priority: The priority of the trigger (higher = more important)
            
        Returns:
            True if successful, False otherwise
        """
        if role_id not in self.role_triggers:
            self.role_triggers[role_id] = []
        
        # Check if the pattern is valid regex
        try:
            re.compile(trigger_pattern)
        except re.error:
            return False
        
        # Add the trigger
        self.role_triggers[role_id].append({
            "pattern": trigger_pattern,
            "priority": priority,
            "source": "custom"
        })
        
        return True
    
    async def remove_custom_trigger(self, role_id: str, trigger_pattern: str) -> bool:
        """Remove a custom trigger for a role
        
        Args:
            role_id: The ID of the role to remove the trigger from
            trigger_pattern: The regex pattern of the trigger to remove
            
        Returns:
            True if successful, False otherwise
        """
        if role_id not in self.role_triggers:
            return False
        
        # Find the trigger
        for i, trigger in enumerate(self.role_triggers[role_id]):
            if trigger["pattern"] == trigger_pattern and trigger["source"] == "custom":
                # Remove the trigger
                self.role_triggers[role_id].pop(i)
                return True
        
        return False
    
    async def get_role_triggers(self, role_id: str) -> List[Dict[str, Any]]:
        """Get all triggers for a role
        
        Args:
            role_id: The ID of the role to get triggers for
            
        Returns:
            List of triggers for the role
        """
        if role_id not in self.role_triggers:
            return []
        
        return self.role_triggers[role_id]
