#!/usr/bin/env python3
"""
Script para testar o Chart Generator Agent com as configurações padronizadas
"""

import json
import requests
import time


def test_agent_health():
    """Testa se o agente está respondendo"""
    try:
        response = requests.get("http://localhost:10011/.well-known/agent.json")
        if response.status_code == 200:
            agent_info = response.json()
            print("✅ Agent está ativo!")
            print(f"   Nome: {agent_info['name']}")
            print(f"   URL: {agent_info['url']}")
            print(f"   Streaming: {agent_info['capabilities']['streaming']}")
            return True
        else:
            print(f"❌ Agent não está respondendo: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar com o agent: {e}")
        return False


def test_chart_generation():
    """Testa a geração de gráficos"""
    test_data = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [
                    {
                        "kind": "text",
                        "text": "Generate a chart of revenue: Jan,$1000 Feb,$2000 Mar,$1500 Apr,$2500 May,$3000"
                    }
                ],
                "messageId": "test-chart-001",
                "contextId": "test-context"
            }
        },
        "id": 1
    }
    
    try:
        response = requests.post(
            "http://localhost:10011/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Teste de geração de gráfico executado!")
            print(f"   Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Erro na geração do gráfico: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar geração de gráfico: {e}")
        return False


def main():
    """Função principal de teste"""
    print("🧪 Testando Chart Generator Agent (Configuração Padronizada)")
    print("=" * 60)
    
    # Teste 1: Verificar se o agent está ativo
    print("\n1. Verificando saúde do agent...")
    if not test_agent_health():
        print("\n❌ Agent não está ativo. Inicie o agent primeiro:")
        print("   cd backup-reorganized/active-prototypes/analytics")
        print("   python __main__.py")
        return
    
    # Teste 2: Verificar geração de gráficos
    print("\n2. Testando geração de gráficos...")
    test_chart_generation()
    
    print("\n🎉 Testes concluídos!")
    print("\nPara iniciar o agent manualmente:")
    print("   cd backup-reorganized/active-prototypes/analytics")
    print("   python __main__.py --host localhost --port 10011")


if __name__ == "__main__":
    main() 