import logging
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.types import (
    Part,
    FilePart,
    FileWithBytes,
    TextPart,
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
)
from a2a.utils import (
    new_agent_text_message,
    new_task,
    new_text_artifact,
)
from agent import ChartGenerationAgent
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChartGenerationAgentExecutor(AgentExecutor):
    """
    Chart Generation Agent executor following HelloWorld Agent pattern.
    """

    def __init__(self):
        self.agent = ChartGenerationAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute a Chart Generation task following HelloWorld Agent pattern."""
        query = context.get_user_input()
        task = context.current_task
        
        # 1. Criar tarefa se não existir
        if not task:
            logger.info(f"Creating new task for message: {context.message}")
            
            # Verificar se context.message é válido
            if context.message is None:
                logger.warning("context.message is None, creating a default message")
                # Criar uma mensagem padrão
                from a2a.types import Message, Part, Role, TextPart
                default_message = Message(
                    messageId=f"chart-{uuid.uuid4()}",
                    contextId=context.context_id,
                    role=Role.user,
                    parts=[Part(root=TextPart(text=query or "Generate chart"))]
                )
                task = new_task(default_message)
            else:
                task = new_task(context.message)
            
            if task is None:
                logger.error("Failed to create task: new_task returned None")
                raise ValueError("Failed to create task")
            await event_queue.enqueue_event(task)
            logger.info(f"Created new task: {task.id}")

        # 2. Marcar tarefa como em andamento
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                status=TaskStatus(
                    state=TaskState.working,
                    message=new_agent_text_message(
                        "Processing chart generation request...",
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
            result = self.agent.invoke(query, task.contextId)
            logger.info(f"Agent invoke result: {result}")
            
            # Verificar se result é válido
            if result is None:
                logger.error("Agent invoke returned None")
                raise ValueError("Agent invoke returned None")
            
            # Verificar se result tem o atributo raw
            if not hasattr(result, 'raw'):
                logger.error(f"Agent invoke result missing 'raw' attribute: {result}")
                raise ValueError("Agent invoke result missing 'raw' attribute")
            
            # 4. Verificar se a geração foi bem-sucedida
            data = self.agent.get_image_data(
                session_id=task.contextId, image_key=result.raw
            )
            
            # Determinar se a task foi completada com sucesso
            is_task_complete = data and not data.error
            success = is_task_complete
            
            # 5. Criar artefato com resultado
            if success:
                # Success - create file artifact
                artifact = new_text_artifact(
                    name="chart_generation_result",
                    description="Chart generated successfully",
                    text=f"Chart generated: {data.name}",
                )
                # TODO: Convert to file artifact when needed
                logger.info(f"Chart generated successfully: {data.name}")
            else:
                # Error - create text artifact
                error_msg = data.error if data else 'Failed to generate chart image.'
                artifact = new_text_artifact(
                    name="error_result",
                    description="Chart generation error",
                    text=error_msg,
                )
                logger.error(f"Chart generation failed: {error_msg}")

            # 6. Enviar artefato
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

            # 7. Marcar tarefa como completa ✅ (APENAS SE SUCESSO)
            if is_task_complete:
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(
                            state=TaskState.completed,
                            message=new_agent_text_message(
                                "Chart generation completed successfully",
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
                # Marcar como falhou se houve erro
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        status=TaskStatus(
                            state=TaskState.failed,
                            message=new_agent_text_message(
                                f"Chart generation failed: {error_msg}",
                                task.contextId,
                                task.id,
                            ),
                        ),
                        final=True,
                        contextId=task.contextId,
                        taskId=task.id,
                    )
                )
                logger.info(f"Task {task.id} marked as FAILED")

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
        """Cancel a running chart generation task."""
        task = context.current_task
        if task:
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    status=TaskStatus(
                        state=TaskState.cancelled,
                        message=new_agent_text_message(
                            "Chart generation task cancelled by user",
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

    # Skill method - following HelloWorld pattern
    async def chart_generator(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Generate a chart based on CSV-like data passed in."""
        await self.execute(context, event_queue)