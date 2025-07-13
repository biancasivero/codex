# GUARDIAN-SISTEMA-COMPLETO

## 🛡️ Organization Guardian - Sistema Autônomo de Organização

### Como Funciona

O Guardian é um agente autônomo que mantém seu projeto sempre em 100% de organização:

1. **Monitoramento Contínuo** - Detecta mudanças em tempo real
2. **Score em Tempo Real** - Calcula score de organização (0-100%)
3. **Correções Automáticas** - Aplica fixes sem intervenção manual
4. **Relatórios Detalhados** - Gera documentação do progresso

### Componentes do Sistema

```
Organization Guardian
├── Score Agent (calcula pontuação)
├── Monitor Agent (observa mudanças)
└── Guardian Agent (coordena tudo)
```

### Score de Organização (100 pontos)

| Categoria | Peso | Descrição |
|-----------|------|-----------|
| **Localização** | 30% | Arquivos nos lugares certos |
| **Nomenclatura** | 20% | Padrões de nomes corretos |
| **Sem Duplicatas** | 20% | Nenhum arquivo duplicado |
| **Documentação** | 15% | Docs completa e organizada |
| **Estrutura** | 15% | Pastas bem estruturadas |

### Estrutura Ideal do Projeto

```
claude-flow/
├── src/
│   ├── agents/        # Todos os agentes
│   ├── mcp/          # Integração MCP
│   ├── core/         # Módulos principais
│   ├── organization/ # Sistema de organização
│   ├── utils/        # Utilitários
│   ├── tests/        # Testes
│   └── index.ts      # Entry point
│
├── docs/             # Documentação (MAIÚSCULAS)
│   ├── GUARDIAN-STATUS.md
│   ├── ORGANIZATION-SCORE.md
│   └── *.MD
│
├── config/           # Todos os docker-compose
├── scripts/          # Scripts bash
├── examples/         # Exemplos de uso
│
├── README.md         # Principal
├── package.json      # Dependências
└── tsconfig.json     # Config TypeScript
```

### Como Executar

#### 1. Local (Desenvolvimento)
```bash
npm run guardian
```

#### 2. Docker (Produção)
```bash
npm run docker:guardian
```

#### 3. PM2 (Background)
```bash
./scripts/start-guardian.sh
# Escolher opção 2
```

### Comandos Úteis

```bash
# Ver score atual
cat docs/ORGANIZATION-SCORE.md

# Ver status do Guardian
cat docs/GUARDIAN-STATUS.md

# Ver tarefas pendentes
cat docs/ORGANIZATION-TODOS.md

# Logs do Docker
npm run docker:guardian:logs

# Parar Guardian
npm run docker:guardian:stop
```

### Correções Automáticas

O Guardian corrige automaticamente:

✅ **Arquivos no lugar errado**
- Move .md para /docs
- Organiza .ts em subpastas
- Move configs para /config

✅ **Nomenclatura incorreta**
- Docs em MAIÚSCULAS-COM-HÍFENS
- Adiciona prefixos temáticos
- Padroniza sufixos de status

✅ **Estrutura de pastas**
- Cria pastas faltantes
- Organiza por tipo/função

❌ **Requer ação manual**
- Consolidar duplicatas
- Criar documentação faltante
- Resolver conflitos complexos

### Configurações

```typescript
{
  checkInterval: 60000,      // Verificar a cada 1 min
  targetScore: 100,          // Meta sempre 100%
  autoFix: true,             // Correções automáticas
  workDelay: 5000,           // 5s antes de processar
  maxHistorySize: 100        // Histórico de ações
}
```

### Integração com MCP

O Guardian usa MCP desktop-commander para:
- `move_file` - Mover arquivos
- `create_directory` - Criar pastas
- `edit_block` - Corrigir imports
- `read_file` - Analisar conteúdo

### Status Atual do Projeto

- **Score**: 82% 🟡
- **Próximo objetivo**: 100%
- **Ações pendentes**: 
  - Consolidar 12 arquivos de organização
  - Decidir sobre package-lock.json

### Benefícios

1. **Zero manutenção** - Trabalha sozinho
2. **Sempre organizado** - Meta de 100%
3. **Documentação automática** - Relatórios atualizados
4. **Histórico completo** - Todas as ações registradas
5. **Correções inteligentes** - Preserva funcionalidade

### Próximos Passos

Para alcançar 100%:
1. Consolidar arquivos de organização duplicados
2. Manter Guardian rodando continuamente
3. Monitorar relatórios de progresso

```bash
# Executar Guardian agora
npm run guardian
```

O Guardian continuará trabalhando até alcançar e manter 100% de organização!