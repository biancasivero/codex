#!/usr/bin/env python3
"""
Exemplos práticos: Diferenciação entre listar MCP vs listar Agentes
Demonstra como o Orchestrator Agent deve responder diferentemente
"""

import asyncio
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from a2a_mcp.mcp.client import init_session

def extract_result(result):
    if hasattr(result, 'content') and len(result.content) > 0:
        content = result.content[0].text
        if isinstance(content, str):
            try:
                return json.loads(content)
            except:
                return content
        return content
    return None

async def demonstrate_differentiation():
    print("🤖 ORCHESTRATOR AGENT - Demonstração de Diferenciação")
    print("=" * 70)
    
    try:
        async with init_session('localhost', 10100, 'sse') as session:
            print("✅ Conectado ao A2A MCP Server")
            
            # CENÁRIO 1: Usuário pergunta "O que você consegue fazer?"
            print("\n" + "="*50)
            print("📋 CENÁRIO 1: Usuário pergunta 'O que você consegue fazer?'")
            print("🎯 RESPOSTA: Usar system_info para mostrar FERRAMENTAS MCP")
            
            result = await session.call_tool('system_info', {})
            info = extract_result(result)
            
            if info:
                print(f"\n✅ Resposta do Orchestrator:")
                print(f"   'Tenho {len(info.get('available_tools', []))} ferramentas MCP disponíveis:'")
                print(f"   • Ferramentas de sistema: generate_unique_id, validate_json, calculate_basic")
                print(f"   • Gestão de agentes: list_agents, search_agents, get_agent_details, analyze_agent")
                print(f"   • Automação web: web_navigate, web_screenshot, web_click, browser_open")
                print(f"   'Posso coordenar agentes e automatizar tarefas web!'")
            
            # CENÁRIO 2: Usuário pergunta "Que agentes posso usar?"
            print("\n" + "="*50)
            print("📋 CENÁRIO 2: Usuário pergunta 'Que agentes posso usar?'")
            print("🎯 RESPOSTA: Usar list_agents para mostrar AGENTES delegáveis")
            
            try:
                agents_result = await session.call_tool('list_agents', {})
                agents_data = extract_result(agents_result)
                
                print(f"\n✅ Resposta do Orchestrator:")
                if agents_data and agents_data.get('success'):
                    print(f"   'Encontrei os seguintes agentes disponíveis para delegação:'")
                    # Simular lista de agentes
                    print(f"   • Calculator Agent - Para cálculos matemáticos")
                    print(f"   • Research Agent - Para pesquisas e análises") 
                    print(f"   • WebScraper Agent - Para extração de dados")
                else:
                    print(f"   'Atualmente não há agentes específicos configurados,'")
                    print(f"   'mas posso usar ferramentas diretas para automação!'")
                    
            except Exception as e:
                print(f"   ⚠️ Erro testando agentes: {e}")
            
            # CENÁRIO 3: Usuário pede "Calcule 5+3"
            print("\n" + "="*50)
            print("📋 CENÁRIO 3: Usuário pede 'Calcule 5+3'")
            print("🎯 DECISÃO: Ferramenta direta vs Delegação de agente")
            
            # Opção A: Ferramenta direta
            calc_result = await session.call_tool('calculate_basic', {
                'operation': 'add',
                'a': 5,
                'b': 3
            })
            calc_data = extract_result(calc_result)
            
            print(f"\n✅ Opção A - Ferramenta direta:")
            print(f"   Resultado: {calc_data.get('result', 'N/A') if calc_data else 'N/A'}")
            print(f"   'Calculei diretamente: 5 + 3 = 8'")
            
            # Opção B: Buscar agente calculadora
            search_result = await session.call_tool('search_agents', {
                'query': 'calculator math'
            })
            search_data = extract_result(search_result)
            
            print(f"\n✅ Opção B - Buscar agente:")
            if search_data and search_data.get('success'):
                print(f"   'Encontrei Calculator Agent - delegando tarefa...'")
            else:
                print(f"   'Nenhum agente calculadora encontrado, usando ferramenta direta.'")
            
            # CENÁRIO 4: Usuário pede "Abra google.com"
            print("\n" + "="*50)
            print("📋 CENÁRIO 4: Usuário pede 'Abra google.com'")
            print("🎯 RESPOSTA: Usar automação web direta")
            
            print(f"\n✅ Resposta do Orchestrator:")
            print(f"   'Abrindo google.com no seu navegador...'")
            print(f"   Comando usado: browser_open(url='https://google.com')")
            
            print("\n" + "="*70)
            print("🎉 RESUMO DA DIFERENCIAÇÃO:")
            print("┌─────────────────────────────────────────────────────────────────┐")
            print("│ PERGUNTA                    │ COMANDO      │ PROPÓSITO          │")
            print("├─────────────────────────────────────────────────────────────────┤")
            print("│ 'O que você faz?'           │ system_info  │ Mostrar ferramentas│")
            print("│ 'Que agentes posso usar?'   │ list_agents  │ Mostrar delegáveis │")
            print("│ 'Calcule X'                 │ Direto/Agent │ Decidir melhor via │")
            print("│ 'Abra site X'               │ web_navigate │ Automação direta   │")
            print("└─────────────────────────────────────────────────────────────────┘")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(demonstrate_differentiation())