# Claude Code - A2A Bridge Server via MCP Tools

## 🎯 **Visão Geral**

O Claude Code oferece acesso direto ao A2A Bridge Server da Smithery através de ferramentas MCP (Model Context Protocol). Esta integração permite controle manual e direto sobre o registro de agentes, envio de mensagens e gerenciamento de tarefas no ecossistema A2A global.

## 🔧 **Instalação e Configuração**

### **1. Instalação do A2A Bridge Server**

```bash
# Comando de instalação no Claude Code
claude mcp add --transport http a-2-a-bridge-server \
  "https://server.smithery.ai/@GongRzhe/A2A-MCP-Server/mcp?api_key=8f573867-52c3-46bb-993e-fb65291459b2&profile=naughty-echidna-jd9SWG"
```

### **2. Verificação da Instalação**

```bash
# Listar servidores MCP instalados
claude mcp list

# Verificar detalhes do servidor
claude mcp get a-2-a-bridge-server
```

**Resultado esperado:**
```
a-2-a-bridge-server: https://server.smithery.ai/@GongRzhe/A2A-MCP-Server/mcp... (HTTP)
```

## 🛠️ **Ferramentas MCP Disponíveis**

### **1. mcp__a-2-a-bridge-server__register_agent**

**Função:** Registra um novo agente no A2A Bridge Server global

**Parâmetros:**
- `url` (string): URL pública do agente a ser registrado

**Exemplo de uso:**
```javascript
mcp__a-2-a-bridge-server__register_agent({
  "url": "https://my-public-domain.com/agent"
})
```

**Requisitos:**
- ✅ Agent Card disponível em `/.well-known/agent.json`
- ✅ URL deve ser publicamente acessível
- ✅ Agente deve implementar protocolo A2A

### **2. mcp__a-2-a-bridge-server__list_agents**

**Função:** Lista todos os agentes registrados no bridge

**Parâmetros:** Nenhum

**Exemplo de uso:**
```javascript
mcp__a-2-a-bridge-server__list_agents()
```

**Resposta típica:**
```json
{
  "agents": [
    {
      "id": "currency-agent",
      "url": "http://localhost:10000/",
      "description": "Helps with exchange rates for currencies"
    },
    {
      "id": "reimbursement-agent", 
      "url": "http://localhost:10002/",
      "description": "Handles reimbursement process for employees"
    }
  ]
}
```

### **3. mcp__a-2-a-bridge-server__unregister_agent**

**Função:** Remove um agente do bridge

**Parâmetros:**
- `url` (string): URL do agente a ser removido

**Exemplo de uso:**
```javascript
mcp__a-2-a-bridge-server__unregister_agent({
  "url": "https://my-domain.com/agent"
})
```

### **4. mcp__a-2-a-bridge-server__send_message**

**Função:** Envia mensagem para um agente através do bridge

**Parâmetros:**
- `agent_url` (string): URL do agente destino
- `message` (string): Mensagem a ser enviada
- `session_id` (string, opcional): ID da sessão para conversas multi-turn

**Exemplo de uso:**
```javascript
mcp__a-2-a-bridge-server__send_message({
  "agent_url": "http://localhost:10000/",
  "message": "Convert 100 USD to EUR",
  "session_id": "session-123"
})
```

### **5. mcp__a-2-a-bridge-server__get_task_result**

**Função:** Recupera resultado de uma tarefa executada

**Parâmetros:**
- `task_id` (string): ID da tarefa
- `history_length` (number, opcional): Número de itens do histórico

**Exemplo de uso:**
```javascript
mcp__a-2-a-bridge-server__get_task_result({
  "task_id": "task-456",
  "history_length": 10
})
```

### **6. mcp__a-2-a-bridge-server__cancel_task**

**Função:** Cancela uma tarefa em execução

**Parâmetros:**
- `task_id` (string): ID da tarefa a ser cancelada

**Exemplo de uso:**
```javascript
mcp__a-2-a-bridge-server__cancel_task({
  "task_id": "task-789"
})
```

### **7. mcp__a-2-a-bridge-server__send_message_stream**

**Função:** Envia mensagem com resposta em streaming

**Parâmetros:**
- `agent_url` (string): URL do agente destino
- `message` (string): Mensagem a ser enviada
- `session_id` (string, opcional): ID da sessão

