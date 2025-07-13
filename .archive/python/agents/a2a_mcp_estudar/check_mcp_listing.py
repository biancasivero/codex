#!/usr/bin/env python3
"""
Verificar se MCP está listando DiegoTools
"""

import asyncio
import json
import sys
import os

sys.path.insert(0, 'src')
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

async def check_mcp_listing():
    print("🔍 Verificando se MCP lista DiegoTools...")
    
    try:
        async with init_session('localhost', 10100, 'sse') as session:
            print("✅ Conectado ao servidor A2A MCP")
            
            # Chamar system_info
            result = await session.call_tool('system_info', {})
            info = extract_result(result)
            
            if info:
                print(f"Sistema: {info.get('system_name', 'N/A')}")
                print(f"Total ferramentas: {len(info.get('available_tools', []))}")
                
                # Verificar DiegoTools
                diego = info.get('diego_tools', {})
                available = diego.get('available', False)
                tools_count = len(diego.get('tools', []))
                
                print(f"DiegoTools disponível: {available}")
                print(f"DiegoTools count: {tools_count}")
                
                if available and tools_count > 0:
                    print("🎉 SIM! MCP consegue listar DiegoTools!")
                    print(f"📋 Ferramentas DiegoTools disponíveis ({tools_count}):")
                    for i, tool in enumerate(diego.get('tools', []), 1):
                        print(f"  {i:2d}. {tool}")
                        
                    print("\n✅ O Orchestrator Agent pode usar todas essas ferramentas!")
                else:
                    print("❌ DiegoTools não está sendo listado corretamente")
                    
                # Listar todas as ferramentas A2A
                print(f"\n📋 Todas as ferramentas A2A ({len(info.get('available_tools', []))}):")
                for i, tool in enumerate(info.get('available_tools', []), 1):
                    print(f"  {i:2d}. {tool}")
                    
            else:
                print(f"❌ Erro obtendo system_info: {result}")
                
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    asyncio.run(check_mcp_listing())