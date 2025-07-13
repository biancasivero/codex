import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class HelloWorldAgent:
    """Simple Hello World agent with intelligent greeting."""

    def __init__(self):
        self.name = "HelloWorld Agent"
        self.description = "Intelligent agent that provides contextual hello world responses"

    async def hello_world(self, query: str, session_id: str) -> Dict[str, Any]:
        """Process a hello world request with intelligent response detection."""
        try:
            logger.info(f"Processing hello_world request: {query} (session: {session_id})")
            
            # Lógica inteligente para detectar tipo de resposta
            query_lower = query.lower()
            
            if any(word in query_lower for word in ["super", "amazing", "awesome", "fantastic", "incredible"]):
                result = "🌟 SUPER Hello World! 🌟"
                response_type = "super"
            elif any(word in query_lower for word in ["simple", "basic", "plain"]):
                result = "Hello World!"
                response_type = "basic"
            else:
                # Resposta padrão amigável
                result = "Hello World! 👋"
                response_type = "standard"
            
            return {
                "is_task_complete": True,
                "require_user_input": False,
                "result": result,
                "response_type": response_type,
                "success": True
            }
        except Exception as e:
            logger.exception(f"Error in hello_world for session {session_id}")
            return {
                "is_task_complete": False,
                "require_user_input": False,
                "result": f"Error: {str(e)}",
                "success": False
            }

    async def process_request(self, query: str, session_id: str, skill: str = None) -> Dict[str, Any]:
        """Process a general request."""
        return await self.hello_world(query, session_id) 