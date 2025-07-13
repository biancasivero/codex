# Agent-Systems: Sistemas de Agentes e Orquestração

> Documentação de agentes especializados, orquestração multi-agente e coordenação de tarefas

## 📋 Visão Geral

Este cluster contém toda documentação relacionada aos sistemas de agentes do Codex, incluindo agentes especializados (Auto-commit, Organizador, Guardian), orchestrator, coordenação multi-agente, estados de tarefas e monitoramento de agentes em tempo real.

## 📁 Documentos por Categoria

### 🤖 Agentes Especializados
- **[AGENTE-AUTO-COMMIT.md](./AGENTE-AUTO-COMMIT.md)** - Agent de commits automáticos com conventional commits
- **[AGENTE-ORGANIZADOR-AUTONOMO.md](./AGENTE-ORGANIZADOR-AUTONOMO.md)** - Agent organizador autônomo de arquivos e estruturas
- **[GUARDIAN-SISTEMA-COMPLETO.md](./GUARDIAN-SISTEMA-COMPLETO.md)** - Sistema Guardian para monitoramento e proteção

### 🎼 Orquestração e Coordenação
- **[ORCHESTRATOR_AGENT_GUIDE.md](./ORCHESTRATOR_AGENT_GUIDE.md)** - Guia completo do Orchestrator Agent
- **[ORCHESTRATOR_AGENT_GUIA.md](./ORCHESTRATOR_AGENT_GUIA.md)** - Guia em português do Orchestrator
- **[CLAUDE_FLOW_A2A_ORCHESTRATOR.md](./CLAUDE_FLOW_A2A_ORCHESTRATOR.md)** - Integração Claude Flow com A2A
- **[ORCHESTRATOR-RESOLUTION-SUMMARY.md](./ORCHESTRATOR-RESOLUTION-SUMMARY.md)** - Resumo de resoluções do Orchestrator

### 📊 Estados e Monitoramento
- **[HELLOWORLD_AGENT_TASKSTATE_COMPLETED.md](./HELLOWORLD_AGENT_TASKSTATE_COMPLETED.md)** - Exemplo de agent HelloWorld com estado completo
- **[HELLOWORLD_TESTE_REMOTO.md](./HELLOWORLD_TESTE_REMOTO.md)** - Testes remotos de agents HelloWorld

### 🔧 Estrutura e Configuração
- **[ESTRUTURA-ORGANIZADOR-COMPLETA.md](./ESTRUTURA-ORGANIZADOR-COMPLETA.md)** - Estrutura completa do sistema organizador
- **[NOVOS_AGENTES_MCP.md](./NOVOS_AGENTES_MCP.md)** - Novos agentes com integração MCP
- **[AGENTES_REMOVIDOS.md](./AGENTES_REMOVIDOS.md)** - Log de agentes removidos e razões

## 🎯 Por Casos de Uso

### 🚀 **Quick Start com Agentes**
1. [HELLOWORLD_AGENT_TASKSTATE_COMPLETED.md](./HELLOWORLD_AGENT_TASKSTATE_COMPLETED.md) - Primeiro agent
2. [ORCHESTRATOR_AGENT_GUIDE.md](./ORCHESTRATOR_AGENT_GUIDE.md) - Orquestração básica
3. [AGENTE-AUTO-COMMIT.md](./AGENTE-AUTO-COMMIT.md) - Automação de commits

### 🏗️ **Desenvolvimento de Novos Agentes**
1. [NOVOS_AGENTES_MCP.md](./NOVOS_AGENTES_MCP.md) - Framework para novos agentes
2. [ESTRUTURA-ORGANIZADOR-COMPLETA.md](./ESTRUTURA-ORGANIZADOR-COMPLETA.md) - Estrutura organizacional
3. [GUARDIAN-SISTEMA-COMPLETO.md](./GUARDIAN-SISTEMA-COMPLETO.md) - Padrões de monitoramento

### 🎼 **Orquestração Avançada**
1. [CLAUDE_FLOW_A2A_ORCHESTRATOR.md](./CLAUDE_FLOW_A2A_ORCHESTRATOR.md) - Integração Claude Flow
2. [ORCHESTRATOR-RESOLUTION-SUMMARY.md](./ORCHESTRATOR-RESOLUTION-SUMMARY.md) - Resolução de problemas
3. [HELLOWORLD_TESTE_REMOTO.md](./HELLOWORLD_TESTE_REMOTO.md) - Testes remotos

## 🔗 Integrações e Dependências

### Sistema A2A
- **Protocolo**: [A2A-Core](../A2A-Core/) - Comunicação entre agentes
- **API**: [A2A-API-SPECIFICATION.md](../A2A-Core/A2A-API-SPECIFICATION.md)

