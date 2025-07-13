# 🛠️ Ferramentas MCP no Sistema A2A MCP - Versão Simplificada

## 🎯 Entendendo MCP Tools vs Agentes

### **MCP Tools = Ferramentas/Utilitários**
- **Não são agentes independentes**
- **Executam tarefas específicas** (formatar, calcular, validar)
- **Não têm contexto próprio** - são chamadas sob demanda
- **Exemplo**: `find_agent()`, `generate_unique_id()`, `validate_json()`

### **Agentes A2A = Sistemas Inteligentes**
- **Usam ferramentas MCP** para resolver problemas
- **Têm contexto e memória** de conversas
- **Podem coordenar múltiplas ferramentas**
- **Exemplo**: `Orchestrator Agent`

## 📋 Ferramentas MCP Disponíveis

### **1. Ferramentas de Descoberta**
```python
@mcp.tool(name='find_agent')
def find_agent(query: str) -> str:
    # Encontra agente mais relevante usando embeddings
    # Entrada: "Coordenar uma tarefa complexa"
    # Saída: Agent card do orchestrator agent
```

### **2. Ferramentas de Utilidade**
```python
@mcp.tool(name='generate_unique_id')
def generate_unique_id(prefix: str = "task") -> dict:
    # Gera IDs únicos para tarefas, sessões, etc.
    # Entrada: "session"
    # Saída: {'id': 'session_abc123', 'timestamp': '...'}
```

```python
@mcp.tool(name='validate_json')
def validate_json(json_string: str) -> dict:
    # Valida se uma string é JSON válido
    # Entrada: '{"valid": true}'
    # Saída: {'valid': True, 'parsed': {...}}
```

```python
@mcp.tool(name='format_text')
def format_text(text: str, format_type: str = "upper") -> dict:
    # Formata texto de diferentes maneiras
    # Entrada: "hello world", "title"
    # Saída: {'formatted': 'Hello World', 'applied_format': 'title'}
```

```python
@mcp.tool(name='calculate_basic')
def calculate_basic(operation: str, a: float, b: float = 0) -> dict:
    # Realiza cálculos básicos
    # Entrada: "add", 5, 3
    # Saída: {'result': 8, 'operation': 'add'}
```

### **3. Ferramentas de Sistema**
```python
@mcp.tool(name='system_info')
def system_info() -> dict:
    # Informações sobre o sistema A2A MCP
    # Saída: {'system_name': 'A2A MCP System', 'available_tools': [...]}
```

## 🔧 Ferramentas Removidas

### **❌ Ferramentas Removidas do Sistema**
- **`query_places_data`** - Busca dados do Google Places API
- **`query_travel_data`** - Consulta banco de dados SQLite de viagens

### **🎯 Razão da Remoção**
Essas ferramentas foram removidas para:
1. **Simplificar o sistema** e focar em ferramentas utilitárias
2. **Reduzir dependências** externas (Google Places API, SQLite)
3. **Melhorar manutenibilidade** do código
4. **Focar em ferramentas reutilizáveis** para diferentes cenários

## 🚀 Como Usar as Ferramentas MCP

### **1. Via Agentes A2A**
Os agentes automaticamente usam as ferramentas MCP quando necessário:
```python
# Um agente pode usar as ferramentas durante sua execução
# Por exemplo, o Orchestrator Agent pode usar find_agent() para descobrir outros agentes
```

### **2. Via Cliente MCP Direto**
```python
# Teste das ferramentas via cliente MCP
from a2a_mcp.mcp.client import init_session
import asyncio

async def test_tools():
    async with init_session('localhost', 10100, 'sse') as session:
        # Testar geração de ID único
        result = await session.call_tool('generate_unique_id', {'prefix': 'test'})
        print(f"ID gerado: {result}")
        
        # Testar validação JSON
        result = await session.call_tool('validate_json', {'json_string': '{"valid": true}'})
        print(f"Validação: {result}")
        
        # Testar formatação de texto
        result = await session.call_tool('format_text', {'text': 'hello world', 'format_type': 'title'})
        print(f"Formatação: {result}")

asyncio.run(test_tools())
```

### **3. Via API REST (se configurado)**
```bash
# Exemplo de uso via curl (se servidor REST estiver configurado)
curl -X POST http://localhost:10100/tools/generate_unique_id \
  -H "Content-Type: application/json" \
  -d '{"prefix": "task"}'
```

## 🔧 Como Adicionar Novas Ferramentas

