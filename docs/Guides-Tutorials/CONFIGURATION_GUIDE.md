# Guia de Configuração A2A - a2a-unified.json

## 📋 Visão Geral

Este documento detalha como configurar e usar o arquivo de configuração centralizada `config/a2a-unified.json` para gerenciar todos os agentes A2A do sistema de forma unificada.

## 🗂️ Estrutura do Arquivo

```json
{
  "version": "1.0",
  "metadata": { ... },
  "global_defaults": { ... },
  "agents": [ ... ],
  "configuration_notes": { ... }
}
```

## 📊 Seções Detalhadas

### 1. Metadata

```json
{
  "metadata": {
    "created_by": "SPARC:coder - Configuration Consolidation",
    "created_at": "2025-07-13", 
    "description": "Configuração A2A unificada consolidando todos os arquivos a2a-config.json dispersos",
    "consolidation_source": [
      "./ui/agent_cards/",
      "./ui/utils/",
      "./ui/state/",
      // ... outros diretórios
    ],
    "total_agents": 10
  }
}
```

**Campos:**
- `created_by`: Sistema que criou o arquivo
- `created_at`: Data de criação
- `description`: Descrição do propósito do arquivo
- `consolidation_source`: Lista de diretórios consolidados
- `total_agents`: Total de agentes configurados

### 2. Global Defaults

Define configurações padrão aplicadas a todos os agentes:

```json
{
  "global_defaults": {
    "enabled": true,
    "protocol_version": "1.0",
    "discovery": {
      "auto_register": true,
      "registry_url": "http://localhost:8080/api/agents",
      "heartbeat_interval": 30000
    },
    "communication": {
      "transport": "http",
      "format": "json", 
      "compression": false,
      "timeout": 30000
    },
    "cooperation": {
      "task_delegation": true,
      "result_sharing": true,
      "skill_advertisement": true
    },
    "security": {
      "authentication": false,
      "encryption": false,
      "rate_limiting": true
    },
    "monitoring": {
      "metrics": true,
      "logging": true,
      "health_checks": true
    }
  }
}
```

#### 2.1 Discovery Settings

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `auto_register` | Boolean | true | Auto-registro no registry |
| `registry_url` | String | localhost:8080 | URL do registry central |
| `heartbeat_interval` | Number | 30000 | Intervalo de heartbeat (ms) |

#### 2.2 Communication Settings

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `transport` | String | "http" | Protocolo de transporte |
| `format` | String | "json" | Formato de dados |
| `compression` | Boolean | false | Compressão de dados |
| `timeout` | Number | 30000 | Timeout de comunicação (ms) |

#### 2.3 Cooperation Settings

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `task_delegation` | Boolean | true | Permite delegação de tarefas |
| `result_sharing` | Boolean | true | Compartilha resultados |
| `skill_advertisement` | Boolean | true | Anuncia capacidades |

#### 2.4 Security Settings

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `authentication` | Boolean | false | Autenticação obrigatória |
| `encryption` | Boolean | false | Encriptação de dados |
| `rate_limiting` | Boolean | true | Limitação de taxa |

#### 2.5 Monitoring Settings

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `metrics` | Boolean | true | Coleta de métricas |
| `logging` | Boolean | true | Logging habilitado |
| `health_checks` | Boolean | true | Verificações de saúde |

### 3. Configuração de Agentes

Cada agente é definido com esta estrutura:

```json
{
  "agent_name": "exemplo_agent",
  "project_name": "exemplo", 
  "location": "./path/to/agent/",
  "config_file": "./path/to/agent/a2a-config.json",
  "overrides": {
    // Configurações específicas que sobrescrevem global_defaults
  }
}
```

#### 3.1 Agentes Configurados

