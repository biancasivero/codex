# 🚀 DiegoTools MCP

MCP Server com apenas **3 ferramentas essenciais**: `agents`, `browser` e `puppeteer`.

## ✨ Características

- **✅ Leve e rápido**: Apenas dependências essenciais
- **✅ Fácil manutenção**: Código simplificado sem complexidade desnecessária  
- **✅ 3 tools principais**: Funcionalidades focadas e específicas

## 🛠️ Tools Disponíveis

### 1. **Puppeteer Tools**
- `puppeteer_navigate` - Navegar para URLs
- `puppeteer_screenshot` - Capturar screenshots

### 2. **Browser Tools**
- `browser_open_url` - Abrir URLs no navegador padrão

### 3. **Agents Tools**
- `agents_list` - Listar agentes disponíveis

## 🚀 Instalação e Uso

```bash
# Instalar dependências
npm install

# Compilar TypeScript
npm run build

# Iniciar servidor MCP
npm start
```

## 🔧 Configuração

O servidor usa **stdio transport** e está pronto para integração com Claude Desktop ou outros clientes MCP.

### Exemplo de configuração no Claude Desktop:

```json
{
  "mcpServers": {
    "diego-tools": {
      "command": "node",
      "args": ["/caminho/para/build/basic-server.js"]
    }
  }
}
```

## ✅ Status

- **Compilação**: ✅ Sem erros TypeScript
- **Servidor**: ✅ Iniciando corretamente
- **Tools**: ✅ 3 tools funcionais
- **Dependências**: ✅ Limpas e otimizadas
