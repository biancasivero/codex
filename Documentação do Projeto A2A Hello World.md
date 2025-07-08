# Documentação do Projeto A2A Hello World

## 1. Introdução

Este documento detalha a implementação de um projeto "Hello World" utilizando o protocolo Agent-to-Agent (A2A). O objetivo é demonstrar a comunicação básica entre um agente A2A e um cliente, seguindo as diretrizes e exemplos fornecidos pela documentação oficial do projeto A2A. O projeto consiste em um agente simples que responde com "Hello World" a uma solicitação e um cliente que interage com este agente.

## 2. Arquitetura do Projeto

A arquitetura do projeto "Hello World" do A2A é composta por dois componentes principais:

*   **Agente Hello World**: Um servidor que implementa o protocolo A2A, expondo uma habilidade (`skill`) que retorna a mensagem "Hello World".
*   **Cliente A2A**: Um script Python que interage com o Agente Hello World, enviando uma solicitação e exibindo a resposta.

A comunicação entre o cliente e o agente é realizada via HTTP, utilizando o protocolo A2A para a troca de mensagens e a descoberta de habilidades do agente. O agente publica um `Agent Card` que descreve suas capacidades e habilidades, permitindo que o cliente descubra e invoque essas habilidades.

## 3. Implementação

### 3.1. Estrutura de Diretórios

O projeto está organizado na seguinte estrutura de diretórios:

```
a2a-hello-world/
├── .venv/                 # Ambiente virtual Python
├── agents/                # Contém o código do agente A2A
│   └── helloworld/        # Agente Hello World
│       ├── __init__.py
│       ├── __main__.py    # Ponto de entrada do agente
│       └── agent_executor.py # Lógica de execução das habilidades do agente
├── client/                # Contém o código do cliente A2A
│   └── client.py          # Script do cliente
└── requirements.txt       # Dependências do projeto
```

### 3.2. Agente Hello World (`agents/helloworld/__main__.py`)

O agente é implementado usando o `a2a-sdk` e `uvicorn`. Ele define duas habilidades: `hello_world` (pública) e `super_hello_world` (autenticada). O `AgentCard` descreve essas habilidades e as capacidades do agente.

```python
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from .agent_executor import (
    HelloWorldAgentExecutor,  # type: ignore[import-untyped]
)

# 1. Define Agent Skill
skill = AgentSkill(
    id=\'hello_world\
    name=\'Returns hello world\
    description=\'just returns hello world\
    tags=[\'hello world\'],
    examples=[\'hi\', \'hello world\'],
)
# --8<-- [end:AgentSkill]
extended_skill = AgentSkill(
    id=\'super_hello_world\
    name=\'Returns a SUPER Hello World\
    description=\'A more enthusiastic greeting, only for authenticated users.\
    tags=[\'hello world\', \'super\', \'extended\'],
    examples=[\'super hi\', \'give me a super hello\'],
)
# --8<-- [start:AgentCard]
# This will be the public-facing agent card
public_agent_card = AgentCard(
    name=\'Hello World Agent\
    description=\'Just a hello world agent\
    url=\'http://localhost:9999/\
    version=\'1.0.0\
    defaultInputModes=[\'text\'],
    defaultOutputModes=[\'text\'],
    capabilities=AgentCapabilities(streaming=True),
    skills=[skill],  # Only the basic skill for the public card
    supportsAuthenticatedExtendedCard=True,
)
# --8<-- [end:AgentCard]
# This will be the authenticated extended agent card
# It includes the additional \'extended_skill\'
specific_extended_agent_card = public_agent_card.model_copy(
    update={
        \'name\': \'Hello World Agent - Extended Edition\',  # Different name for clarity
        \'description\': \'The full-featured hello world agent for authenticated users.\
        \'version\': \'1.0.1\',  # Could even be a different version
        # Capabilities and other fields like url, defaultInputModes, defaultOutputModes,
        # supportsAuthenticatedExtendedCard are inherited from public_agent_card unless specified here.
        \'skills\': [
            skill,
            extended_skill,
        ],
    }
)
request_handler = DefaultRequestHandler(
    agent_executor=HelloWorldAgentExecutor(),
    task_store=InMemoryTaskStore(),
)
server = A2AStarletteApplication(
    agent_card=public_agent_card,
    http_handler=request_handler,
    extended_agent_card=specific_extended_agent_card,
)

app = server.build()

if __name__ == \'__main__\':
    uvicorn.run(app, host=\'0.0.0.0\', port=9999)
```

