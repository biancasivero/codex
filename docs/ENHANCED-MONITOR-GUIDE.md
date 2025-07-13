# 📊 Enhanced Monitor - Guia Completo

## 🎯 O que é o Enhanced Monitor?

O **Enhanced Monitor** é um sistema de monitoramento avançado do Claude Flow que combina múltiplas camadas de observabilidade para fornecer visibilidade completa do sistema de agentes.

---

## 🏗️ Arquitetura do Enhanced Monitor

### 1. **Portainer** (Interface Web Principal)
- **Porta**: 9000
- **Função**: Monitoramento visual de containers Docker
- **Acesso**: http://localhost:9000

### 2. **Dashboard Flask** (Analytics Reais)
- **Porta**: 5001
- **Função**: Dashboard com dados reais do Mem0 + Docker
- **Acesso**: http://localhost:5001

### 3. **Agent Log API** (Dados de Execução)
- **Porta**: 3001
- **Função**: API para estatísticas de agentes
- **Acesso**: http://localhost:3001

### 4. **Dashboard Terminal** (Tempo Real)
- **Função**: Monitor em tempo real no terminal
- **Atualização**: A cada 30 segundos

---

## 🚀 Como Usar o Enhanced Monitor

### 1️⃣ **Iniciar Monitoramento Web**
```bash
# Só o Portainer
docker-compose --profile monitor up -d

# Acesse: http://localhost:9000
```

### 2️⃣ **Iniciar Stack Completo com Analytics**
```bash
# Monitor + Analytics + Dashboard
docker-compose --profile full --profile flask --profile monitor up -d

# Interfaces disponíveis:
# - Portainer: http://localhost:9000
# - Dashboard Flask: http://localhost:5001
# - API Analytics: http://localhost:3001
```

### 3️⃣ **Iniciar Dashboard Terminal**
```bash
# Terminal dashboard em tempo real
docker-compose --profile dashboard up -d

# Ou executar diretamente:
docker-compose logs -f dashboard
```

### 4️⃣ **Tudo Ligado** 
```bash
# Monitoramento completo
docker-compose --profile full --profile monitor --profile dashboard --profile flask up -d
```

---

## 🎛️ Funcionalidades do Enhanced Monitor

### 📊 **Portainer (Monitor Web)**
- **Containers**: Status, logs, estatísticas
- **Imagens**: Lista de imagens Docker
- **Volumes**: Gerenciamento de volumes
- **Redes**: Configuração de redes Docker
- **Stacks**: Gerenciamento de docker-compose

### 📈 **Dashboard Flask (Analytics)**
- **Agentes Ativos**: Lista de agentes rodando
- **Estatísticas**: Execuções, taxa de sucesso, duração
- **Logs Reais**: Dados vindos do Mem0
- **Tarefas**: Monitoramento de tarefas em tempo real
- **Pipeline Report**: Relatório completo do pipeline

### 🔧 **Agent Log API (Endpoints)**
```
GET  /health                    - Status do serviço
GET  /api/stats                 - Estatísticas gerais
GET  /api/executions           - Execuções recentes
GET  /api/pipeline-report      - Relatório do pipeline
GET  /api/agent/<nome>         - Detalhes de um agente
GET  /api/docker-agents        - Agentes Docker
GET  /api/tasks                - Tarefas em tempo real
```

### 🖥️ **Dashboard Terminal**
- **Serviços Ativos**: Lista de containers rodando
- **Últimos Commits**: Histórico git
- **Atualização**: Timestamp da última verificação
- **Comandos**: Sugestões de comandos úteis

---

## 🔍 Dados Monitorados

### **Agentes Docker**
- ✅ **Organization Guardian**: Organização de projeto
- ✅ **Agent Log Service**: Análise e relatórios
- ✅ **Portainer**: Monitoramento visual
- ✅ **Dashboard**: Status em tempo real

