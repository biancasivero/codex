# 🔧 Guia de Integração de Servidores MCP ao DiegoTools

Este documento explica como integrar qualquer servidor MCP existente como uma ferramenta do DiegoTools, permitindo centralizar todas as suas capacidades em um único servidor.

## 📋 Visão Geral

O DiegoTools é projetado com arquitetura modular que facilita a integração de novos servidores MCP. A integração do `claude_execute` demonstra como isso pode ser feito de forma limpa e eficiente.

## 🎯 Por que Integrar?

1. **Centralização**: Todas as ferramentas em um único servidor MCP
2. **Composição**: Combine ferramentas de diferentes servidores em workflows
3. **Reutilização**: Aproveite ferramentas existentes sem duplicar código
4. **Manutenção**: Um único ponto de instalação e atualização

## 📦 Passo a Passo para Integração

### 1. Analisar o Servidor MCP Original

Primeiro, examine o servidor que deseja integrar:

```typescript
// Identifique:
// - Ferramentas oferecidas
// - Parâmetros de entrada
// - Formato de saída
// - Dependências necessárias
```

### 2. Criar Estrutura de Diretório

```bash
src/tools/
├── seu-mcp/
│   └── index.ts    # Módulo adaptado
```

### 3. Adicionar Tipos ao `types.ts`

```typescript
// src/types.ts

// Adicione ao enum ToolName
export enum ToolName {
  // ... ferramentas existentes
  SEU_TOOL = 'seu_tool_name'
}

// Adicione interface de parâmetros
export interface SeuToolParams {
  param1: string;
  param2?: number;
  // ... outros parâmetros
}
```

### 4. Criar Schema de Validação

```typescript
// src/schemas.ts

export const SeuToolSchema = z.object({
  param1: z.string().min(1, 'Param1 é obrigatório'),
  param2: z.number().optional()
});

// Adicione ao mapa de schemas
export const ToolSchemas = {
  // ... outros schemas
  [ToolName.SEU_TOOL]: SeuToolSchema
};
```

### 5. Adaptar o Código do Servidor

Crie o módulo adaptado em `src/tools/seu-mcp/index.ts`:

```typescript
import { 
  SeuToolParams, 
  ContentBlock, 
  MCPError, 
  ErrorCode,
  ToolName 
} from '../../types';
import { SeuToolSchema } from '../../schemas';

// Importe as dependências do servidor original
import { FuncaoOriginal } from 'servidor-original';

/**
 * Handler adaptado para DiegoTools
 */
export async function handleSeuTool(params: SeuToolParams): Promise<ContentBlock[]> {
  // Validação com Zod
  const validatedParams = SeuToolSchema.parse(params);
  
  try {
    // Adapte a lógica do servidor original
    const resultado = await FuncaoOriginal(validatedParams);
    
    // Retorne no formato ContentBlock
    return [{
      type: 'text',
      text: resultado
    }];
    
  } catch (error) {
    // Tratamento de erros padronizado
    throw new MCPError(
      ErrorCode.INTERNAL_ERROR,
      `Erro ao executar ferramenta: ${error.message}`
    );
  }
}

// Exporta definição da ferramenta
export const seuTool = {
  name: ToolName.SEU_TOOL,
  description: 'Descrição da sua ferramenta',
  inputSchema: {
    type: 'object' as const,
    properties: {
      param1: {
        type: 'string',
        description: 'Descrição do parâmetro 1'
      },
      param2: {
        type: 'number',
        description: 'Descrição do parâmetro 2'
      }
    },
    required: ['param1']
  }
};
```

### 6. Registrar no Sistema

Atualize `src/tools/index.ts`:

```typescript
// Adicione a importação
export {
  seuTool,
  handleSeuTool
} from './seu-mcp/index.js';

// Adicione ao array allTools
export const allTools = [
  // ... outras ferramentas
  seuTool
];

// Adicione ao mapa de handlers
export const toolHandlers = {
  // ... outros handlers
  'seu_tool_name': handleSeuTool
};
```

### 7. Atualizar Documentação

Adicione a nova ferramenta ao `CLAUDE.md`:

```markdown
### 🆕 Sua Nova Categoria (X ferramentas)
1. **seu_tool_name** - Descrição da ferramenta
   - Parâmetro 1: descrição
   - Parâmetro 2: descrição
```