### 3.3. Executor do Agente (`agents/helloworld/agent_executor.py`)

Este arquivo contém a lógica para executar as habilidades definidas no agente. Ele estende `AgentExecutor` e implementa os métodos para as habilidades `hello_world` e `super_hello_world`.

```python
from a2a.server.agent_execution import AgentExecutor
from a2a.types import (
    AgentSkillInvoke,
    AgentSkillOutput,
    MediaTypes,
)


class HelloWorldAgentExecutor(AgentExecutor):
    async def hello_world(self, skill_invoke: AgentSkillInvoke) -> AgentSkillOutput:
        return AgentSkillOutput(
            output=MediaTypes.TEXT_PLAIN.create_content("Hello World")
        )

    async def super_hello_world(
        self, skill_invoke: AgentSkillInvoke
    ) -> AgentSkillOutput:
        return AgentSkillOutput(
            output=MediaTypes.TEXT_PLAIN.create_content("Hello World")
        )
```

### 3.4. Cliente A2A (`client/client.py`)

O cliente utiliza o `a2a-sdk` para descobrir o `Agent Card` do agente e invocar suas habilidades. Ele demonstra como buscar o `Agent Card` público e o estendido (autenticado), e como invocar as habilidades `hello_world` e `super_hello_world`.

```python
import logging
import httpx
from uuid import uuid4

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendStreamingMessageRequest,
)


async def main() -> None:
    PUBLIC_AGENT_CARD_PATH = \'/.well-known/agent.json\'
    EXTENDED_AGENT_CARD_PATH = \'/agent/authenticatedExtendedCard\'

    # Configure logging to show INFO level messages
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)  # Get a logger instance

    base_url = \'http://localhost:9999\'
    async with httpx.AsyncClient() as httpx_client:
        # Initialize A2ACardResolver
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url,
            # agent_card_path uses default, extended_agent_card_path also uses default
        )

        # Fetch Public Agent Card and Initialize Client
        final_agent_card_to_use: AgentCard | None = None
        try:
            logger.info(
                f\'Attempting to fetch public agent card from: {base_url}{PUBLIC_AGENT_CARD_PATH}\'
            )
            _public_card = (
                await resolver.get_agent_card()
            )  # Fetches from default public path
            logger.info(\'Successfully fetched public agent card:\')
            logger.info(
                _public_card.model_dump_json(indent=2, exclude_none=True)
            )
            final_agent_card_to_use = _public_card
            logger.info(
                \'\nUsing PUBLIC agent card for client initialization (default).\'
            )

            if _public_card.supportsAuthenticatedExtendedCard:
                try:
                    logger.info(
                        f\'\nPublic card supports authenticated extended card. Attempting to fetch from: {base_url}{EXTENDED_AGENT_CARD_PATH}\'
                    )
                    auth_headers_dict = {
                        \'Authorization\': \'Bearer dummy-token-for-extended-card\'
                    }
                    _extended_card = await resolver.get_agent_card(
                        relative_card_path=EXTENDED_AGENT_CARD_PATH,
                        http_kwargs={\'headers\': auth_headers_dict},
                    )
                    logger.info(
                        \'Successfully fetched authenticated extended agent card:\'
                    )
                    logger.info(
                        _extended_card.model_dump_json(
                            indent=2, exclude_none=True
                        )
                    )
                    final_agent_card_to_use = (
                        _extended_card  # Update to use the extended card
                    )
                    logger.info(
                        \'\nUsing AUTHENTICATED EXTENDED agent card for client initialization.\'
                    )
                except Exception as e_extended:
                    logger.warning(
                        f\'Failed to fetch extended agent card: {e_extended}. Will proceed with public card.\',
                        exc_info=True,
                    )
            elif (
                _public_card
            ):  # supportsAuthenticatedExtendedCard is False or None
                logger.info(
                    \'\nPublic card does not indicate support for an extended card. Using public card.\'
                )
        except Exception as e:
            logger.error(
                f\'Critical error fetching public agent card: {e}\', exc_info=True
            )
            raise RuntimeError(
                \'Failed to fetch the public agent card. Cannot continue.\'
            ) from e

        client = A2AClient(
            httpx_client=httpx_client, agent_card=final_agent_card_to_use
        )
        logger.info(\'A2AClient initialized.\')

        send_message_payload: dict[str, Any] = {
            \'message\': {
                \'role\': \'user\',
                \'parts\': [
                    {\'kind\': \'text\', \'text\': \'how much is 10 USD in INR?\'}
                ],
                \'messageId\': uuid4().hex,
            },
        }
        request = SendMessageRequest(
            id=str(uuid4()), params=MessageSendParams(**send_message_payload)
        )
        response = await client.send_message(request)
        print(response.model_dump(mode=\'json\', exclude_none=True))

        streaming_request = SendStreamingMessageRequest(
            id=str(uuid4()), params=MessageSendParams(**send_message_payload)
        )
        stream_response = client.send_message_streaming(streaming_request)
        async for chunk in stream_response:
            print(chunk.model_dump(mode=\'json\', exclude_none=True))


if __name__ == \'__main__\':
    import asyncio

    asyncio.run(main())
```

