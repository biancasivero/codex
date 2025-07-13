# Infrastructure: Infraestrutura e Banco de Dados

> Documentação de infraestrutura, PostgreSQL, Docker, monitoramento e sistemas de memória

## 📋 Visão Geral

Este cluster contém toda documentação relacionada à infraestrutura do sistema Codex, incluindo configuração de banco de dados PostgreSQL, containerização Docker, sistemas de monitoramento, memória híbrida e adaptações Mem0-OSS.

## 📁 Documentos por Categoria

### 🗄️ **Banco de Dados**
- **[01-POSTGRESQL.md](./01-POSTGRESQL.md)** - Setup e configuração do PostgreSQL
- **[A2A-POSTGRESQL-INTEGRATION.md](./A2A-POSTGRESQL-INTEGRATION.md)** - Integração PostgreSQL com A2A
- **[HYBRID_MEMORY_SYSTEM.md](./HYBRID_MEMORY_SYSTEM.md)** - Sistema de memória híbrida

### 🐳 **Containerização**
- **[DOCKER-COMPOSE-UNIFICADO.md](./DOCKER-COMPOSE-UNIFICADO.md)** - Docker Compose unificado
- **[AUTO-COMMIT-DOCKER-GUIDE.md](./AUTO-COMMIT-DOCKER-GUIDE.md)** - Docker para auto-commit
- **[CONTAINERS-ESPECIALIZADOS.md](./CONTAINERS-ESPECIALIZADOS.md)** - Containers especializados

### 📊 **Monitoramento**
- **[ENHANCED-MONITOR-GUIDE.md](./ENHANCED-MONITOR-GUIDE.md)** - Guia de monitoramento aprimorado
- **[ENHANCED-MONITOR-SUMMARY.md](./ENHANCED-MONITOR-SUMMARY.md)** - Resumo do sistema de monitoramento

### 🧠 **Sistemas de Memória**
- **[MEM0-OSS-ADAPTATION-PLAN.md](./MEM0-OSS-ADAPTATION-PLAN.md)** - Plano de adaptação Mem0-OSS
- **[MEM0-OSS-IMPLEMENTATION-SUMMARY.md](./MEM0-OSS-IMPLEMENTATION-SUMMARY.md)** - Resumo da implementação Mem0

## 🚀 Setup Rápido

### 1. **Infraestrutura Básica (15 minutos)**
```bash
# 1. PostgreSQL
docs/Infrastructure/01-POSTGRESQL.md

# 2. Docker Compose
docs/Infrastructure/DOCKER-COMPOSE-UNIFICADO.md

# 3. Verificar setup
./claude-flow status
```

### 2. **Monitoramento (10 minutos)**
```bash
# 1. Enhanced Monitor
docs/Infrastructure/ENHANCED-MONITOR-GUIDE.md

# 2. Ativar monitoramento
./claude-flow monitor --enhanced

# 3. Dashboard
open http://localhost:3002/monitor
```

### 3. **Memória Avançada (20 minutos)**
```bash
# 1. Sistema híbrido
docs/Infrastructure/HYBRID_MEMORY_SYSTEM.md

# 2. Mem0-OSS
docs/Infrastructure/MEM0-OSS-IMPLEMENTATION-SUMMARY.md

# 3. Configurar memória
./claude-flow memory config --hybrid
```

## 🎯 Por Casos de Uso

### 🏗️ **Deploy de Produção**
1. **[DOCKER-COMPOSE-UNIFICADO.md](./DOCKER-COMPOSE-UNIFICADO.md)** - Container orchestration
2. **[01-POSTGRESQL.md](./01-POSTGRESQL.md)** - Database production setup
3. **[ENHANCED-MONITOR-GUIDE.md](./ENHANCED-MONITOR-GUIDE.md)** - Production monitoring
4. **[A2A-POSTGRESQL-INTEGRATION.md](./A2A-POSTGRESQL-INTEGRATION.md)** - A2A integration

