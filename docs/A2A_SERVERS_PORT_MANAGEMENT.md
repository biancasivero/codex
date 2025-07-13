# Servidores A2A e Gerenciamento de Portas

## Mapa de Servidores A2A Disponíveis

### 🎯 Servidores MCP com Integração A2A

| Servidor | Porta | Status | Tipo | Capabilities | Comando |
|----------|-------|--------|------|--------------|---------|
| **Memory Agent** | 3001 | ✅ Ativo | MCP/Uvicorn | memory_storage, memory_retrieval, memory_search | `uvicorn mcp_server_memory.server:app --port 3001` |
| **Sequential Thinking** | 3010 | ⏸️ Configurado | MCP/Node | sequential_reasoning, problem_solving, decision_making | `node mcp-server-sequential-thinking/dist/index.js` |
| **Desktop Commander** | 3011 | ⏸️ Configurado | MCP/NPX | file_operations, system_commands, process_management | `npx @modelcontextprotocol/server-desktop-commander` |
| **Terminal Agent** | 3012 | ⏸️ Configurado | MCP/NPX | command_execution, shell_operations | `npx @modelcontextprotocol/server-terminal` |
| **Everything Agent** | 3013 | ⏸️ Configurado | MCP/NPX | utility_functions, examples, testing | `npx @modelcontextprotocol/server-everything` |

### 🌐 Servidores A2A Externos

| Servidor | URL/Porta | Status | Tipo | Capabilities |
|----------|-----------|--------|------|--------------|
| **A2A Bridge Smithery** | `server.smithery.ai` | ✅ Disponível | HTTP/API | agent_registration, message_sending, task_retrieval |

### 🔧 Infraestrutura A2A

| Componente | Porta | Status | Função |
|------------|-------|--------|---------|
| **A2A Coordination Bridge** | 8080 | ⏸️ Configurado | Central de coordenação entre agentes |
| **Service Registry** | 8080/api/agents | ⏸️ Configurado | Registro e descoberta de serviços |
| **Load Balancer** | 8080/api/route | ⏸️ Configurado | Balanceamento de carga |
| **Metrics Endpoint** | 8080/api/metrics | ⏸️ Configurado | Métricas e telemetria |

## 📊 Containers Claude Flow (Ativos)

| Container | Porta | Status | Função |
|-----------|-------|--------|---------|
| **claude-flow-orchestrator** | 3003 | 🔄 Restarting | Orchestrador principal |
| **organization-guardian** | - | ✅ Up 10h | Monitor A2A compliance |
| **mem0-bridge** | 3002 | ✅ Up 10h | Sistema híbrido de memória |
| **chroma-db** | 8000 | ⚠️ Unhealthy | Vector database |
| **redis** | 6379 | ✅ Up 10h | Cache e pub/sub |
| **portainer** | 9000/9443 | ✅ Up 10h | Gerenciamento Docker |

## 🗺️ Sistema de Organização de Portas

### Faixas de Portas por Categoria

```
3000-3099: Servidores MCP A2A
├── 3001: Memory Agent (MCP) ✅ ATIVO
├── 3002: Mem0-Bridge (Docker) ✅ ATIVO  
├── 3003: Orchestrator HTTP ⚠️ RESTARTING
├── 3010: Sequential Thinking MCP
├── 3011: Desktop Commander MCP
├── 3012: Terminal Agent MCP
├── 3013: Everything Agent MCP
├── 3014-3020: [Reservado para novos MCP]
└── 3021-3099: [Disponível]

6000-6999: Databases & Cache
├── 6379: Redis ✅ ATIVO
└── 6380-6999: [Disponível]

8000-8099: A2A Infrastructure 
├── 8000: ChromaDB ⚠️ UNHEALTHY
├── 8080: A2A Bridge/Coordination
├── 8081: A2A Service Registry  
├── 8082: A2A Load Balancer
└── 8083-8099: [Disponível]

9000-9999: Management & Monitoring
├── 9000: Portainer HTTP ✅ ATIVO
├── 9443: Portainer HTTPS ✅ ATIVO
└── 9001-9442, 9444-9999: [Disponível]
```

## 🚀 Como Iniciar Servidores A2A

