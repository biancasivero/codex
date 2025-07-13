# Guia Completo de Migração A2A: De a2a-server.js para BaseA2AServer

## 📋 Visão Geral

Este guia documenta como migrar servidores A2A existentes (`a2a-server.js`) para a nova arquitetura unificada `BaseA2AServer`, eliminando duplicação de código e adicionando recursos avançados.

### 🎯 Benefícios da Migração

**Performance e Cache:**
- ✅ Cache Redis com connection pooling
- ✅ Compressão de resposta (gzip)
- ✅ Cache warming automático
- ✅ Invalidação inteligente de cache

**Monitoramento e Observabilidade:**
- ✅ Métricas de performance em tempo real
- ✅ Logging estruturado com timestamps
- ✅ Health checks avançados
- ✅ Endpoints de estatísticas

**Robustez e Segurança:**
- ✅ Headers de segurança automáticos
- ✅ Graceful shutdown
- ✅ Error handling estruturado
- ✅ Rate limiting preparado

**Manutenibilidade:**
- ✅ Eliminação de ~80% do código duplicado
- ✅ Configuração centralizada
- ✅ Padrões consistentes
- ✅ Documentação automática

### ⚡ Antes vs Depois

**ANTES (Implementação Legacy):**
```javascript
// ~80 linhas por servidor
// Código duplicado em cada implementação
// Middlewares básicos apenas
// Sem cache ou monitoramento
// Manutenção fragmentada
```

**DEPOIS (BaseA2AServer):**
```javascript
// ~10-20 linhas por servidor
// Reutilização total da infraestrutura
// Cache Redis + compressão + monitoramento
// Endpoints avançados automáticos
// Manutenção centralizada
```

## 🔧 Pré-requisitos

### Dependências Obrigatórias
```bash
npm install express compression
```

### Dependências Opcionais (Recomendadas)
```bash
# Para cache Redis (altamente recomendado)
npm install redis ioredis

# Para monitoramento avançado
npm install prom-client
```

### Estrutura de Arquivos Necessária
```
projeto/
├── BaseA2AServer.js          # Classe base (deve existir)
├── RedisCache.js             # Cache Redis (opcional)
├── CacheMiddleware.js        # Middleware de cache (opcional)
├── .well-known/
│   └── agent.json           # Agent card (obrigatório)
└── [seu-modulo]/
    ├── a2a-server.js        # Arquivo a ser migrado
    └── agents/
        └── [agent-class].js # Sua implementação de agente
```

## 🚀 Padrões de Migração

### Padrão 1: Herança (Recomendado para Customizações)

**Quando usar:**
- Precisa de customizações específicas
- Quer manter controle total sobre a inicialização
- Implementação tem lógica especial

**Estrutura:**
```javascript
const BaseA2AServer = require('../../BaseA2AServer');
const SeuAgent = require('./agents/seu_agent');

class A2AServer extends BaseA2AServer {
  constructor() {
    const agent = new SeuAgent();
    const port = process.env.A2A_PORT || 8080;
    const options = {
      agentCardPath: '.well-known/agent.json',
      enableCache: true,
      corsOrigin: '*'
    };
    
    super(agent, port, options);
  }
  
  // Métodos customizados opcionais
  customMethod() {
    // Sua lógica específica
  }
}

// Start server if run directly
if (require.main === module) {
  const server = new A2AServer();
  server.start();
}

module.exports = A2AServer;
```

### Padrão 2: Configuração (Recomendado para Casos Simples)

**Quando usar:**
- Implementação simples sem customizações
- Quer máxima simplicidade
- Configuração baseada em parâmetros

**Estrutura:**
```javascript
const BaseA2AServer = require('../shared/BaseA2AServer');
const SeuAgent = require('./agents/seu_agent');

// Configuração simples e direta
const server = new BaseA2AServer({
  port: process.env.A2A_PORT || 8080,
  agentClass: SeuAgent,
  agentName: 'Seu Agent',
  basePath: __dirname,
  wellKnownPath: '.well-known'
});

// Start server if run directly
if (require.main === module) {
  server.start().catch(error => {
    console.error('❌ Failed to start A2A Server:', error);
    process.exit(1);
  });
}

module.exports = server;
```

## 📋 Processo Passo-a-Passo de Migração

### Passo 1: Backup e Análise 📁

**1.1 Criar backup do código atual:**
```bash
# Backup completo do arquivo atual
cp a2a-server.js a2a-server.js.backup
cp -r agents/ agents.backup/
```

