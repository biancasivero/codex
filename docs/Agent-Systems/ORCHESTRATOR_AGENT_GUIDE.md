# Guia do Orchestrator Agent - Diferenciação de Comandos

## 🤖 Orchestrator Agent - Comandos e Capacidades

### 📋 **IMPORTANTE: Distinção entre MCP e Agentes**

O Orchestrator Agent precisa distinguir claramente entre:

## 1️⃣ **LISTAR FERRAMENTAS MCP** 
**Comando:** `system_info`
**Propósito:** Ver TODAS as ferramentas disponíveis no sistema A2A MCP
**Retorna:** Lista completa de capacidades do sistema (17 ferramentas totais)

```python
# Para ver FERRAMENTAS MCP disponíveis
await session.call_tool('system_info', {})
```

**Resultado inclui:**
- ✅ Ferramentas A2A nativas (6): generate_unique_id, validate_json, calculate_basic, etc.
- ✅ Ferramentas DiegoTools (11): web_navigate, list_agents, browser_open, etc.
- ✅ Informações do sistema e estatísticas

---

## 2️⃣ **LISTAR AGENTES DISPONÍVEIS**
**Comando:** `list_agents` (via DiegoTools)
**Propósito:** Ver agentes específicos disponíveis no Claude Flow
**Retorna:** Lista de agentes individuais que podem ser delegados

```python
# Para ver AGENTES disponíveis para delegação
await session.call_tool('list_agents', {})
```

**Resultado inclui:**
- 🤖 Agentes específicos: Calculator Agent, Research Agent, etc.
- 📊 Capacidades de cada agente
- 🔧 Ferramentas que cada agente possui

---

## 🔄 **Fluxo de Trabalho do Orchestrator**

### **Cenário 1: "Quais ferramentas você tem?"**
→ Use `system_info` para mostrar capacidades MCP completas

### **Cenário 2: "Quais agentes posso usar?"** 
→ Use `list_agents` para mostrar agentes delegáveis

### **Cenário 3: "Faça X tarefa"**
1. Use `list_agents` → encontrar agente adequado
2. Use `get_agent_details` → verificar capacidades específicas  
3. Delegar tarefa ao agente apropriado

### **Cenário 4: "Abra um site"**
→ Use ferramentas web diretamente: `web_navigate`, `browser_open`

---

## 📚 **Comandos Disponíveis por Categoria**

### 🛠️ **Ferramentas de Sistema (MCP)**
- `system_info` - Ver todas as capacidades do sistema
- `generate_unique_id` - Gerar IDs únicos
- `validate_json` - Validar JSON
- `calculate_basic` - Cálculos básicos

### 🤖 **Gestão de Agentes (DiegoTools)**
- `list_agents` - Listar agentes disponíveis
- `search_agents` - Buscar agentes por critério
- `get_agent_details` - Detalhes de agente específico
- `analyze_agent` - Analisar capacidades do agente

### 🌐 **Automação Web (DiegoTools)**
- `web_navigate` - Navegar com Puppeteer
- `web_screenshot` - Capturar telas
- `web_click` - Clicar elementos
- `web_type` - Digitar texto
- `web_get_content` - Obter conteúdo
- `open_browser` - Abrir browser Puppeteer
- `browser_open` - Abrir browser padrão

---

## ⚠️ **Pontos de Atenção**

1. **Não confunda:** 
   - `system_info` = FERRAMENTAS disponíveis
   - `list_agents` = AGENTES delegáveis

2. **Para coordenação:**
   - Primeiro: `list_agents` → ver quem pode fazer
   - Depois: `get_agent_details` → verificar capacidades  
   - Finalmente: delegar ou usar ferramenta direta

3. **Para automação:**
   - Use ferramentas web diretamente
   - Não precisa delegar para agentes simples

---

## 💡 **Exemplos Práticos**

### Exemplo 1: Usuário pergunta "O que você consegue fazer?"
```
Resposta: "Posso coordenar agentes e automatizar tarefas web. 
Tenho 17 ferramentas MCP disponíveis, incluindo gestão de agentes e automação web."
Use: system_info
```

### Exemplo 2: Usuário pergunta "Que agentes posso usar?"
```
Resposta: "Deixe-me verificar os agentes disponíveis..."
Use: list_agents
```

### Exemplo 3: Usuário pede "Calcule 5+3"
```
Opção A: Use calculate_basic diretamente
Opção B: Use search_agents('calculator') → delegar
```

---

## 🎯 **Resumo para o Orchestrator**

**Quando listar MCP:** Mostrar capacidades do sistema
**Quando listar agentes:** Mostrar opções de delegação
**Objetivo:** Coordenar eficientemente entre ferramentas diretas e delegação de agentes