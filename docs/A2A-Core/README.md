# A2A-Core: Arquitetura Central e Protocolo

> Documentação fundamental do sistema Agent-to-Agent (A2A) - arquitetura, protocolos e especificações técnicas

## 📋 Visão Geral

Este cluster contém a documentação central do protocolo A2A (Agent-to-Agent), incluindo especificações de arquitetura, APIs, protocolos de comunicação e guias de implementação. É a base técnica para todo o sistema de coordenação entre agentes.

## 📁 Documentos Principais

### 🏗️ Arquitetura e Design
- **[A2A-ARCHITECTURE.md](./A2A-ARCHITECTURE.md)** - Arquitetura completa do sistema A2A
- **[A2A-UNIFIED-SYSTEM.md](./A2A-UNIFIED-SYSTEM.md)** - Sistema unificado A2A e especificações integradas

### 📡 API e Protocolos
- **[A2A-API-SPECIFICATION.md](./A2A-API-SPECIFICATION.md)** - Especificação completa da API A2A
- **[A2A-PROTOCOL-API.md](./A2A-PROTOCOL-API.md)** - Protocolos de comunicação e APIs
- **[a2a-sse-implementation.md](./a2a-sse-implementation.md)** - Implementação de Server-Sent Events

### 🔄 Migração e Estados
- **[A2A-MIGRATION-GUIDE.md](./A2A-MIGRATION-GUIDE.md)** - Guia de migração para nova versão A2A
- **[a2a-interaction-modes.md](./a2a-interaction-modes.md)** - Modos de interação entre agentes

### 🖥️ Servidor e Gerenciamento
- **[A2A_MCP_SERVER_STATUS.md](./A2A_MCP_SERVER_STATUS.md)** - Status do servidor MCP integrado
- **[A2A_SERVERS_PORT_MANAGEMENT.md](./A2A_SERVERS_PORT_MANAGEMENT.md)** - Gerenciamento de portas e servidores

## 🎯 Por Casos de Uso

### 👩‍💻 **Para Desenvolvedores**
1. Comece com [A2A-ARCHITECTURE.md](./A2A-ARCHITECTURE.md) para entender a estrutura
2. Consulte [A2A-API-SPECIFICATION.md](./A2A-API-SPECIFICATION.md) para implementação
3. Use [a2a-interaction-modes.md](./a2a-interaction-modes.md) para padrões de comunicação

### 🏗️ **Para Arquitetos de Sistema**
1. [A2A-UNIFIED-SYSTEM.md](./A2A-UNIFIED-SYSTEM.md) - Visão sistêmica completa
2. [A2A-ARCHITECTURE.md](./A2A-ARCHITECTURE.md) - Decisões arquiteturais
3. [A2A_SERVERS_PORT_MANAGEMENT.md](./A2A_SERVERS_PORT_MANAGEMENT.md) - Planejamento de infraestrutura

### 🔄 **Para Migração/Upgrade**
1. [A2A-MIGRATION-GUIDE.md](./A2A-MIGRATION-GUIDE.md) - Processo de migração
2. [A2A_MCP_SERVER_STATUS.md](./A2A_MCP_SERVER_STATUS.md) - Status de compatibilidade

## 🔗 Links Relacionados

### Documentação Complementar
- **Agentes**: [Agent-Systems](../Agent-Systems/) - Implementação de agentes
- **Infraestrutura**: [Infrastructure](../Infrastructure/) - Setup e deployment
- **MCP**: [MCP-Integration](../MCP-Integration/) - Integração MCP detalhada

### Guias Práticos
- **Setup**: [Configuração Completa](../Guides-Tutorials/CONFIGURACAO_COMPLETA.md)
- **Execução**: [Executar Sistema](../Guides-Tutorials/EXECUTAR_SISTEMA.md)
- **Debugging**: [Guardian Sistema](../Agent-Systems/GUARDIAN-SISTEMA-COMPLETO.md)

## 🚀 Quick Start A2A

```bash
# 1. Verificar status do servidor A2A
./claude-flow status

# 2. Inicializar sistema A2A
./claude-flow start --ui --port 3000

# 3. Testar comunicação entre agentes
./claude-flow agent spawn researcher
./claude-flow agent spawn coder

# 4. Monitorar interações A2A
./claude-flow monitor
```

## 📊 Fluxo de Comunicação A2A

```
Agent A ──► A2A Protocol ──► Agent B
   ↓           ↓              ↓
Task Queue → MCP Bridge → Response Handler
   ↓           ↓              ↓
Memory Store → Status Track → Result Sync
```

## 🔧 Configurações Críticas

### Portas Padrão
- **A2A Server**: 3000
- **MCP Bridge**: 3001
- **Monitor**: 3002

### Protocolos Suportados
- **HTTP/HTTPS**: API REST
- **WebSocket**: Comunicação em tempo real
- **SSE**: Server-Sent Events para streaming

## 📝 Contribuindo

Ao modificar documentos A2A-Core:

1. **Manter compatibilidade** com especificações existentes
2. **Atualizar diagramas** de arquitetura quando necessário
3. **Versionamento semântico** para mudanças de protocolo
4. **Testes de integração** para validar mudanças

## ⚠️ Avisos Importantes

- Mudanças em A2A-PROTOCOL-API.md requerem restart do sistema
- Migração deve seguir estritamente o A2A-MIGRATION-GUIDE.md
- Portas devem ser configuradas conforme A2A_SERVERS_PORT_MANAGEMENT.md

---

[← Voltar à Documentação Principal](../README.md) | [Próximo: Agent-Systems →](../Agent-Systems/README.md)