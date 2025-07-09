# resolve-library-id (context-7)

**Nome da Ferramenta:** resolve-library-id  
**Nome Completo:** mcp__context-7__resolve-library-id

## Descrição:
Resolve um nome de pacote/produto para um ID de biblioteca compatível com Context7 e retorna uma lista de bibliotecas correspondentes.

Você **DEVE** chamar esta função antes de 'get-library-docs' para obter um ID de biblioteca compatível com Context7 válido, **A MENOS QUE** o usuário forneça explicitamente um ID de biblioteca no formato '/org/project' ou '/org/project/version' em sua consulta.

## Processo de Seleção:
1. Analise a consulta para entender qual biblioteca/pacote o usuário está procurando
2. Retorne a correspondência mais relevante baseada em:
   - Similaridade do nome com a consulta (correspondências exatas têm prioridade)
   - Relevância da descrição para a intenção da consulta
   - Cobertura da documentação (priorize bibliotecas com contagens maiores de Code Snippet)
   - Pontuação de confiança (considere bibliotecas com pontuações de 7-10 mais autoritativas)

## Formato de Resposta:
- Retorne o ID da biblioteca selecionada em uma seção claramente marcada
- Forneça uma breve explicação do porquê esta biblioteca foi escolhida
- Se múltiplas boas correspondências existirem, reconheça isso mas prossiga com a mais relevante
- Se não existirem boas correspondências, declare claramente isso e sugira refinamentos da consulta

Para consultas ambíguas, solicite esclarecimento antes de prosseguir com uma correspondência de melhor tentativa.

## Parâmetros:
• **libraryName** (obrigatório): string - Nome da biblioteca

---

# get-library-docs (context-7)

**Nome da Ferramenta:** get-library-docs  
**Nome Completo:** mcp__context-7__get-library-docs

## Descrição:
Busca documentação atualizada para uma biblioteca. Você deve chamar 'resolve-library-id' primeiro para obter o ID de biblioteca compatível com Context7 exato necessário para usar esta ferramenta, **A MENOS QUE** o usuário forneça explicitamente um ID de biblioteca no formato '/org/project' ou '/org/project/version' em sua consulta.

## Parâmetros:
• **context7CompatibleLibraryID** (obrigatório): string - ID de biblioteca compatível com Context7 exato (ex: '/mongodb/docs', '/vercel/next.js', '/supabase/supabase', '/vercel/next.js/v14.3.0-canary.87') obtido de 'resolve-library-id' ou diretamente da consulta do usuário no formato '/org/project' ou '/org/project/version'.

• **topic**: string - Tópico para focar a documentação (ex: 'hooks', 'routing').

• **tokens**: number - Número máximo de tokens de documentação para recuperar (padrão: 10000). Valores maiores fornecem mais contexto mas consomem mais tokens.

---

**Dica:** Quer que o Claude lembre de algo? Pressione # para adicionar preferências, ferramentas e instruções à memória do Claude.