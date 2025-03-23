from typing import Dict, List, Any, Optional, Tuple
from app.services.trigger_service import TriggerService
from app.services.role_service import RoleService
from app.models.role import Role
from app.models.memory import Memory, MemoryCreate

class ContextSwitchingService:
    """Service for managing context switching between roles"""
    
    def __init__(self, role_service: RoleService, trigger_service: TriggerService):
        """Initialize the context switching service
        
        Args:
            role_service: Service for managing roles
            trigger_service: Service for detecting triggers
        """
        self.role_service = role_service
        self.trigger_service = trigger_service
        
        # Track active sessions
        # Format: {session_id: {"current_role_id": str, "history": List[Dict]}}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def initialize_roles(self) -> None:
        """Initialize triggers for all roles"""
        roles = await self.role_service.get_roles()
        for role in roles:
            await self.trigger_service.register_role_triggers(role)
    
    async def create_session(self, session_id: str, initial_role_id: str) -> Dict[str, Any]:
        """Create a new session
        
        Args:
            session_id: Unique identifier for the session
            initial_role_id: ID of the initial role to use
            
        Returns:
            Session information
        """
        # Verify the role exists
        role = await self.role_service.get_role(initial_role_id)
        
        # Create the session
        self.active_sessions[session_id] = {
            "current_role_id": initial_role_id,
            "history": [],
            "last_switch_reason": "Initial role selection"
        }
        
        return self.active_sessions[session_id]
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information
        
        Args:
            session_id: ID of the session to get
            
        Returns:
            Session information, or None if the session doesn't exist
        """
        return self.active_sessions.get(session_id)
    
    async def process_query_with_context_switching(
        self, 
        session_id: str, 
        query: str,
        custom_instructions: Optional[str] = None,
        force_role_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a query with context switching
        
        Args:
            session_id: ID of the session to use
            query: The query to process
            custom_instructions: Optional custom instructions
            force_role_id: Optional role ID to force using
            
        Returns:
            Result including response and context switching information
        """
        # Check if the session exists
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} does not exist")
        
        session = self.active_sessions[session_id]
        current_role_id = session["current_role_id"]
        
        # Determine the best role for this query
        context_switch = False
        switch_reason = None
        new_role_id = current_role_id
        
        if not force_role_id:
            detected_role_id = await self.trigger_service.get_best_role_for_query(query, current_role_id)
            
            # If we detected a different role and it's not the current one, switch
            if detected_role_id and detected_role_id != current_role_id:
                new_role_id = detected_role_id
                context_switch = True
                switch_reason = "Detected triggers for a different role"
        else:
            # Force using a specific role
            new_role_id = force_role_id
            if force_role_id != current_role_id:
                context_switch = True
                switch_reason = "Manually switched to a different role"
        
        # If we're switching context, update the session
        if context_switch:
            # Get the old and new role information
            old_role = await self.role_service.get_role(current_role_id)
            new_role = await self.role_service.get_role(new_role_id)
            
            # Record the switch in session history
            session["history"].append({
                "timestamp": "now",  # In a real implementation, use actual timestamp
                "from_role_id": current_role_id,
                "to_role_id": new_role_id,
                "reason": switch_reason,
                "query": query
            })
            
            # Update the current role
            session["current_role_id"] = new_role_id
            session["last_switch_reason"] = switch_reason
            
            # Add context switching information to custom instructions
            context_switch_info = f"""You are switching from the role of {old_role.name} to {new_role.name}.
            The user's query appears to be more relevant to your expertise as {new_role.name}.
            Previous role description: {old_role.description}
            Your new role description: {new_role.description}
            """
            
            if custom_instructions:
                custom_instructions = context_switch_info + "\n\n" + custom_instructions
            else:
                custom_instructions = context_switch_info
        
        # Process the query with the appropriate role
        response = await self.role_service.process_query(
            new_role_id,
            query,
            custom_instructions
        )
        
        # Return the result with context switching information
        return {
            "role_id": new_role_id,
            "query": query,
            "response": response,
            "context_switched": context_switch,
            "switch_reason": switch_reason if context_switch else None,
            "session_id": session_id
        }
    
    async def process_query_stream_with_context_switching(
        self, 
        session_id: str, 
        query: str,
        custom_instructions: Optional[str] = None,
        force_role_id: Optional[str] = None
    ):
        """Process a query with context switching and streaming response
        
        Args:
            session_id: ID of the session to use
            query: The query to process
            custom_instructions: Optional custom instructions
            force_role_id: Optional role ID to force using
            
        Yields:
            Chunks of the response along with context switching information
        """
        # Check if the session exists
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} does not exist")
        
        session = self.active_sessions[session_id]
        current_role_id = session["current_role_id"]
        
        # Determine the best role for this query
        context_switch = False
        switch_reason = None
        new_role_id = current_role_id
        
        if not force_role_id:
            detected_role_id = await self.trigger_service.get_best_role_for_query(query, current_role_id)
            
            # If we detected a different role and it's not the current one, switch
            if detected_role_id and detected_role_id != current_role_id:
                new_role_id = detected_role_id
                context_switch = True
                switch_reason = "Detected triggers for a different role"
        else:
            # Force using a specific role
            new_role_id = force_role_id
            if force_role_id != current_role_id:
                context_switch = True
                switch_reason = "Manually switched to a different role"
        
        # If we're switching context, update the session
        if context_switch:
            # Get the old and new role information
            old_role = await self.role_service.get_role(current_role_id)
            new_role = await self.role_service.get_role(new_role_id)
            
            # Record the switch in session history
            session["history"].append({
                "timestamp": "now",  # In a real implementation, use actual timestamp
                "from_role_id": current_role_id,
                "to_role_id": new_role_id,
                "reason": switch_reason,
                "query": query
            })
            
            # Update the current role
            session["current_role_id"] = new_role_id
            session["last_switch_reason"] = switch_reason
            
            # Add context switching information to custom instructions
            context_switch_info = f"""You are switching from the role of {old_role.name} to {new_role.name}.
            The user's query appears to be more relevant to your expertise as {new_role.name}.
            Previous role description: {old_role.description}
            Your new role description: {new_role.description}
            """
            
            if custom_instructions:
                custom_instructions = context_switch_info + "\n\n" + custom_instructions
            else:
                custom_instructions = context_switch_info
            
            # Yield context switch information as a special chunk
            context_switch_data = {
                "type": "context_switch",
                "from_role": {
                    "id": old_role.id,
                    "name": old_role.name
                },
                "to_role": {
                    "id": new_role.id,
                    "name": new_role.name
                },
                "reason": switch_reason
            }
            yield f"{{\"context_switch\":{context_switch_data}}}\n\n"
        
        # Process the query with streaming response
        async for chunk in self.role_service.process_query_stream(
            new_role_id,
            query,
            custom_instructions
        ):
            yield chunk
    
    async def manually_switch_context(
        self, 
        session_id: str, 
        new_role_id: str,
        reason: str = "Manual switch by user"
    ) -> Dict[str, Any]:
        """Manually switch the context to a different role
        
        Args:
            session_id: ID of the session to switch context for
            new_role_id: ID of the role to switch to
            reason: Reason for the switch
            
        Returns:
            Updated session information
        """
        # Check if the session exists
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} does not exist")
        
        session = self.active_sessions[session_id]
        current_role_id = session["current_role_id"]
        
        # If we're already using this role, do nothing
        if current_role_id == new_role_id:
            return session
        
        # Verify the new role exists
        new_role = await self.role_service.get_role(new_role_id)
        
        # Record the switch in session history
        session["history"].append({
            "timestamp": "now",  # In a real implementation, use actual timestamp
            "from_role_id": current_role_id,
            "to_role_id": new_role_id,
            "reason": reason,
            "query": None  # No query associated with this switch
        })
        
        # Update the current role
        session["current_role_id"] = new_role_id
        session["last_switch_reason"] = reason
        
        return session
    
    async def get_context_switch_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get the context switch history for a session
        
        Args:
            session_id: ID of the session to get history for
            
        Returns:
            List of context switches
        """
        # Check if the session exists
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} does not exist")
        
        return self.active_sessions[session_id]["history"]
    
    async def close_session(self, session_id: str) -> bool:
        """Close a session
        
        Args:
            session_id: ID of the session to close
            
        Returns:
            True if successful, False otherwise
        """
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            return True
        
        return False
