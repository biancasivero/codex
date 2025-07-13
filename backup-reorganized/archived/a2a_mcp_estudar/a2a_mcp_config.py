# Configuração do Sistema A2A MCP
# Arquivo de configuração centralizado para todos os agentes

import os
from typing import Dict, List

class A2AMCPConfig:
    """Configuração centralizada do sistema A2A MCP"""
    
    # Configurações do servidor MCP
    MCP_HOST = "localhost"
    MCP_PORT = 10100
    MCP_TRANSPORT = "sse"
    MCP_URL = f"http://{MCP_HOST}:{MCP_PORT}/sse"
    
    # Configurações dos agentes
    AGENT_CONFIGS = {
        "orchestrator": {
            "name": "Orchestrator Agent",
            "port": 10101,
            "card_file": "agent_cards/orchestrator_agent.json",
            "description": "Agente orquestrador que coordena tarefas e gerencia operações"
        }
    }
    
    # Configurações de ambiente
    REQUIRED_ENV_VARS = [
        "GOOGLE_API_KEY"
    ]
    
    OPTIONAL_ENV_VARS = {
        "A2A_LOG_LEVEL": "Nível de log (DEBUG, INFO, WARNING, ERROR)"
    }
    
    # Novos agentes adaptativos para as ferramentas MCP utilitárias
    NEW_AGENTS = {
        "text_processor": {
            "name": "Text Processor Agent",
            "port": 10102,
            "card_file": "agent_cards/text_processor_agent.json",
            "description": "Agente especializado em processamento de texto usando ferramentas MCP",
            "tools": ["format_text", "validate_json", "generate_unique_id"]
        },
        "calculator": {
            "name": "Calculator Agent",
            "port": 10103,
            "card_file": "agent_cards/calculator_agent.json",
            "description": "Agente especializado em cálculos matemáticos usando ferramentas MCP",
            "tools": ["calculate_basic", "generate_unique_id", "validate_json"]
        },
        "data_validator": {
            "name": "Data Validator Agent",
            "port": 10104,
            "card_file": "agent_cards/data_validator_agent.json",
            "description": "Agente especializado em validação de dados usando ferramentas MCP",
            "tools": ["validate_json", "format_text", "generate_unique_id"]
        },
        "utility_helper": {
            "name": "Utility Helper Agent",
            "port": 10105,
            "card_file": "agent_cards/utility_helper_agent.json",
            "description": "Agente utilitário geral que usa todas as ferramentas MCP",
            "tools": ["generate_unique_id", "validate_json", "format_text", "calculate_basic", "system_info"]
        }
    }
    
    @classmethod
    def get_mcp_server_config(cls) -> Dict:
        """Retorna configuração do servidor MCP"""
        return {
            "host": cls.MCP_HOST,
            "port": cls.MCP_PORT,
            "transport": cls.MCP_TRANSPORT,
            "url": cls.MCP_URL
        }
    
    @classmethod
    def get_agent_config(cls, agent_name: str) -> Dict:
        """Retorna configuração de um agente específico"""
        return cls.AGENT_CONFIGS.get(agent_name, {})
    
    @classmethod
    def get_all_agent_ports(cls) -> List[int]:
        """Retorna todas as portas dos agentes"""
        return [config["port"] for config in cls.AGENT_CONFIGS.values()]
    
    @classmethod
    def get_new_agent_config(cls, agent_name: str) -> Dict:
        """Retorna configuração de um novo agente"""
        return cls.NEW_AGENTS.get(agent_name, {})
    
    @classmethod
    def activate_new_agent(cls, agent_name: str) -> bool:
        """Ativa um novo agente"""
        if agent_name in cls.NEW_AGENTS:
            cls.AGENT_CONFIGS[agent_name] = cls.NEW_AGENTS[agent_name]
            return True
        return False
    
    @classmethod
    def get_available_tools(cls) -> List[str]:
        """Retorna lista de ferramentas MCP disponíveis"""
        return [
            "find_agent",
            "generate_unique_id", 
            "system_info",
            "validate_json",
            "format_text",
            "calculate_basic"
        ]
    
    @classmethod
    def check_environment(cls) -> Dict:
        """Verifica variáveis de ambiente necessárias"""
        env_status = {
            "required": {},
            "optional": {},
            "all_required_present": True
        }
        
        # Verificar variáveis obrigatórias
        for var in cls.REQUIRED_ENV_VARS:
            value = os.getenv(var)
            env_status["required"][var] = {
                "present": value is not None,
                "value": "***" if value else None
            }
            if not value:
                env_status["all_required_present"] = False
        
        # Verificar variáveis opcionais
        for var, description in cls.OPTIONAL_ENV_VARS.items():
            value = os.getenv(var)
            env_status["optional"][var] = {
                "present": value is not None,
                "value": "***" if value else None,
                "description": description
            }
        
        return env_status
    
    @classmethod
    def display_config(cls):
        """Exibe configuração do sistema"""
        print("🔧 Configuração do Sistema A2A MCP")
        print("=" * 50)
        print(f"Servidor MCP: {cls.MCP_URL}")
        print(f"Agentes ativos: {len(cls.AGENT_CONFIGS)}")
        
        print("\n📋 Agentes ativos:")
        for name, config in cls.AGENT_CONFIGS.items():
            print(f"  • {config['name']} - Porta {config['port']}")
            print(f"    {config['description']}")
        
        if cls.NEW_AGENTS:
            print(f"\n🆕 Novos agentes disponíveis: {len(cls.NEW_AGENTS)}")
            for name, config in cls.NEW_AGENTS.items():
                print(f"  • {config['name']} - Porta {config['port']}")
                print(f"    {config['description']}")
                print(f"    Ferramentas: {', '.join(config['tools'])}")
        
        print("\n🌍 Variáveis de ambiente:")
        env_status = cls.check_environment()
        
        for var in cls.REQUIRED_ENV_VARS:
            status = "✅" if env_status["required"][var]["present"] else "❌"
            print(f"  {status} {var} (obrigatória)")
        
        for var, info in env_status["optional"].items():
            status = "✅" if info["present"] else "⚠️"
            print(f"  {status} {var} (opcional) - {info['description']}")
        
        print("\n🛠️  Ferramentas MCP disponíveis:")
        for tool in cls.get_available_tools():
            print(f"  • {tool}")
        
        if not env_status["all_required_present"]:
            print("\n❌ Algumas variáveis obrigatórias estão faltando!")
            return False
        
        print("\n✅ Configuração válida!")
        return True


if __name__ == "__main__":
    # Teste da configuração
    A2AMCPConfig.display_config() 