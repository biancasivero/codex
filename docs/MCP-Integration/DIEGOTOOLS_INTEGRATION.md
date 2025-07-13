# 🛠️ DiegoTools Integration - A2A MCP com Automação Web e Gestão de Agentes

## 🎯 Visão Geral

As **DiegoTools** foram integradas ao sistema A2A MCP, permitindo que o **Orchestrator Agent** coordene tarefas que envolvem:
- **Automação Web** via Puppeteer
- **Gestão de Agentes** 
- **Automação de Browser**

## 📋 Ferramentas Disponíveis

### 🌐 **Web Automation (Puppeteer)**

#### `web_navigate`
Navegar para uma URL usando Puppeteer
```python
await session.call_tool('web_navigate', {
    'url': 'https://example.com',
    'wait_for': '#content'  # opcional
})
```

#### `web_screenshot`
Tirar screenshot da página atual
```python
await session.call_tool('web_screenshot', {
    'name': 'homepage',
    'selector': '#main-content'  # opcional
})
```

#### `web_click`
Clicar em um elemento da página
```python
await session.call_tool('web_click', {
    'selector': 'button.submit'
})
```

#### `web_type`
Digitar texto em um campo
```python
await session.call_tool('web_type', {
    'selector': '#email',
    'text': 'user@example.com'
})
```

#### `web_get_content`
Obter conteúdo da página
```python
await session.call_tool('web_get_content', {
    'selector': '.article'  # opcional
})
```

#### `open_browser`
Abrir browser Puppeteer
```python
await session.call_tool('open_browser', {
    'headless': True
})
```

### 🖥️ **Browser Básico**

#### `browser_open`
Abrir URL no browser padrão do sistema
```python
await session.call_tool('browser_open', {
    'url': 'https://example.com'
})
```

### 🤖 **Gestão de Agentes**

#### `list_agents`
Listar agentes disponíveis no sistema
```python
await session.call_tool('list_agents', {})
```

#### `get_agent_details`
Obter detalhes de um agente específico
```python
await session.call_tool('get_agent_details', {
    'agent_id': 'orchestrator_agent'
})
```

#### `analyze_agent`
Analisar capacidades de um agente
```python
await session.call_tool('analyze_agent', {
    'agent_id': 'calculator_agent'
})
```

#### `search_agents`
Buscar agentes por critérios
```python
await session.call_tool('search_agents', {
    'query': 'calculadora matemática'
})
```

## 🔧 Arquitetura da Integração

### **1. Diego Tools Bridge**
- **Arquivo**: `src/a2a_mcp/mcp/diego_tools_bridge.py`
- **Função**: Ponte entre A2A MCP e mcp-run-ts-tools
- **Comunicação**: MCP stdio protocol

### **2. Servidor MCP Atualizado**
- **Arquivo**: `src/a2a_mcp/mcp/server.py` 
- **Adicionado**: 11 novas ferramentas DiegoTools
- **Integração**: Async calls via bridge

### **3. Configuração Automática**
- **Path Discovery**: Localiza automaticamente mcp-run-ts-tools
- **Health Check**: Verifica disponibilidade das ferramentas
- **Error Handling**: Graceful degradation se indisponível

## 🚀 Como o Orchestrator Agent Usa

### **Exemplo 1: Automação Web Completa**
```python
# O Orchestrator pode coordenar uma sequência de ações web:
# 1. Abrir browser
await orchestrator.call_tool('open_browser', {'headless': False})

# 2. Navegar para site
await orchestrator.call_tool('web_navigate', {'url': 'https://example.com'})

# 3. Preencher formulário
await orchestrator.call_tool('web_type', {
    'selector': '#username', 
    'text': 'diego'
})

# 4. Clicar submit
await orchestrator.call_tool('web_click', {'selector': 'button[type="submit"]'})

# 5. Tirar screenshot do resultado
await orchestrator.call_tool('web_screenshot', {'name': 'login_result'})
```

### **Exemplo 2: Gestão de Agentes**
```python
# O Orchestrator pode descobrir e coordenar outros agentes:
# 1. Buscar agente específico
agents = await orchestrator.call_tool('search_agents', {
    'query': 'calculadora'
})

# 2. Analisar capacidades
capabilities = await orchestrator.call_tool('analyze_agent', {
    'agent_id': agents['result'][0]['id']
})

# 3. Obter detalhes completos
details = await orchestrator.call_tool('get_agent_details', {
    'agent_id': agents['result'][0]['id']
})
```

### **Exemplo 3: Workflow Híbrido**
```python
# O Orchestrator pode combinar web automation + agent management:
# 1. Navegar para página de dados
await orchestrator.call_tool('web_navigate', {'url': 'https://data-site.com'})

# 2. Extrair dados
data = await orchestrator.call_tool('web_get_content', {'selector': '.data-table'})

# 3. Encontrar agente processador
processor = await orchestrator.call_tool('search_agents', {
    'query': 'processamento dados'
})

# 4. Delegar processamento ao agente especializado
# (via A2A communication)
```

