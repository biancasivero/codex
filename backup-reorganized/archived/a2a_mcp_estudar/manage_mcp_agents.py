#!/usr/bin/env python3
# Script de gerenciamento para agentes MCP utilitários

import argparse
import asyncio
import json
import logging
import subprocess
import sys
import time
from pathlib import Path

from a2a_mcp_config import A2AMCPConfig


logger = logging.getLogger(__name__)


class MCPAgentManager:
    """Gerenciador para agentes MCP utilitários."""
    
    def __init__(self):
        self.config = A2AMCPConfig()
        self.running_processes = []
    
    def list_available_agents(self):
        """Lista agentes disponíveis para ativação."""
        print("🆕 Agentes MCP Utilitários Disponíveis:")
        print("=" * 50)
        
        for name, config in self.config.NEW_AGENTS.items():
            print(f"\n📋 {name}")
            print(f"   Nome: {config['name']}")
            print(f"   Porta: {config['port']}")
            print(f"   Descrição: {config['description']}")
            print(f"   Ferramentas: {', '.join(config['tools'])}")
            
            # Verificar se agent card existe
            card_file = Path(config['card_file'])
            if card_file.exists():
                print(f"   Status: ✅ Agent card existe")
            else:
                print(f"   Status: ❌ Agent card não encontrado")
    
    def activate_agent(self, agent_name: str):
        """Ativa um agente específico."""
        if agent_name not in self.config.NEW_AGENTS:
            print(f"❌ Agente '{agent_name}' não encontrado.")
            print("Agentes disponíveis:")
            for name in self.config.NEW_AGENTS.keys():
                print(f"  - {name}")
            return False
        
        # Ativar na configuração
        success = self.config.activate_new_agent(agent_name)
        if success:
            print(f"✅ Agente '{agent_name}' ativado com sucesso!")
            return True
        else:
            print(f"❌ Falha ao ativar agente '{agent_name}'")
            return False
    
    def start_agent(self, agent_name: str, host: str = "localhost"):
        """Inicia um agente específico."""
        if agent_name not in self.config.NEW_AGENTS:
            print(f"❌ Agente '{agent_name}' não encontrado.")
            return None
        
        config = self.config.NEW_AGENTS[agent_name]
        card_file = config['card_file']
        port = config['port']
        
        # Verificar se agent card existe
        if not Path(card_file).exists():
            print(f"❌ Agent card não encontrado: {card_file}")
            return None
        
        # Comando para iniciar o agente
        cmd = [
            'python', 'src/a2a_mcp/agents/',
            '--agent-card', card_file,
            '--host', host,
            '--port', str(port)
        ]
        
        print(f"🚀 Iniciando {config['name']} na porta {port}...")
        print(f"Comando: {' '.join(cmd)}")
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.running_processes.append((agent_name, process))
            
            # Aguardar um pouco para verificar se iniciou
            time.sleep(2)
            
            if process.poll() is None:
                print(f"✅ {config['name']} iniciado com sucesso!")
                print(f"   URL: http://{host}:{port}")
                return process
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Falha ao iniciar {config['name']}")
                print(f"   Erro: {stderr.decode()}")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao iniciar agente: {e}")
            return None
    
    def stop_agent(self, agent_name: str):
        """Para um agente específico."""
        for name, process in self.running_processes:
            if name == agent_name:
                print(f"🛑 Parando {name}...")
                process.terminate()
                process.wait()
                self.running_processes.remove((name, process))
                print(f"✅ {name} parado com sucesso!")
                return True
        
        print(f"❌ Agente '{agent_name}' não está rodando.")
        return False
    
    def stop_all_agents(self):
        """Para todos os agentes."""
        if not self.running_processes:
            print("ℹ️  Nenhum agente está rodando.")
            return
        
        print("🛑 Parando todos os agentes...")
        for name, process in self.running_processes[:]:
            print(f"   Parando {name}...")
            process.terminate()
            process.wait()
            self.running_processes.remove((name, process))
        
        print("✅ Todos os agentes foram parados!")
    
    def status(self):
        """Mostra status dos agentes."""
        print("📊 Status dos Agentes MCP:")
        print("=" * 50)
        
        print(f"🆕 Agentes disponíveis: {len(self.config.NEW_AGENTS)}")
        print(f"🔄 Agentes rodando: {len(self.running_processes)}")
        
        if self.running_processes:
            print("\n🟢 Agentes em execução:")
            for name, process in self.running_processes:
                config = self.config.NEW_AGENTS[name]
                print(f"   • {config['name']} (porta {config['port']})")
        else:
            print("\n⚪ Nenhum agente em execução.")
    
    def test_agent(self, agent_name: str):
        """Testa um agente específico."""
        if agent_name not in self.config.NEW_AGENTS:
            print(f"❌ Agente '{agent_name}' não encontrado.")
            return False
        
        config = self.config.NEW_AGENTS[agent_name]
        port = config['port']
        
        print(f"🧪 Testando {config['name']}...")
        
        # Teste básico de conexão
        try:
            import requests
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ {config['name']} está respondendo!")
                return True
            else:
                print(f"⚠️  {config['name']} respondeu com status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro ao testar {config['name']}: {e}")
            return False
    
    def run_demo(self):
        """Executa uma demonstração dos agentes MCP."""
        print("🎯 Demonstração dos Agentes MCP Utilitários")
        print("=" * 50)
        
        # Exemplo de uso de cada agente
        demos = {
            "text_processor": {
                "description": "Processamento de texto",
                "examples": [
                    "Converta 'hello world' para título",
                    "Valide este JSON: {'name': 'test'}",
                    "Gere um ID único para sessão"
                ]
            },
            "calculator": {
                "description": "Cálculos matemáticos",
                "examples": [
                    "Calcule 15 + 25",
                    "Qual é 2 elevado a 8?",
                    "Calcule a raiz quadrada de 64"
                ]
            },
            "data_validator": {
                "description": "Validação de dados",
                "examples": [
                    "Valide esta estrutura JSON",
                    "Normalize estes nomes",
                    "Verifique a integridade dos dados"
                ]
            },
            "utility_helper": {
                "description": "Utilitário geral",
                "examples": [
                    "Formate texto e calcule resultado",
                    "Valide JSON e gere ID único",
                    "Mostre info do sistema"
                ]
            }
        }
        
        for agent_name, demo in demos.items():
            if agent_name in self.config.NEW_AGENTS:
                config = self.config.NEW_AGENTS[agent_name]
                print(f"\n🤖 {config['name']} (porta {config['port']})")
                print(f"   {demo['description']}")
                print("   Exemplos de uso:")
                for example in demo['examples']:
                    print(f"     • {example}")
                print(f"   Ferramentas: {', '.join(config['tools'])}")


