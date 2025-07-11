# HelloWorld Agent - A2A Completo

**Agente Hello World com estrutura completa para produção** baseado na migração de `hello_world` + funcionalidades avançadas existentes.

## 🚀 Funcionalidades

### Básicas (migradas de hello_world)
- ✅ **Skills A2A**: `hello_world`, `super_hello_world`
- ✅ **Servidor A2A**: Configuração completa com Starlette
- ✅ **Streaming**: Suporte a streaming de mensagens
- ✅ **Agent Cards**: Públicos e autenticados
- ✅ **Deploy**: Container ready com Containerfile

### Avançadas (existentes em helloworld)
- ✅ **MCP Integration**: Servidor e cliente MCP completos
- ✅ **Google AI**: Integração com Gemini e embeddings
- ✅ **SQLite Database**: Persistência de dados
- ✅ **Multiple Skills**: Conversão de moedas, busca semântica
- ✅ **Places API**: Integração com Google Places

## 📦 Instalação e Uso

### 1. Desenvolvimento Local

```bash
# Instalar dependências
uv sync

# Executar servidor
uv run .

# Testar com cliente
uv run test_client.py
```

### 2. Container Deploy

```bash
# Build container
podman build . -t helloworld-a2a-server

# Run container
podman run -p 9999:9999 helloworld-a2a-server
```

### 3. Validação A2A

```bash
# Em terminal separado
cd samples/python/hosts/cli
uv run . --agent http://localhost:9999
```

## 🛠️ Estrutura do Projeto

```
helloworld/
├── README.md                   # Esta documentação
├── pyproject.toml             # Configuração e dependências
├── uv.lock                    # Lock de dependências
├── Containerfile              # Deploy em container
├── test_client.py             # Cliente de teste completo
├── __init__.py                # Módulo Python
├── __main__.py                # Servidor principal
├── agent_executor.py          # Lógica do agente
├── pedido_client.py           # Cliente MCP
├── agent_cards/               # Cards dinâmicos
├── mcp/                       # Integração MCP
└── __pycache__/               # Cache Python (ignorar)
```

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Google AI API
GOOGLE_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite:///./helloworld.db

# Server
HOST=0.0.0.0
PORT=9999
```

## 🎯 Skills Disponíveis

### Skills Básicas
- **hello_world**: Retorna mensagem simples
- **super_hello_world**: Versão estendida para usuários autenticados

### Skills Avançadas  
- **currency_conversion**: Conversão de moedas
- **semantic_search**: Busca semântica com embeddings
- **places_search**: Busca de lugares via Google Places API

## 🧪 Testes

```bash
# Cliente de teste básico
uv run test_client.py

# Cliente MCP
uv run pedido_client.py

# Teste manual via curl
curl http://localhost:9999/.well-known/agent.json
```

## 📚 Documentação API

### Agent Cards

- **Público**: `/.well-known/agent.json`
- **Autenticado**: `/agent/authenticatedExtendedCard`

### Endpoints

- **Health**: `/health`
- **Skills**: Definidas no Agent Card
- **Streaming**: Suportado via WebSocket

## 🔒 Segurança

⚠️ **Importante**: Este código é para demonstração. Em produção:

- Valide todas as entradas de agentes externos
- Sanitize dados antes de usar em LLMs
- Implemente autenticação adequada
- Trate agentes externos como não-confiáveis

## 🏆 Resultado da Migração

Esta versão combina:
- **Estrutura sólida** de `hello_world` (produção ready)
- **Funcionalidades avançadas** de `helloworld` (MCP, AI, etc.)
- **Melhor dos dois mundos** para desenvolvimento e produção

---
*Migrado automaticamente via sistema A2A - Claude Flow*