## 📊 Verificação de Status

### **system_info** Atualizado
O comando `system_info` agora inclui informações sobre DiegoTools:

```python
info = await session.call_tool('system_info', {})
print(info['diego_tools'])

# Output:
{
    "available": True,
    "path": "/Users/agents/Desktop/codex/claude-code-10x/mcp-run-ts-tools",
    "tools": [
        "web_navigate", "web_screenshot", "web_click", 
        "web_type", "web_get_content", "open_browser",
        "browser_open", "list_agents", "get_agent_details",
        "analyze_agent", "search_agents"
    ]
}
```

## 🔀 Mapeamento de Ferramentas

| **A2A MCP Tool** | **DiegoTools MCP** | **Categoria** |
|------------------|---------------------|---------------|
| `web_navigate` | `puppeteer_navigate` | Puppeteer |
| `web_screenshot` | `puppeteer_screenshot` | Puppeteer |
| `web_click` | `puppeteer_click` | Puppeteer |
| `web_type` | `puppeteer_type` | Puppeteer |
| `web_get_content` | `puppeteer_get_content` | Puppeteer |
| `open_browser` | `open_browser` | Puppeteer |
| `browser_open` | `browser_open_url` | Browser |
| `list_agents` | `agents_list` | Agents |
| `get_agent_details` | `agents_get_details` | Agents |
| `analyze_agent` | `agents_analyze` | Agents |
| `search_agents` | `agents_search` | Agents |

## 🛠️ Configuração e Teste

### **1. Iniciar Sistema A2A com DiegoTools**
```bash
cd /Users/agents/Desktop/codex/agents/a2a_mcp
python start_a2a_mcp.py
```

### **2. Testar Integração**
```python
import asyncio
from a2a_mcp.mcp.client import init_session

async def test_diego_tools():
    async with init_session('localhost', 10100, 'sse') as session:
        # Verificar status das DiegoTools
        info = await session.call_tool('system_info', {})
        print("DiegoTools Status:", info['diego_tools'])
        
        # Testar automação web
        result = await session.call_tool('web_navigate', {
            'url': 'https://httpbin.org/get'
        })
        print("Navigation:", result)
        
        # Testar gestão de agentes
        agents = await session.call_tool('list_agents', {})
        print("Agents:", agents)

asyncio.run(test_diego_tools())
```

### **3. Verificar Logs**
```bash
# Logs do A2A MCP Server
tail -f /var/log/a2a-mcp.log

# Logs do DiegoTools
tail -f /Users/agents/Desktop/codex/claude-code-10x/mcp-run-ts-tools/logs/server.log
```

## 🔧 Troubleshooting

### **DiegoTools Não Disponível**
Se `diego_tools.available = false`:

1. **Verificar Path**:
   ```bash
   ls -la /Users/agents/Desktop/codex/claude-code-10x/mcp-run-ts-tools/
   ```

2. **Verificar Run Script**:
   ```bash
   chmod +x /Users/agents/Desktop/codex/claude-code-10x/mcp-run-ts-tools/run.sh
   ```

3. **Testar DiegoTools Diretamente**:
   ```bash
   cd /Users/agents/Desktop/codex/claude-code-10x/mcp-run-ts-tools
   ./run.sh
   ```

### **Erro de Timeout**
Se há timeouts nas chamadas:

1. **Aumentar Timeout** no bridge:
   ```python
   # Em diego_tools_bridge.py
   timeout=10  # aumentar de 5 para 10 segundos
   ```

2. **Verificar Dependências**:
   ```bash
   cd /Users/agents/Desktop/codex/claude-code-10x/mcp-run-ts-tools
   npm install
   npm run build
   ```

## 💡 Benefícios da Integração

### **1. Orquestração Unificada**
- O Orchestrator Agent agora pode coordenar tanto agentes A2A quanto automação web
- Single point of control para workflows complexos

### **2. Capacidades Expandidas**
- **Antes**: Apenas ferramentas utilitárias (JSON, cálculo, formatação)
- **Agora**: Automação web completa + gestão de agentes

### **3. Flexibilidade**
- Graceful degradation se DiegoTools não estiver disponível
- Ferramentas A2A continuam funcionando independentemente

### **4. Reutilização**
- DiegoTools já testadas e funcionais no Claude Flow
- Aproveitamento de investimento em desenvolvimento

## 🚀 Próximos Passos

### **1. Workflows Avançados**
Criar workflows que combinem:
- Web scraping via Puppeteer
- Processamento via agentes A2A
- Armazenamento em sistemas externos

### **2. Monitoramento**
- Métricas de uso das DiegoTools
- Performance monitoring
- Error tracking

### **3. Extensões**
- Adicionar mais ferramentas conforme necessário
- Integração com outros sistemas MCP
- Suporte a batch operations

---

**🎉 DiegoTools integradas com sucesso ao A2A MCP!**  
**O Orchestrator Agent agora tem poderes de automação web completa!**