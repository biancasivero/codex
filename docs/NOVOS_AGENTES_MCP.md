# 🆕 Novos Agentes MCP Utilitários - Guia Completo

## 🎯 Visão Geral

O sistema A2A MCP foi adaptado para incluir 4 novos agentes especializados que usam as ferramentas MCP utilitárias. Estes agentes são **focados em funcionalidades reutilizáveis** e **não limitados a domínios específicos**.

### ✅ **Agentes Disponíveis:**

1. **Text Processor Agent** (porta 10102) - Processamento de texto
2. **Calculator Agent** (porta 10103) - Cálculos matemáticos
3. **Data Validator Agent** (porta 10104) - Validação de dados
4. **Utility Helper Agent** (porta 10105) - Utilitário geral

## 🛠️ Ferramentas MCP Utilizadas

### **Ferramentas Principais:**
- `format_text` - Formatação de texto (upper, lower, title, etc.)
- `calculate_basic` - Cálculos matemáticos básicos
- `validate_json` - Validação de estruturas JSON
- `generate_unique_id` - Geração de IDs únicos
- `system_info` - Informações do sistema
- `find_agent` - Busca de agentes por descrição

## 📋 Detalhes dos Agentes

### **1. Text Processor Agent**
- **Porta**: 10102
- **Especialidade**: Processamento de texto
- **Ferramentas**: `format_text`, `validate_json`, `generate_unique_id`
- **Agent Card**: `agent_cards/text_processor_agent.json`

#### **Exemplos de Uso:**
```
• "Converta 'hello world' para título"
• "Transforme este texto para maiúscula"
• "Valide este JSON: {'name': 'test'}"
• "Gere um ID único para sessão"
```

#### **Skills:**
- **text_formatting**: Formata texto em diferentes estilos
- **json_validation**: Valida estruturas JSON
- **id_generation**: Gera identificadores únicos

### **2. Calculator Agent**
- **Porta**: 10103
- **Especialidade**: Cálculos matemáticos
- **Ferramentas**: `calculate_basic`, `generate_unique_id`, `validate_json`
- **Agent Card**: `agent_cards/calculator_agent.json`

#### **Exemplos de Uso:**
```
• "Calcule 15 + 25"
• "Qual é 2 elevado a 8?"
• "Divida 100 por 4"
• "Calcule a raiz quadrada de 64"
```

#### **Skills:**
- **basic_calculations**: Operações matemáticas básicas
- **math_analysis**: Análise de operações matemáticas
- **calculation_tracking**: Rastreamento de cálculos

### **3. Data Validator Agent**
- **Porta**: 10104
- **Especialidade**: Validação de dados
- **Ferramentas**: `validate_json`, `format_text`, `generate_unique_id`
- **Agent Card**: `agent_cards/data_validator_agent.json`

#### **Exemplos de Uso:**
```
• "Valide este JSON e corrija erros"
• "Padronize estes dados de texto"
• "Normalize os nomes nesta lista"
• "Verifique a integridade dos dados"
```

#### **Skills:**
- **json_validation**: Validação de estruturas JSON
- **data_formatting**: Formatação de dados
- **data_tracking**: Rastreamento de validações

### **4. Utility Helper Agent**
- **Porta**: 10105
- **Especialidade**: Utilitário geral
- **Ferramentas**: Todas as ferramentas MCP disponíveis
- **Agent Card**: `agent_cards/utility_helper_agent.json`

#### **Exemplos de Uso:**
```
• "Formate este texto e calcule o resultado"
• "Valide este JSON e gere um ID único"
• "Mostre informações do sistema"
• "Ajude-me com formatação de texto e cálculos"
```

#### **Skills:**
- **general_utilities**: Serviços utilitários gerais
- **text_processing**: Processamento de texto
- **math_operations**: Operações matemáticas
- **system_assistance**: Assistência do sistema

## 🚀 Como Usar

### **1. Gerenciador de Agentes**
```bash
# Listar agentes disponíveis
python manage_mcp_agents.py list

# Ver demonstração
python manage_mcp_agents.py demo

# Iniciar um agente específico
python manage_mcp_agents.py start --agent text_processor

# Ver status
python manage_mcp_agents.py status

# Parar um agente
python manage_mcp_agents.py stop --agent text_processor
```

### **2. Iniciar Sistema Completo**
```bash
# Iniciar servidor MCP + todos os agentes
python start_a2a_mcp.py

# Iniciar apenas servidor MCP
python start_a2a_mcp.py --mcp-only

# Iniciar agente específico
python start_a2a_mcp.py --agent text_processor
```

### **3. Iniciar Agente Individual**
```bash
# Text Processor Agent
python src/a2a_mcp/agents/ --agent-card agent_cards/text_processor_agent.json --port 10102

# Calculator Agent  
python src/a2a_mcp/agents/ --agent-card agent_cards/calculator_agent.json --port 10103

# Data Validator Agent
python src/a2a_mcp/agents/ --agent-card agent_cards/data_validator_agent.json --port 10104

# Utility Helper Agent
python src/a2a_mcp/agents/ --agent-card agent_cards/utility_helper_agent.json --port 10105
```

## 🔧 Configuração

### **Portas Utilizadas:**
- **10100** - Servidor MCP (SSE)
- **10101** - Orchestrator Agent
- **10102** - Text Processor Agent
- **10103** - Calculator Agent
- **10104** - Data Validator Agent
- **10105** - Utility Helper Agent

### **Variáveis de Ambiente:**
```bash
# Obrigatória
export GOOGLE_API_KEY="sua_chave_google_aqui"

# Opcional
export A2A_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
```

