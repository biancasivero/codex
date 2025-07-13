# DiegoTools API Documentation

## 🌐 Puppeteer Tools

### puppeteer_navigate

Navega para uma URL específica.

**Parâmetros:**
```typescript
{
  url: string;  // URL completa para navegar (obrigatório)
}
```

**Resposta:**
```typescript
{
  content: [{
    type: "text",
    text: "Navegação concluída para: <url>\nTítulo: <título da página>"
  }]
}
```

**Exemplo:**
```javascript
await puppeteer_navigate({ 
  url: "https://github.com" 
});
```

---

### puppeteer_screenshot

Captura screenshot da página atual.

**Parâmetros:**
```typescript
{
  path: string;        // Caminho para salvar o screenshot (obrigatório)
  fullPage?: boolean;  // Capturar página inteira (padrão: false)
}
```

**Resposta:**
```typescript
{
  content: [{
    type: "text",
    text: "Screenshot salvo em: <caminho>\nTamanho: <largura>x<altura> pixels"
  }]
}
```

**Exemplo:**
```javascript
await puppeteer_screenshot({ 
  path: "/tmp/screenshot.png",
  fullPage: true 
});
```

---

### puppeteer_click

Clica em um elemento usando seletor CSS.

**Parâmetros:**
```typescript
{
  selector: string;  // Seletor CSS do elemento (obrigatório)
}
```

**Resposta:**
```typescript
{
  content: [{
    type: "text",
    text: "Click realizado no elemento: <seletor>"
  }]
}
```

**Exemplo:**
```javascript
await puppeteer_click({ 
  selector: "#login-button" 
});
```

---

### puppeteer_type

Digita texto em um campo de input.

**Parâmetros:**
```typescript
{
  selector: string;  // Seletor CSS do campo (obrigatório)
  text: string;      // Texto para digitar (obrigatório)
}
```

**Resposta:**
```typescript
{
  content: [{
    type: "text",
    text: "Texto digitado no elemento: <seletor>"
  }]
}
```

**Exemplo:**
```javascript
await puppeteer_type({ 
  selector: "#email",
  text: "usuario@exemplo.com" 
});
```

---

### puppeteer_get_content

Obtém o conteúdo HTML da página atual.

**Parâmetros:**
Nenhum parâmetro necessário.

**Resposta:**
```typescript
{
  content: [{
    type: "text",
    text: "<html completo da página>"
  }]
}
```

**Exemplo:**
```javascript
const html = await puppeteer_get_content();
```

---


---

## 🖥️ Browser Tools

### browser_open_url

Abre uma URL no navegador padrão do sistema.

**Parâmetros:**
```typescript
{
  url: string;  // URL para abrir (obrigatório)
}
```

**Resposta:**
```typescript
{
  content: [{
    type: "text",
    text: "URL aberta no navegador padrão: <url>"
  }]
}
```

**Exemplo:**
```javascript
await browser_open_url({
  url: "https://github.com/diegofornalha/claude-code-10x"
});
```

---

## 🤖 Claude CLI Tools

### claude_execute

Executa o Claude Code com capacidades completas para tarefas complexas.

**Parâmetros:**
```typescript
{
  prompt: string;      // Instrução para o Claude (obrigatório)
  workFolder?: string; // Diretório de trabalho (padrão: atual)
}
```

**Resposta:**
```typescript
{
  content: [{
    type: "text",
    text: "<resultado da execução do Claude>"
  }]
}
```

**Capacidades do Claude:**
- Criar, ler, editar, mover, copiar e deletar arquivos
- Executar comandos no terminal
- Fazer análise de código
- Gerar código e documentação
- Executar operações Git e GitHub
- Buscar informações na web
- Analisar imagens e screenshots

**Exemplos:**
```javascript
// Refatoração de código
await claude_execute({
  prompt: "Analise o arquivo src/index.js e refatore para melhorar a performance",
  workFolder: "/Users/projeto"
});

// Workflow completo
await claude_execute({
  prompt: `Por favor:
    1. Atualize a versão no package.json para 2.0.0
    2. Gere o CHANGELOG.md com mudanças desde v1.0.0
    3. Faça commit e push
    4. Crie uma release no GitHub`,
  workFolder: "/Users/projeto"
});

// Análise de imagem
await claude_execute({
  prompt: "Analise o screenshot bug.png e crie uma issue detalhada no GitHub",
  workFolder: "/tmp"
});
```

---

## 🔧 Convenções Gerais

### Tratamento de Erros

Todas as ferramentas retornam erros no formato:

```typescript
{
  content: [{
    type: "text",
    text: "Erro ao executar <ferramenta>: <mensagem de erro>"
  }],
  isError: true
}
```


## 📚 Recursos Adicionais

- [Documentação MCP](https://modelcontextprotocol.io/)
- [Puppeteer API](https://pptr.dev/)
---