### 🔧 **Desenvolvimento Local**
1. **[AUTO-COMMIT-DOCKER-GUIDE.md](./AUTO-COMMIT-DOCKER-GUIDE.md)** - Dev containers
2. **[CONTAINERS-ESPECIALIZADOS.md](./CONTAINERS-ESPECIALIZADOS.md)** - Specialized containers
3. **[HYBRID_MEMORY_SYSTEM.md](./HYBRID_MEMORY_SYSTEM.md)** - Local memory setup

### 📊 **Monitoramento e Analytics**
1. **[ENHANCED-MONITOR-SUMMARY.md](./ENHANCED-MONITOR-SUMMARY.md)** - Overview
2. **[ENHANCED-MONITOR-GUIDE.md](./ENHANCED-MONITOR-GUIDE.md)** - Detailed setup
3. **Sistema de métricas** em tempo real

### 🧠 **Sistemas de Memória Avançados**
1. **[MEM0-OSS-ADAPTATION-PLAN.md](./MEM0-OSS-ADAPTATION-PLAN.md)** - Planning
2. **[MEM0-OSS-IMPLEMENTATION-SUMMARY.md](./MEM0-OSS-IMPLEMENTATION-SUMMARY.md)** - Implementation
3. **[HYBRID_MEMORY_SYSTEM.md](./HYBRID_MEMORY_SYSTEM.md)** - Hybrid approach

## 🏗️ Arquitetura de Infraestrutura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web UI        │    │   A2A Core      │    │   MCP Bridge    │
│   (Port 3000)   │────│   (Port 3001)   │────│   (Port 3002)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Network                              │
├─────────────────┬─────────────────┬─────────────────┬─────────┤
│   PostgreSQL    │   Redis Cache   │   Monitor       │   Mem0  │
│   (Port 5432)   │   (Port 6379)   │   (Port 8080)   │   OSS   │
└─────────────────┴─────────────────┴─────────────────┴─────────┘
```

## 🐳 Docker Compose Setup

### Arquivo Principal
```yaml
# docker-compose.yml (ver DOCKER-COMPOSE-UNIFICADO.md)
version: '3.8'
services:
  codex-app:
    build: .
    ports: ["3000:3000"]
    depends_on: [postgres, redis]
    
  postgres:
    image: postgres:15
    ports: ["5432:5432"]
    environment:
      POSTGRES_DB: codex
      POSTGRES_USER: codex_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    
  redis:
    image: redis:7
    ports: ["6379:6379"]
    
  monitor:
    build: ./monitor
    ports: ["8080:8080"]
```

### Comandos Essenciais
```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Rebuild specific service
docker-compose build codex-app
docker-compose up -d codex-app

# Cleanup
docker-compose down -v
```

## 🗄️ PostgreSQL Configuration

### Setup Inicial
```sql
-- Database creation (ver 01-POSTGRESQL.md)
CREATE DATABASE codex;
CREATE USER codex_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE codex TO codex_user;

