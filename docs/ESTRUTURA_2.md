# HelloWorld Agent - Implementação Experimental e Avançada

## Visão Geral

O `helloworld` é um **agente experimental com recursos avançados** que demonstra integração com MCP (Model Context Protocol), múltiplas skills complexas e capacidades de IA. Focado em funcionalidades avançadas em vez de infraestrutura de produção.

## Componentes Principais

### 1. **__main__.py** - Servidor A2A Avançado
- **Função**: Servidor com múltiplas skills complexas
- **Características**:
  - 3 skills principais: hello_world, super_hello_world, convert_currency
  - Configuração de cards públicos e estendidos
  - Integração com sistema de skills dinâmico

```python
# Skills disponíveis:
- hello_world: Básica
- super_hello_world: Estendida
- convert_currency: Conversão de moedas com regex
```

### 2. **agent_executor.py** - Executor Multifeatures
- **Função**: Implementa lógica complexa para múltiplas skills
- **Características**:
  - **Conversão de moedas**: Parsing com regex, taxas simuladas
  - **Integração MCP**: Busca e comunicação com outros agentes
  - **Processamento de linguagem natural**: Análise de requests
  - **Tratamento de erros**: Respostas apropriadas para falhas

### 3. **mcp/server.py** - Servidor MCP Completo
- **Função**: Servidor MCP com IA e embeddings
- **Características**:
  - **Google Generative AI**: Integração com Gemini
  - **Embeddings**: Busca semântica de agentes
  - **SQLite**: Banco de dados para travel agency
  - **Google Places API**: Integração com serviços externos
  - **Pandas**: Processamento de dados avançado

### 4. **mcp/client.py** - Cliente MCP Avançado
- **Função**: Cliente MCP com múltiplos transportes
- **Características**:
  - **Dual Transport**: SSE e STDIO
  - **Sessões Gerenciadas**: Context managers
  - **Múltiplas Tools**: find_agent, search_flights, search_hotels
  - **Query Database**: Execução de SQL no SQLite
  - **Logging Avançado**: Debug detalhado

### 5. **agent_cards/** - Cards Dinâmicos
- **Função**: Definição de capacidades em JSON
- **Características**:
  - **Card Público**: Skills básicas
  - **Card Estendido**: Skills premium + conversão de moedas
  - **Versionamento**: Diferentes versões para diferentes níveis

### 6. **pedido_client.py** - Cliente Específico
- **Função**: Cliente focado em teste de MCP
- **Características**:
  - Teste específico da skill `find_and_greet_agent`
  - Configuração manual de AgentCard
  - Integração com httpx

## Recursos Avançados

### ✅ **Integração MCP Completa**
- Servidor MCP com Google AI
- Cliente MCP com dual transport
- Embeddings semânticos
- Busca de agentes distribuídos

### ✅ **Skills Inteligentes**
- Conversão de moedas com regex
- Processamento de linguagem natural
- Comunicação inter-agentes
- Respostas contextuais

### ✅ **Integração com APIs Externas**
- Google Generative AI (Gemini)
- Google Places API
- Sistema de embeddings
- SQLite para persistência

### ✅ **Recursos de IA**
- Busca semântica com embeddings
- Processamento de queries naturais
- Análise de contexto
- Respostas dinâmicas

## Como Usar

### 1. **Configurar Ambiente**
```bash
export GOOGLE_API_KEY="sua-chave-aqui"
export GOOGLE_PLACES_API_KEY="sua-chave-places"
```

### 2. **Iniciar o Servidor**
```bash
cd helloworld
python __main__.py
```

### 3. **Testar MCP**
```bash
python pedido_client.py
```

### 4. **Testar Servidor MCP**
```bash
cd mcp
python server.py --transport stdio
```

## Vantagens desta Implementação

1. **Recursos Avançados**: MCP, IA, embeddings
2. **Integração Externa**: Google AI, Places API
3. **Skills Complexas**: Conversão de moedas, busca semântica
4. **Experimentação**: Prova de conceito para recursos avançados
5. **Flexibilidade**: Múltiplos transportes e configurações
6. **Inovação**: Demonstra capacidades cutting-edge

## Limitações

- **Sem Infraestrutura**: Não possui README, Containerfile, pyproject.toml
- **Sem Testes**: Não possui suite de testes completa
- **Dependências Externas**: Requer APIs do Google
- **Configuração Manual**: Requer setup manual das chaves
- **Experimental**: Código em estado de prova de conceito

## O que Falta (comparado ao hello_world)

### ❌ **Infraestrutura de Produção**
- README.md com documentação
- Containerfile para deploy
- pyproject.toml com dependências
- uv.lock para reprodutibilidade
- test_client.py completo

### ❌ **Qualidade de Código**
- Documentação inline
- Tratamento de erros robusto
- Logging padronizado
- Estrutura de projeto organizada

### ❌ **Deploy Ready**
- Configuração de container
- Variáveis de ambiente padronizadas
- Scripts de inicialização
- Documentação de setup

## Ideal Para

- **Pesquisa**: Explorar recursos avançados de MCP
- **Prototipagem**: Testar integração com IA
- **Experimentação**: Validar conceitos complexos
- **Desenvolvimento**: Base para features avançadas

## Próximos Passos

Para tornar esta implementação production-ready, seria necessário:

1. **Adicionar Infraestrutura**: README, Containerfile, pyproject.toml
2. **Melhorar Documentação**: Comentários e exemplos
3. **Adicionar Testes**: Suite completa de testes
4. **Padronizar Configuração**: Variáveis de ambiente
5. **Otimizar Performance**: Cache, connection pooling
6. **Adicionar Monitoramento**: Logs estruturados, métricas