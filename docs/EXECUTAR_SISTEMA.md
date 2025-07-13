# 🚀 Como Executar o Sistema A2A MCP

## Visão Geral

Este sistema A2A MCP foi simplificado para incluir apenas os componentes essenciais:
- **Servidor MCP** (porta 10100) - Registry de agentes e ferramentas
- **Orchestrator Agent** (porta 10101) - Coordena tarefas e gerencia operações

## 🔧 Pré-requisitos

### 1. Verificar Diretório
```bash
cd /Users/agents/Desktop/codex/agents/a2a_mcp
```

### 2. Configurar Variáveis de Ambiente
```bash
# Obrigatório
export GOOGLE_API_KEY="sua_chave_google_aqui"

# Opcional
export GOOGLE_PLACES_API_KEY="sua_chave_places_aqui"
export A2A_LOG_LEVEL="INFO"
```

### 3. Instalar Dependências
```bash
uv sync
```

## 🚀 Executar o Sistema

### Opção 1: Sistema Completo (Recomendado)
```bash
python start_a2a_mcp.py
```

### Opção 2: Apenas Orchestrator Agent
```bash
python start_a2a_mcp.py --agent orchestrator
```

### Opção 3: Usando Python Module
```bash
python -m a2a_mcp
```

## 📋 Endpoints Disponíveis

Após iniciar o sistema, você terá acesso aos seguintes endpoints:

### Servidor MCP
- **URL**: `http://localhost:10100/sse`
- **Função**: Registry de agentes e ferramentas MCP
- **Ferramentas**: `find_agent`, `query_places_data`, `query_travel_data`

### Orchestrator Agent
- **URL**: `http://localhost:10101`
- **Função**: Coordena tarefas e gerencia operações
- **Protocolo**: A2A com suporte a SSE

## 🛠️ Comandos Úteis

### Verificar Configuração
```bash
python start_a2a_mcp.py --config
```

### Verificar Status
```bash
python start_a2a_mcp.py --status
```

### Parar Sistema
```bash
# Ctrl+C no terminal onde está rodando
# ou
pkill -f "start_a2a_mcp"
```

## 🔍 Verificar Se Está Funcionando

### 1. Testar Servidor MCP
```bash
curl -X GET "http://localhost:10100/health"
```

### 2. Testar Orchestrator Agent
```bash
curl -X GET "http://localhost:10101/health"
```

## 📊 Monitoramento

### Ver Logs em Tempo Real
```bash
tail -f logs/a2a_mcp.log
```

### Verificar Processos
```bash
ps aux | grep -E "(start_a2a_mcp|orchestrator)"
```

## 🔄 Agentes Removidos

Os seguintes agentes foram removidos da configuração ativa mas estão disponíveis para reativação futura:

- **Planner Agent** (porta 10102) - Agent card em `agent_cards/removed/`
- **Air Ticketing Agent** (porta 10103) - Agent card em `agent_cards/removed/`
- **Hotel Booking Agent** (porta 10104) - Agent card em `agent_cards/removed/`
- **Car Rental Agent** (porta 10105) - Agent card em `agent_cards/removed/`

### Para Reativar um Agente
```bash
# Mover agent card de volta
mv agent_cards/removed/planner_agent.json agent_cards/

# Atualizar configuração em a2a_mcp_config.py
# Usar método reactivate_agent() ou editar manualmente
```

## 🐛 Solução de Problemas

### Erro: "Porta já em uso"
```bash
# Verificar processos usando as portas
lsof -i :10100
lsof -i :10101

# Matar processo específico
kill -9 <PID>
```

### Erro: "Variável de ambiente não encontrada"
```bash
# Verificar variáveis
echo $GOOGLE_API_KEY
echo $GOOGLE_PLACES_API_KEY

# Configurar se necessário
export GOOGLE_API_KEY="sua_chave_aqui"
```

### Erro: "Dependências não instaladas"
```bash
# Reinstalar dependências
uv sync --force
```

## 🎯 Próximos Passos

1. **Iniciar Sistema**: Use `python start_a2a_mcp.py`
2. **Integrar com UI**: Registre os agentes na UI Mesop
3. **Testar Funcionalidades**: Use o orchestrator para coordenar tarefas
4. **Monitorar**: Acompanhe logs e status dos agentes

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs
2. Confirme as variáveis de ambiente
3. Teste as portas individualmente
4. Consulte a documentação completa em `README_SIMPLIFICADO.md`

---

**Sistema simplificado e otimizado para foco nas funcionalidades essenciais! 🎉** 