| Agent Name | Project | Location | Descrição |
|------------|---------|----------|-----------|
| `helloworld_agent` | helloworld | `./agents/helloworld/` | Agente de demonstração básica |
| `a2a_mcp_agent` | a2a_mcp | `./ui/a2a_mcp/` | Integração com MCP |
| `memory_agent` | memory | `./claude-code-10x/memory/` | Gerenciamento de memória |
| `agent_cards_agent` | agent_cards | `./ui/agent_cards/` | Sistema de cartas de agentes |
| `components_agent` | components | `./ui/components/` | Componentes de UI |
| `hosts_agent` | hosts | `./ui/hosts/` | Gerenciamento de hosts |
| `pages_agent` | pages | `./ui/pages/` | Páginas da aplicação |
| `scripts_agent` | scripts | `./ui/scripts/` | Scripts utilitários |
| `state_agent` | state | `./ui/state/` | Gerenciamento de estado |
| `utils_agent` | utils | `./ui/utils/` | Utilitários gerais |

## ⚙️ Configurações Específicas por Agente

### Usando Overrides

Para configurar um agente específico diferente dos padrões globais:

```json
{
  "agent_name": "special_agent",
  "project_name": "special",
  "location": "./agents/special/",
  "config_file": "./agents/special/a2a-config.json",
  "overrides": {
    "discovery": {
      "heartbeat_interval": 10000  // Override: heartbeat mais rápido
    },
    "communication": {
      "timeout": 60000,           // Override: timeout maior
      "compression": true         // Override: habilita compressão
    },
    "security": {
      "authentication": true,     // Override: requer autenticação
      "rate_limiting": false      // Override: remove rate limiting
    }
  }
}
```

### Configurações Avançadas

#### Cache Configuration Override
```json
{
  "overrides": {
    "cache": {
      "enabled": true,
      "redis": {
        "host": "redis-cluster.internal",
        "port": 6380,
        "password": "secure_password",
        "db": 2
      },
      "ttl_settings": {
        "discovery": 120,
        "health": 60,
        "agent_card": 1200
      }
    }
  }
}
```

#### Performance Tuning Override
```json
{
  "overrides": {
    "performance": {
      "enable_compression": true,
      "max_payload_size": "50mb",
      "connection_pool_size": 20,
      "keep_alive_timeout": 30000
    }
  }
}
```

## 🔧 Carregamento da Configuração

### No BaseA2AServer

```javascript
const fs = require('fs').promises;
const path = require('path');

class A2AConfigLoader {
  static async loadUnified() {
    const configPath = path.resolve('./config/a2a-unified.json');
    const configData = await fs.readFile(configPath, 'utf-8');
    return JSON.parse(configData);
  }

  static async getAgentConfig(agentName) {
    const unified = await this.loadUnified();
    const agent = unified.agents.find(a => a.agent_name === agentName);
    
    if (!agent) {
      throw new Error(`Agent ${agentName} not found in unified config`);
    }

    // Merge global defaults with agent overrides
    return this.mergeConfig(unified.global_defaults, agent.overrides || {});
  }

  static mergeConfig(defaults, overrides) {
    return {
      ...defaults,
      ...overrides,
      // Deep merge for nested objects
      discovery: { ...defaults.discovery, ...(overrides.discovery || {}) },
      communication: { ...defaults.communication, ...(overrides.communication || {}) },
      cooperation: { ...defaults.cooperation, ...(overrides.cooperation || {}) },
      security: { ...defaults.security, ...(overrides.security || {}) },
      monitoring: { ...defaults.monitoring, ...(overrides.monitoring || {}) }
    };
  }
}

// Uso no BaseA2AServer
class BaseA2AServer {
  constructor(agent, port = null, options = {}) {
    // Carregar configuração específica do agente
    this.loadAgentConfig(agent.name);
    // ... resto da inicialização
  }

  async loadAgentConfig(agentName) {
    try {
      this.agentConfig = await A2AConfigLoader.getAgentConfig(agentName);
      console.log(`✅ Configuração carregada para ${agentName}`);
    } catch (error) {
      console.warn(`⚠️ Falha ao carregar config para ${agentName}:`, error.message);
      // Fallback para configuração padrão
      this.agentConfig = await A2AConfigLoader.loadUnified().global_defaults;
    }
  }
}
```

## 🔄 Migração de Configurações Legacy

### Passo 1: Backup das Configurações Existentes

```bash
# Criar backup de todos os arquivos a2a-config.json
find . -name "a2a-config.json" -exec cp {} {}.backup \;
```

