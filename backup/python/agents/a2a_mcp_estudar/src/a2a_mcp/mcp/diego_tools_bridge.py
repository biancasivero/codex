"""
Diego Tools Bridge - Integração das ferramentas do mcp-run-ts-tools no A2A MCP
Permite que o Orchestrator Agent use as ferramentas: agents, browser, puppeteer
"""

import asyncio
import json
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class DiegoToolsBridge:
    """Bridge para integrar DiegoTools no sistema A2A MCP"""
    
    def __init__(self):
        self.diego_tools_path = Path(__file__).parent.parent.parent.parent.parent.parent / "claude-code-10x" / "mcp-run-ts-tools"
        self.run_script = self.diego_tools_path / "run.sh"
        self.is_available = self._check_availability()
        
    def _check_availability(self) -> bool:
        """Verifica se as DiegoTools estão disponíveis"""
        try:
            if not self.diego_tools_path.exists():
                logger.warning(f"DiegoTools path não encontrado: {self.diego_tools_path}")
                return False
                
            if not self.run_script.exists():
                logger.warning(f"Run script não encontrado: {self.run_script}")
                return False
                
            # Apenas verificar se o run script existe e é executável
            if not self.run_script.is_file():
                logger.warning(f"Run script não é arquivo válido: {self.run_script}")
                return False
                
            import os
            if not os.access(str(self.run_script), os.X_OK):
                logger.warning(f"Run script não é executável: {self.run_script}")
                return False
                
            # Verificar se o build directory existe (indicando que foi built)
            build_dir = self.diego_tools_path / "build"
            if not build_dir.exists():
                logger.warning(f"Build directory não encontrado: {build_dir}")
                return False
                
            return True
            
        except Exception as e:
            logger.warning(f"Erro verificando DiegoTools: {e}")
            return False
    
    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Chama uma ferramenta do DiegoTools via MCP"""
        if not self.is_available:
            return {
                "error": "DiegoTools não disponível",
                "tool": tool_name,
                "available": False
            }
        
        try:
            # Mapear nomes das ferramentas para o formato MCP
            tool_mapping = {
                # Puppeteer tools
                "web_navigate": "puppeteer_navigate",
                "web_screenshot": "puppeteer_screenshot", 
                "web_click": "puppeteer_click",
                "web_type": "puppeteer_type",
                "web_get_content": "puppeteer_get_content",
                "open_browser": "open_browser",
                
                # Browser tools
                "browser_open": "browser_open_url",
                
                # Agents tools
                "list_agents": "agents_list",
                "get_agent_details": "agents_get_details",
                "analyze_agent": "agents_analyze",
                "search_agents": "agents_search"
            }
            
            mcp_tool_name = tool_mapping.get(tool_name, tool_name)
            
            # Criar mensagem MCP para chamar a ferramenta
            mcp_request = {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": mcp_tool_name,
                    "arguments": parameters
                },
                "id": 1
            }
            
            # Executar via subprocess MCP stdio
            process = await asyncio.create_subprocess_exec(
                str(self.run_script),
                cwd=str(self.diego_tools_path),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Enviar requisição MCP
            input_data = json.dumps(mcp_request) + "\n"
            stdout, stderr = await process.communicate(input_data.encode())
            
            if process.returncode != 0:
                logger.error(f"DiegoTools error: {stderr.decode()}")
                return {
                    "error": f"Erro na execução: {stderr.decode()}",
                    "tool": tool_name,
                    "exit_code": process.returncode
                }
            
            # Parse da resposta MCP
            response_lines = stdout.decode().strip().split('\n')
            for line in response_lines:
                if line.strip():
                    try:
                        response = json.loads(line)
                        if "result" in response:
                            return {
                                "success": True,
                                "tool": tool_name,
                                "result": response["result"]
                            }
                        elif "error" in response:
                            return {
                                "error": response["error"],
                                "tool": tool_name
                            }
                    except json.JSONDecodeError:
                        continue
            
            return {
                "error": "Resposta MCP inválida",
                "tool": tool_name,
                "raw_output": stdout.decode()
            }
            
        except asyncio.TimeoutError:
            return {
                "error": "Timeout na execução da ferramenta",
                "tool": tool_name,
                "timeout": True
            }
        except Exception as e:
            logger.error(f"Erro chamando DiegoTools {tool_name}: {e}")
            return {
                "error": str(e),
                "tool": tool_name,
                "exception": type(e).__name__
            }
    
    def get_available_tools(self) -> Dict[str, Dict[str, Any]]:
        """Retorna lista de ferramentas disponíveis"""
        if not self.is_available:
            return {}
        
        return {
            # Puppeteer/Web tools
            "web_navigate": {
                "description": "Navegar para uma URL usando Puppeteer",
                "parameters": {
                    "url": {"type": "string", "required": True, "description": "URL para navegar"},
                    "wait_for": {"type": "string", "required": False, "description": "Seletor para aguardar"}
                }
            },
            "web_screenshot": {
                "description": "Tirar screenshot da página atual",
                "parameters": {
                    "name": {"type": "string", "required": True, "description": "Nome do arquivo"},
                    "selector": {"type": "string", "required": False, "description": "Seletor específico"}
                }
            },
            "web_click": {
                "description": "Clicar em um elemento da página",
                "parameters": {
                    "selector": {"type": "string", "required": True, "description": "Seletor CSS do elemento"}
                }
            },
            "web_type": {
                "description": "Digitar texto em um campo",
                "parameters": {
                    "selector": {"type": "string", "required": True, "description": "Seletor do campo"},
                    "text": {"type": "string", "required": True, "description": "Texto para digitar"}
                }
            },
            "web_get_content": {
                "description": "Obter conteúdo da página",
                "parameters": {
                    "selector": {"type": "string", "required": False, "description": "Seletor específico"}
                }
            },
            "open_browser": {
                "description": "Abrir browser Puppeteer",
                "parameters": {
                    "headless": {"type": "boolean", "required": False, "description": "Modo headless"}
                }
            },
            
            # Browser tools
            "browser_open": {
                "description": "Abrir URL no browser padrão",
                "parameters": {
                    "url": {"type": "string", "required": True, "description": "URL para abrir"}
                }
            },
            
            # Agents tools
            "list_agents": {
                "description": "Listar agentes disponíveis no sistema",
                "parameters": {}
            },
            "get_agent_details": {
                "description": "Obter detalhes de um agente específico",
                "parameters": {
                    "agent_id": {"type": "string", "required": True, "description": "ID do agente"}
                }
            },
            "analyze_agent": {
                "description": "Analisar capacidades de um agente",
                "parameters": {
                    "agent_id": {"type": "string", "required": True, "description": "ID do agente"}
                }
            },
            "search_agents": {
                "description": "Buscar agentes por critérios",
                "parameters": {
                    "query": {"type": "string", "required": True, "description": "Termo de busca"}
                }
            }
        }

# Instância global do bridge
diego_tools_bridge = DiegoToolsBridge()

# Funções convenientes para uso nas ferramentas MCP
async def call_diego_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """Função conveniente para chamar DiegoTools"""
    return await diego_tools_bridge.call_tool(tool_name, kwargs)

def is_diego_tools_available() -> bool:
    """Verifica se DiegoTools está disponível"""
    return diego_tools_bridge.is_available

def get_diego_tools_info() -> Dict[str, Any]:
    """Informações sobre DiegoTools"""
    return {
        "available": diego_tools_bridge.is_available,
        "path": str(diego_tools_bridge.diego_tools_path),
        "tools": list(diego_tools_bridge.get_available_tools().keys())
    }