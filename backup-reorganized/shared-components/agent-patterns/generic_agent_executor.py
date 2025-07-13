# Generic Agent Executor Pattern
# Extracted from multiple A2A MCP projects for reuse

import logging
from typing import Optional, Any

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    DataPart,
    InvalidParamsError,
    SendStreamingMessageSuccessResponse,
    Task,
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatusUpdateEvent,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import new_agent_text_message, new_task
from a2a.utils.errors import ServerError


logger = logging.getLogger(__name__)


class GenericAgentExecutor(AgentExecutor):
    """
    Reusable AgentExecutor pattern extracted from A2A MCP projects.
    
    This pattern is commonly used across:
    - a2a_mcp (travel agents)
    - a2a_mcp_estudar (study version)
    - analytics agent
    - other A2A framework agents
    """

    def __init__(self, agent):
        """Initialize with any agent that implements the BaseAgent interface."""
        self.agent = agent

    async def execute_task(self, task: Task, context: RequestContext) -> None:
        """Standard task execution pattern used across A2A agents."""
        try:
            # Standard pattern: extract message, process, return response
            if not task.data:
                raise InvalidParamsError("Task data is required")

            # Process the task using the agent
            response = await self.agent.process_task(task, context)
            
            # Standard success response
            await context.event_queue.put(
                TaskStatusUpdateEvent(
                    task_id=task.id,
                    task_state=TaskState.COMPLETED,
                    task_result=response
                )
            )
            
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            await context.event_queue.put(
                TaskStatusUpdateEvent(
                    task_id=task.id,
                    task_state=TaskState.FAILED,
                    error_message=str(e)
                )
            )
            raise ServerError(str(e))

    # Additional common methods can be added here as patterns emerge