-- A2A Integration tables
CREATE TABLE agents (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(100) NOT NULL,
  status VARCHAR(50) DEFAULT 'idle',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  agent_id INTEGER REFERENCES agents(id),
  description TEXT,
  status VARCHAR(50) DEFAULT 'pending',
  result JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Performance Tuning
```sql
-- Índices para performance
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_tasks_agent_status ON tasks(agent_id, status);
CREATE INDEX idx_tasks_created ON tasks(created_at);

-- Configurações de performance
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
```

## 📊 Sistema de Monitoramento

### Métricas Principais
- **System Health**: CPU, Memory, Disk usage
- **Agent Performance**: Task completion rate, response time
- **Database**: Connection pool, query performance
- **Network**: A2A communication latency

### Dashboard Endpoints
```bash
# Main dashboard
http://localhost:8080/dashboard

# Metrics API
http://localhost:8080/api/metrics

# Health check
http://localhost:8080/health

# Real-time logs
http://localhost:8080/logs/stream
```

### Alerting
```yaml
# alerts.yml
alerts:
  high_cpu:
    threshold: 80
    action: email
  agent_failure:
    threshold: 3
    action: restart
  memory_leak:
    threshold: 90
    action: cleanup
```

## 🧠 Sistema de Memória Híbrida

### Componentes
1. **PostgreSQL**: Structured data, relationships
2. **Redis**: Cache, session data
3. **Mem0-OSS**: Vector embeddings, semantic search
4. **File System**: Large objects, backups

### Configuration
```json
{
  "memory": {
    "primary": "postgresql",
    "cache": "redis",
    "vector": "mem0-oss",
    "backup": "filesystem",
    "sync_interval": 300
  }
}
```

### Memory Operations
```bash
# Store in hybrid system
./claude-flow memory store "project_context" "Complex project data" --hybrid

# Vector search
./claude-flow memory search "authentication patterns" --semantic

# Backup memory
./claude-flow memory backup --destination ./backups/memory-$(date +%Y%m%d).sql
```

## 🔧 Containers Especializados

### Agent Containers
```dockerfile
# Dockerfile.agent
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Monitor Container
```dockerfile
# Dockerfile.monitor
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY monitor/ .
EXPOSE 8080
CMD ["python", "monitor.py"]
```

### Auto-commit Container
```dockerfile
# Dockerfile.autocommit
FROM alpine/git:latest
RUN apk add --no-cache nodejs npm
WORKDIR /workspace
COPY autocommit/ .
CMD ["./auto-commit.sh"]
```

## 🚨 Monitoramento de Produção

### Health Checks
```bash
# System health
./claude-flow health --comprehensive

# Database connectivity
./claude-flow db check --connection --performance

# Agent status
./claude-flow agent health --all

# Memory usage
./claude-flow memory stats --detailed
```

### Log Aggregation
```bash
# Central logging
./claude-flow logs --aggregate --export json > system.log

# Real-time monitoring
./claude-flow monitor --real-time --alerts

# Performance metrics
./claude-flow metrics --export grafana
```

## 🔒 Security & Backup

### Database Security
```sql
-- User permissions
REVOKE ALL ON DATABASE codex FROM PUBLIC;
GRANT CONNECT ON DATABASE codex TO codex_user;

-- SSL configuration
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/etc/ssl/certs/server.crt';
ALTER SYSTEM SET ssl_key_file = '/etc/ssl/private/server.key';
```

### Backup Strategy
```bash
# Database backup
pg_dump codex > backups/codex-$(date +%Y%m%d).sql

# Memory backup
./claude-flow memory export backups/memory-$(date +%Y%m%d).json

# Full system backup
./scripts/backup-full.sh
```

## 📝 Troubleshooting

### Problemas Comuns
```bash
# Container não inicia
docker-compose logs service_name

# Database connection issues
./claude-flow db diagnose

# Memory leaks
./claude-flow memory cleanup --force

# Port conflicts
./claude-flow config ports --check --fix
```

### Performance Issues
```bash
# Database slow queries
./claude-flow db analyze --slow-queries

# Memory fragmentation
./claude-flow memory defrag

# Network latency
./claude-flow network diagnose --a2a
```

## 🔗 Integrações

### Com Sistema A2A
- **Database**: [A2A-POSTGRESQL-INTEGRATION.md](./A2A-POSTGRESQL-INTEGRATION.md)
- **Protocol**: [A2A-ARCHITECTURE.md](../A2A-Core/A2A-ARCHITECTURE.md)

### Com Agentes
- **Orchestrator**: [ORCHESTRATOR_AGENT_GUIDE.md](../Agent-Systems/ORCHESTRATOR_AGENT_GUIDE.md)
- **Guardian**: [GUARDIAN-SISTEMA-COMPLETO.md](../Agent-Systems/GUARDIAN-SISTEMA-COMPLETO.md)

### Com MCP
- **Integration**: [MCP_TOOLS_INTEGRATION.md](../MCP-Integration/MCP_TOOLS_INTEGRATION.md)
- **Bridge**: [CLAUDE_CODE_A2A_BRIDGE_MCP_TOOLS.md](../MCP-Integration/CLAUDE_CODE_A2A_BRIDGE_MCP_TOOLS.md)

---

[← Guides-Tutorials](../Guides-Tutorials/README.md) | [Voltar à Documentação Principal](../README.md) | [Próximo: MCP-Integration →](../MCP-Integration/README.md)