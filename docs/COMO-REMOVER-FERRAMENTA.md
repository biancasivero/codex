# Como Remover uma Ferramenta do DiegoTools

Este documento descreve o processo genérico para remover completamente uma ferramenta do servidor MCP DiegoTools.

## Pré-requisitos

- Acesso ao código fonte do DiegoTools
- Conhecimento básico de TypeScript
- Terminal com npm disponível

## Passo a Passo

### 1. Identificar a Ferramenta

Primeiro, identifique todos os componentes da ferramenta que será removida:
- Nome da ferramenta (ex: `minha_ferramenta`)
- Diretório da ferramenta (ex: `/src/tools/minha_categoria/`)
- Enum no ToolName (ex: `MINHA_FERRAMENTA`)

### 2. Remover Diretório da Ferramenta

```bash
# Remove o diretório específico da ferramenta
rm -rf /src/tools/[categoria]/
```

**Exemplo:**
```bash
rm -rf /src/tools/claude/
```

### 3. Atualizar `/src/tools/index.ts`

Remova todas as referências da ferramenta no arquivo de exportação:

#### 3.1. Remover Exportações
```typescript
// REMOVER esta seção
export {
  minhaFerramenta,
  handleMinhaFerramenta
} from './categoria/index.js';
```

#### 3.2. Remover Imports
```typescript
// REMOVER este import
import { minhaFerramenta } from './categoria/index.js';
```

#### 3.3. Remover do Array `allTools`
```typescript
export const allTools = [
  ...puppeteerTools,
  ...githubTools,
  ...gitTools
  // REMOVER: minhaFerramenta
];
```

#### 3.4. Remover do Object `toolHandlers`
```typescript
export const toolHandlers = {
  // ... outras ferramentas
  // REMOVER: 'minha_ferramenta': handleMinhaFerramenta
} as const;
```

### 4. Atualizar `/src/types.ts`

#### 4.1. Remover do Enum `ToolName`
```typescript
export enum ToolName {
  // ... outras ferramentas
  // REMOVER: MINHA_FERRAMENTA = 'minha_ferramenta'
}
```

#### 4.2. Remover Interface de Parâmetros
```typescript
// REMOVER toda a interface
export interface MinhaFerramentaParams {
  param1: string;
  param2?: number;
}
```

### 5. Atualizar `/src/schemas.ts`

#### 5.1. Remover Schema Zod
```typescript
// REMOVER o schema
export const MinhaFerramentaSchema = z.object({
  param1: z.string().min(1, 'Param1 é obrigatório'),
  param2: z.number().optional()
});
```

#### 5.2. Remover do Mapa `ToolSchemas`
```typescript
export const ToolSchemas = {
  // ... outros schemas
  // REMOVER: [ToolName.MINHA_FERRAMENTA]: MinhaFerramentaSchema
} as const;
```

### 6. Atualizar `/src/index.ts` (Servidor Principal)

#### 6.1. Remover Import do Handler
```typescript
// REMOVER este import
import { handleMinhaFerramenta } from './tools/categoria/index.js';
```

#### 6.2. Remover do Object `toolHandlers`
```typescript
const toolHandlers: Record<ToolName, (args: any) => Promise<any>> = {
  // ... outros handlers
  // REMOVER: [ToolName.MINHA_FERRAMENTA]: handleMinhaFerramenta
};
```

#### 6.3. Remover da Lista de Ferramentas
No método `setRequestHandler(ListToolsRequestSchema)`, remover o objeto da ferramenta:

```typescript
tools: [
  // ... outras ferramentas
  // REMOVER todo este objeto:
  // {
  //   name: ToolName.MINHA_FERRAMENTA,
  //   description: 'Descrição da ferramenta',
  //   inputSchema: { ... }
  // }
]
```

### 7. Verificar Outras Referências

Use o comando `grep` para verificar se há outras referências:

```bash
# Buscar por referências da ferramenta
grep -r "minha_ferramenta\|MinhaFerramenta\|MINHA_FERRAMENTA" src/
```

Remova qualquer referência encontrada em:
- Comentários
- Documentação
- Testes
- Arquivos de configuração

### 8. Compilar e Testar

#### 8.1. Instalar Dependências (se necessário)
```bash
npm install
```

#### 8.2. Compilar TypeScript
```bash
npm run build
```

#### 8.3. Executar Testes (se existirem)
```bash
npm test
```

### 9. Verificar Funcionamento

#### 9.1. Testar Servidor
```bash
# Executar o servidor para verificar se inicia sem erros
npm start
```

#### 9.2. Verificar Lista de Ferramentas
O servidor deve iniciar sem erros e a ferramenta removida não deve aparecer na lista de ferramentas disponíveis.

## Checklist de Verificação

- [ ] Diretório da ferramenta removido
- [ ] Exportações removidas do `/src/tools/index.ts`
- [ ] Imports removidos do `/src/tools/index.ts`
- [ ] Ferramenta removida do array `allTools`
- [ ] Handler removido do object `toolHandlers`
- [ ] Enum removido de `ToolName` em `/src/types.ts`
- [ ] Interface de parâmetros removida de `/src/types.ts`
- [ ] Schema Zod removido de `/src/schemas.ts`
- [ ] Schema removido do mapa `ToolSchemas`
- [ ] Import do handler removido de `/src/index.ts`
- [ ] Handler removido do registry em `/src/index.ts`
- [ ] Definição removida da lista de ferramentas
- [ ] Busca por referências restantes realizada
- [ ] Compilação TypeScript bem-sucedida
- [ ] Servidor inicia sem erros
- [ ] Testes passam (se existirem)

## Dicas Importantes

1. **Sempre fazer backup** do código antes de remover ferramentas
2. **Testar em ambiente de desenvolvimento** antes de aplicar em produção
3. **Verificar dependências** - outras ferramentas podem depender da que está sendo removida
4. **Atualizar documentação** relacionada à ferramenta removida
5. **Considerar deprecação gradual** em vez de remoção imediata para sistemas em produção

## Troubleshooting

### Erro de Compilação TypeScript
- Verifique se todas as referências foram removidas
- Procure por imports não utilizados
- Verifique se tipos/interfaces ainda estão sendo referenciados

### Servidor Não Inicia
- Verifique logs de erro no console
- Confirme se todas as referências no `toolHandlers` foram removidas
- Verifique se não há imports quebrados

### Ferramenta Ainda Aparece na Lista
- Confirme se foi removida da lista no `ListToolsRequestSchema`
- Verifique se o build foi executado após as alterações
- Reinicie o servidor MCP

## Exemplo Completo

Para ver um exemplo prático de remoção, consulte o commit que removeu a ferramenta Claude do DiegoTools, que seguiu exatamente estes passos.