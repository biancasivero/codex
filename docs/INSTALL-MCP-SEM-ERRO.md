# 🚀 Instalação do DiegoTools MCP (Sem Erros)

## Pré-requisitos
- Node.js 18+ instalado
- Claude CLI instalado (`npm install -g @anthropic-ai/claude-code`)
- Estar no diretório correto: `/Users/agents/Desktop/claude-code-10x/mcp-run-ts-tools`

## Comando de Instalação Completo

### 1️⃣ Comando Único (Copie e Cole)
```bash
cd /Users/agents/Desktop/claude-code-10x/mcp-run-ts-tools && \
rm -rf build node_modules && \
npm install && \
npm run build && \
claude mcp remove DiegoTools -s user 2>/dev/null; \
claude mcp add DiegoTools /Users/agents/Desktop/claude-code-10x/mcp-run-ts-tools/run.sh \
  --env GITHUB_TOKEN=seu_token_aqui \
  --env MEM0_API_KEY=sua_chave_aqui \
  --env MEM0_BASE_URL=https://api.mem0.ai \
  -s user
```

### 2️⃣ Passo a Passo (Se preferir)

1. **Navegue até o diretório correto:**
   ```bash
   cd /Users/agents/Desktop/claude-code-10x/mcp-run-ts-tools
   ```

2. **Limpe builds anteriores:**
   ```bash
   rm -rf build node_modules
   ```

3. **Instale dependências e compile:**
   ```bash
   npm install && npm run build
   ```

4. **Remova instalação anterior (se existir):**
   ```bash
   claude mcp remove DiegoTools -s user
   ```

5. **Adicione o DiegoTools:**
   ```bash
   claude mcp add DiegoTools /Users/agents/Desktop/claude-code-10x/mcp-run-ts-tools/run.sh \
     --env GITHUB_TOKEN=seu_token_aqui \
     --env MEM0_API_KEY=sua_chave_aqui \
     --env MEM0_BASE_URL=https://api.mem0.ai \
     -s user
   ```

## ⚠️ Importante: Tokens de Segurança

**NUNCA** compartilhe seus tokens reais! Substitua:
- `seu_token_aqui` → Seu token GitHub real
- `sua_chave_aqui` → Sua chave Mem0 real

## 🔍 Verificar Instalação

Após instalar, verifique:
```bash
claude mcp list
```

Deve mostrar:
```
DiegoTools - /Users/agents/Desktop/claude-code-10x/mcp-run-ts-tools/run.sh
```

## 🐛 Solução de Problemas

### Erro: "command not found: claude"
```bash
npm install -g @anthropic-ai/claude-code
```

### Erro: "build failed"
```bash
# Instale TypeScript globalmente
npm install -g typescript
# Tente novamente
npm run build
```

### Erro de permissão
```bash
# Use sudo se necessário
sudo npm install -g @anthropic-ai/claude-code
```

## ✅ Teste Final

Crie um novo terminal e execute:
```bash
npx ts-node src/cli.ts agent create gitManager
```

Se o agente for criado sem erros de "stack overflow", a instalação foi bem-sucedida!