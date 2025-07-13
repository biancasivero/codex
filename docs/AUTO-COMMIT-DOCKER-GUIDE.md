# 🐳 Guia do Auto-Commit Docker Unificado

## 🎯 O que mudou

### Antes ❌
- `docker-compose.auto-commit.yml` - Configuração principal
- `docker-compose.auto-push.yml` - Configuração duplicada para push
- Funcionalidades separadas e confusas

### Agora ✅
- **Um único arquivo**: `docker-compose.auto-commit.yml`
- Suporta múltiplos modos (SSH, HTTPS, Dev, Multi-projeto)
- Mensagens inteligentes integradas
- Profiles para diferentes cenários

## 🚀 Modos de Uso

### 1. Modo Padrão (SSH) - RECOMENDADO
```bash
docker-compose -f config/docker-compose.auto-commit.yml up -d
```
- Usa chaves SSH para autenticação
- Push automático habilitado
- Mensagens inteligentes ativas

### 2. Modo HTTPS (com Token)
```bash
docker-compose -f config/docker-compose.auto-commit.yml --profile https up -d
```
- Para quem prefere tokens ao invés de SSH
- Configure `GITHUB_TOKEN` no ambiente

### 3. Múltiplos Projetos
```bash
docker-compose -f config/docker-compose.auto-commit.yml --profile multi up -d
```
- Monitora vários projetos simultaneamente
- Cada um com suas configurações

### 4. Modo Desenvolvimento
```bash
docker-compose -f config/docker-compose.auto-commit.yml --profile dev up -d
```
- AUTO_PUSH desabilitado (só commits locais)
- Intervalo maior (10 segundos)
- Ideal para desenvolvimento

### 5. Com Monitoramento (Portainer)
```bash
docker-compose -f config/docker-compose.auto-commit.yml --profile monitor up -d
```
- Adiciona interface web em http://localhost:9000
- Visualize logs e gerencie containers

## 🔧 Variáveis de Configuração

| Variável | Padrão | Descrição |
|----------|---------|-----------|
| `COMMIT_INTERVAL` | 3 | Segundos entre commits |
| `AUTO_PUSH` | true | Push automático após commit |
| `USE_SMART_COMMITS` | true | Mensagens inteligentes (feat, fix, docs, etc) |
| `WATCH_PATH` | /workspace | Diretório a monitorar |
| `GIT_AUTHOR_NAME` | DiegoFornalha | Nome do autor dos commits |
| `GIT_AUTHOR_EMAIL` | diegofornalha@gmail.com | Email do autor |

## 📝 Exemplos de Mensagens Inteligentes

Com `USE_SMART_COMMITS=true`, os commits são gerados assim:

- `feat: adicionar UserController` - Novos arquivos em /src
- `fix: corrigir validação` - Modificações em código
- `docs: atualizar README` - Arquivos .md
- `build: atualizar configurações` - package.json, docker-compose, etc
- `test: adicionar testes` - Arquivos de teste
- `style: ajustar estilos` - CSS/SCSS
- `chore: 3 arquivos modificados` - Mudanças gerais

## 🛠️ Comandos Úteis

### Ver logs
```bash
docker logs -f auto-commit-main
```

### Parar serviço
```bash
docker-compose -f config/docker-compose.auto-commit.yml down
```

### Reconstruir imagem
```bash
docker-compose -f config/docker-compose.auto-commit.yml build
```

### Ver status
```bash
docker ps | grep auto-commit
```

## 🔄 Migração do Sistema Antigo

Se você estava usando os arquivos separados:

1. **Backup feito em**: `/config/backup-compose/`
2. **Arquivo removido**: `docker-compose.auto-push.yml` (funcionalidade integrada)
3. **Novo arquivo**: `docker-compose.auto-commit.yml` com todas as funcionalidades

## 💡 Dicas

1. **Para projetos pessoais**: Use modo SSH padrão
2. **Para CI/CD**: Use modo HTTPS com token
3. **Para desenvolvimento**: Use modo dev (sem push)
4. **Para monitorar múltiplos**: Use profile multi

## 🐛 Troubleshooting

### Container não inicia
```bash
# Ver logs detalhados
docker logs auto-commit-main

# Verificar se já existe outro rodando
docker ps -a | grep auto-commit
```

### Commits não têm mensagens inteligentes
Verifique se `USE_SMART_COMMITS=true` está configurado:
```bash
docker inspect auto-commit-main | grep USE_SMART_COMMITS
```

### Push falha
- Verifique suas chaves SSH ou token
- Confirme que o remote está configurado corretamente
- Use `docker logs` para ver erros específicos

---
*Sistema unificado criado em: ${new Date().toLocaleDateString('pt-BR')}*