## 📊 Arquitetura do Sistema

### **Fluxo de Funcionamento:**
1. **Servidor MCP** hospeda as ferramentas utilitárias
2. **Agentes especializados** carregam ferramentas específicas
3. **Usuário** faz requisições via A2A protocol
4. **Agente** usa ferramentas MCP para resolver tarefas
5. **Resposta** é formatada e retornada

### **Integração com Orchestrator:**
```python
# O Orchestrator pode descobrir e usar os novos agentes
query = "Formate este texto e valide JSON"
# → find_agent() encontra Text Processor Agent
# → Delega tarefa via A2A protocol
```

## 🎯 Casos de Uso Práticos

### **1. Processamento de Texto**
```bash
# Exemplo: Normalizar dados de entrada
curl -X POST http://localhost:10102/execute \
  -H "Content-Type: application/json" \
  -d '{"text": "Normalize estes DADOS de texto"}'
```

### **2. Cálculos Matemáticos**
```bash
# Exemplo: Calcular operações complexas
curl -X POST http://localhost:10103/execute \
  -H "Content-Type: application/json" \
  -d '{"operation": "power", "a": 2, "b": 10}'
```

### **3. Validação de Dados**
```bash
# Exemplo: Validar estrutura JSON
curl -X POST http://localhost:10104/execute \
  -H "Content-Type: application/json" \
  -d '{"json": "{\"name\": \"test\", \"valid\": true}"}'
```

### **4. Utilitário Geral**
```bash
# Exemplo: Múltiplas operações
curl -X POST http://localhost:10105/execute \
  -H "Content-Type: application/json" \
  -d '{"tasks": ["format_text", "validate_json", "generate_id"]}'
```

## 🧪 Testes e Validação

### **Teste Individual:**
```bash
# Testar conectividade
python manage_mcp_agents.py test --agent text_processor

# Verificar status
python manage_mcp_agents.py status
```

### **Teste via Cliente MCP:**
```python
import asyncio
from a2a_mcp.mcp.client import init_session

async def test_tools():
    async with init_session('localhost', 10100, 'sse') as session:
        # Testar formatação
        result = await session.call_tool('format_text', {
            'text': 'hello world',
            'format_type': 'title'
        })
        print(f"Formatação: {result}")
        
        # Testar cálculo
        result = await session.call_tool('calculate_basic', {
            'operation': 'add',
            'a': 15,
            'b': 25
        })
        print(f"Cálculo: {result}")

asyncio.run(test_tools())
```

## 🔄 Extensibilidade

### **Criar Novo Agente MCP:**
1. **Criar Agent Card** em `agent_cards/`
2. **Definir Prompt** em `src/a2a_mcp/common/mcp_prompts.py`
3. **Adicionar Configuração** em `a2a_mcp_config.py`
4. **Registrar** em `src/a2a_mcp/agents/__main__.py`

### **Exemplo de Novo Agente:**
```python
# Em mcp_prompts.py
NEW_AGENT_INSTRUCTIONS = """
Você é um especialista em [sua especialidade] que usa ferramentas MCP.
Suas ferramentas incluem: [lista de ferramentas]
"""

# Em a2a_mcp_config.py
NEW_AGENTS = {
    "meu_agente": {
        "name": "Meu Agente",
        "port": 10106,
        "card_file": "agent_cards/meu_agente.json",
        "description": "Descrição do meu agente",
        "tools": ["ferramenta1", "ferramenta2"]
    }
}
```

## 📈 Benefícios dos Novos Agentes

### **1. Reutilização**
- Agentes genéricos aplicáveis a vários cenários
- Ferramentas MCP compartilhadas
- Não limitados a domínios específicos

### **2. Especialização**
- Cada agente focado em uma área específica
- Prompts otimizados para cada especialidade
- Ferramentas filtradas por relevância

### **3. Escalabilidade**
- Fácil adicionar novos agentes
- Sistema modular e extensível
- Configuração centralizada

### **4. Manutenibilidade**
- Código limpo e bem estruturado
- Documentação clara
- Testes automatizados

## 🎉 Comandos Rápidos

### **Início Rápido:**
```bash
# Ver configuração
python start_a2a_mcp.py --config

# Listar agentes
python manage_mcp_agents.py list

# Iniciar sistema completo
python start_a2a_mcp.py

# Testar agente específico
python manage_mcp_agents.py start --agent utility_helper
```

### **Desenvolvimento:**
```bash
# Criar novo agente
cp agent_cards/utility_helper_agent.json agent_cards/meu_agente.json
# Editar e configurar...

# Testar novo agente
python src/a2a_mcp/agents/ --agent-card agent_cards/meu_agente.json --port 10106
```

## 📞 Endpoints

### **Servidor MCP:**
- `http://localhost:10100/sse` - Server-Sent Events
- `http://localhost:10100/tools` - Lista de ferramentas

### **Agentes A2A:**
- `http://localhost:10101/` - Orchestrator Agent
- `http://localhost:10102/` - Text Processor Agent
- `http://localhost:10103/` - Calculator Agent
- `http://localhost:10104/` - Data Validator Agent
- `http://localhost:10105/` - Utility Helper Agent

---

**Sistema A2A MCP com novos agentes utilitários especializados! 🚀**

### **Próximos Passos:**
1. Teste os agentes individualmente
2. Integre com o Orchestrator
3. Crie novos agentes específicos para suas necessidades
4. Desenvolva ferramentas MCP customizadas 