# 📝 Auto-Commit com Conventional Commits

## 🎯 O que foi implementado

O sistema de auto-commit agora gera mensagens inteligentes seguindo o padrão [Conventional Commits](https://www.conventionalcommits.org/):

### Antes ❌
```
Auto-commit: 12/06/2025, 15:22:41
```

### Depois ✅
```
feat: adicionar UserController, AuthService
fix: corrigir validação de email
docs: atualizar README e CONTRIBUTING
build: atualizar configurações
test: atualizar testes
style: ajustar estilos
chore: 3 arquivos modificados, 1 arquivo removido
```

## 🤖 Como funciona

### 1. Análise Automática
O sistema analisa automaticamente:
- **Novos arquivos** em `/src/` → `feat:` (nova funcionalidade)
- **Modificações** em código → `fix:` (correção)
- **Arquivos .md** → `docs:` (documentação)
- **Arquivos de config** → `build:` (configuração)
- **Arquivos de teste** → `test:` (testes)
- **Arquivos CSS/SCSS** → `style:` (estilos)
- **Outros** → `chore:` (tarefas gerais)

### 2. Mensagens Descritivas
- Lista arquivos principais modificados
- Agrupa múltiplas mudanças
- Mantém mensagens concisas
- Usa português para consistência

## 🚀 Como usar

### Executar diretamente
```bash
npm run auto-commit
```

### Com Docker
```bash
docker-compose -f config/docker-compose.auto-commit.yml up
```

## 📋 Tipos de Commit

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `feat` | Nova funcionalidade | `feat: adicionar autenticação JWT` |
| `fix` | Correção de bug | `fix: corrigir validação de senha` |
| `docs` | Documentação | `docs: atualizar README` |
| `style` | Formatação, estilos | `style: ajustar espaçamento` |
| `refactor` | Refatoração de código | `refactor: simplificar lógica de login` |
| `test` | Testes | `test: adicionar testes unitários` |
| `build` | Build, dependências | `build: atualizar webpack config` |
| `chore` | Tarefas gerais | `chore: atualizar .gitignore` |
| `perf` | Performance | `perf: otimizar queries` |
| `ci` | Integração contínua | `ci: configurar GitHub Actions` |

## 🔧 Configuração

### Variáveis de ambiente (Docker)
```env
COMMIT_INTERVAL=3      # Segundos antes do commit
AUTO_PUSH=true         # Push automático
WATCH_PATH=/app        # Diretório a monitorar
```

## 💡 Benefícios

1. **Histórico mais claro**: Fácil entender o que foi feito
2. **Busca facilitada**: `git log --grep="^feat"` para ver features
3. **Changelog automático**: Ferramentas podem gerar changelog
4. **CI/CD melhorado**: Triggers baseados em tipo de commit
5. **Review mais rápido**: Revisores entendem mudanças rapidamente

## 📝 Exemplos de mensagens geradas

```bash
# Adicionando novo arquivo
feat: adicionar UserController

# Modificando múltiplos arquivos
fix: corrigir auth e validation

# Atualizando documentação
docs: atualizar README e API

# Mudanças genéricas
chore: 5 arquivos modificados, 2 arquivos removidos

# Configurações
build: atualizar package.json e tsconfig

# Testes
test: adicionar testes para UserService
```

## 🎯 Próximos passos

- [ ] Adicionar escopo: `feat(auth): adicionar login`
- [ ] Análise de conteúdo para mensagens mais precisas
- [ ] Configuração de padrões personalizados
- [ ] Integração com issue tracker