**Exemplo de uso:**
```javascript
mcp__a-2-a-bridge-server__send_message_stream({
  "agent_url": "http://localhost:10000/",
  "message": "Explain currency conversion process",
  "session_id": "stream-session-001"
})
```

## 🔄 **Fluxo de Trabalho Típico**

### **1. Descoberta de Agentes**
```javascript
// 1. Listar agentes disponíveis
const agents = await mcp__a-2-a-bridge-server__list_agents();

// 2. Escolher agente apropriado
const currencyAgent = agents.find(a => a.description.includes("currency"));
```

### **2. Comunicação com Agente**
```javascript
// 3. Enviar mensagem
const response = await mcp__a-2-a-bridge-server__send_message({
  "agent_url": currencyAgent.url,
  "message": "Convert 500 EUR to USD"
});

// 4. Obter resultado
const result = await mcp__a-2-a-bridge-server__get_task_result({
  "task_id": response.task_id
});
```

### **3. Registro de Novo Agente**
```javascript
// 5. Registrar seu próprio agente (se público)
await mcp__a-2-a-bridge-server__register_agent({
  "url": "https://my-public-agent.herokuapp.com/"
});
```

## ⚡ **Vantagens do Acesso Direto via MCP**

### **✅ Controle Granular**
- Acesso direto a todas as funcionalidades
- Controle manual sobre registro/desregistro
- Debugging e monitoramento detalhado

### **✅ Flexibilidade**
- Uso programático ou manual
- Integração com workflows personalizados
- Testes e experimentação facilitados

### **✅ Transparência**
- Visibilidade completa das operações
- Logs detalhados de cada chamada
- Controle de sessões e task IDs

## 🚨 **Limitações e Considerações**

### **🔒 Conectividade**
- Agentes devem estar publicamente acessíveis
- URLs `localhost` não funcionam através do bridge
- Necessário tunnel público (ngrok, etc.) para agentes locais

### **⚠️ Dependências**
- Requer conexão com internet
- Dependente da disponibilidade do servidor Smithery
- Rate limits podem aplicar

### **🛡️ Segurança**
- URLs públicos expostos globalmente
- Considere autenticação nos agentes
- Monitore uso não autorizado

## 📖 **Exemplos Práticos**

### **Exemplo 1: Conversor de Moedas**
```javascript
// Descobrir agente de moedas
const agents = await mcp__a-2-a-bridge-server__list_agents();
const currencyAgent = agents.find(a => a.id === "currency-agent");

// Converter moeda
const conversion = await mcp__a-2-a-bridge-server__send_message({
  "agent_url": currencyAgent.url,
  "message": "Convert 1000 BRL to USD"
});

console.log("Task ID:", conversion.task_id);

// Aguardar e obter resultado
setTimeout(async () => {
  const result = await mcp__a-2-a-bridge-server__get_task_result({
    "task_id": conversion.task_id
  });
  console.log("Conversion result:", result);
}, 3000);
```

### **Exemplo 2: Workflow de Reembolso**
```javascript
// Workflow completo de reembolso
async function processReimbursement(amount, purpose) {
  const agents = await mcp__a-2-a-bridge-server__list_agents();
  const reimbursementAgent = agents.find(a => a.id === "reimbursement-agent");
  
  const request = await mcp__a-2-a-bridge-server__send_message({
    "agent_url": reimbursementAgent.url,
    "message": `Process reimbursement for $${amount} - ${purpose}`,
    "session_id": `reimbursement-${Date.now()}`
  });
  
  return request.task_id;
}

// Usar função
const taskId = await processReimbursement(150.00, "Business lunch with client");
```

## 🎯 **Conclusão**

O acesso ao A2A Bridge Server via MCP Tools no Claude Code oferece **controle direto e flexível** sobre o ecossistema A2A global. É ideal para:

- 🔧 **Desenvolvimento e testes** de integrações A2A
- 🎛️ **Controle manual** de agentes e tarefas
- 🔍 **Debugging** de comunicações entre agentes
- ⚡ **Workflows personalizados** e automações específicas

Esta abordagem complementa perfeitamente a orquestração automática do Claude Flow, oferecendo o melhor dos dois mundos: automação quando necessário e controle manual quando desejado.