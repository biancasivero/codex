#!/usr/bin/env python3
"""
Orchestrator Agent simples inspirado no Hello World Agent.
Foco: Uma skill, lógica simples, funcionalidade eficaz.
"""

import uvicorn
import logging
from typing import Dict, Any
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleOrchestratorAgent:
    """Orchestrator Agent simples com foco em MCP e coordenação."""

    def __init__(self):
        self.name = "Simple Orchestrator Agent"
        self.description = "Coordena tarefas e agentes usando protocolo MCP"
        
        # Conhecimento MCP simplificado
        self.mcp_tools = [
            "find_agent", "find_mcp", "generate_unique_id", 
            "validate_json", "format_text", "calculate_basic", "system_info"
        ]
        self.tasks_completed = 0

    async def task_executor(self, query: str, session_id: str) -> Dict[str, Any]:
        """Executa coordenação de tarefas com foco em MCP."""
        try:
            logger.info(f"Executando tarefa de orquestração: {query} (sessão: {session_id})")
            
            query_lower = query.lower()
            
            # Detectar tipo de tarefa
            if any(word in query_lower for word in ["listar", "lista", "tarefas", "status"]):
                result = f"📋 **Status do Orchestrator Agent:**\n\n✅ Tarefas completadas: {self.tasks_completed}\n🛠️ Ferramentas MCP: {len(self.mcp_tools)} disponíveis\n🎯 Capacidades: Task Executor, MCP Coordinator"
                task_type = "status_check"
                
            elif any(word in query_lower for word in ["mcp", "protocolo", "ferramentas"]):
                result = f"🔧 **Ferramentas MCP Disponíveis:**\n\n{chr(10).join([f'• {tool}' for tool in self.mcp_tools])}\n\n💡 MCP é um protocolo de comunicação padronizado para agentes."
                task_type = "mcp_info"
                
            elif any(word in query_lower for word in ["coordenar", "executar", "agente"]):
                result = f"🚀 **Coordenação Ativa:**\n\nPosso coordenar tarefas entre agentes usando:\n• Protocolo A2A para comunicação\n• Ferramentas MCP para execução\n• Sistema de registro de tarefas\n\nEspecifique qual tarefa deseja executar!"
                task_type = "coordination"
                
            else:
                # Resposta padrão amigável
                result = f"👋 **Orchestrator Agent Ativo!**\n\nSou especializado em:\n• 📋 Coordenação de tarefas\n• 🔧 Protocolo MCP ({len(self.mcp_tools)} ferramentas)\n• 🤖 Comunicação entre agentes A2A\n\nComo posso ajudar?"
                task_type = "greeting"
            
            self.tasks_completed += 1
            
            return {
                "is_task_complete": True,
                "require_user_input": False,
                "result": result,
                "task_type": task_type,
                "success": True,
                "tools_available": len(self.mcp_tools)
            }
            
        except Exception as e:
            logger.exception(f"Erro na execução da tarefa para sessão {session_id}")
            return {
                "is_task_complete": True,
                "require_user_input": False,
                "result": f"❌ Erro: {str(e)}\n\nMas continue! Sou resiliente. 💪",
                "success": False
            }

    async def process_request(self, query: str, session_id: str) -> Dict[str, Any]:
        """Processa requisições gerais."""
        return await self.task_executor(query, session_id)


class SimpleOrchestratorExecutor(AgentExecutor):
    """Executor simples para o Orchestrator Agent."""

    def __init__(self):
        self.agent = SimpleOrchestratorAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Executa tarefa de orquestração com ciclo de vida completo."""
        query = context.get_user_input()
        task = context.current_task
        
        # 1. Criar tarefa se não existir
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)
            logger.info(f"Nova tarefa criada: {task.id}")

        # 2. Marcar como em andamento
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                status=TaskStatus(
                    state=TaskState.working,
                    message=new_agent_text_message(
                        "🎯 Coordenando tarefa...",
                        task.contextId,
                        task.id,
                    ),
                ),
                final=False,
                contextId=task.contextId,
                taskId=task.id,
            )
        )
        logger.info(f"Tarefa {task.id} em execução")

        try:
            # 3. Executar lógica do agente
            result = await self.agent.process_request(query, task.contextId)
            
            # 4. Criar artefato com resultado
            artifact = new_text_artifact(
                name="orchestrator_response",
                description="Resposta de coordenação do Orchestrator Agent",
                text=result["result"],
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

            # 6. Marcar como completa
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    status=TaskStatus(
                        state=TaskState.completed,
                        message=new_agent_text_message(
                            "✅ Coordenação completa",
                            task.contextId,
                            task.id,
                        ),
                    ),
                    final=True,
                    contextId=task.contextId,
                    taskId=task.id,
                )
            )
            logger.info(f"Tarefa {task.id} completada com sucesso")

        except Exception as e:
            logger.exception(f"Erro na execução da tarefa {task.id}")
            # Marcar como falha mas de forma elegante
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    status=TaskStatus(
                        state=TaskState.failed,
                        message=new_agent_text_message(
                            f"❌ Erro: {str(e)}, mas continuo funcionando!",
                            task.contextId,
                            task.id,
                        ),
                    ),
                    final=True,
                    contextId=task.contextId,
                    taskId=task.id,
                )
            )

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        """Cancelar tarefa."""
        logger.info("Tarefa cancelada")


# Definir skill simples
skill = AgentSkill(
    id="task_executor",
    name="Task Executor",
    description="Executa coordenação de tarefas usando protocolo MCP e comunicação A2A",
    tags=["mcp", "task-execution", "orchestration", "coordination"],
    examples=[
        "Coordenar tarefa",
        "Status das tarefas",
        "Ferramentas MCP disponíveis",
        "Listar agentes",
        "Executar coordenação"
    ],
)

# Agent Card simples
public_agent_card = AgentCard(
    name="Simple Orchestrator Agent",
    description="Coordena tarefas e agentes usando protocolo MCP",
    url="http://localhost:10101/",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(
        streaming=True,
        pushNotifications=True
    ),
    skills=[skill],
)

# Configurar servidor
request_handler = DefaultRequestHandler(
    agent_executor=SimpleOrchestratorExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=public_agent_card,
    http_handler=request_handler,
)

app = server.build()

if __name__ == "__main__":
    print("🚀 Iniciando Simple Orchestrator Agent (estilo Hello World)")
    print("📋 Porta: 10101")
    print("🎯 Uma skill, lógica simples, máxima eficácia!")
    uvicorn.run(app, host="0.0.0.0", port=10101) 