# AGENTE-ORGANIZADOR-AUTONOMO

## Visão Geral

O Agente Monitor de Organização é uma versão autônoma do agente organizador que:
- **Monitora continuamente** criação e modificação de arquivos .md
- **Move automaticamente** documentos para /docs
- **Consolida documentos similares** (>70% similaridade)
- **Aplica padrões de nomenclatura** automaticamente
- **Gera relatórios de status** em /docs/ORGANIZATION-STATUS.md

## Como Funciona

### 1. Monitoramento em Tempo Real
```typescript
// Usa chokidar para observar mudanças
watcher.on('add', (file) => processMarkdownFile(file))
watcher.on('change', (file) => processMarkdownFile(file))
```

### 2. Processamento Inteligente
Quando um arquivo .md é detectado:

1. **Análise de Conteúdo**
   - Verifica se é documentação (tem títulos, >200 caracteres)
   - Ignora READMEs da raiz
   
2. **Validação de Nome**
   - Sugere nome seguindo padrões
   - MAIÚSCULAS para docs finais
   - Prefixos temáticos (DOCKER-, AGENTE-, etc)

3. **Detecção de Similaridade**
   - Compara com docs existentes em /docs
   - Usa análise de conteúdo, títulos e estrutura
   
4. **Ação Automática**
   - Se similar >70%: consolida com existente
   - Se não: move com nome apropriado
   - Cria backups antes de consolidar

## Uso

### Execução Local
```bash
npm run agent:org-monitor
```

### Docker
```bash
npm run docker:org-agent
```

### Demonstração
```bash
npx tsx examples/demo-org-monitor.ts
```

## Exemplo de Fluxo

### 1. Arquivo Criado
```
novo-tutorial.md → Detectado pelo agente
```

### 2. Análise
- Nome inadequado → Sugestão: DOCKER-TUTORIAL-FINAL.md
- Conteúdo similar a DOCKER-SETUP-COMPLETO.md (85%)

### 3. Consolidação
- Backup: .backups/auto-consolidation/2024-12-06/novo-tutorial.md
- Conteúdo único adicionado a DOCKER-SETUP-COMPLETO.md
- Arquivo original removido

### 4. Relatório
ORGANIZATION-STATUS.md atualizado com:
- Estatísticas de consolidação
- Documentos processados
- Ações realizadas

## Configuração

### Variáveis
```typescript
{
  processDelay: 10000,      // 10s após última mudança
  autoMove: true,           // Mover para /docs automaticamente
  autoConsolidate: true,    // Consolidar similares
  minSimilarity: 0.7        // 70% para consolidar
}
```

### Padrões Ignorados
- node_modules/
- .git/
- dist/
- build/

## Estrutura de Backups
```
.backups/
└── auto-consolidation/
    └── 2024-12-06/
        ├── 1234567890-arquivo-original.md
        └── 1234567891-outro-arquivo.md
```

## Benefícios

1. **Zero Intervenção Manual**
   - Organização acontece automaticamente
   - Sem necessidade de comandos

2. **Preservação de Conteúdo**
   - Backups automáticos
   - Consolidação inteligente preserva conteúdo único

3. **Documentação Sempre Organizada**
   - /docs mantido limpo e estruturado
   - Nomenclatura consistente
   - Sem duplicações

4. **Rastreabilidade**
   - Logs detalhados de todas ações
   - Relatório de status sempre atualizado
   - Histórico em backups

## Logs do Agente

```
👁️  Modo de monitoramento autônomo ativado
🔍 Iniciando monitoramento de arquivos...
📝 Novo arquivo: tutorial-docker.md
⚡ Processando 1 eventos...
📋 Analisando: tutorial-docker.md
   ✓ Arquivo deve estar em /docs
   ✓ Renomeando para: DOCKER-TUTORIAL-FINAL.md
   ✓ Documento similar encontrado: DOCKER-SETUP-COMPLETO.md
   ✓ Similaridade: 78%
🔗 Consolidando tutorial-docker.md com DOCKER-SETUP-COMPLETO.md
✅ Consolidação completa!
```