# 🤖 Agent-to-Agent (A2A) Architecture

## Visão Geral

Este projeto implementa uma arquitetura Agent-to-Agent (A2A) que permite:

- **Coordenação de múltiplos agentes**: Cada agente possui especialização específica
- **Comunicação assíncrona**: Protocolos padronizados para troca de mensagens
- **Escalabilidade**: Adição dinâmica de novos agentes
- **Interoperabilidade**: Integração com diferentes frameworks

## Componentes Principais

### 1. Agent Card (`.well-known/agent.json`)
Configuração que define:
- Capacidades do agente
- Endpoints de comunicação
- Esquemas de entrada/saída
- Metadados de descoberta

### 2. Task Manager
Responsável por:
- Recebimento de tarefas
- Delegação para agentes especializados
- Monitoramento de progresso
- Consolidação de resultados

### 3. A2A Servers
Servidores que implementam:
- Protocolo de comunicação A2A
- Descoberta de agentes
- Roteamento de mensagens
- Balanceamento de carga

### 4. MCP Integration
Integração com Model Context Protocol para:
- Ferramentas especializadas
- Contexto compartilhado
- Recursos externos

## Padrões de Comunicação

### Request/Response
```typescript
interface A2ARequest {
  id: string;
  method: string;
  params: any;
  agent_target?: string;
}
```

### Task Delegation
```typescript
interface TaskRequest {
  task_id: string;
  task_type: string;
  payload: any;
  priority: number;
}
```

## Implementação

Para implementar um novo agente A2A:

1. **Definir Agent Card** em `.well-known/agent.json`
2. **Implementar TaskManager** para handling de tarefas
3. **Configurar A2A Server** para comunicação
4. **Registrar no Discovery** para ser encontrado por outros agentes

## Benefícios

- ✅ **Modularidade**: Agentes especializados e independentes
- ✅ **Escalabilidade**: Adição horizontal de capacidades
- ✅ **Resiliência**: Falha de um agente não afeta o sistema
- ✅ **Flexibilidade**: Diferentes tecnologias podem coexistir

---
*Documentação gerada automaticamente pelo Guardian A2A*
