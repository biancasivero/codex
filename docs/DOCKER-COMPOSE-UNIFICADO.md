# 🐳 Docker Compose Unificado - Claude Flow

## ✅ O que foi feito

### Antes (6 arquivos separados) ❌
- `docker-compose.yml` - Configuração base
- `docker-compose.auto-commit.yml` - Auto-commit
- `docker-compose.auto-push.yml` - Duplicado do auto-commit
- `docker-compose.organization.yml` - Organização básica
- `docker-compose.auto-organization.yml` - Auto-fix
- `docker-compose.guardian.yml` - Guardian
- `docker-compose.org-agent.yml` - Agente organização

### Agora (1 arquivo único) ✅
- `docker-compose.yml` - **TUDO UNIFICADO!**

## 🎯 Benefícios da Unificação

1. **Sem sobreposição**: Um único arquivo evita duplicação
2. **Mais simples**: Fácil entender o que cada serviço faz
3. **Profiles**: Use apenas o que precisa
4. **Manutenção**: Um arquivo para atualizar

## 🚀 Como Usar

### 1️⃣ Auto-commit (mais comum)
```bash
cd /Users/agents/Desktop/claude-code-10x/claude-flow/config
docker-compose up -d auto-commit
```

### 2️⃣ Guardian (organização 100%)
```bash
docker-compose --profile guardian up -d
```

### 3️⃣ Stack Completo (auto-commit + guardian)
```bash
docker-compose --profile full up -d
```

### 4️⃣ Desenvolvimento (sem push)
```bash
docker-compose --profile dev up -d
```

### 5️⃣ Análise de Organização
```bash
docker-compose --profile analyze up
```

### 6️⃣ Com Monitoramento Web
```bash
docker-compose --profile monitor up -d
# Acesse: http://localhost:9000
```

### 7️⃣ Tudo Ligado
```bash
docker-compose --profile full --profile monitor --profile dashboard up -d
```

## 📊 Serviços Disponíveis

| Serviço | Descrição | Profile | Container |
|---------|-----------|---------|-----------|
| `auto-commit` | Commits inteligentes com push | default | `auto-commit-main` |
| `guardian` | Mantém organização em 100% | guardian, full | `organization-guardian` |
| `full-stack` | Auto-commit + Guardian juntos | full | `claude-flow-full` |
| `dev` | Modo desenvolvimento (sem push) | dev | `auto-commit-dev` |
| `analyze` | Análise única de organização | analyze | `organization-analyze` |
| `auto-commit-https` | Com token GitHub | https | `auto-commit-https` |
| `portainer` | Interface web de monitoramento | monitor, full | `portainer` |
| `dashboard` | Dashboard no terminal | dashboard | `claude-flow-dashboard` |

## 🔧 Variáveis de Ambiente

Todas configuráveis via `.env`:

```env
# Git
GIT_AUTHOR_NAME=SeuNome
GIT_AUTHOR_EMAIL=seu@email.com
GITHUB_TOKEN=ghp_xxx

# Auto-commit
COMMIT_INTERVAL=3
AUTO_PUSH=true
USE_SMART_COMMITS=true

# Organization
TARGET_SCORE=100
AUTO_FIX=true
CHECK_INTERVAL=60000
```

## 🛠️ Comandos Úteis

```bash
# Ver logs
docker-compose logs -f auto-commit

# Status
docker-compose ps

# Parar tudo
docker-compose down

# Reconstruir
docker-compose build

# Limpar tudo (cuidado!)
docker-compose down -v
```

## 📁 Arquivos Removidos

Os seguintes arquivos foram unificados e removidos:
- ❌ docker-compose.auto-commit.yml
- ❌ docker-compose.auto-push.yml
- ❌ docker-compose.organization.yml
- ❌ docker-compose.auto-organization.yml
- ❌ docker-compose.guardian.yml
- ❌ docker-compose.org-agent.yml

**Backup disponível em**: `/config/backup-compose/`

## 💡 Migração

Se você estava usando os arquivos antigos:

| Comando Antigo | Comando Novo |
|----------------|--------------|
| `docker-compose -f docker-compose.auto-commit.yml up` | `docker-compose up -d auto-commit` |
| `docker-compose -f docker-compose.guardian.yml up` | `docker-compose --profile guardian up -d` |
| `docker-compose -f docker-compose.organization.yml up` | `docker-compose --profile analyze up` |

## 🎉 Resultado

- **1 arquivo** ao invés de 6
- **Zero sobreposição** de funcionalidades
- **Mais fácil** de entender e manter
- **Profiles** para controle fino
- **Documentação** integrada no arquivo

---
*Unificação realizada em: ${new Date().toLocaleDateString('pt-BR')}*