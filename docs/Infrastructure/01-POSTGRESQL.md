# 🗄️ Planejamento: Migração de Conversas para PostgreSQL

## 📋 Situação Atual

### Sistema de Armazenamento Híbrido
- **PostgreSQL** (`flowagents` database): Apenas diagramas
- **SQLite** (`travel_agency.db`): Embeddings e dados dos agentes
- **Memória** (`InMemoryFakeAgentManager`): Conversas e mensagens (temporárias)

### Funcionalidades Desejadas
- ✅ **Persistência**: Conversas salvas permanentemente
- ✅ **Histórico**: Recuperar conversas anteriores
- ✅ **Escalabilidade**: Suporte a múltiplos usuários
- ✅ **Backup**: Dados seguros e recuperáveis
- ✅ **Busca**: Pesquisar em conversas históricas

## 🏗️ Arquitetura Proposta

### Estrutura do Banco de Dados

```sql
-- Tabela de Conversas
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL DEFAULT '',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB -- Para extensibilidade
);

-- Tabela de Mensagens
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    parts JSONB, -- Para diferentes tipos de conteúdo
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Tabela de Tarefas
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL, -- 'pending', 'in_progress', 'completed'
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Tabela de Eventos
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    actor VARCHAR(255) NOT NULL DEFAULT '',
    content JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    event_type VARCHAR(100) NOT NULL
);

-- Índices para performance
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at DESC);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX idx_tasks_conversation_id ON tasks(conversation_id);
CREATE INDEX idx_events_conversation_id ON events(conversation_id);
CREATE INDEX idx_events_timestamp ON events(timestamp DESC);
```

### Alterações no Código

#### 1. Gerenciador de Banco de Dados
```python
# service/database/postgresql_manager.py
import asyncio
import asyncpg
from typing import List, Optional
from service.types import Conversation, Message, Task, Event

class PostgreSQLManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None
    
    async def initialize(self):
        self.pool = await asyncpg.create_pool(self.database_url)
    
    async def create_conversation(self, name: str = "") -> Conversation:
        # Implementar criação de conversa
        pass
    
    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        # Implementar recuperação de conversa
        pass
    
    async def save_message(self, message: Message) -> Message:
        # Implementar salvamento de mensagem
        pass
    
    async def get_messages(self, conversation_id: str) -> List[Message]:
        # Implementar recuperação de mensagens
        pass
```

#### 2. Substituição do InMemoryManager
```python
# service/server/postgresql_application_manager.py
from service.database.postgresql_manager import PostgreSQLManager
from service.server.application_manager import ApplicationManager

class PostgreSQLApplicationManager(ApplicationManager):
    def __init__(self, database_url: str):
        self.db_manager = PostgreSQLManager(database_url)
    
    async def initialize(self):
        await self.db_manager.initialize()
    
    def create_conversation(self) -> Conversation:
        # Implementar usando PostgreSQL
        pass
    
    def send_message(self, conversation_id: str, message: Message) -> Message:
        # Implementar usando PostgreSQL
        pass
```

## 📅 Cronograma de Implementação

### Fase 1: Preparação (1-2 dias)
- [ ] **Configurar dependências PostgreSQL**
  - Adicionar `asyncpg` ao requirements.txt
  - Configurar variáveis de ambiente
  - Documentar configuração

### Fase 2: Estrutura do Banco (2-3 dias)
- [ ] **Criar scripts de migração**
  - Script de criação das tabelas
  - Script de inserção de dados iniciais
  - Script de rollback
- [ ] **Implementar PostgreSQLManager**
  - Conexão com banco
  - Operações CRUD básicas
  - Tratamento de erros

### Fase 3: Integração (3-4 dias)
- [ ] **Substituir InMemoryManager**
  - Implementar PostgreSQLApplicationManager
  - Migrar funcionalidades existentes
  - Manter compatibilidade com API atual

### Fase 4: Testes e Validação (2-3 dias)
- [ ] **Testes unitários**
  - Testar operações de banco
  - Testar fluxo completo
  - Testar performance

### Fase 5: Migração de Dados (1 dia)
- [ ] **Estratégia de migração**
  - Backup dos dados atuais
  - Migração incremental
  - Verificação de integridade

## 🔧 Configuração Necessária

### Variáveis de Ambiente
```bash
# .env
DATABASE_URL=postgresql://username:password@localhost:5432/flowagents
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=flowagents
POSTGRES_USER=agents
POSTGRES_PASSWORD=your_password
```

### Dependências
```txt
# requirements.txt
asyncpg>=0.29.0
psycopg2-binary>=2.9.0
alembic>=1.8.0  # Para migrações
```

## 🚀 Estratégia de Migração

### Abordagem Incremental
1. **Implementação paralela**: Manter sistema atual funcionando
2. **Migração gradual**: Implementar por módulos
3. **Testes contínuos**: Validar cada etapa
4. **Rollback planejado**: Possibilidade de reverter mudanças

### Compatibilidade
- Manter interface atual (`ApplicationManager`)
- Implementar flag para escolher storage (memória vs PostgreSQL)
- Período de transição com ambos sistemas

## 📊 Benefícios Esperados

### Performance
- **Consultas otimizadas**: Índices adequados
- **Paginação**: Carregar mensagens sob demanda
- **Cache**: Implementar cache para dados frequentes

### Funcionalidades Avançadas
- **Busca textual**: Full-text search em mensagens
- **Estatísticas**: Métricas de uso e performance
- **Backup automático**: Rotinas de backup
- **Auditoria**: Log de mudanças

## ⚠️ Considerações e Riscos

### Riscos Técnicos
- **Complexidade**: Aumento na complexidade do sistema
- **Performance**: Possível impacto na velocidade
- **Dependências**: Nova dependência externa

### Mitigações
- **Testes abrangentes**: Cobertura de testes > 90%
- **Monitoramento**: Métricas de performance
- **Documentação**: Guias de troubleshooting

## 🔄 Plano de Rollback

### Critérios para Rollback
- Performance degradada > 50%
- Bugs críticos não resolvidos em 24h
- Perda de dados

### Processo de Rollback
1. Parar sistema atual
2. Restaurar código anterior
3. Restaurar dados do backup
4. Verificar integridade
5. Reiniciar sistema

## 📈 Métricas de Sucesso

### KPIs Técnicos
- **Tempo de resposta**: < 200ms para operações básicas
- **Disponibilidade**: > 99.9%
- **Integridade**: 0 perda de dados

### KPIs de Negócio
- **Histórico preservado**: 100% das conversas salvas
- **Busca eficiente**: Resultados em < 1s
- **Escalabilidade**: Suporte a 10x mais usuários

---

## 📝 Próximos Passos

1. **Revisão técnica**: Validar arquitetura proposta
2. **Aprovação**: Confirmar cronograma e recursos
3. **Configuração**: Preparar ambiente de desenvolvimento
4. **Implementação**: Iniciar Fase 1

---

*Documento criado em: 2025-01-09*
*Autor: Sistema de Planejamento*
*Versão: 1.0*