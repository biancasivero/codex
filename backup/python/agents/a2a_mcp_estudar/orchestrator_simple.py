#!/usr/bin/env python3
"""
Versão simplificada do Orchestrator Agent sem problemas de herança.
"""

import os
import json
import logging
import asyncio
import httpx
import uvicorn
import uuid
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google import genai

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleOrchestratorAgent:
    """Versão simplificada do Orchestrator Agent."""
    
    def __init__(self):
        # Configurar Google API
        os.environ['GOOGLE_API_KEY'] = 'AIzaSyBb1eDoRJmNdrwSi9ii0lF_rL4epIncsMo'
        
        self.agent_name = "Orchestrator Agent"
        self.description = "Orchestrates the task generation and execution"
        self.version = "1.0.0"
        self.capabilities = {
            "streaming": True,
            "pushNotifications": True,
            "stateTransitionHistory": False
        }
        
        # Estado do agente
        self.results = []
        self.travel_context = {}
        self.query_history = []
        self.task_history = []  # Histórico de tarefas completadas
        
        # Conhecimento MCP com as 7 ferramentas disponíveis
        self.mcp_knowledge = {
            "protocol": "Model Context Protocol - protocolo de comunicação padronizado",
            "tools": {
                "find_agent": "Descoberta e localização de agentes no sistema",
                "find_mcp": "Informações sobre o protocolo MCP e ferramentas disponíveis",
                "generate_unique_id": "Geração de identificadores únicos (UUID)",
                "validate_json": "Validação e verificação de dados JSON",
                "format_text": "Formatação de texto (upper, lower, title, etc.)",
                "calculate_basic": "Cálculos matemáticos básicos (+, -, *, /, %, **)",
                "system_info": "Informações do sistema operacional e ambiente"
            },
            "task_types": [
                "mcp_tool_query: Uso direto de ferramentas MCP",
                "agent_coordination: Coordenação entre agentes A2A", 
                "data_processing: Processamento de dados",
                "summary_generation: Geração de resumos"
            ]
        }
    
    def get_agent_card(self):
        """Retorna o agent card em formato A2A."""
        return {
            "name": self.agent_name,
            "description": self.description,
            "url": "http://localhost:10101/",
            "version": self.version,
            "capabilities": self.capabilities,
            "defaultInputModes": ["text", "text/plain"],
            "defaultOutputModes": ["text", "text/plain"],
            "skills": [
                {
                    "id": "task_executor",
                    "name": "Task Executor",
                    "description": "Executa tarefas usando ferramentas MCP",
                    "tags": ["mcp", "task-execution", "orchestration"]
                },
                {
                    "id": "task_lister", 
                    "name": "Task Lister",
                    "description": "Lista e monitora status de tarefas",
                    "tags": ["task-management", "monitoring", "status"]
                },
                {
                    "id": "mcp_explainer",
                    "name": "MCP Explainer", 
                    "description": "Explica conceitos e ferramentas MCP",
                    "tags": ["mcp", "documentation", "explanation"]
                },
                {
                    "id": "agent_coordinator",
                    "name": "Agent Coordinator",
                    "description": "Coordena comunicação entre agentes A2A",
                    "tags": ["a2a", "coordination", "communication"]
                }
            ]
        }

    def create_task_record(self, message: str, task_type: str = "mcp_query") -> dict:
        """Cria um registro de tarefa para o histórico."""
        task_id = str(uuid.uuid4())
        task_record = {
            "id": task_id,
            "type": task_type,
            "description": message,
            "status": "in_progress",
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "agent": self.agent_name,
            "mcp_tools_used": [],
            "result_summary": None
        }
        return task_record

    def complete_task_record(self, task_record: dict, response: str, tools_used: list = None):
        """Completa um registro de tarefa."""
        task_record["status"] = "completed"
        task_record["completed_at"] = datetime.now().isoformat()
        task_record["result_summary"] = response[:200] + "..." if len(response) > 200 else response
        task_record["mcp_tools_used"] = tools_used or []
        self.task_history.append(task_record)
        
        logger.info(f"Tarefa completada: {task_record['id']} - {task_record['description']}")

    async def register_task_with_ui(self, task_record: dict):
        """Registra a tarefa completada com a UI via API."""
        try:
            async with httpx.AsyncClient() as client:
                # Payload para registrar tarefa na UI
                payload = {
                    "task_id": task_record["id"],
                    "agent_name": self.agent_name,
                    "description": task_record["description"],
                    "status": task_record["status"],
                    "created_at": task_record["created_at"],
                    "completed_at": task_record.get("completed_at"),
                    "tools_used": task_record.get("mcp_tools_used", []),
                    "result": task_record.get("result_summary", "")
                }
                
                # Tentar registrar via endpoint da UI
                response = await client.post(
                    "http://localhost:12000/task/register",
                    json=payload,
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Tarefa {task_record['id']} registrada na UI com sucesso")
                else:
                    logger.warning(f"Falha ao registrar tarefa na UI: {response.status_code}")
                    
        except Exception as e:
            logger.warning(f"Não foi possível registrar tarefa na UI: {e}")

    def get_completed_tasks_summary(self) -> str:
        """Retorna um resumo das tarefas completadas."""
        if not self.task_history:
            return "Nenhuma tarefa completada ainda."
        
        completed_tasks = [t for t in self.task_history if t["status"] == "completed"]
        
        summary = f"📋 **Resumo de Tarefas Completadas ({len(completed_tasks)} tarefas):**\n\n"
        
        for i, task in enumerate(completed_tasks[-5:], 1):  # Últimas 5 tarefas
            tools_str = ", ".join(task.get("mcp_tools_used", [])) or "Nenhuma ferramenta MCP"
            summary += f"{i}. **{task['description'][:50]}...**\n"
            summary += f"   - Status: ✅ {task['status']}\n"
            summary += f"   - Ferramentas MCP: {tools_str}\n"
            summary += f"   - Completada: {task['completed_at'][:19]}\n\n"
        
        return summary

    async def call_mcp_tool(self, tool_name: str, params: dict = None) -> str:
        """Simula chamada para ferramenta MCP."""
        tools_mapping = {
            "find_mcp": "Informações do protocolo MCP retornadas",
            "generate_unique_id": f"UUID gerado: {str(uuid.uuid4())}",
            "validate_json": "JSON validado com sucesso",
            "format_text": "Texto formatado conforme solicitado",
            "calculate_basic": "Cálculo realizado",
            "system_info": "Informações do sistema coletadas",
            "find_agent": "Agente mais relevante encontrado"
        }
        
        result = tools_mapping.get(tool_name, f"Ferramenta {tool_name} executada")
        logger.info(f"Ferramenta MCP chamada: {tool_name} -> {result}")
        return result

    async def process_message(self, message: str) -> dict:
        """Processa mensagens usando conhecimento MCP e registra tarefas."""
        
        logger.info(f"Processing message: {message}")
        
        # Criar registro de tarefa
        task_record = self.create_task_record(message)
        
        try:
            client = genai.Client()
            
            # Detectar se deve listar tarefas completadas
            if any(keyword in message.lower() for keyword in ["tarefas completadas", "task list", "lista de tarefas", "histórico"]):
                tasks_summary = self.get_completed_tasks_summary()
                
                self.complete_task_record(task_record, tasks_summary, ["task_lister"])
                await self.register_task_with_ui(task_record)
                
                return {
                    "status": "completed",
                    "response": tasks_summary,
                    "agent": self.agent_name,
                    "mcp_capable": True,
                    "task_id": task_record["id"]
                }
            
            # Detectar ferramentas MCP mencionadas
            tools_used = []
            for tool_name in self.mcp_knowledge["tools"].keys():
                if tool_name in message.lower():
                    tools_used.append(tool_name)
                    await self.call_mcp_tool(tool_name)

            # Prompt com conhecimento MCP e histórico de tarefas
            prompt = f"""
Você é um Orchestrator Agent especializado em MCP (Model Context Protocol) com sistema de rastreamento de tarefas.

CONHECIMENTO MCP ATUALIZADO:
- MCP: {self.mcp_knowledge['protocol']}
- 7 Ferramentas disponíveis: {json.dumps(self.mcp_knowledge['tools'], indent=2)}
- Tipos de tarefa: {self.mcp_knowledge['task_types']}

CAPACIDADES:
- Task Executor: Executo tarefas usando ferramentas MCP
- Task Lister: Listo e monitoro status de tarefas (agora funcional!)
- MCP Explainer: Explico conceitos e ferramentas MCP
- Agent Coordinator: Coordeno comunicação entre agentes A2A

TAREFAS COMPLETADAS RECENTES: {len(self.task_history)} tarefas registradas

MENSAGEM DO USUÁRIO: {message}

Responda em português brasileiro, seja específico sobre MCP e suas capacidades.
Se o usuário perguntar sobre tarefas completadas, mencione que agora mantenho um histórico.
"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config={'temperature': 0.1}
            )
            
            # Completar registro da tarefa
            self.complete_task_record(task_record, response.text, tools_used)
            await self.register_task_with_ui(task_record)
            
            return {
                "status": "completed",
                "response": response.text,
                "agent": self.agent_name,
                "mcp_capable": True,
                "task_id": task_record["id"],
                "tools_used": tools_used
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            task_record["status"] = "failed"
            task_record["result_summary"] = f"Erro: {str(e)}"
            
            return {
                "status": "error",
                "error": str(e),
                "fallback_response": f"Sou o Orchestrator Agent com conhecimento completo sobre MCP. 7 Ferramentas disponíveis: {', '.join(self.mcp_knowledge['tools'].keys())}",
                "task_id": task_record["id"]
            }

# Criar aplicação FastAPI
app = FastAPI(title="Simple Orchestrator Agent")

# Instância do agente
agent = SimpleOrchestratorAgent()

@app.get("/.well-known/agent.json")
async def get_agent_card():
    """Retorna o agent card."""
    return JSONResponse(agent.get_agent_card())

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": agent.agent_name}

@app.post("/")
async def process_request(request: dict):
    """Processa requisições A2A."""
    try:
        if "params" in request and "message" in request["params"]:
            message_parts = request["params"]["message"].get("parts", [])
            if message_parts and "text" in message_parts[0]:
                user_message = message_parts[0]["text"]
                
                result = await agent.process_message(user_message)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "id": request["params"].get("id", "unknown"),
                        "status": {
                            "state": "completed",
                            "message": {
                                "role": "agent",
                                "parts": [{"type": "text", "text": result.get("response", "Resposta do orquestrador")}]
                            }
                        },
                        "artifacts": [{
                            "name": "orchestrator-response",
                            "parts": [{"type": "text", "text": result.get("response", "Resposta do orquestrador")}]
                        }]
                    }
                }
    except Exception as e:
        logger.error(f"Error in process_request: {e}")
        return {
            "jsonrpc": "2.0", 
            "id": request.get("id"),
            "error": {"code": -32603, "message": str(e)}
        }

if __name__ == "__main__":
    print("🚀 Iniciando Simple Orchestrator Agent na porta 10101")
    print("📋 Agent Card: http://localhost:10101/.well-known/agent.json")
    print("❤️ Health Check: http://localhost:10101/health")
    uvicorn.run(app, host="localhost", port=10101) 