**1.2 Analisar implementação atual:**
```bash
# Verificar dependências atuais
grep -n "require(" a2a-server.js

# Verificar endpoints implementados
grep -n "app\." a2a-server.js

# Verificar porta e configurações
grep -n "PORT\|port\|process.env" a2a-server.js
```

**1.3 Identificar customizações:**
- [ ] Middlewares customizados?
- [ ] Endpoints adicionais?
- [ ] Lógica específica de negócio?
- [ ] Configurações especiais?

### Passo 2: Preparação do Ambiente 🛠️

**2.1 Verificar BaseA2AServer:**
```bash
# Verificar se BaseA2AServer existe
ls -la BaseA2AServer.js

# Verificar se dependências estão instaladas
npm list express compression redis
```

**2.2 Instalar dependências ausentes:**
```bash
npm install express compression redis ioredis
```

**2.3 Verificar estrutura de diretórios:**
```bash
# Criar .well-known se não existir
mkdir -p .well-known

# Verificar agent.json
ls -la .well-known/agent.json
```

### Passo 3: Escolha do Padrão de Migração 🎯

**Decisão baseada em complexidade:**

| Característica | Herança | Configuração |
|---------------|---------|--------------|
| Customizações | ✅ Ideal | ❌ Limitado |
| Simplicidade | ⚠️ Moderada | ✅ Máxima |
| Flexibilidade | ✅ Total | ⚠️ Configurável |
| Manutenção | ⚠️ Moderada | ✅ Mínima |

**Para decidir, responda:**
1. Precisa de middlewares customizados? → **Herança**
2. Tem endpoints específicos? → **Herança**
3. Implementação é padrão? → **Configuração**
4. Quer máxima simplicidade? → **Configuração**

### Passo 4: Implementação da Migração 🚀

#### Opção A: Implementação por Herança

**4A.1 Identificar componentes do código atual:**
```javascript
// No arquivo atual, encontre:
const express = require('express');           // → Remover
const SeuAgent = require('./agents/...');     // → Manter
const app = express();                        // → Remover
const port = process.env.A2A_PORT || XXXX;    // → Extrair porta
```

**4A.2 Implementar nova estrutura:**
```javascript
const BaseA2AServer = require('../../BaseA2AServer');
const SeuAgent = require('./agents/seu_agent'); // ← Manter do código original

class A2AServer extends BaseA2AServer {
  constructor() {
    const agent = new SeuAgent();
    const port = process.env.A2A_PORT || XXXX; // ← Porta do código original
    const options = {
      agentCardPath: '.well-known/agent.json',
      enableCache: true,
      corsOrigin: '*'
    };
    
    super(agent, port, options);
    
    // ← Adicionar customizações aqui se necessário
  }
}

// Start server if run directly
if (require.main === module) {
  const server = new A2AServer();
  server.start();
}

module.exports = A2AServer;
```

#### Opção B: Implementação por Configuração

**4B.1 Implementar estrutura simplificada:**
```javascript
const BaseA2AServer = require('../shared/BaseA2AServer');
const SeuAgent = require('./agents/seu_agent'); // ← Do código original

const server = new BaseA2AServer({
  port: process.env.A2A_PORT || XXXX,          // ← Porta do código original
  agentClass: SeuAgent,
  agentName: 'Nome do Seu Agent',              // ← Nome descritivo
  basePath: __dirname,
  wellKnownPath: '.well-known'
});

// Start server if run directly
if (require.main === module) {
  server.start().catch(error => {
    console.error('❌ Failed to start A2A Server:', error);
    process.exit(1);
  });
}

module.exports = server;
```

### Passo 5: Validação e Teste 🧪

**5.1 Verificação sintática:**
```bash
# Verificar sintaxe JavaScript
node -c a2a-server.js
```

**5.2 Teste de inicialização:**
```bash
# Testar start do servidor
node a2a-server.js &
PID=$!

# Aguardar inicialização
sleep 3

# Verificar se está rodando
ps -p $PID

# Matar processo de teste
kill $PID
```

**5.3 Teste de endpoints básicos:**
```bash
# Definir porta para testes
export TEST_PORT=8080  # Use a porta do seu servidor

# Testar discovery
curl -s http://localhost:$TEST_PORT/discover | jq .

# Testar health
curl -s http://localhost:$TEST_PORT/health | jq .

# Testar agent card
curl -s http://localhost:$TEST_PORT/agent.json | jq .

# Testar info (novo endpoint)
curl -s http://localhost:$TEST_PORT/info | jq .
```