### **Métricas Coletadas**
- 📊 **Execuções**: Total de execuções por agente
- ✅ **Taxa de Sucesso**: Percentual de sucesso
- ⏱️ **Duração**: Tempo médio de execução
- 🐛 **Erros**: Contagem e detalhes de erros
- 📈 **Tendências**: Análise temporal

### **Integração com Mem0**
- 🧠 **Memória Persistente**: Dados armazenados no Mem0
- 🔄 **Sincronização**: Dados reais em tempo real
- 📝 **Logs**: Histórico completo de execuções

---

## 🛠️ Comandos Úteis

### **Ver Logs**
```bash
# Portainer
docker logs -f portainer

# Dashboard Flask
docker logs -f agent-log-flask

# Agent Log API
docker logs -f agent-log-service

# Dashboard Terminal
docker logs -f claude-flow-dashboard
```

### **Verificar Status**
```bash
# Status de todos os serviços
docker-compose ps

# Status específico do monitor
docker-compose ps | grep -E "(portainer|dashboard|agent-log)"
```

### **Parar Serviços**
```bash
# Parar apenas monitoramento
docker-compose --profile monitor down

# Parar tudo
docker-compose down
```

---

## 🚨 Troubleshooting

### **Problema: Portainer não carrega**
```bash
# Verificar se a porta está livre
netstat -tuln | grep 9000

# Reiniciar Portainer
docker-compose restart portainer
```

### **Problema: Dashboard Flask sem dados**
```bash
# Verificar variável MEM0_API_KEY
echo $MEM0_API_KEY

# Verificar conexão com Mem0
docker logs agent-log-flask | grep "Mem0"
```

### **Problema: Agent Log API não responde**
```bash
# Testar endpoint
curl http://localhost:3001/health

# Verificar logs
docker logs agent-log-service
```

---

## 🎯 Casos de Uso

### **Para Desenvolvedores**
1. **Debug**: Usar Portainer para logs detalhados
2. **Performance**: Dashboard Flask para métricas
3. **Monitoramento**: Terminal dashboard para status rápido

### **Para Operações**
1. **Saúde do Sistema**: Agent Log API
2. **Alertas**: Dashboard Flask com dados reais
3. **Manutenção**: Portainer para gerenciamento

### **Para Análise**
1. **Relatórios**: Pipeline report via API
2. **Tendências**: Dashboard Flask
3. **Histórico**: Dados do Mem0

---

## ⚡ Performance

### **Recursos Utilizados**
- **Portainer**: ~50MB RAM
- **Dashboard Flask**: ~100MB RAM
- **Agent Log API**: ~30MB RAM
- **Dashboard Terminal**: ~10MB RAM

### **Portas Utilizadas**
- **9000**: Portainer
- **5001**: Dashboard Flask
- **3001**: Agent Log API
- **3002**: Mem0 Bridge

---

## 🔐 Segurança

### **Acesso Local**
- Todas as interfaces estão configuradas para acesso local
- Nenhuma exposição externa por padrão

### **Dados Sensíveis**
- Logs não contêm dados sensíveis
- API Keys são mascaradas nos logs

---

## 📚 Recursos Extras

### **Documentação das APIs**
- Todas as APIs têm endpoints `/health`
- Dados em formato JSON padronizado
- CORS habilitado para integração

### **Extensibilidade**
- Fácil adicionar novos agentes
- Configuração via labels Docker
- Integração com sistemas externos

---

## 🎉 Resumo

O **Enhanced Monitor** oferece:
- 🖥️ **4 interfaces diferentes** para diferentes necessidades
- 📊 **Dados reais** do Mem0 + Docker
- ⚡ **Tempo real** com atualizações automáticas
- 🔧 **APIs completas** para integração
- 🎯 **Fácil de usar** e configurar

**Comando rápido para iniciar tudo:**
```bash
docker-compose --profile full --profile monitor --profile dashboard --profile flask up -d
```

**Acesse:**
- Portainer: http://localhost:9000
- Dashboard: http://localhost:5001
- API: http://localhost:3001
- Terminal: `docker logs -f claude-flow-dashboard` 