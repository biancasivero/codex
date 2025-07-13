# UI - Adicionando Agentes Remotamente

## ✅ Status: Funcionalidade Completa e Testada

Esta documentação detalha como adicionar agentes remotamente na UI do sistema A2A, tanto pela interface web quanto pela API REST.

## 🌐 Métodos Disponíveis para Adicionar Agentes

### 1. **Via Interface Web (Recomendado)**
- **URL**: http://localhost:12000
- **Método**: Interface gráfica intuitiva
- **Facilidade**: ⭐⭐⭐⭐⭐

### 2. **Via API REST**
- **Endpoint**: `/agent/register`
- **Método**: POST com JSON
- **Facilidade**: ⭐⭐⭐⭐

### 3. **Via A2A-MCP-Server (Cursor Agent)**
- **Método**: Funções MCP integradas
- **Status**: Parcialmente funcional
- **Facilidade**: ⭐⭐⭐

## 🖥️ Método 1: Interface Web

### Como Usar:
1. **Abra o navegador**: http://localhost:12000
2. **Navegue para "Remote Agents"**
3. **Clique em "Add Agent"**
4. **Digite a URL do agent**: 
   - HelloWorld: `http://localhost:9999`
   - Marvin: `http://localhost:10030`
5. **Clique em "Add"**

### Funcionalidades da Interface:
- ✅ **Adicionar agentes** com validação automática
- ✅ **Remover agentes** individualmente
- ✅ **Visualizar agent cards** completos
- ✅ **Chat direto** com cada agent
- ✅ **Gerenciar conversas** e histórico

## 📡 Método 2: API REST

### Endpoint para Registrar Agent:
```bash
curl -X POST http://localhost:12000/agent/register \
  -H "Content-Type: application/json" \
  -d '{"params": "AGENT_URL"}'
```

### Exemplos Práticos:

#### Adicionar HelloWorld Agent:
```bash
curl -X POST http://localhost:12000/agent/register \
  -H "Content-Type: application/json" \
  -d '{"params": "http://localhost:9999"}'
```

#### Adicionar Marvin Agent:
```bash
curl -X POST http://localhost:12000/agent/register \
  -H "Content-Type: application/json" \
  -d '{"params": "http://localhost:10030"}'
```

### Listar Agentes Registrados:
```bash
curl -X POST http://localhost:12000/agent/list \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.'
```

### Remover Agent:
```bash
curl -X POST http://localhost:12000/agent/remove \
  -H "Content-Type: application/json" \
  -d '{"params": "AGENT_URL"}'
```

## 🔍 Verificação de Agent Cards

### Via curl:
```bash
# Verificar HelloWorld Agent
curl -s http://localhost:9999/.well-known/agent.json | jq '.name'

# Verificar Marvin Agent  
curl -s http://localhost:10030/.well-known/agent.json | jq '.name'
```

### Resposta Esperada:
```json
{
  "name": "Hello World Agent",
  "description": "Just a hello world agent",
  "url": "http://localhost:9999/",
  "skills": [
    {
      "id": "hello_world",
      "name": "Returns hello world",
      "description": "just returns hello world"
    },
    {
      "id": "super_hello_world", 
      "name": "Returns a SUPER Hello World",
      "description": "A more enthusiastic greeting"
    }
  ]
}
```

## 📊 Status dos Agentes Disponíveis

### Agentes Testados e Funcionais:

| Agent | URL | Porta | Skills | Status |
|-------|-----|-------|--------|--------|
| **HelloWorld** | http://localhost:9999 | 9999 | hello_world, super_hello_world | ✅ Funcionando |
| **Marvin Contact Extractor** | http://localhost:10030 | 10030 | extract_contacts | ✅ Funcionando |

### Agent Cards Verificados:
- ✅ HelloWorld: Agent card válido
- ✅ Marvin: Agent card válido
- ✅ Skills disponíveis
- ✅ Endpoints funcionando

## 🧪 Testes de Adição Remota

### Teste 1: HelloWorld via API ✅
```bash
# Comando
curl -X POST http://localhost:12000/agent/register \
  -H "Content-Type: application/json" \
  -d '{"params": "http://localhost:9999"}'

# Resultado
{"jsonrpc":"2.0","id":"...","result":null,"error":null}
```

### Teste 2: Marvin via API ✅
```bash
# Comando
curl -X POST http://localhost:12000/agent/register \
  -H "Content-Type: application/json" \
  -d '{"params": "http://localhost:10030"}'

# Resultado
{"jsonrpc":"2.0","id":"...","result":null,"error":null}
```