**5.4 Teste de funcionalidades avançadas:**
```bash
# Testar métricas
curl -s http://localhost:$TEST_PORT/metrics | jq .

# Testar cache stats (se Redis disponível)
curl -s http://localhost:$TEST_PORT/cache/stats | jq .

# Testar comunicação
curl -X POST http://localhost:$TEST_PORT/communicate \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

### Passo 6: Deploy e Finalização 🚁

**6.1 Backup final do código antigo:**
```bash
# Mover código antigo para backup dated
mv a2a-server.js.backup "a2a-server-legacy-$(date +%Y%m%d).js"
```

**6.2 Atualizar documentação:**
```bash
# Documentar mudanças no README local se existir
echo "## Migração para BaseA2AServer - $(date)" >> README.md
echo "- Migrado para BaseA2AServer em $(date)" >> README.md
echo "- Recursos adicionados: cache Redis, métricas, compressão" >> README.md
```

**6.3 Verificação final:**
```bash
# Restart definitivo
node a2a-server.js &

# Aguardar e verificar logs
sleep 5

# Verificar endpoints críticos
curl -s http://localhost:$TEST_PORT/discover >/dev/null && echo "✅ Discovery OK"
curl -s http://localhost:$TEST_PORT/health >/dev/null && echo "✅ Health OK"
curl -s http://localhost:$TEST_PORT/agent.json >/dev/null && echo "✅ Agent Card OK"
```

## 🔄 Exemplos Práticos de Migração

### Exemplo 1: Implementação Básica (Components Agent)

#### ANTES - Implementação Legacy (83 linhas)
```javascript
/**
 * A2A Server for components
 * Implements Agent2Agent Protocol endpoints
 */

const express = require('express');
const ComponentsAgent = require('./agents/components_agent');

class A2AServer {
  constructor() {
    this.app = express();
    this.port = process.env.A2A_PORT || 8149;
    this.agent = new ComponentsAgent();
    
    this.setupMiddleware();
    this.setupRoutes();
  }

  setupMiddleware() {
    this.app.use(express.json());
    this.app.use((req, res, next) => {
      res.header('Access-Control-Allow-Origin', '*');
      res.header('X-A2A-Protocol', '1.0');
      next();
    });
  }

  setupRoutes() {
    // A2A Protocol Endpoints
    this.app.get('/discover', async (req, res) => {
      const discovery = await this.agent.discover();
      res.json(discovery);
    });

    this.app.post('/communicate', async (req, res) => {
      const response = await this.agent.communicate(req.body);
      res.json(response);
    });

    this.app.post('/delegate', async (req, res) => {
      const result = await this.agent.delegate(req.body);
      res.json(result);
    });

    this.app.get('/health', async (req, res) => {
      const health = await this.agent.health();
      res.json(health);
    });

    // Agent Card endpoint
    this.app.get('/agent.json', async (req, res) => {
      const fs = require('fs').promises;
      const path = require('path');
      
      try {
        const agentCard = await fs.readFile(
          path.join(__dirname, '.well-known', 'agent.json'), 
          'utf-8'
        );
        res.json(JSON.parse(agentCard));
      } catch (error) {
        res.status(404).json({ error: 'Agent card not found' });
      }
    });
  }

  start() {
    this.app.listen(this.port, () => {
      console.log(`🤖 A2A Server for ${this.agent.name} running on port ${this.port}`);
      console.log(`📋 Endpoints:`);
      console.log(`   Discovery: http://localhost:${this.port}/discover`);
      console.log(`   Health: http://localhost:${this.port}/health`);
    });
  }
}

// Start server if run directly
if (require.main === module) {
  const server = new A2AServer();
  server.start();
}

module.exports = A2AServer;
```

#### DEPOIS - Com BaseA2AServer (27 linhas)
```javascript
/**
 * A2A Server for components
 * Refactored to use BaseA2AServer - eliminates code duplication
 */

const BaseA2AServer = require('../../BaseA2AServer');
const ComponentsAgent = require('./agents/components_agent');

class A2AServer extends BaseA2AServer {
  constructor() {
    const agent = new ComponentsAgent();
    const port = process.env.A2A_PORT || 8149;
    const options = {
      agentCardPath: '.well-known/agent.json',
      enableCache: true,
      corsOrigin: '*'
    };
    
    super(agent, port, options);
  }
}

