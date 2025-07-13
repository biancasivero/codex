# ⚡ Comandos Rápidos - HelloWorld Agent

## 🚀 Inicialização Rápida

### Executar o Agente
```bash
cd /Users/agents/Desktop/codex/agents/helloworld
python app.py
```

### Registrar na UI
```bash
curl -X POST "http://localhost:12000/agent/register" \
  -H "Content-Type: application/json" \
  -d '{"params": "http://localhost:9999"}'
```

## 🧪 Testes Rápidos

### Verificar Status
```bash
curl -s "http://localhost:9999/health" | jq '.'
```

### Testar Agent Card
```bash
curl -s "http://localhost:9999/.well-known/agent.json" | jq '.name'
```

### Testar Skills
```bash
# Skill básica
curl -X POST "http://localhost:9999/skills/hello_world" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}' | jq '.response'

# Skill avançada
curl -X POST "http://localhost:9999/skills/super_hello_world" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}' | jq '.response'
```

## 📋 Verificação da UI

### Listar Agentes Registrados
```bash
curl -s -X POST "http://localhost:12000/agent/list" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.result[].name'
```

### Acessar UI
```bash
# Abrir no navegador
open http://localhost:12000
```

## 🔧 Troubleshooting

### Verificar Processos
```bash
# Verificar HelloWorld Agent
lsof -i :9999

# Verificar UI
lsof -i :12000
```

### Parar Processos
```bash
# Parar HelloWorld Agent
pkill -f "python app.py"

# Parar UI
pkill -f "python main.py"
```

### Logs
```bash
# Ver logs em tempo real
tail -f /var/log/system.log | grep python
```

## 🎯 URLs Importantes

- **HelloWorld Agent**: http://localhost:9999
- **Agent Card**: http://localhost:9999/.well-known/agent.json
- **Health Check**: http://localhost:9999/health
- **UI Dashboard**: http://localhost:12000 