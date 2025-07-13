# Integração A2A MCP com UI Mesop

## 🎯 Objetivo

Integrar o sistema A2A MCP com a UI Mesop que já está rodando na porta 12000, criando uma experiência completa de gerenciamento de agentes.

## 🔗 Conexão com a UI Existente

### UI Mesop (Porta 12000)
A UI já está rodando e pode ser acessada em: http://localhost:12000

### Sistema A2A MCP (Portas 10100-10105)
O sistema A2A MCP roda nas portas 10100-10105 com os agentes especializados.

## 📋 Passos para Integração

### 1. Registrar Agentes A2A MCP na UI

#### Orchestrator Agent
```bash
curl -X POST http://localhost:12000/agent/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_card": {
      "name": "A2A MCP Orchestrator",
      "description": "Coordena tarefas de viagem usando múltiplos agentes especializados",
      "url": "http://localhost:10101/",
      "version": "1.0.0",
      "capabilities": {
        "streaming": true,
        "pushNotifications": true
      },
      "skills": [
        {
          "id": "executor",
          "name": "Travel Orchestrator",
          "description": "Planeja e executa viagens completas coordenando múltiplos agentes",
          "tags": ["travel", "orchestration", "planning"],
          "examples": [
            "Planejar viagem para Londres",
            "Reservar voo, hotel e carro para Paris",
            "Organizar viagem de negócios para Nova York"
          ]
        }
      ]
    }
  }'
```

#### Planner Agent
```bash
curl -X POST http://localhost:12000/agent/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_card": {
      "name": "A2A MCP Planner",
      "description": "Quebra requisições de viagem em tarefas executáveis",
      "url": "http://localhost:10102/",
      "version": "1.0.0",
      "capabilities": {
        "streaming": true,
        "pushNotifications": true
      },
      "skills": [
        {
          "id": "planner",
          "name": "Travel Planner",
          "description": "Analisa requisições e cria planos detalhados de viagem",
          "tags": ["planning", "travel", "breakdown"],
          "examples": [
            "Planejar trip para Londres em maio",
            "Criar itinerário de 7 dias para Paris",
            "Organizar viagem de negócios"
          ]
        }
      ]
    }
  }'
```

### 2. Executar Sistema Completo

#### Terminal 1: UI Mesop
```bash
cd ui
A2A_DATABASE_URL="sqlite+aiosqlite:///ui.db" uv run python main.py
```

#### Terminal 2: Sistema A2A MCP
```bash
cd agents/a2a_mcp
export GOOGLE_API_KEY="AIzaSyC9fcFGqMBJZXgmTNFsVP8qWnvqLaEbhE0"
python start_a2a_mcp.py
```

### 3. Teste de Integração

#### Via UI (Recomendado)
1. Acesse: http://localhost:12000
2. Vá para "Agent List" 
3. Veja os agentes A2A MCP registrados
4. Clique em "Test Agent" para enviar uma mensagem
5. Teste com: "Planejar viagem para Londres em junho"

#### Via API Direta
```bash
curl -X POST http://localhost:12000/message/send \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test-conversation",
    "message": "Planejar viagem para Londres em junho",
    "agent_url": "http://localhost:10101/"
  }'
```

## 🎯 Fluxo de Trabalho Integrado

### Cenário: Planejamento de Viagem
1. **Usuário na UI**: Envia "Planejar viagem para Londres"
2. **UI Mesop**: Encaminha para Orchestrator Agent (10101)
3. **Orchestrator**: Coordena com Planner Agent (10102)
4. **Planner**: Quebra em tarefas (voo, hotel, carro)
5. **Orchestrator**: Coordena agentes específicos:
   - Air Ticketing Agent (10103)
   - Hotel Booking Agent (10104)
   - Car Rental Agent (10105)
6. **UI Mesop**: Recebe e exibe resultados em tempo real

### Diagrama de Integração
```
UI Mesop (12000) 
    ↓
Orchestrator (10101)
    ↓
Planner (10102) + MCP Server (10100)
    ↓
Air Ticketing (10103) + Hotel Booking (10104) + Car Rental (10105)
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```bash
# Para UI Mesop
export A2A_DATABASE_URL="sqlite+aiosqlite:///ui.db"

# Para Sistema A2A MCP
export GOOGLE_API_KEY="AIzaSyC9fcFGqMBJZXgmTNFsVP8qWnvqLaEbhE0"
export GOOGLE_PLACES_API_KEY="opcional"
export A2A_LOG_LEVEL="INFO"
```

### Monitoramento Integrado
```bash
# Verificar todas as portas
lsof -i :12000  # UI Mesop
lsof -i :10100  # MCP Server
lsof -i :10101  # Orchestrator
lsof -i :10102  # Planner
lsof -i :10103  # Air Ticketing
lsof -i :10104  # Hotel Booking
lsof -i :10105  # Car Rental
```

## 📊 Recursos Disponíveis

### UI Mesop
- ✅ Chat interface
- ✅ Agent management
- ✅ Task tracking
- ✅ Event monitoring
- ✅ Conversation history

### Sistema A2A MCP
- ✅ Multi-agent coordination
- ✅ Travel planning
- ✅ Real-time streaming
- ✅ MCP registry
- ✅ Specialized agents

## 🎉 Casos de Uso

### 1. Planejamento de Viagem Completa
```
"Planejar viagem de negócios para Londres de 15 a 22 de junho, 
classe executiva, hotel 4 estrelas, carro alugado"
```

### 2. Reserva Específica
```
"Reservar voo São Paulo para Paris em julho, 
classe econômica, 2 passageiros"
```

### 3. Comparação de Opções
```
"Comparar preços de hotéis em Londres para 3 noites em maio"
```

## 🔍 Troubleshooting Integração

### Problema: UI não encontra agentes A2A MCP
```bash
# Verificar se agentes estão registrados
curl http://localhost:12000/agent/list

# Re-registrar se necessário
curl -X POST http://localhost:12000/agent/register -d '{...}'
```

### Problema: Timeout na comunicação
```bash
# Verificar conectividade
curl http://localhost:10101/health
curl http://localhost:10102/health
```

### Problema: Logs não aparecem
```bash
# Habilitar logs detalhados
export A2A_LOG_LEVEL="DEBUG"
```

## 🌟 Benefícios da Integração

1. **Interface Única**: Gerenciar todos os agentes em uma UI
2. **Monitoramento**: Acompanhar tarefas em tempo real
3. **Histórico**: Manter conversas e resultados
4. **Flexibilidade**: Usar agentes individuais ou orquestrados
5. **Escalabilidade**: Fácil adicionar novos agentes

## 🎯 Resultado Final

Com esta integração, você terá:
- **UI Mesop** rodando na porta 12000
- **Sistema A2A MCP** rodando nas portas 10100-10105
- **Comunicação integrada** entre ambos
- **Experiência completa** de gerenciamento de agentes
- **Planejamento de viagem** automatizado e coordenado

**Acesse http://localhost:12000 e teste o sistema completo!** 