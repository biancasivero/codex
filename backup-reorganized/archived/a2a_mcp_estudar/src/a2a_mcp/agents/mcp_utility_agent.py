# type: ignore

import json
import logging
import re

from collections.abc import AsyncIterable
from typing import Any

from a2a_mcp.common.agent_runner import AgentRunner
from a2a_mcp.common.base_agent import BaseAgent
from a2a_mcp.common.utils import get_mcp_server_config, init_api_key
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams
from google.genai import types as genai_types


logger = logging.getLogger(__name__)


class MCPUtilityAgent(BaseAgent):
    """Agente genérico que usa ferramentas MCP utilitárias."""

    def __init__(self, agent_name: str, description: str, instructions: str, specialized_tools: list = None):
        init_api_key()

        super().__init__(
            agent_name=agent_name,
            description=description,
            content_types=['text', 'text/plain', 'application/json'],
        )

        logger.info(f'Init {self.agent_name}')

        self.instructions = instructions
        self.specialized_tools = specialized_tools or []
        self.agent = None

    async def init_agent(self):
        logger.info(f'Initializing {self.agent_name} with MCP tools')
        config = get_mcp_server_config()
        logger.info(f'MCP Server url={config.url}')
        
        # Carregar todas as ferramentas MCP disponíveis
        tools = await MCPToolset(
            connection_params=SseServerParams(url=config.url)
        ).get_tools()

        # Filtrar ferramentas se especializadas
        if self.specialized_tools:
            filtered_tools = []
            for tool in tools:
                if tool.name in self.specialized_tools:
                    filtered_tools.append(tool)
                    logger.info(f'Loaded specialized tool: {tool.name}')
            tools = filtered_tools
        else:
            for tool in tools:
                logger.info(f'Loaded tool: {tool.name}')

        generate_content_config = genai_types.GenerateContentConfig(
            temperature=0.2
        )
        
        self.agent = Agent(
            name=self.agent_name,
            instruction=self.instructions,
            model='gemini-2.0-flash',
            disallow_transfer_to_parent=True,
            disallow_transfer_to_peers=True,
            generate_content_config=generate_content_config,
            tools=tools,
        )
        self.runner = AgentRunner()

    async def invoke(self, query, session_id) -> dict:
        logger.info(f'Running {self.agent_name} for session {session_id}')
        raise NotImplementedError('Please use the streaming function')

    async def stream(
        self, query, context_id, task_id
    ) -> AsyncIterable[dict[str, Any]]:
        logger.info(
            f'Running {self.agent_name} stream for session {context_id} {task_id} - {query}'
        )

        if not query:
            raise ValueError('Query cannot be empty')

        if not self.agent:
            await self.init_agent()
            
        async for chunk in self.runner.run_stream(
            self.agent, query, context_id
        ):
            logger.info(f'Received chunk: {chunk}')
            if isinstance(chunk, dict) and chunk.get('type') == 'final_result':
                response = chunk['response']
                yield self.get_agent_response(response)
            else:
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': f'{self.agent_name}: Processing Request...',
                }

    def format_response(self, chunk):
        """Formata a resposta do agente."""
        # Tentar extrair JSON de blocos de código
        patterns = [
            r'```json\s*(.*?)\s*```',
            r'```\s*(.*?)\s*```',
            r'```tool_outputs\s*(.*?)\s*```',
        ]

        for pattern in patterns:
            match = re.search(pattern, chunk, re.DOTALL)
            if match:
                content = match.group(1)
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return content
        
        # Se não tem padrão específico, retornar o chunk original
        return chunk

    def get_agent_response(self, chunk):
        """Processa a resposta do agente e retorna formato padronizado."""
        logger.info(f'Response Type: {type(chunk)}')
        data = self.format_response(chunk)
        logger.info(f'Formatted Response: {data}')
        
        try:
            # Se é um dicionário, verificar se é resposta estruturada
            if isinstance(data, dict):
                if 'status' in data and data['status'] == 'input_required':
                    return {
                        'response_type': 'text',
                        'is_task_complete': False,
                        'require_user_input': True,
                        'content': data.get('question', 'Input required'),
                    }
                
                # Resposta estruturada com dados
                return {
                    'response_type': 'data',
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': data,
                }
            
            # Tentar parsear como JSON se for string
            if isinstance(data, str):
                try:
                    parsed_data = json.loads(data)
                    return {
                        'response_type': 'data',
                        'is_task_complete': True,
                        'require_user_input': False,
                        'content': parsed_data,
                    }
                except json.JSONDecodeError:
                    pass
            
            # Resposta de texto simples
            return {
                'response_type': 'text',
                'is_task_complete': True,
                'require_user_input': False,
                'content': str(data),
            }
        except Exception as e:
            logger.error(f'Error in get_agent_response: {e}')
            return {
                'response_type': 'text',
                'is_task_complete': True,
                'require_user_input': False,
                'content': f'Error processing response: {str(e)}',
            } 