// Start server if run directly
if (require.main === module) {
  const server = new A2AServer();
  server.start();
}

module.exports = A2AServer;
```

**📊 Redução: 83 → 27 linhas (67% menos código)**

#### Recursos Adicionados Automaticamente:
- ✅ Cache Redis com connection pooling
- ✅ Compressão gzip
- ✅ Métricas de performance (`/metrics`)
- ✅ Cache statistics (`/cache/stats`)
- ✅ Server info (`/info`)
- ✅ Headers de segurança
- ✅ Logging estruturado
- ✅ Error handling robusto
- ✅ Graceful shutdown

### Exemplo 2: Implementação por Configuração (Ainda Mais Simples)

#### Padrão de Configuração (18 linhas)
```javascript
/**
 * A2A Server for components
 * Uses unified BaseA2AServer to eliminate duplication
 */

const BaseA2AServer = require('../shared/BaseA2AServer');
const ComponentsAgent = require('./agents/components_agent');

// Simple configuration-based approach using BaseA2AServer
const server = new BaseA2AServer({
  port: process.env.A2A_PORT || 8149,
  agentClass: ComponentsAgent,
  agentName: 'Components Agent',
  basePath: __dirname,
  wellKnownPath: '.well-known'
});

// Start server if run directly
if (require.main === module) {
  server.start().catch(error => {
    console.error('❌ Failed to start A2A Server:', error);
    process.exit(1);
  });
}

module.exports = server;
```

**📊 Redução: 83 → 18 linhas (78% menos código)**

## ✅ Checklist de Verificação Pós-Migração

### Preparação e Dependências
- [ ] **Backup criado** - Código original salvo com data
- [ ] **BaseA2AServer.js existe** - Arquivo base disponível
- [ ] **Dependências instaladas** - `express`, `compression`, `redis`
- [ ] **Estrutura de diretórios** - `.well-known/agent.json` presente
- [ ] **Agent class funcionando** - Implementação do agente válida

### Implementação
- [ ] **Padrão escolhido** - Herança ou configuração definido
- [ ] **Importações corretas** - BaseA2AServer e Agent importados
- [ ] **Porta configurada** - Porta original mantida
- [ ] **Options configuradas** - `agentCardPath` e outras opções
- [ ] **Sintaxe válida** - `node -c a2a-server.js` passa

### Testes Funcionais
- [ ] **Start/Stop funciona** - Servidor inicia sem erros
- [ ] **Discovery endpoint** - `/discover` retorna dados válidos
- [ ] **Health endpoint** - `/health` retorna status
- [ ] **Communication endpoint** - `/communicate` aceita POST
- [ ] **Delegation endpoint** - `/delegate` aceita POST
- [ ] **Agent card endpoint** - `/agent.json` retorna card válido

### Novos Recursos
- [ ] **Info endpoint** - `/info` mostra detalhes do servidor
- [ ] **Metrics endpoint** - `/metrics` mostra estatísticas
- [ ] **Cache endpoints** - `/cache/stats` disponível
- [ ] **Headers avançados** - Headers de segurança presentes
- [ ] **Logging funciona** - Logs estruturados aparecem
- [ ] **Compressão ativa** - Response-Encoding: gzip presente

### Performance e Cache
- [ ] **Redis opcional** - Sistema funciona com/sem Redis
- [ ] **Cache warming** - Cache aquece na inicialização (se Redis)
- [ ] **Response time** - Header X-Response-Time presente
- [ ] **Error handling** - Erros retornam JSON estruturado
- [ ] **Graceful shutdown** - SIGTERM/SIGINT tratados

### Validação Final
- [ ] **Compatibilidade A2A** - Protocol headers corretos
- [ ] **Agent integration** - Agent methods chamados corretamente
- [ ] **Environment vars** - Variáveis de ambiente respeitadas
- [ ] **Documentation updated** - README ou docs atualizados
- [ ] **Legacy code archived** - Código antigo movido para backup

## 🚨 Troubleshooting Comum

### Problema: "Cannot find module 'BaseA2AServer'"

**Sintomas:**
```
Error: Cannot find module '../../BaseA2AServer'
```

**Soluções:**
```bash
# 1. Verificar se arquivo existe
ls -la ../../BaseA2AServer.js

# 2. Verificar caminho relativo
pwd
ls -la BaseA2AServer.js

