import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Literal, Set
import numpy as np
from app.models.memory import Memory, MemoryCreate
from app.models.role import Role
from app.config import settings

class MemoryService:
    """Service for managing memory storage and retrieval"""
    
    def __init__(self):
        """Initialize the memory service"""
        # In-memory storage for memories
        # For production, this would be replaced with a proper database
        self.memories: Dict[str, List[Memory]] = {}
    
    async def store_memory(self, memory_create: MemoryCreate, embedding: Optional[List[float]] = None) -> Memory:
        """Store a new memory
        
        Args:
            memory_create: The memory data to store
            embedding: Optional vector embedding of the memory content
            
        Returns:
            The stored memory
        """
        # Calculate expiration time based on memory type
        expires_at = None
        if memory_create.type == "session":
            expires_at = datetime.now() + timedelta(seconds=settings.memory_ttl_session)
        elif memory_create.type == "user":
            expires_at = datetime.now() + timedelta(seconds=settings.memory_ttl_user)
        elif memory_create.type == "knowledge":
            expires_at = datetime.now() + timedelta(seconds=settings.memory_ttl_knowledge)
        
        # Create the memory object
        memory = Memory(
            role_id=memory_create.role_id,
            content=memory_create.content,
            type=memory_create.type,
            importance=memory_create.importance,
            embedding=embedding,
            expires_at=expires_at,
            tags=memory_create.tags,
            category=memory_create.category,
            shared_with=memory_create.shared_with,
            parent_memory_id=memory_create.parent_memory_id
        )
        
        # Initialize role memories list if it doesn't exist
        if memory.role_id not in self.memories:
            self.memories[memory.role_id] = []
        
        # Add memory to storage
        self.memories[memory.role_id].append(memory)
        
        # If this memory is shared with other roles, add references to their memory collections
        for shared_role_id in memory.shared_with:
            if shared_role_id not in self.memories:
                self.memories[shared_role_id] = []
            
            # Create a shared copy with the parent memory ID reference
            shared_memory = Memory(
                role_id=shared_role_id,
                content=memory.content,
                type=memory.type,
                importance=memory.importance,
                embedding=memory.embedding,
                expires_at=memory.expires_at,
                tags=memory.tags,
                category=memory.category,
                shared_with=[],  # Don't propagate sharing further
                parent_memory_id=memory.id  # Reference the original memory
            )
            
            self.memories[shared_role_id].append(shared_memory)
        
        return memory
    
    async def get_memories_by_role_id(
        self, 
        role_id: str, 
        memory_type: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        include_shared: bool = True,
        include_inherited: bool = True,
        role: Optional[Role] = None
    ) -> List[Memory]:
        """Get memories for a specific role
        
        Args:
            role_id: The ID of the role to get memories for
            memory_type: Optional type of memories to retrieve
            category: Optional category to filter by
            tags: Optional list of tags to filter by (memories must have at least one matching tag)
            include_shared: Whether to include memories shared from other roles
            include_inherited: Whether to include memories inherited from parent roles
            role: Optional role object to use for inheritance settings
            
        Returns:
            List of memories for the role
        """
        # Initialize result list
        all_memories = []
        
        # Check if role has any memories
        if role_id in self.memories:
            # Filter expired memories
            now = datetime.now()
            valid_memories = [m for m in self.memories[role_id] if not m.expires_at or m.expires_at > now]
            
            # Update the memories list to remove expired memories
            self.memories[role_id] = valid_memories
            
            # Add to result list
            all_memories.extend(valid_memories)
        
        # Include inherited memories if requested and role has a parent
        if include_inherited and role and role.inherit_memories and role.parent_role_id:
            # Get parent role memories (recursive call)
            parent_memories = await self.get_memories_by_role_id(
                role_id=role.parent_role_id,
                memory_type=memory_type,
                category=category,
                tags=tags,
                include_shared=include_shared,
                include_inherited=True  # Continue up the inheritance chain
            )
            
            # Filter parent memories based on access level
            if role.memory_access_level == "standard":
                # Standard access only gets knowledge memories
                parent_memories = [m for m in parent_memories if m.type == "knowledge"]
            elif role.memory_access_level == "elevated":
                # Elevated access gets knowledge and user memories
                parent_memories = [m for m in parent_memories if m.type in ["knowledge", "user"]]
            # Admin access gets all memory types
            
            # Filter by categories if the role has specific memory categories
            if role.memory_categories:
                parent_memories = [
                    m for m in parent_memories 
                    if not m.category or m.category in role.memory_categories
                ]
            
            # Add inherited memories to result
            all_memories.extend(parent_memories)
        
        # Apply filters to all collected memories
        filtered_memories = all_memories
        
        # Filter by type if specified
        if memory_type:
            filtered_memories = [m for m in filtered_memories if m.type == memory_type]
        
        # Filter by category if specified
        if category:
            filtered_memories = [m for m in filtered_memories if m.category == category]
        
        # Filter by tags if specified
        if tags and len(tags) > 0:
            filtered_memories = [m for m in filtered_memories if any(tag in m.tags for tag in tags)]
        
        # Filter out shared memories if not requested
        if not include_shared:
            filtered_memories = [m for m in filtered_memories if not m.parent_memory_id]
        
        # Remove duplicates (in case of multiple inheritance paths)
        unique_memories = {}
        for memory in filtered_memories:
            if memory.id not in unique_memories:
                unique_memories[memory.id] = memory
        
        return list(unique_memories.values())
    
    async def get_relevant_memories(
        self, 
        role_id: str, 
        query: str, 
        embedding: List[float], 
        limit: int = 5,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        include_shared: bool = True,
        cross_role: bool = False,
        related_role_ids: Optional[List[str]] = None
    ) -> List[Memory]:
        """Get memories relevant to a query using vector similarity
        
        Args:
            role_id: The ID of the role to get memories for
            query: The query to find relevant memories for
            embedding: The vector embedding of the query
            limit: Maximum number of memories to return
            category: Optional category to filter by
            tags: Optional list of tags to filter by
            include_shared: Whether to include memories shared from other roles
            cross_role: Whether to search across all roles (for admin/supervisor roles)
            related_role_ids: Optional list of specific role IDs to include in the search
            
        Returns:
            List of relevant memories
        """
        if not embedding:
            return []
        
        # Determine which roles to search
        roles_to_search = []
        
        if cross_role:
            # Search across all roles
            roles_to_search = list(self.memories.keys())
        elif related_role_ids and len(related_role_ids) > 0:
            # Search only in specified roles
            roles_to_search = [r for r in related_role_ids if r in self.memories]
        else:
            # Search only in the specified role
            if role_id in self.memories:
                roles_to_search = [role_id]
        
        if not roles_to_search:
            return []
        
        # Collect all memories from relevant roles
        all_memories = []
        for r_id in roles_to_search:
            # Get memories with appropriate filters
            role_memories = await self.get_memories_by_role_id(
                r_id, 
                category=category,
                tags=tags,
                include_shared=include_shared
            )
            all_memories.extend(role_memories)
        
        # Filter memories that have embeddings
        memories_with_embeddings = [m for m in all_memories if m.embedding]
        
        if not memories_with_embeddings:
            return []
        
        # Calculate similarity scores
        # In a production environment, this would use a proper vector database
        scores = []
        for memory in memories_with_embeddings:
            # Skip memories without embeddings
            if not memory.embedding:
                continue
                
            # Convert embeddings to numpy arrays for calculation
            memory_embedding = np.array(memory.embedding)
            query_embedding = np.array(embedding)
            
            # Calculate cosine similarity
            similarity = np.dot(memory_embedding, query_embedding) / (
                np.linalg.norm(memory_embedding) * np.linalg.norm(query_embedding)
            )
            
            # Adjust score by importance
            importance_multiplier = {
                "low": 0.8,
                "medium": 1.0,
                "high": 1.2
            }.get(memory.importance, 1.0)
            
            # Adjust score by recency (newer memories get higher scores)
            time_diff = (datetime.now() - memory.created_at).total_seconds()
            recency_factor = max(0.8, 1.0 - (time_diff / (30 * 24 * 60 * 60)) * 0.2)  # Decay over 30 days
            
            # Adjust score by tag relevance if tags are provided
            tag_factor = 1.0
            if tags and len(tags) > 0 and memory.tags:
                matching_tags = sum(1 for tag in tags if tag in memory.tags)
                tag_factor = 1.0 + (matching_tags / len(tags)) * 0.2  # Up to 20% boost for matching tags
            
            # Calculate final score
            adjusted_score = similarity * importance_multiplier * recency_factor * tag_factor
            
            scores.append((memory, adjusted_score))
        
        # Sort by similarity score
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top memories
        return [m[0] for m in scores[:limit]]
    
    async def clear_memories_by_role_id(
        self, 
        role_id: str, 
        memory_type: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        shared_only: bool = False
    ) -> bool:
        """Clear memories for a specific role
        
        Args:
            role_id: The ID of the role to clear memories for
            memory_type: Optional type of memories to clear
            category: Optional category of memories to clear
            tags: Optional tags to filter which memories to clear
            shared_only: If True, only clear memories that were shared from other roles
            
        Returns:
            True if successful
        """
        if role_id not in self.memories:
            return True
        
        # Start with all memories
        memories = self.memories[role_id]
        
        # Apply filters to determine which memories to keep
        if memory_type:
            memories = [m for m in memories if m.type != memory_type]
        
        if category:
            memories = [m for m in memories if m.category != category]
        
        if tags and len(tags) > 0:
            memories = [m for m in memories if not any(tag in m.tags for tag in tags)]
        
        if shared_only:
            memories = [m for m in memories if not m.parent_memory_id]
        
        # Update the memories list
        self.memories[role_id] = memories
        
        return True
    
    async def get_role_inheritance_chain(self, role_id: str, role_service) -> List[Role]:
        """Get the inheritance chain for a role
        
        Args:
            role_id: The ID of the role to get the inheritance chain for
            role_service: The role service to use for role lookups
            
        Returns:
            List of roles in the inheritance chain, starting with the specified role
        """
        # Initialize result list and visited set to prevent cycles
        inheritance_chain = []
        visited_roles = set()
        
        # Start with the specified role
        current_role_id = role_id
        
        # Follow the inheritance chain
        while current_role_id and current_role_id not in visited_roles:
            # Mark as visited to prevent cycles
            visited_roles.add(current_role_id)
            
            # Get the role
            role = await role_service.get_role_by_id(current_role_id)
            if not role:
                break
                
            # Add to inheritance chain
            inheritance_chain.append(role)
            
            # Move to parent role
            current_role_id = role.parent_role_id if role.inherit_memories else None
        
        return inheritance_chain
    
    async def get_related_roles(self, role_id: str, role_service) -> List[str]:
        """Get related roles (roles that share memories or have inheritance relationships)
        
        Args:
            role_id: The ID of the role to get related roles for
            role_service: The role service to use for role lookups
            
        Returns:
            List of role IDs that are related to the specified role
        """
        related_roles = set()
        
        # Get the role
        role = await role_service.get_role_by_id(role_id)
        if not role:
            return []
            
        # Add parent role if inheriting memories
        if role.inherit_memories and role.parent_role_id:
            related_roles.add(role.parent_role_id)
            
        # Add child roles (roles that inherit from this role)
        all_roles = await role_service.get_roles()
        for other_role in all_roles:
            if other_role.parent_role_id == role_id and other_role.inherit_memories:
                related_roles.add(other_role.id)
                
        # Add roles that this role has shared memories with
        if role_id in self.memories:
            for memory in self.memories[role_id]:
                related_roles.update(memory.shared_with)
                
        # Add roles that have shared memories with this role
        for other_role_id in self.memories:
            if other_role_id == role_id:
                continue
                
            for memory in self.memories[other_role_id]:
                if role_id in memory.shared_with:
                    related_roles.add(other_role_id)
                    
        # Remove the original role ID from the set
        if role_id in related_roles:
            related_roles.remove(role_id)
            
        return list(related_roles)
    
    async def close(self):
        """Clean up resources"""
        # In a production environment, this would clean up database connections
        pass