### **1. Adicionar Ferramenta ao Servidor MCP**
```python
# Em agents/a2a_mcp/src/a2a_mcp/mcp/server.py
@mcp.tool(name='nova_ferramenta')
def nova_ferramenta(parametro: str) -> dict:
    """Descrição da nova ferramenta"""
    logger.info(f'Executando nova ferramenta com: {parametro}')
    
    # Sua implementação aqui
    resultado = f"Processado: {parametro}"
    
    return {
        'input': parametro,
        'output': resultado,
        'timestamp': datetime.datetime.now().isoformat()
    }
```

### **2. Atualizar Lista de Ferramentas**
```python
# Atualizar system_info() para incluir nova ferramenta
'available_tools': [
    'find_agent',
    'generate_unique_id',
    'system_info',
    'validate_json',
    'format_text',
    'calculate_basic',
    'nova_ferramenta'  # Adicionar aqui
]
```

### **3. Testar Nova Ferramenta**
```bash
# Iniciar sistema
python start_a2a_mcp.py

# Testar via cliente
python -c "
import asyncio
from a2a_mcp.mcp.client import init_session

async def test():
    async with init_session('localhost', 10100, 'sse') as session:
        result = await session.call_tool('nova_ferramenta', {'parametro': 'teste'})
        print(result)

asyncio.run(test())
"
```

## 📊 Exemplos de Uso das Ferramentas

### **1. Formatação de Texto**
```python
# Diferentes tipos de formatação
formats = ['upper', 'lower', 'title', 'capitalize', 'reverse', 'all']

for format_type in formats:
    result = await session.call_tool('format_text', {
        'text': 'hello world',
        'format_type': format_type
    })
    print(f"{format_type}: {result['formatted']}")
```

### **2. Cálculos Básicos**
```python
# Diferentes operações matemáticas
operations = [
    ('add', 5, 3),
    ('multiply', 4, 7),
    ('power', 2, 8),
    ('sqrt', 16, 0)
]

for op, a, b in operations:
    result = await session.call_tool('calculate_basic', {
        'operation': op,
        'a': a,
        'b': b
    })
    print(f"{op}({a}, {b}) = {result['result']}")
```

### **3. Validação e Geração de IDs**
```python
# Gerar ID único
id_result = await session.call_tool('generate_unique_id', {'prefix': 'user'})
user_id = id_result['id']

# Validar JSON
json_data = '{"user_id": "' + user_id + '", "active": true}'
validation = await session.call_tool('validate_json', {'json_string': json_data})

print(f"ID: {user_id}")
print(f"JSON válido: {validation['valid']}")
```

## 💡 Benefícios da Abordagem Simplificada

### **1. Menos Dependências**
- Não precisa do Google Places API
- Não precisa do SQLite
- Foco em ferramentas Python nativas

### **2. Mais Reutilizáveis**
- Ferramentas genéricas que servem para vários cenários
- Não limitadas a domínio específico (viagens)
- Podem ser usadas por qualquer agente

### **3. Mais Testáveis**
- Funcionalidades isoladas e bem definidas
- Fácil criar testes unitários
- Menos pontos de falha

### **4. Mais Extensíveis**
- Estrutura clara para adicionar novas ferramentas
- Padrão consistente para implementação
- Documentação clara dos parâmetros

## 🔄 Migração de Ferramentas Específicas

### **Se Precisar das Ferramentas Removidas**
```python
# Para casos específicos, você pode adicionar ferramentas customizadas:

@mcp.tool(name='custom_database_query')
def custom_database_query(query: str, database_path: str) -> dict:
    """Consulta customizada para banco de dados específico"""
    # Implementação específica para seu caso de uso
    pass

@mcp.tool(name='custom_api_call')
def custom_api_call(endpoint: str, params: dict) -> dict:
    """Chamada customizada para API externa"""
    # Implementação específica para sua API
    pass
```

## 📞 Suporte e Próximos Passos

### **1. Testar o Sistema**
```bash
# Iniciar sistema simplificado
python start_a2a_mcp.py

# Verificar ferramentas disponíveis
python start_a2a_mcp.py --config
```

### **2. Explorar Ferramentas**
```bash
# Testar via cliente
python -c "
import asyncio
from a2a_mcp.mcp.client import init_session

async def explore():
    async with init_session('localhost', 10100, 'sse') as session:
        # Ver informações do sistema
        info = await session.call_tool('system_info', {})
        print(info)

asyncio.run(explore())
"
```

### **3. Adicionar Suas Próprias Ferramentas**
- Use os exemplos acima como base
- Foque em ferramentas reutilizáveis
- Documente bem os parâmetros

---

**Sistema A2A MCP agora focado em ferramentas utilitárias essenciais! 🎉** 