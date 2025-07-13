# 🐳 Containers Especializados - Claude Flow

## 📋 Visão Geral

O Claude Flow possui **5 containers especializados**, cada um otimizado para uma função específica:

---

## 1. 🎯 **Dockerfile** (Container Principal)
**Arquivo**: `docker/Dockerfile`

### Função
- Container base para agentes principais
- Guardian e agentes de organização
- Funcionalidades gerais do sistema

### Características
- **Base**: Node.js 20 Alpine
- **Tecnologias**: TypeScript, tsx, Git
- **Usuário**: Não-root (agent)
- **Volumes**: `/workspace`
- **Foco**: Segurança e performance

### Usa Para
- Organization Guardian
- Agentes de análise
- Tarefas de organização

---

## 2. 📊 **Dockerfile.agent-log** (Analytics)
**Arquivo**: `docker/Dockerfile.agent-log`

### Função
- Sistema de logging e analytics
- API REST para dados de agentes
- Monitoramento de execuções

### Características
- **Base**: Node.js 20 Alpine
- **Porta**: 3001
- **Health Check**: Curl endpoint
- **Tecnologias**: TypeScript, Express
- **Usuário**: nodejs (não-root)

### Endpoints
- `/health` - Status do serviço
- `/api/stats` - Estatísticas
- `/api/executions` - Execuções

---

## 3. 🌐 **Dockerfile.flask** (Dashboard Web)
**Arquivo**: `docker/Dockerfile.flask`

### Função
- Dashboard web interativo
- Visualização de dados em tempo real
- Interface web para monitoramento

### Características
- **Base**: Python 3.11 Slim
- **Porta**: 5001
- **Tecnologias**: Flask, Docker CLI
- **Integração**: Mem0, Docker API
- **Templates**: HTML dinâmico

### Funcionalidades
- Dashboard interativo
- Relatórios visuais
- Integração com Mem0
- Monitoramento Docker

---

## 4. 🧠 **Dockerfile.mem0-bridge** (Memória)
**Arquivo**: `docker/Dockerfile.mem0-bridge`

### Função
- Ponte entre agentes e Mem0
- Adaptador de memória simples
- Armazenamento JSON local

### Características
- **Base**: Node.js 20 Alpine
- **Porta**: 3002
- **Tecnologias**: Express, UUID
- **Storage**: JSON local
- **Fallback**: Quando Mem0 não está disponível

### Uso
- Backup de memória
- Desenvolvimento local
- Testes sem Mem0

---

## 5. 🚀 **Dockerfile.orchestrator-final** (Orquestração)
**Arquivo**: `docker/Dockerfile.orchestrator-final`

### Função
- Orquestrador principal do Claude Flow
- Coordenação entre agentes
- SPARC (Sistema de Coordenação)

### Características
- **Base**: Node.js 20 Slim
- **Porta**: 3003
- **Tecnologias**: Deno, Claude-Flow CLI
- **Funcionalidades**: Coordenação, Memória
- **Arquitetura**: SPARC

### Funcionalidades
- Inicialização de projetos
- Coordenação de agentes
- Gerenciamento de memória
- Interface SPARC

---

## 🎯 Resumo dos Containers

| Container | Função | Porta | Tecnologia | Especialização |
|-----------|--------|-------|------------|----------------|
| **Principal** | Agentes básicos | - | Node.js/TS | Organização |
| **Agent Log** | Analytics | 3001 | Node.js/TS | Logging |
| **Flask** | Dashboard | 5001 | Python/Flask | Interface Web |
| **Mem0 Bridge** | Memória | 3002 | Node.js/TS | Armazenamento |
| **Orchestrator** | Orquestração | 3003 | Node.js/Deno | Coordenação |

---

## 🚀 Como Usar

### 1. **Container Principal**
```bash
# Via docker-compose
docker-compose --profile guardian up -d

# Direto
docker build -f docker/Dockerfile -t claude-flow-main .
docker run -v $(pwd):/workspace claude-flow-main
```

### 2. **Agent Log**
```bash
# Via docker-compose
docker-compose --profile analytics up -d

# Direto
docker build -f docker/Dockerfile.agent-log -t agent-log .
docker run -p 3001:3001 agent-log
```

### 3. **Flask Dashboard**
```bash
# Via docker-compose
docker-compose --profile flask up -d

# Direto
docker build -f docker/Dockerfile.flask -t flask-dashboard .
docker run -p 5001:5001 flask-dashboard
```

### 4. **Mem0 Bridge**
```bash
# Via docker-compose
docker-compose --profile mem0-oss up -d

# Direto
docker build -f docker/Dockerfile.mem0-bridge -t mem0-bridge .
docker run -p 3002:3002 mem0-bridge
```

### 5. **Orchestrator**
```bash
# Via docker-compose
docker-compose --profile sparc up -d

# Direto
docker build -f docker/Dockerfile.orchestrator-final -t orchestrator .
docker run -p 3003:3003 orchestrator
```

---

## 🛠️ Desenvolvimento

### Construir Todos
```bash
# Construir todos os containers
docker-compose build

# Construir um específico
docker-compose build portainer
docker-compose build agent-log-flask
```

### Logs
```bash
# Logs de todos
docker-compose logs -f

# Logs específicos
docker logs -f agent-log-service
docker logs -f agent-log-flask
```

---

## 🔧 Personalização

### Adicionar Novo Container
1. Criar `docker/Dockerfile.novo-servico`
2. Adicionar ao `docker-compose.yml`
3. Configurar profile apropriado
4. Testar isoladamente

### Exemplo de Novo Container
```dockerfile
FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY src/ ./src/
EXPOSE 3004

CMD ["npx", "tsx", "/app/src/novo-servico.ts"]
```

---

## 🎉 Benefícios

### **Separação de Responsabilidades**
- Cada container tem uma função específica
- Fácil manutenção e debugging
- Escalabilidade independente

### **Segurança**
- Usuários não-root em todos os containers
- Isolamento de processos
- Health checks configurados

### **Performance**
- Imagens otimizadas por função
- Cache de dependências
- Builds multi-stage quando necessário

### **Flexibilidade**
- Containers podem ser usados independentemente
- Profiles para diferentes cenários
- Fácil integração com sistemas externos

---

## 🎯 Resumo Final

**5 containers especializados** = **Sistema completo e profissional**

Cada container é otimizado para sua função específica, garantindo:
- ✅ **Performance** máxima
- ✅ **Segurança** rigorosa  
- ✅ **Facilidade** de uso
- ✅ **Flexibilidade** total 