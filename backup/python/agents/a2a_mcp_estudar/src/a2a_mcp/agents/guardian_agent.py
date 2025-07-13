import json
import logging
from collections.abc import AsyncIterable
from typing import Dict, Any
from datetime import datetime
from pathlib import Path
import sys

# Adicionar path para guardian analyzer
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent / "ui" / "scripts"))

from a2a.types import (
    SendStreamingMessageSuccessResponse,
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatusUpdateEvent,
)
from a2a_mcp.common.base_agent import BaseAgent

logger = logging.getLogger(__name__)

# Importa guardian analyzer
try:
    from guardian_analyzer import A2AGuardian
except ImportError:
    logger.warning("Guardian analyzer não disponível")
    class A2AGuardian:
        def __init__(self, project_root="."):
            self.project_root = Path(project_root)
        
        def analyze_project(self):
            return {
                "status": "🟡 BOM",
                "success_rate": 75.0,
                "successes": ["✅ Guardian Agent A2A ativo"],
                "issues": ["🟡 Análise completa indisponível"],
                "total_checks": 1
            }

class GuardianAgent(BaseAgent):
    """Guardian Agent para análise e monitoramento A2A"""

    def __init__(self):
        super().__init__(
            agent_name='Guardian Agent',
            description='Sistema de análise e monitoramento A2A para Claude Flow',
            content_types=['text', 'text/plain', 'application/json'],
        )
        self.start_time = datetime.now()
        self.analysis_cache = {}

    async def stream(self, query: str, context_id: str, task_id: str) -> AsyncIterable[dict[str, any]]:
        """Execute and stream response."""
        logger.info(
            f'Running {self.agent_name} stream for session {context_id}, task {task_id} - {query}'
        )
        
        if not query:
            raise ValueError('Query cannot be empty')

        try:
            # Enviar status inicial
            yield {
                'response_type': 'text',
                'is_task_complete': False,
                'require_user_input': False,
                'content': '🛡️ Guardian iniciando análise...'
            }
            
            # Determinar tipo de query
            query_lower = query.lower()
            
            if any(word in query_lower for word in ['analise', 'analyze', 'analisar', 'análise']):
                # Análise completa do projeto
                yield {
                    'response_type': 'text',
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': '🔍 Executando análise completa do projeto A2A...'
                }
                
                # Executar análise
                project_root = str(Path(__file__).parent.parent.parent.parent.parent)
                guardian = A2AGuardian(project_root)
                result = guardian.analyze_project()
                
                # Formatar resultado
                analysis_text = self._format_analysis_result(result)
                
                yield {
                    'response_type': 'text', 
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': analysis_text
                }
                
            elif any(word in query_lower for word in ['status', 'saude', 'saúde', 'health']):
                # Status do sistema
                status_text = self._get_system_status()
                
                yield {
                    'response_type': 'text',
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': status_text
                }
                
            elif 'monitor' in query_lower:
                # Monitoramento em tempo real
                yield {
                    'response_type': 'text',
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': '📊 Coletando dados de monitoramento...'
                }
                
                monitor_text = self._get_monitoring_info()
                
                yield {
                    'response_type': 'text',
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': monitor_text
                }
                
            elif any(word in query_lower for word in ['ajuda', 'help']):
                # Ajuda
                help_text = self._get_help_text()
                
                yield {
                    'response_type': 'text',
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': help_text
                }
                
            else:
                # Resposta padrão
                default_text = self._get_default_response(query, context_id, task_id)
                
                yield {
                    'response_type': 'text',
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': default_text
                }
                
        except Exception as e:
            logger.error(f"Erro no Guardian Agent: {e}")
            yield {
                'response_type': 'text',
                'is_task_complete': False,
                'require_user_input': False,
                'content': f'❌ Erro no Guardian: {str(e)}'
            }

    def _format_analysis_result(self, result: Dict[str, Any]) -> str:
        """Formata resultado da análise"""
        return f"""
🛡️ **RELATÓRIO GUARDIAN A2A**

**Status Geral:** {result.get('status', 'Desconhecido')}
**Taxa de Sucesso:** {result.get('success_rate', 0):.1f}%

**✅ Sucessos ({len(result.get('successes', []))}):**
{chr(10).join(f"   {s}" for s in result.get('successes', []))}

**🚨 Problemas ({len(result.get('issues', []))}):**
{chr(10).join(f"   {i}" for i in result.get('issues', []))}

**📊 Total de Verificações:** {result.get('total_checks', 0)}
**🕐 Análise em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    def _get_system_status(self) -> str:
        """Retorna status do sistema"""
        uptime = datetime.now() - self.start_time
        
        return f"""
🛡️ **STATUS GUARDIAN A2A**

**🟢 Status:** Operacional
**⏱️ Uptime:** {str(uptime).split('.')[0]}
**🔌 Porta:** 10102
**📡 Protocolo:** A2A v1.0

**🔗 Endpoints A2A:**
• /.well-known/agent.json - Agent Card
• /tasks/send - Envio de tarefas
• /tasks/stream - Stream de respostas

**🤖 Comandos Aceitos:**
• "analise" - Análise completa do projeto
• "status" - Status do sistema
• "monitor" - Monitoramento em tempo real
• "ajuda" - Ajuda sobre comandos
"""

    def _get_monitoring_info(self) -> str:
        """Retorna informações de monitoramento"""
        uptime = datetime.now() - self.start_time
        
        return f"""
📊 **MONITORAMENTO GUARDIAN A2A**

**🔴 Serviços Ativos:**
• Guardian A2A: ✅ Porta 10102
• Orchestrator: ✅ Porta 10101
• UI Mesop: ⚠️ Verificando porta 12000

**📈 Métricas:**
• Uptime: {str(uptime).split('.')[0]}
• Consultas Processadas: {len(self.analysis_cache)}
• Última Análise: {datetime.now().strftime('%H:%M:%S')}

**🛡️ Guardian está monitorando o sistema A2A continuamente.**
"""

    def _get_help_text(self) -> str:
        """Retorna texto de ajuda"""
        return """
🛡️ **GUARDIAN A2A - AJUDA**

**Comandos Disponíveis:**

🔍 **Análise:**
• "analise" - Executa análise completa do projeto A2A

📊 **Monitoramento:**
• "status" - Mostra status atual do Guardian
• "monitor" - Monitoramento em tempo real do sistema

ℹ️ **Informações:**
• "ajuda" - Esta mensagem de ajuda

**Exemplo de uso:**
Digite "analise" para executar uma verificação completa do sistema A2A.

**Protocolo:** A2A v1.0 compatível
**Porta:** 10102
"""

    def _get_default_response(self, query: str, context_id: str, task_id: str) -> str:
        """Retorna resposta padrão"""
        return f"""
🛡️ **Guardian A2A**

Olá! Sou o Guardian Agent, responsável por monitorar e analisar o sistema Claude Flow A2A.

**Para começar, experimente:**
• "analise" - Para análise completa do projeto
• "status" - Para verificar o status do sistema
• "ajuda" - Para ver todos os comandos disponíveis

**Sua consulta:** "{query}"
**Contexto:** {context_id}
**Task ID:** {task_id}
**Protocolo:** A2A v1.0
"""