## 4. Como Executar o Projeto

Siga os passos abaixo para configurar e executar o projeto "Hello World" do A2A:

1.  **Navegue até o diretório do projeto:**

    ```bash
    cd a2a-hello-world
    ```

2.  **Crie e ative o ambiente virtual e instale as dependências:**

    ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Inicie o Agente Hello World:**

    Em um terminal, execute o seguinte comando para iniciar o agente. Ele será executado em segundo plano na porta `9999`.

    ```bash
    uvicorn agents.helloworld.__main__:app --host 0.0.0.0 --port 9999 &
    ```

4.  **Execute o Cliente A2A:**

    Em outro terminal (ou após o agente iniciar), execute o script do cliente:

    ```bash
    python client/client.py
    ```

    Você deverá ver a saída do cliente, que inclui a busca do `Agent Card` e as respostas das invocações das habilidades `hello_world` e `super_hello_world`.

## 5. Resultados do Teste

Ao executar o cliente, você observará a seguinte sequência de eventos:

1.  O cliente tenta buscar o `Agent Card` público do agente na URL `http://localhost:9999/.well-known/agent.json`.
2.  Após obter o `Agent Card` público, o cliente verifica se o agente suporta um `Agent Card` estendido (autenticado).
3.  Se suportado, o cliente tenta buscar o `Agent Card` estendido em `http://localhost:9999/agent/authenticatedExtendedCard` com um token de autenticação fictício.
4.  O cliente inicializa o `A2AClient` com o `Agent Card` apropriado (público ou estendido).
5.  O cliente invoca a habilidade `hello_world` do agente. A resposta esperada é um JSON contendo a mensagem "Hello World".
6.  O cliente invoca a habilidade `super_hello_world` do agente. A resposta esperada também é um JSON contendo a mensagem "Hello World".

As saídas do console durante a execução do cliente confirmam que o `Agent Card` foi buscado com sucesso e que as habilidades foram invocadas corretamente, demonstrando a comunicação bem-sucedida entre o cliente e o agente A2A.

## 6. Conclusão

Este projeto "Hello World" demonstra com sucesso os conceitos fundamentais do protocolo A2A, incluindo a descoberta de agentes via `Agent Card` e a invocação de habilidades. Ele serve como um ponto de partida para o desenvolvimento de agentes A2A mais complexos e interoperáveis.

---

**Autor:** Manus AI
**Data:** 8 de julho de 2025


