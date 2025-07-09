#!/bin/bash

echo "=== MONITOR DE LOGS - CONVERSAS ==="
echo "Iniciando monitoramento..."
echo ""

# Função para capturar logs
monitor_logs() {
    echo "📋 Logs do MCP Server:"
    tail -f /Users/agents/Desktop/codex/mcp_server.log 2>/dev/null &
    
    echo "📋 Logs do sistema UI:"
    find /Users/agents/Desktop/codex/ui -name "*.log" -exec tail -f {} \; 2>/dev/null &
    
    echo "📋 Monitorando processos Python relacionados..."
    ps aux | grep -i python | grep -v grep
    
    echo ""
    echo "🔍 Aguardando logs... (Ctrl+C para parar)"
    wait
}

# Executar monitoramento
monitor_logs