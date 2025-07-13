# 🔄 Agentes Removidos do Sistema A2A MCP

## 📋 Resumo das Alterações

O sistema A2A MCP foi simplificado para incluir apenas os componentes essenciais:

### ✅ Agentes Ativos
- **Servidor MCP** (porta 10100) - Registry de agentes e ferramentas
- **Orchestrator Agent** (porta 10101) - Coordena tarefas e gerencia operações

### ❌ Agentes Removidos
- **Planner Agent** (porta 10102) - Agente planejador que quebra requisições em tarefas
- **Air Ticketing Agent** (porta 10103) - Agente de reserva de passagens aéreas
- **Hotel Booking Agent** (porta 10104) - Agente de reserva de hotéis
- **Car Rental Agent** (porta 10105) - Agente de aluguel de carros

## 📂 Alterações nos Arquivos

### 1. a2a_mcp_config.py
- Movidos agentes para seção `REMOVED_AGENTS`
- Mantido apenas `orchestrator` em `AGENT_CONFIGS`
- Adicionados métodos `get_removed_agent_config()` e `reactivate_agent()`
- Atualizada exibição de configuração

### 2. Agent Cards
- Movidos para `agent_cards/removed/`:
  - `planner_agent.json`
  - `air_ticketing_agent.json`
  - `hotel_booking_agent.json`
  - `car_rental_agent.json`
- Mantido apenas `orchestrator_agent.json` ativo

### 3. Documentação
- Atualizado `EXECUTAR_SISTEMA.md` com nova arquitetura
- Criado este arquivo de documentação das alterações

## 🔄 Como Reativar um Agente

### Método 1: Reativação Manual
```bash
# Mover agent card de volta
mv agent_cards/removed/planner_agent.json agent_cards/

# Editar a2a_mcp_config.py
# Mover configuração de REMOVED_AGENTS para AGENT_CONFIGS
```

### Método 2: Usando Código Python
```python
from a2a_mcp_config import A2AMCPConfig

# Reativar agente
success = A2AMCPConfig.reactivate_agent("planner")
if success:
    print("Agente reativado com sucesso!")
else:
    print("Agente não encontrado nos removidos")
```

### Método 3: Reativação Completa
```bash
# Restaurar todos os agent cards
mv agent_cards/removed/*.json agent_cards/

# Editar a2a_mcp_config.py manualmente
# Mover todas as configurações de REMOVED_AGENTS para AGENT_CONFIGS
```

## 📊 Comparação de Recursos

### Sistema Simplificado (Atual)
- **Portas**: 2 (10100, 10101)
- **Agentes**: 1 + Servidor MCP
- **Complexidade**: Baixa
- **Uso de Recursos**: Mínimo
- **Tempo de Startup**: Rápido

### Sistema Completo (Original)
- **Portas**: 6 (10100-10105)
- **Agentes**: 5 + Servidor MCP
- **Complexidade**: Alta
- **Uso de Recursos**: Moderado
- **Tempo de Startup**: Lento

## 🎯 Benefícios da Simplificação

1. **Menor Complexidade**: Apenas os componentes essenciais
2. **Startup Mais Rápido**: Menos processos para iniciar
3. **Menos Recursos**: Menor uso de CPU e memória
4. **Mais Estável**: Menos pontos de falha
5. **Fácil Debug**: Menos logs e processos para monitorar

## 📝 Configuração Atual

### Portas Utilizadas
- `10100` - Servidor MCP (SSE)
- `10101` - Orchestrator Agent (A2A)

### Portas Liberadas
- `10102` - Planner Agent (disponível)
- `10103` - Air Ticketing Agent (disponível)
- `10104` - Hotel Booking Agent (disponível)
- `10105` - Car Rental Agent (disponível)

## 🚀 Como Usar o Sistema Simplificado

```bash
# Iniciar sistema completo (apenas orchestrator + MCP)
python start_a2a_mcp.py

# Verificar configuração
python start_a2a_mcp.py --config

# Verificar status
python start_a2a_mcp.py --status
```

## 🔍 Testando o Sistema

### Endpoints Disponíveis
```bash
# Servidor MCP
curl -X GET "http://localhost:10100/health"

# Orchestrator Agent
curl -X GET "http://localhost:10101/health"

# Agent Card do Orchestrator
curl -X GET "http://localhost:10101/.well-known/agent.json"
```

## 📞 Suporte

Se precisar reativar algum agente:
1. Consulte a seção "Como Reativar um Agente" acima
2. Verifique se as dependências estão instaladas
3. Teste individualmente antes de reativar no sistema completo

---

**Alterações realizadas em:** {{ data_atual }}
**Objetivo:** Simplificar o sistema para focar nos componentes essenciais
**Impacto:** Redução de complexidade e melhoria na estabilidade 