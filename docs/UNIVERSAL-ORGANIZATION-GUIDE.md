# 🌍 UNIVERSAL ORGANIZATION GUIDE

## Sistema de Organização Universal para Qualquer Projeto

### ✅ O Que Foi Feito

1. **Criado Universal Organization Guardian**
   - Sistema independente de projeto
   - Detecta automaticamente tipo de projeto
   - Adapta regras dinamicamente
   - Funciona com Node.js, Python, ou qualquer projeto

2. **Removidos Agentes Duplicados**
   - Movidos para `/src/organization-deprecated/`
   - Mantido apenas o sistema universal
   - Simplificado package.json

3. **Testado com mcp-run-ts-tools**
   - Score inicial: 29%
   - Após correções automáticas: 50%
   - Sistema funcionando corretamente

### 📊 Como Funciona

#### Detecção Automática de Projeto
```typescript
- Node.js/TypeScript: Detecta package.json + tsconfig.json
- Python: Detecta requirements.txt, setup.py, pyproject.toml
- Genérico: Aplica regras universais para qualquer projeto
```

#### Regras Universais Aplicadas
1. **Arquivos na Raiz**
   - Máximo recomendado: 15-20 arquivos
   - Permitidos: README, configs principais, LICENSE

2. **Organização de Pastas**
   - `/docs`: Toda documentação .md (exceto README)
   - `/config`: Arquivos .yml, .yaml, .json de configuração
   - `/scripts`: Scripts .sh, .bash, .ps1, .bat
   - `/src`: Código com máximo 5 arquivos soltos

3. **Score de Organização (0-100%)**
   - Localização de Arquivos: 30%
   - Nomenclatura Consistente: 15%
   - Sem Duplicatas: 20%
   - Documentação: 15%
   - Estrutura de Pastas: 20%

### 🚀 Como Usar

#### Comando Simples
```bash
# Organizar projeto atual
npm run organize

# Organizar projeto específico
npm run organize /caminho/para/projeto
```

#### Comando Avançado
```bash
# Modo single (análise única)
npm run organize:universal /caminho/para/projeto single

# Modo continuous (monitoramento)
npm run organize:universal /caminho/para/projeto continuous
```

### 📁 Estrutura Final

```
claude-flow/
├── src/
│   ├── organization/                  # Sistema universal
│   │   ├── universal-organization-guardian.ts
│   │   └── README.md
│   └── organization-deprecated/       # Agentes antigos (não usar)
│       ├── organization-guardian-agent.ts
│       ├── organization-score-agent.ts
│       └── ...
├── scripts/
│   └── organize-project.sh          # Script helper
└── package.json                      # Scripts simplificados
```

### 🔧 Correções Automáticas

O sistema aplica automaticamente:
- ✅ Move arquivos .md para /docs
- ✅ Move configs para /config  
- ✅ Cria pastas necessárias
- ✅ Organiza estrutura básica

### 📈 Exemplo Real: mcp-run-ts-tools

**Antes (29%)**:
- 16 arquivos na raiz (muitos)
- 8 arquivos soltos em src/
- Sem README.md
- Configs espalhados

**Depois (50%)**:
- Movidos: CLAUDE.md → docs/
- Movidos: .improvements-queue.json → config/
- Movidos: improvement-report.json → config/
- Ainda pendente: criar README.md e organizar src/

### 🎯 Próximos Passos

Para melhorar ainda mais o score de um projeto:
1. Criar README.md com descrição
2. Organizar arquivos soltos em src/ em subpastas
3. Consolidar arquivos similares
4. Adicionar documentação em /docs

### 💡 Dica Pro

Execute periodicamente para manter projetos organizados:
```bash
# Verificar organização sem monitoramento
npm run organize /meu/projeto

# Deixar rodando para organização contínua
npm run organize:universal /meu/projeto continuous
```

---
*Sistema Universal de Organização - Funciona com qualquer projeto!*