# 3. Ajustar import path
# Se BaseA2AServer está na raiz: require('../../BaseA2AServer')
# Se BaseA2AServer está em shared: require('../shared/BaseA2AServer')
```

### Problema: "Redis connection failed"

**Sintomas:**
```
⚠️ Failed to initialize Redis cache: ECONNREFUSED
🔄 Server will continue without caching
```

**Soluções:**
```bash
# 1. Instalar Redis (macOS)
brew install redis
brew services start redis

# 2. Verificar se Redis está rodando
redis-cli ping  # Deve retornar PONG

# 3. Configurar Redis custom
export REDIS_HOST=seu-redis-host
export REDIS_PORT=6379
export REDIS_PASSWORD=sua-senha

# 4. Desabilitar cache se necessário
const options = { enableCache: false };
```

### Problema: "Port already in use"

**Sintomas:**
```
Error: listen EADDRINUSE :::8080
```

**Soluções:**
```bash
# 1. Verificar processo usando a porta
lsof -i :8080

# 2. Matar processo específico
kill -9 PID_DO_PROCESSO

# 3. Usar porta diferente
export A2A_PORT=8181

# 4. Configurar porta no código
const port = process.env.A2A_PORT || 8080;
```

### Problema: "Agent card not found"

**Sintomas:**
```
GET /agent.json → 404 Agent card not found
```

**Soluções:**
```bash
# 1. Verificar se arquivo existe
ls -la .well-known/agent.json

# 2. Criar diretório se necessário
mkdir -p .well-known

# 3. Criar agent.json básico
cat > .well-known/agent.json << 'EOF'
{
  "name": "Seu Agent",
  "version": "1.0.0",
  "description": "Descrição do seu agent",
  "capabilities": ["communicate", "delegate", "discover"],
  "endpoints": {
    "base": "http://localhost:8080"
  }
}
EOF

# 4. Configurar caminho custom
const options = { agentCardPath: 'caminho/para/agent.json' };
```

### Problema: "Agent methods not found"

**Sintomas:**
```
TypeError: this.agent.discover is not a function
```

**Soluções:**
```javascript
// 1. Verificar se agent implementa métodos obrigatórios
class SeuAgent {
  async discover() { /* implementação */ }
  async communicate(message) { /* implementação */ }
  async delegate(task) { /* implementação */ }
  async health() { /* implementação */ }
}

// 2. Verificar import do agent
const SeuAgent = require('./agents/seu_agent');
console.log(typeof SeuAgent); // Deve ser 'function'

// 3. Verificar instanciação
const agent = new SeuAgent();
console.log(typeof agent.discover); // Deve ser 'function'
```

### Problema: "Slow response warnings"

**Sintomas:**
```
⚠️ Slow response: GET /discover took 1250ms
```

**Soluções:**
```javascript
// 1. Implementar cache no agent
class SeuAgent {
  constructor() {
    this.cache = new Map();
  }
  
  async discover() {
    if (this.cache.has('discovery')) {
      return this.cache.get('discovery');
    }
    
    const result = await this.computeDiscovery();
    this.cache.set('discovery', result);
    return result;
  }
}

// 2. Usar cache Redis
const options = { 
  enableCache: true,
  cacheTTL: 300 // 5 minutos
};

// 3. Otimizar operações assíncronas
async function optimizedOperation() {
  // Use Promise.all para operações paralelas
  const [result1, result2] = await Promise.all([
    operation1(),
    operation2()
  ]);
  return { result1, result2 };
}
```

### Problema: "Memory usage growing"

**Sintomas:**
```
Memory usage growing over time
Heap usage: 150MB → 300MB → 450MB
```

**Soluções:**
```javascript
// 1. Limpar caches periodicamente
setInterval(() => {
  if (this.cache.size > 1000) {
    this.cache.clear();
  }
}, 60000); // A cada minuto

// 2. Usar WeakMap para referências
this.weakCache = new WeakMap();

// 3. Implementar TTL no cache local
class TTLCache {
  constructor(ttl = 300000) { // 5 minutos
    this.cache = new Map();
    this.timers = new Map();
    this.ttl = ttl;
  }
  
  set(key, value) {
    this.clear(key);
    this.cache.set(key, value);
    this.timers.set(key, setTimeout(() => {
      this.cache.delete(key);
      this.timers.delete(key);
    }, this.ttl));
  }
}