### MCP Integration
- **Tools**: [MCP-Integration](../MCP-Integration/) - Ferramentas MCP
- **Bridge**: [CLAUDE_CODE_A2A_BRIDGE_MCP_TOOLS.md](../MCP-Integration/CLAUDE_CODE_A2A_BRIDGE_MCP_TOOLS.md)

### Infraestrutura
- **Docker**: [DOCKER-COMPOSE-UNIFICADO.md](../Infrastructure/DOCKER-COMPOSE-UNIFICADO.md)
- **Monitor**: [ENHANCED-MONITOR-GUIDE.md](../Infrastructure/ENHANCED-MONITOR-GUIDE.md)

## 🚀 Comandos de Agentes

### Criação e Gerenciamento
```bash
# Listar agentes disponíveis
./claude-flow agent list

# Criar agente especializado
./claude-flow agent spawn researcher --name "data-analyst"
./claude-flow agent spawn coder --name "backend-dev"

# Status dos agentes
./claude-flow agent status
```

### Orquestração SPARC
```bash
# Modo orchestrator (padrão)
./claude-flow sparc "Implement user authentication system"

# Modo específico
./claude-flow sparc run coder "Create API endpoints for user management"
./claude-flow sparc run tester "Write comprehensive tests for auth system"

# Coordenação swarm
./claude-flow swarm "Build e-commerce platform" --strategy development --max-agents 8
```

### Agentes Especializados
```bash
# Auto-commit agent
git add . && ./scripts/auto-commit.sh

# Organizador autônomo
./claude-flow agent spawn organizer --auto-structure

# Guardian monitoring
./claude-flow monitor --guardian --alerts
```

## 📊 Fluxo de Coordenação

```
Orchestrator ──► Task Distribution ──► Specialized Agents
     ↓                   ↓                      ↓
Task Queue ──► A2A Protocol ──► Agent Communication
     ↓                   ↓                      ↓
Memory Store ──► State Tracking ──► Result Aggregation
```

## 🏗️ Arquitetura de Agentes

### Tipos de Agentes
1. **Core Agents**: researcher, coder, analyzer, tester
2. **Specialized**: auto-commit, organizer, guardian
3. **Coordination**: orchestrator, swarm-coordinator
4. **Support**: documenter, debugger, memory-manager

### Estados de Agente
- **idle**: Aguardando tarefas
- **active**: Executando tarefas
- **coordinating**: Coordenando com outros agentes
- **error**: Estado de erro
- **completed**: Tarefa finalizada

## ⚙️ Configuração de Agentes

### Configuração Global
```json
{
  "max_agents": 10,
  "timeout": 300000,
  "auto_cleanup": true,
  "monitoring": true,
  "guardian_enabled": true
}
```

### Agente Auto-commit
```json
{
  "conventional_commits": true,
  "auto_push": false,
  "branch_protection": true,
  "commit_patterns": ["feat:", "fix:", "docs:", "refactor:"]
}
```

## 📝 Desenvolvendo Novos Agentes

### 1. Estrutura Base
```typescript
class NewAgent extends BaseAgent {
  async execute(task: Task): Promise<Result> {
    // Implementação do agente
  }
  
  async coordinate(agents: Agent[]): Promise<void> {
    // Coordenação A2A
  }
}
```

### 2. Registro no Sistema
```bash
# Registrar novo agente
./claude-flow agent register ./agents/new-agent.ts

# Testar agente
./claude-flow agent test new-agent --dry-run
```

### 3. Documentação
- Seguir padrão dos agentes existentes
- Incluir exemplos de uso
- Documentar dependências MCP

## 🔍 Debugging e Monitoramento

### Logs de Agentes
```bash
# Logs em tempo real
./claude-flow logs --agent orchestrator --follow

# Logs específicos
./claude-flow logs --agent auto-commit --last 100

# Guardian monitoring
./claude-flow guardian status --detailed
```

### Troubleshooting Comum
- **Agent não responde**: Verificar A2A connectivity
- **Estado inconsistente**: Usar `./claude-flow agent reset`
- **Memoria saturada**: Executar memory cleanup
- **Coordenação falha**: Verificar orchestrator logs

## ⚠️ Boas Práticas

1. **Sempre usar TodoWrite** para coordenação de tarefas
2. **Memory storage** para estado persistente entre agentes
3. **Guardian monitoring** para sistemas críticos
4. **Conventional commits** para auto-commit agent
5. **Testes remotos** antes de deploy em produção

---

[← A2A-Core](../A2A-Core/README.md) | [Voltar à Documentação Principal](../README.md) | [Próximo: Guides-Tutorials →](../Guides-Tutorials/README.md)