### Passo 2: Consolidar Configurações

```javascript
const consolidateConfigs = async () => {
  const paths = [
    './ui/agent_cards/',
    './ui/utils/',
    './ui/state/',
    // ... outros caminhos
  ];

  const consolidated = {
    version: "1.0",
    global_defaults: { /* padrões */ },
    agents: []
  };

  for (const path of paths) {
    const configFile = `${path}a2a-config.json`;
    if (fs.existsSync(configFile)) {
      const config = JSON.parse(await fs.readFile(configFile, 'utf-8'));
      consolidated.agents.push({
        agent_name: `${path.split('/').pop()}_agent`,
        project_name: path.split('/').pop(),
        location: path,
        config_file: configFile,
        overrides: extractOverrides(config)
      });
    }
  }

  await fs.writeFile('./config/a2a-unified.json', 
    JSON.stringify(consolidated, null, 2));
};
```

### Passo 3: Validar Migração

```bash
# Script de validação
node scripts/validate-config.js
```

## 🧪 Validação da Configuração

### Schema de Validação

```javascript
const configSchema = {
  version: { type: 'string', required: true },
  metadata: { type: 'object', required: true },
  global_defaults: { type: 'object', required: true },
  agents: { type: 'array', required: true, minItems: 1 },
  configuration_notes: { type: 'object', required: false }
};

const validateConfig = (config) => {
  // Implementar validação JSON Schema
  return ajv.validate(configSchema, config);
};
```

### Testes de Configuração

```javascript
describe('A2A Unified Configuration', () => {
  test('should load valid configuration', async () => {
    const config = await A2AConfigLoader.loadUnified();
    expect(config.version).toBe('1.0');
    expect(config.agents).toHaveLength(10);
  });

  test('should merge agent overrides correctly', () => {
    const merged = A2AConfigLoader.mergeConfig(
      { timeout: 30000, enabled: true },
      { timeout: 60000 }
    );
    expect(merged.timeout).toBe(60000);
    expect(merged.enabled).toBe(true);
  });
});
```

## ⚡ Performance e Otimização

### Cache de Configuração

```javascript
class A2AConfigCache {
  static cache = new Map();
  static TTL = 5 * 60 * 1000; // 5 minutos

  static async getConfig(agentName) {
    const cacheKey = `config:${agentName}`;
    const cached = this.cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < this.TTL) {
      return cached.config;
    }

    const config = await A2AConfigLoader.getAgentConfig(agentName);
    this.cache.set(cacheKey, {
      config,
      timestamp: Date.now()
    });

    return config;
  }
}
```

### Watch para Mudanças

```javascript
const chokidar = require('chokidar');

chokidar.watch('./config/a2a-unified.json').on('change', () => {
  console.log('🔄 Configuração alterada, recarregando...');
  A2AConfigCache.cache.clear();
  // Notificar agentes sobre mudança de config
});
```

## 🔍 Troubleshooting

### Problemas Comuns

**1. Arquivo de configuração não encontrado**
```bash
Error: ENOENT: no such file or directory, open './config/a2a-unified.json'
```
**Solução:** Verificar se o arquivo existe e o caminho está correto.

**2. JSON inválido**
```bash
SyntaxError: Unexpected token } in JSON
```
**Solução:** Validar JSON com ferramenta online ou `jsonlint`.

**3. Agente não encontrado**
```bash
Error: Agent my_agent not found in unified config
```
**Solução:** Verificar se o `agent_name` está correto no arquivo de configuração.

### Debugging

```javascript
// Habilitar logs detalhados
process.env.A2A_DEBUG = 'true';

// Verificar configuração carregada
console.log('Config carregada:', JSON.stringify(config, null, 2));

// Validar merge de overrides
console.log('Merged config:', mergedConfig);
```

## 📚 Referências

- [A2A Protocol Specification](./A2A_PROTOCOL.md)
- [BaseA2AServer Documentation](./BASEA2ASERVER.md)
- [Cache System Guide](./CACHE_SYSTEM.md)
- [Migration Guide](./MIGRATION_GUIDE.md)

---

**Para mais informações, consulte a documentação técnica completa.**