## 🔍 Exemplo Real: Integração do Claude CLI

A integração do `claude_execute` demonstra o processo completo:

### Análise Original
- **Ferramenta**: `claude_execute` 
- **Função**: Executar Claude Code CLI com prompts
- **Parâmetros**: `prompt` (obrigatório), `workFolder` (opcional)
- **Timeout**: 30 minutos configurável
- **Localização**: `src/tools/claude/`

### Adaptações Realizadas
1. **Separação de responsabilidades**: Lógica movida para módulo independente
2. **Padronização de erros**: MCPError ao invés de McpError
3. **Validação**: Schema Zod integrado
4. **Debug**: Sistema unificado com `MCP_CLAUDE_DEBUG`
5. **Remoção de duplicação**: Servidor one-shot original removido

## ⚙️ Considerações Técnicas

### Dependências
- Adicione dependências necessárias ao `package.json`
- Evite conflitos de versão com dependências existentes
- Use imports relativos para módulos internos

### Variáveis de Ambiente
- Documente variáveis necessárias
- Use dotenv para carregamento
- Forneça valores padrão quando possível

### Performance
- Considere singleton para recursos pesados (como browser)
- Implemente cleanup de recursos
- Use timeouts apropriados

### Tratamento de Erros
- Use MCPError para erros conhecidos
- Preserve stack traces para debugging
- Mensagens em português para consistência

## 🧪 Testando a Integração

### 1. Compilar TypeScript
```bash
npm run build
```

### 2. Reinstalar no Claude Code
```bash
cd /mcp-run-ts-tools
npm install && npm run build && claude mcp add DiegoTools "node /mcp-run-ts-tools/build/index.js" --env GITHUB_TOKEN=ghp_xyz
```

### 3. Testar Ferramenta
```javascript
// No Claude Code
await seu_tool_name({
  param1: "valor teste",
  param2: 123
});
```

## 📚 Recursos Úteis

### Padrões de Integração
1. **Wrapper Pattern**: Encapsular funcionalidade externa
2. **Adapter Pattern**: Converter interfaces incompatíveis
3. **Facade Pattern**: Simplificar APIs complexas

### Tipos de Servidores MCP Comuns
- **Ferramentas de arquivo**: fs-server, file-manager
- **Integrações de API**: github, gitlab, jira
- **Automação**: puppeteer, playwright
- **Dados**: sqlite, postgres, redis
- **Utilidades**: weather, time, calculator
- **AI/LLM**: claude-cli, openai, anthropic

## 🎯 Checklist de Integração

- [ ] Analisar servidor MCP original
- [ ] Adicionar tipos em `types.ts`
- [ ] Criar schema em `schemas.ts`
- [ ] Implementar handler adaptado
- [ ] Registrar em `tools/index.ts`
- [ ] Atualizar documentação
- [ ] Compilar e testar
- [ ] Adicionar exemplos de uso

## 💡 Dicas Finais

1. **Mantenha a simplicidade**: Não complique demais a adaptação
2. **Preserve funcionalidade**: Mantenha todas as capacidades originais
3. **Documente bem**: Facilite o uso futuro
4. **Teste extensivamente**: Cubra casos de erro
5. **Contribua de volta**: Compartilhe integrações úteis

## 🏗️ Estrutura Atual do DiegoTools

```
src/
├── index.ts          # Servidor MCP principal
├── types.ts          # Tipos e interfaces TypeScript
├── schemas.ts        # Validação Zod
├── utils.ts          # Utilitários compartilhados
├── middleware.ts     # Sistema de middlewares
├── factory.ts        # Factory pattern para ferramentas
├── handlers.ts       # Handlers centralizados
└── tools/            # Ferramentas organizadas por categoria
    ├── index.ts      # Exporta todas as ferramentas
    ├── puppeteer/    # 5 ferramentas de automação web
    ├── github/       # 6 ferramentas GitHub API
    ├── git/          # 4 ferramentas Git local
    └── claude/       # 1 ferramenta Claude CLI
```

### Total: 16 ferramentas integradas e funcionando!

Com este guia, você pode integrar qualquer servidor MCP ao DiegoTools, criando um hub centralizado e poderoso de ferramentas para o Claude Code!