// 4. Monitorar uso de memória
app.get('/memory', (req, res) => {
  const usage = process.memoryUsage();
  res.json({
    rss: Math.round(usage.rss / 1024 / 1024) + 'MB',
    heapUsed: Math.round(usage.heapUsed / 1024 / 1024) + 'MB',
    heapTotal: Math.round(usage.heapTotal / 1024 / 1024) + 'MB'
  });
});
```

### Problema: "CORS issues in production"

**Sintomas:**
```
Access to fetch at 'http://agent:8080/discover' from origin 'http://frontend:3000' 
has been blocked by CORS policy
```

**Soluções:**
```javascript
// 1. Configurar CORS específico
const options = {
  corsOrigin: 'https://seu-frontend.com'
};

// 2. Múltiplas origens
const options = {
  corsOrigin: ['https://app.com', 'https://admin.com']
};

// 3. CORS dinâmico
const options = {
  corsOrigin: (origin) => {
    const allowed = ['https://app.com', 'https://staging.app.com'];
    return allowed.includes(origin);
  }
};

// 4. Headers adicionais se necessário
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Credentials', 'true');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization, X-A2A-Protocol');
  next();
});
```

## 📚 Recursos Adicionais

### Scripts de Automação

**Script de migração automática:**
```bash
#!/bin/bash
# migrate-a2a.sh

echo "🚀 Iniciando migração A2A para BaseA2AServer..."

# Backup
cp a2a-server.js "a2a-server-backup-$(date +%Y%m%d).js"
echo "✅ Backup criado"

# Extrair informações do arquivo atual
AGENT_REQUIRE=$(grep "require.*agent" a2a-server.js | head -1)
PORT=$(grep -o "process.env.A2A_PORT || [0-9]*" a2a-server.js | head -1)

echo "📋 Dados extraídos:"
echo "   Agent: $AGENT_REQUIRE"
echo "   Port: $PORT"

# Confirmar migração
read -p "Continuar com migração? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo "❌ Migração cancelada"
    exit 1
fi

# TODO: Implementar geração automática do novo arquivo
echo "🔄 Migração manual necessária - use o guia de migração"
```

**Script de teste automático:**
```bash
#!/bin/bash
# test-a2a.sh

PORT=${1:-8080}
echo "🧪 Testando A2A Server na porta $PORT..."

# Testar se servidor responde
if ! curl -s "http://localhost:$PORT/health" > /dev/null; then
    echo "❌ Servidor não está respondendo"
    exit 1
fi

echo "✅ Servidor está online"

# Testar endpoints críticos
declare -a endpoints=("/discover" "/health" "/agent.json" "/info")

for endpoint in "${endpoints[@]}"; do
    if curl -s "http://localhost:$PORT$endpoint" | jq . > /dev/null 2>&1; then
        echo "✅ $endpoint OK"
    else
        echo "❌ $endpoint FALHOU"
    fi
done

echo "🎉 Testes concluídos"
```

### Links Úteis

- **BaseA2AServer Documentation**: [Ver código fonte](../BaseA2AServer.js)
- **A2A Protocol Specification**: [A2A-UNIFIED-SYSTEM.md](./A2A-UNIFIED-SYSTEM.md)
- **Configuration Guide**: [CONFIGURATION_GUIDE.md](./CONFIGURATION_GUIDE.md)
- **Redis Setup Guide**: https://redis.io/docs/getting-started/
- **Express.js Documentation**: https://expressjs.com/
- **Node.js Performance Best Practices**: https://nodejs.org/en/docs/guides/simple-profiling/

---

## 📞 Suporte

**Problemas não cobertos neste guia?**

1. **Verificar logs detalhados** - Ativar logging verboso
2. **Testar com versão mínima** - Remover opções avançadas
3. **Comparar com exemplos** - Ver implementações em `/agents/` e `/ui/`
4. **Documentar o problema** - Incluir logs, configuração e steps para reproduzir

**Template para report de problemas:**
```markdown
## Problema
Descrição do problema encontrado

## Ambiente
- Node.js version: X.X.X
- OS: macOS/Linux/Windows
- Redis version: X.X.X (se aplicável)

## Código
```javascript
// Código relevante
```

## Logs
```
// Logs de erro
```

## Steps to reproduce
1. Step 1
2. Step 2
3. Step 3
```

---

**✨ Migração concluída com sucesso!**

Seu servidor A2A agora tem cache Redis, compressão, métricas, monitoramento e muito mais - tudo isso com significativamente menos código para manter.