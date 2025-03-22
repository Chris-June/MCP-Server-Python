import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Literal
import numpy as np
from app.models.memory import Memory, MemoryCreate
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
            expires_at=expires_at
        )
        
        # Initialize role memories list if it doesn't exist
        if memory.role_id not in self.memories:
            self.memories[memory.role_id] = []
        
        # Add memory to storage
        self.memories[memory.role_id].append(memory)
        
        return memory
    
    async def get_memories_by_role_id(self, role_id: str, memory_type: Optional[str] = None) -> List[Memory]:
        """Get memories for a specific role
        
        Args:
            role_id: The ID of the role to get memories for
            memory_type: Optional type of memories to retrieve
            
        Returns:
            List of memories for the role
        """
        # Check if role has any memories
        if role_id not in self.memories:
            return []
        
        # Filter expired memories
        now = datetime.now()
        valid_memories = [m for m in self.memories[role_id] if not m.expires_at or m.expires_at > now]
        
        # Update the memories list to remove expired memories
        self.memories[role_id] = valid_memories
        
        # Filter by type if specified
        if memory_type:
            return [m for m in valid_memories if m.type == memory_type]
        
        return valid_memories
    
    async def get_relevant_memories(self, role_id: str, query: str, embedding: List[float], limit: int = 5) -> List[Memory]:
        """Get memories relevant to a query using vector similarity
        
        Args:
            role_id: The ID of the role to get memories for
            query: The query to find relevant memories for
            embedding: The vector embedding of the query
            limit: Maximum number of memories to return
            
        Returns:
            List of relevant memories
        """
        if not embedding or role_id not in self.memories:
            return []
        
        # Get all valid memories for the role
        memories = await self.get_memories_by_role_id(role_id)
        
        # Filter memories that have embeddings
        memories_with_embeddings = [m for m in memories if m.embedding]
        
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
            
            adjusted_score = similarity * importance_multiplier
            
            scores.append((memory, adjusted_score))
        
        # Sort by similarity score
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top memories
        return [m[0] for m in scores[:limit]]
    
    async def clear_memories_by_role_id(self, role_id: str, memory_type: Optional[str] = None) -> bool:
        """Clear memories for a specific role
        
        Args:
            role_id: The ID of the role to clear memories for
            memory_type: Optional type of memories to clear
            
        Returns:
            True if successful
        """
        if role_id not in self.memories:
            return True
        
        if memory_type:
            # Only remove memories of the specified type
            self.memories[role_id] = [m for m in self.memories[role_id] if m.type != memory_type]
        else:
            # Remove all memories for the role
            self.memories[role_id] = []
        
        return True
    
    async def close(self):
        """Clean up resources"""
        # In a production environment, this would clean up database connections
        pass
