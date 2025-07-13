#!/usr/bin/env python3
"""
Script de Startup para o Sistema A2A MCP
Facilita o gerenciamento e execução dos agentes A2A MCP
"""

import os
import sys
import signal
import subprocess
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import json

# Adicionar o diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

from a2a_mcp_config import A2AMCPConfig

class A2AMCPManager:
    """Gerenciador do sistema A2A MCP"""
    
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.running = False
        self.config = A2AMCPConfig()
    
    def check_environment(self) -> bool:
        """Verifica se o ambiente está configurado corretamente"""
        print("🔍 Verificando ambiente...")
        
        # Verificar se estamos no diretório correto
        if not Path("pyproject.toml").exists():
            print("❌ Erro: Execute o script no diretório do projeto A2A MCP")
            return False
        
        # Verificar variáveis de ambiente
        if not self.config.display_config():
            print("\n💡 Configure as variáveis de ambiente necessárias:")
            print("   export GOOGLE_API_KEY='sua_chave_aqui'")
            print("   export GOOGLE_PLACES_API_KEY='sua_chave_places_aqui'  # opcional")
            return False
        
        # Verificar se as dependências estão instaladas
        try:
            result = subprocess.run(
                ["uv", "sync"], 
                capture_output=True, 
                text=True,
                cwd=Path.cwd()
            )
            if result.returncode != 0:
                print(f"❌ Erro ao instalar dependências: {result.stderr}")
                return False
        except FileNotFoundError:
            print("❌ Erro: 'uv' não encontrado. Instale o uv primeiro.")
            return False
        
        print("✅ Ambiente verificado com sucesso!")
        return True
    
    def start_mcp_server(self) -> bool:
        """Inicia o servidor MCP"""
        print(f"🚀 Iniciando servidor MCP na porta {self.config.MCP_PORT}...")
        
        try:
            cmd = [
                "uv", "run", "a2a-mcp", 
                "--run", "mcp-server",
                "--host", self.config.MCP_HOST,
                "--port", str(self.config.MCP_PORT),
                "--transport", self.config.MCP_TRANSPORT
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path.cwd()
            )
            
            self.processes["mcp_server"] = process
            
            # Aguardar um pouco para o servidor iniciar
            time.sleep(3)
            
            # Verificar se o processo ainda está rodando
            if process.poll() is None:
                print(f"✅ Servidor MCP iniciado com sucesso!")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Erro ao iniciar servidor MCP:")
                print(f"   stdout: {stdout}")
                print(f"   stderr: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao iniciar servidor MCP: {e}")
            return False
    
    def start_agent(self, agent_name: str) -> bool:
        """Inicia um agente específico"""
        config = self.config.get_agent_config(agent_name)
        if not config:
            print(f"❌ Configuração não encontrada para o agente: {agent_name}")
            return False
        
        print(f"🤖 Iniciando {config['name']} na porta {config['port']}...")
        
        try:
            cmd = [
                "uv", "run", "src/a2a_mcp/agents/",
                "--agent-card", config["card_file"],
                "--host", "localhost",
                "--port", str(config["port"])
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path.cwd()
            )
            
            self.processes[agent_name] = process
            
            # Aguardar um pouco para o agente iniciar
            time.sleep(2)
            
            # Verificar se o processo ainda está rodando
            if process.poll() is None:
                print(f"✅ {config['name']} iniciado com sucesso!")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Erro ao iniciar {config['name']}:")
                print(f"   stdout: {stdout}")
                print(f"   stderr: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao iniciar {config['name']}: {e}")
            return False
    
    def start_all_agents(self) -> bool:
        """Inicia todos os agentes"""
        success = True
        
        for agent_name in self.config.AGENT_CONFIGS.keys():
            if not self.start_agent(agent_name):
                success = False
        
        return success
    
    def stop_all(self):
        """Para todos os processos"""
        print("\n🛑 Parando todos os processos...")
        
        for name, process in self.processes.items():
            try:
                print(f"   Parando {name}...")
                process.terminate()
                process.wait(timeout=5)
                print(f"   ✅ {name} parado")
            except subprocess.TimeoutExpired:
                print(f"   ⚠️ Forçando parada de {name}...")
                process.kill()
                process.wait()
                print(f"   ✅ {name} forçadamente parado")
            except Exception as e:
                print(f"   ❌ Erro ao parar {name}: {e}")
        
        self.processes.clear()
        self.running = False
    
    def status(self):
        """Mostra status dos processos"""
        print("📊 Status do Sistema A2A MCP")
        print("=" * 50)
        
        if not self.processes:
            print("🔴 Nenhum processo rodando")
            return
        
        for name, process in self.processes.items():
            if process.poll() is None:
                print(f"🟢 {name} - Rodando (PID: {process.pid})")
            else:
                print(f"🔴 {name} - Parado")
    
    def run_full_system(self):
        """Executa o sistema completo"""
        print("🎯 Iniciando Sistema A2A MCP Completo")
        print("=" * 50)
        
        # Verificar ambiente
        if not self.check_environment():
            return False
        
        # Configurar handler para SIGINT (Ctrl+C)
        def signal_handler(signum, frame):
            print("\n🛑 Recebido sinal de interrupção...")
            self.stop_all()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Iniciar servidor MCP
        if not self.start_mcp_server():
            return False
        
        # Aguardar servidor MCP estar pronto
        time.sleep(5)
        
        # Iniciar todos os agentes
        if not self.start_all_agents():
            print("⚠️ Alguns agentes falharam ao iniciar")
        
        self.running = True
        
        print("\n🎉 Sistema A2A MCP iniciado com sucesso!")
        print("📋 Endpoints disponíveis:")
        print(f"   • Servidor MCP: {self.config.MCP_URL}")
        
        for agent_name, config in self.config.AGENT_CONFIGS.items():
            print(f"   • {config['name']}: http://localhost:{config['port']}")
        
        print("\n💡 Comandos disponíveis:")
        print("   • Ctrl+C para parar todos os processos")
        print("   • Use outro terminal para interagir com os agentes")
        
        # Manter o script rodando
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_all()
        
        return True
    
    def run_single_agent(self, agent_name: str):
        """Executa um único agente"""
        print(f"🎯 Iniciando agente individual: {agent_name}")
        print("=" * 50)
        
        # Verificar ambiente
        if not self.check_environment():
            return False
        
        # Configurar handler para SIGINT (Ctrl+C)
        def signal_handler(signum, frame):
            print("\n🛑 Recebido sinal de interrupção...")
            self.stop_all()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Iniciar agente
        if not self.start_agent(agent_name):
            return False
        
        self.running = True
        
        config = self.config.get_agent_config(agent_name)
        print(f"\n🎉 {config['name']} iniciado com sucesso!")
        print(f"📋 Endpoint: http://localhost:{config['port']}")
        
        # Manter o script rodando
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_all()
        
        return True

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Gerenciador do Sistema A2A MCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python start_a2a_mcp.py                     # Inicia sistema completo
  python start_a2a_mcp.py --agent orchestrator  # Inicia apenas o orchestrator
  python start_a2a_mcp.py --config            # Mostra configuração
  python start_a2a_mcp.py --status            # Mostra status
        """
    )
    
    parser.add_argument(
        "--agent",
        choices=list(A2AMCPConfig.AGENT_CONFIGS.keys()),
        help="Inicia apenas um agente específico"
    )
    
    parser.add_argument(
        "--config",
        action="store_true",
        help="Mostra configuração do sistema"
    )
    
    parser.add_argument(
        "--status",
        action="store_true", 
        help="Mostra status dos processos"
    )
    
    args = parser.parse_args()
    
    manager = A2AMCPManager()
    
    if args.config:
        manager.config.display_config()
        return
    
    if args.status:
        manager.status()
        return
    
    if args.agent:
        return manager.run_single_agent(args.agent)
    else:
        return manager.run_full_system()

if __name__ == "__main__":
    main() 