import logging
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.types import (
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
)
from a2a.utils import (
    new_agent_text_message,
    new_task,
    new_text_artifact,
    new_data_artifact,
)
from agent import HelloWorldAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HelloWorldAgentExecutor(AgentExecutor):
    """
    HelloWorld Agent executor with complete task lifecycle management.
    """

    def __init__(self):
        self.agent = HelloWorldAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute a HelloWorld task with complete lifecycle management."""
        query = context.get_user_input()
        task = context.current_task
        
        # 1. Criar tarefa se não existir
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)
            logger.info(f"Created new task: {task.id}")

        # 2. Marcar tarefa como em andamento
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                status=TaskStatus(
                    state=TaskState.working,
                    message=new_agent_text_message(
                        "Processing your request...",
                        task.contextId,
                        task.id,
                    ),
                ),
                final=False,
                contextId=task.contextId,
                taskId=task.id,
            )
        )
        logger.info(f"Task {task.id} marked as working")

        try:
            # 3. Executar a lógica do agente
            result = await self.agent.process_request(query, task.contextId)
            
            is_task_complete = result.get("is_task_complete", True)
            success = result.get("success", True)
            result_text = result.get("result", "Hello World!")
            
            # 4. Criar artefato com resultado
            if success:
                artifact = new_text_artifact(
                    name="hello_world_result",
                    description="HelloWorld intelligent response",
                    text=result_text,
                )
            else:
                artifact = new_text_artifact(
                    name="error_result",
                    description="Error response",
                    text=result_text,
                )

            # 5. Enviar artefato
            await event_queue.enqueue_event(
                TaskArtifactUpdateEvent(
                    append=False,
                    contextId=task.contextId,
                    taskId=task.id,
                    lastChunk=True,
                    artifact=artifact,
                )
            )
            logger.info(f"Artifact sent for task {task.id}")

            # 6. Marcar tarefa como completa ✅
            if is_task_complete:
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(
                            state=TaskState.completed,
                            message=new_agent_text_message(
                                "Task completed successfully",
                                task.contextId,
                                task.id,
                            ),
                        ),
                        final=True,
                        contextId=task.contextId,
                        taskId=task.id,
                    )
                )
                logger.info(f"Task {task.id} marked as COMPLETED ✅")
            else:
                # Marcar como necessitando input do usuário
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(
                            state=TaskState.input_required,
                            message=new_agent_text_message(
                                "Waiting for user input",
                                task.contextId,
                                task.id,
                            ),
                        ),
                        final=False,
                        contextId=task.contextId,
                        taskId=task.id,
                    )
                )
                logger.info(f"Task {task.id} requires user input")

        except Exception as e:
            logger.exception(f"Error executing task {task.id}")
            
            # Marcar tarefa como falhou
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    status=TaskStatus(
                        state=TaskState.failed,
                        message=new_agent_text_message(
                            f"Error: {str(e)}",
                            task.contextId,
                            task.id,
                        ),
                    ),
                    final=True,
                    contextId=task.contextId,
                    taskId=task.id,
                )
            )
            logger.error(f"Task {task.id} marked as FAILED")

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel a running task."""
        task = context.current_task
        if task:
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    status=TaskStatus(
                        state=TaskState.cancelled,
                        message=new_agent_text_message(
                            "Task cancelled by user",
                            task.contextId,
                            task.id,
                        ),
                    ),
                    final=True,
                    contextId=task.contextId,
                    taskId=task.id,
                )
            )
            logger.info(f"Task {task.id} cancelled")
        else:
            logger.warning("No task to cancel")

    # Método de skill único
    async def hello_world(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Send an intelligent Hello World message."""
        await self.execute(context, event_queue)

    async def find_and_greet_agent(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Locate other agents using MCP and greet them."""
        # Implementação MCP mantida para compatibilidade
        from .mcp import client as mcp_client
        from a2a.client import A2AClient

        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        try:
            # Marcar como em andamento
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    status=TaskStatus(state=TaskState.working),
                    contextId=task.contextId,
                    taskId=task.id,
                )
            )

            # Find agents using the MCP client
            agents = await mcp_client.find_agents("hello world")
            if not agents:
                result = "No agents found."
            else:
                results = []
                for agent in agents:
                    client = A2AClient(agent_card=agent)
                    async with client.connect() as connection:
                        response = await connection.execute_skill("hello_world")
                        results.append(f"Agent {agent.name} responded: {response}")
                result = "\n".join(results)

            # Criar artefato e marcar como completa
            artifact = new_text_artifact(
                name="greet_agents_result",
                description="Results from greeting other agents",
                text=result,
            )
            
            await event_queue.enqueue_event(
                TaskArtifactUpdateEvent(
                    contextId=task.contextId,
                    taskId=task.id,
                    artifact=artifact,
                    lastChunk=True,
                )
            )
            
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    status=TaskStatus(state=TaskState.completed),
                    final=True,
                    contextId=task.contextId,
                    taskId=task.id,
                )
            )
            
        except Exception as e:
            logger.exception(f"Error in find_and_greet_agent")
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    status=TaskStatus(state=TaskState.failed),
                    final=True,
                    contextId=task.contextId,
                    taskId=task.id,
                )
            )