### 1. Memória (Já Ativo)
```bash
# Já rodando via Docker
curl http://localhost:3002/health
```

### 2. Sequential Thinking  
```bash
# Instalar e iniciar na porta 3010
npm install -g @modelcontextprotocol/server-sequential-thinking
MCP_PORT=3010 npx @modelcontextprotocol/server-sequential-thinking
```

### 3. Desktop Commander
```bash
# Iniciar na porta 3011
MCP_PORT=3011 npx @modelcontextprotocol/server-desktop-commander
```

### 4. Terminal Agent
```bash  
# Iniciar na porta 3012
MCP_PORT=3012 npx @modelcontextprotocol/server-terminal
```

### 5. Everything (Utilitários)
```bash
# Iniciar na porta 3013  
MCP_PORT=3013 npx @modelcontextprotocol/server-everything
```

### 6. A2A Bridge Central
```bash
# Iniciar coordenação na porta 8080
cd scripts
./start-unified-a2a-system.sh
```

## 📋 Configuração Unificada

A configuração está centralizada em:
```json
// a2a-mcp-unified-config.json
{
  "mcp_servers": {
    "memory": { "port": 3001 },
    "sequential_thinking": { "port": 3010 }, 
    "desktop_commander": { "port": 3011 },
    "terminal": { "port": 3012 },
    "everything": { "port": 3013 }
  },
  "a2a_coordination": {
    "bridge_port": 8080,
    "registry_port": 8080,
    "metrics_port": 8080
  }
}
```

## 🔍 Monitoramento de Status

### Health Checks
```bash
# Verificar todos os servidores A2A
curl http://localhost:3001/health  # Memory
curl http://localhost:3002/health  # Mem0-Bridge  
curl http://localhost:3010/health  # Sequential Thinking
curl http://localhost:3011/health  # Desktop Commander
curl http://localhost:3012/health  # Terminal
curl http://localhost:3013/health  # Everything
curl http://localhost:8080/health  # A2A Bridge
```

### Docker Containers
```bash
# Status dos containers
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"

# Logs específicos
docker logs organization-guardian --tail 10
docker logs mem0-bridge --tail 10
```

### Portas em Uso
```bash
# Verificar portas ocupadas na faixa A2A
lsof -i :3001,:3002,:3003,:3010,:3011,:3012,:3013,:8080 | grep LISTEN
```

## 🛠️ Scripts de Automação

### Iniciar Todos os Servidores A2A
```bash
# Script para iniciar sistema completo
./scripts/start-unified-a2a-system.sh

# Ou individuais
./scripts/start-mcp-memory.sh
./scripts/start-mcp-sequential-thinking.sh  
./scripts/start-mcp-desktop-commander.sh
./scripts/start-mcp-terminal.sh
./scripts/start-mcp-everything.sh
```

### Parar Todos os Servidores
```bash
# Parar containers Docker
docker-compose down

# Parar processos MCP  
pkill -f "mcp-server"
pkill -f "uvicorn.*3001"
```

## 🔐 Segurança e Rate Limiting

```json
{
  "security": {
    "rate_limiting": {
      "enabled": true,
      "max_requests_per_minute": 100
    },
    "cors": {
      "enabled": true,
      "origins": ["http://localhost:*"]
    }
  }
}
```

## 📈 Próximos Passos

1. **Ativar A2A Bridge Central** (porta 8080)
2. **Iniciar MCP Servers restantes** (3010-3013)
3. **Configurar Service Discovery**
4. **Implementar Load Balancing**
5. **Adicionar Health Monitoring**
6. **Configurar Metrics Collection**

## 🚨 Resolução de Conflitos de Porta

### Se uma porta estiver ocupada:
```bash
# Verificar processo usando a porta
lsof -i :PORTA

# Matar processo se necessário  
kill -9 PID

# Ou usar porta alternativa
MCP_PORT=3020 npx servidor-mcp
```

### Portas de Fallback:
- MCP Servers: 3020-3099
- A2A Infrastructure: 8090-8099
- Monitoring: 9500-9599

---

**Última atualização:** 2025-07-12  
**Responsável:** Diego (Claude Code)  
**Status:** Documentação completa - Sistema híbrido ativo