def main():
    """Função principal do gerenciador."""
    parser = argparse.ArgumentParser(description='Gerenciador de Agentes MCP Utilitários')
    parser.add_argument('command', choices=[
        'list', 'activate', 'start', 'stop', 'stop-all', 'status', 'test', 'demo'
    ], help='Comando a executar')
    parser.add_argument('--agent', help='Nome do agente')
    parser.add_argument('--host', default='localhost', help='Host para iniciar agentes')
    
    args = parser.parse_args()
    
    manager = MCPAgentManager()
    
    try:
        if args.command == 'list':
            manager.list_available_agents()
        
        elif args.command == 'activate':
            if not args.agent:
                print("❌ --agent é obrigatório para ativar")
                sys.exit(1)
            manager.activate_agent(args.agent)
        
        elif args.command == 'start':
            if not args.agent:
                print("❌ --agent é obrigatório para iniciar")
                sys.exit(1)
            manager.start_agent(args.agent, args.host)
        
        elif args.command == 'stop':
            if not args.agent:
                print("❌ --agent é obrigatório para parar")
                sys.exit(1)
            manager.stop_agent(args.agent)
        
        elif args.command == 'stop-all':
            manager.stop_all_agents()
        
        elif args.command == 'status':
            manager.status()
        
        elif args.command == 'test':
            if not args.agent:
                print("❌ --agent é obrigatório para testar")
                sys.exit(1)
            manager.test_agent(args.agent)
        
        elif args.command == 'demo':
            manager.run_demo()
    
    except KeyboardInterrupt:
        print("\n🛑 Operação interrompida pelo usuário")
        manager.stop_all_agents()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 