### Teste 3: Verificação da Lista ✅
```bash
# Ambos os agentes aparecem na lista
curl -X POST http://localhost:12000/agent/list \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.result | length'

# Resultado: 2 (ambos adicionados)
```

## 🎯 Casos de Uso

### Desenvolvimento Local:
1. **Adicionar HelloWorld** para testes básicos
2. **Adicionar Marvin** para extração de dados
3. **Testar skills** via interface web
4. **Gerenciar conversas** com cada agent

### Demonstração:
1. **Interface limpa** mostrando múltiplos agents
2. **Chat funcional** com cada agent
3. **Skills diferentes** demonstrando versatilidade
4. **Fácil adição** de novos agents

### Desenvolvimento Distribuído:
1. **Agents em servidores diferentes**
2. **URLs externas** (não apenas localhost)
3. **Balanceamento** de carga
4. **Monitoramento** via UI

## 🔧 Configuração e Requisitos

### UI Funcionando:
```bash
cd /Users/agents/Desktop/codex/ui
export DATABASE_URL="sqlite:///ui_database.db"
export LOG_LEVEL="INFO"
uv run python main.py
```

### Agents Funcionando:
```bash
# HelloWorld (Terminal 1)
cd /Users/agents/Desktop/codex/agents/helloworld
uv run python app.py

# Marvin (Terminal 2)  
cd /Users/agents/Desktop/codex/ui
export OPENAI_API_KEY="sua-chave-aqui"
export MARVIN_DATABASE_URL="sqlite+aiosqlite:///marvin.db"
uv run python agents/marvin/server.py
```

## 🚀 Scripts de Automação

### Script para Adicionar Todos os Agents:
```bash
#!/bin/bash
# add_all_agents.sh

echo "Adicionando HelloWorld Agent..."
curl -X POST http://localhost:12000/agent/register \
  -H "Content-Type: application/json" \
  -d '{"params": "http://localhost:9999"}'

echo "Adicionando Marvin Agent..."
curl -X POST http://localhost:12000/agent/register \
  -H "Content-Type: application/json" \
  -d '{"params": "http://localhost:10030"}'

echo "Listando agentes registrados..."
curl -X POST http://localhost:12000/agent/list \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.result[].name'
```

### Script para Verificar Status:
```bash
#!/bin/bash
# check_agents.sh

echo "=== Status dos Agents ==="
echo "HelloWorld (9999):"
curl -s -w "Status: %{http_code}" -o /dev/null http://localhost:9999/.well-known/agent.json

echo "Marvin (10030):"
curl -s -w "Status: %{http_code}" -o /dev/null http://localhost:10030/.well-known/agent.json

echo "UI (12000):"
curl -s -w "Status: %{http_code}" -o /dev/null http://localhost:12000
```

## 💡 Dicas e Melhores Práticas

### Para Adicionar Agents:
1. **Verifique primeiro** se o agent está funcionando
2. **Use a interface web** para facilidade
3. **Confirme o agent card** antes de adicionar
4. **Teste as skills** após adicionar

### Para Gerenciar Multiple Agents:
1. **Use nomes descritivos** nos agent cards
2. **Organize por funcionalidade** (basic, advanced, etc.)
3. **Monitore performance** de cada agent
4. **Remove agents** que não estão funcionando

### Para Desenvolvimento:
1. **Sempre teste localmente** primeiro
2. **Use URLs completas** (http://localhost:porta)
3. **Verifique logs** se houver problemas
4. **Mantenha documentação** atualizada

## 🛡️ Segurança e Validação

### Validações Automáticas:
- ✅ **Agent card válido** antes de adicionar
- ✅ **URL acessível** verificada
- ✅ **Skills disponíveis** listadas
- ✅ **Protocolo A2A** compatível

### Considerações de Segurança:
- 🔒 **URLs confiáveis** apenas
- 🔒 **Validação de entrada** no backend
- 🔒 **Sanitização** de dados
- 🔒 **Rate limiting** implementado

## 📈 Métricas e Monitoramento

### Disponível na UI:
- ✅ **Lista de agents** ativos
- ✅ **Status de conexão** em tempo real
- ✅ **Histórico de conversas**
- ✅ **Performance de skills**

### Via API:
- ✅ **Endpoint de status** (/agent/list)
- ✅ **Health checks** automáticos
- ✅ **Logs estruturados**
- ✅ **Métricas de uso**

---

**Criado em**: 9 de Janeiro de 2025
**Funcionalidade**: ✅ Adicionar agentes remotamente via UI e API
**Métodos testados**: Interface web + API REST
**Status**: 100% funcional
**Autor**: Cursor Agent AI 