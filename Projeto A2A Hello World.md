# Projeto A2A Hello World

Este projeto demonstra uma implementação básica de um agente Agent-to-Agent (A2A) em Python, seguindo as diretrizes e exemplos fornecidos pela documentação oficial do projeto A2A. O objetivo é estabelecer uma comunicação fundamental entre um agente A2A e um cliente, servindo como um ponto de partida para o desenvolvimento de agentes A2A mais complexos e interoperáveis.

## Visão Geral do Projeto

O projeto "Hello World" do A2A é composto por dois componentes principais:

*   **Agente Hello World**: Um servidor que implementa o protocolo A2A, expondo habilidades (`skills`) que retornam mensagens simples.
*   **Cliente A2A**: Um script Python que interage com o Agente Hello World, enviando solicitações e exibindo as respostas.

A comunicação entre o cliente e o agente é realizada via HTTP, utilizando o protocolo A2A para a troca de mensagens e a descoberta de habilidades do agente. O agente publica um `Agent Card` que descreve suas capacidades e habilidades, permitindo que o cliente descubra e invoque essas habilidades.

## Arquitetura do Projeto

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

## Habilidades do Agente (Agent Skills)

Uma **Agent Skill** descreve uma capacidade ou função específica que o agente pode realizar. É um bloco de construção que informa aos clientes quais tipos de tarefas o agente pode executar.

Este agente implementa as seguintes habilidades:

*   `hello_world`: Uma habilidade pública que simplesmente retorna a mensagem "Hello World".
*   `super_hello_world`: Uma habilidade estendida, disponível apenas para usuários autenticados, que também retorna "Hello World" (demonstrando o conceito de habilidades restritas).

## Cartão do Agente (Agent Card)

O **Agent Card** é um documento JSON que um servidor A2A disponibiliza, tipicamente em um endpoint `.well-known/agent.json`. Ele funciona como um cartão de visitas digital para o agente, descrevendo suas capacidades e as habilidades que oferece.

Este projeto define um `Agent Card` público e um `Agent Card` estendido (para usuários autenticados), que inclui a habilidade `super_hello_world`.

## Como Executar o Projeto

Siga os passos abaixo para configurar e executar o projeto "Hello World" do A2A:

### Pré-requisitos

*   Python 3.10 ou superior.
*   Acesso a um terminal ou prompt de comando.

### Passos de Execução

1.  **Navegue até o diretório raiz do projeto:**

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

## Resultados Esperados

Ao executar o cliente, você observará a seguinte sequência de eventos:

1.  O cliente tenta buscar o `Agent Card` público do agente na URL `http://localhost:9999/.well-known/agent.json`.
2.  Após obter o `Agent Card` público, o cliente verifica se o agente suporta um `Agent Card` estendido (autenticado).
3.  Se suportado, o cliente tenta buscar o `Agent Card` estendido em `http://localhost:9999/agent/authenticatedExtendedCard` com um token de autenticação fictício.
4.  O cliente inicializa o `A2AClient` com o `Agent Card` apropriado (público ou estendido).
5.  O cliente invoca a habilidade `hello_world` do agente. A resposta esperada é um JSON contendo a mensagem "Hello World".
6.  O cliente invoca a habilidade `super_hello_world` do agente. A resposta esperada também é um JSON contendo a mensagem "Hello World".

As saídas do console durante a execução do cliente confirmarão que o `Agent Card` foi buscado com sucesso e que as habilidades foram invocadas corretamente, demonstrando a comunicação bem-sucedida entre o cliente e o agente A2A.

## Conclusão

Este projeto "Hello World" demonstra com sucesso os conceitos fundamentais do protocolo A2A, incluindo a descoberta de agentes via `Agent Card` e a invocação de habilidades. Ele serve como um ponto de partida para o desenvolvimento de agentes A2A mais complexos e interoperáveis.

---

**Autor:** Manus AI
**Data:** 8 de julho de 2025





# Arquitetura do Projeto Hello World A2A

## Estrutura de Diretórios

Para o projeto "Hello World" do protocolo A2A, a estrutura de diretórios será simples e organizada, seguindo as convenções de projetos Python e as diretrizes do tutorial A2A. Isso garantirá clareza e facilidade de navegação para qualquer pessoa que queira entender ou estender o projeto.

```
a2a-hello-world/
├── .venv/                  # Ambiente virtual Python
├── agents/                 # Contém os agentes A2A
│   └── helloworld/         # Agente Hello World
│       ├── __init__.py     # Inicialização do módulo
│       └── __main__.py     # Lógica principal do agente (skills, card, executor, server)
├── client/                 # Contém o script cliente para interagir com o agente
│   └── client.py           # Script Python para enviar requisições ao agente
├── requirements.txt        # Dependências Python do projeto
├── README.md               # Documentação do projeto
└── todo.md                 # Lista de tarefas (já criada)
```

Esta estrutura permite uma clara separação entre o código do agente e o código do cliente, além de manter as dependências do projeto em um arquivo centralizado. O ambiente virtual (`.venv/`) garante que as dependências sejam isoladas do sistema global, evitando conflitos de pacotes.



## Componentes Principais

O projeto "Hello World" do protocolo A2A será composto por quatro componentes principais, cada um desempenhando um papel crucial na demonstração da funcionalidade básica do protocolo:

1.  **Agent Skill (Habilidade do Agente):** No contexto do A2A, uma Habilidade do Agente descreve uma capacidade específica que o agente pode executar. Para o nosso "Hello World", teremos uma habilidade simples que retorna a mensagem "Hello, World!". Esta habilidade será definida com um ID único, um nome legível por humanos e uma descrição clara de sua função. Ela também especificará os tipos de entrada e saída que suporta (neste caso, texto simples).

2.  **Agent Card (Cartão do Agente):** O Cartão do Agente é um documento JSON que serve como uma "identidade" para o agente. Ele contém metadados sobre o agente, como seu nome, descrição, versão, o endpoint onde ele pode ser acessado e uma lista das habilidades que ele oferece. O Cartão do Agente é fundamental para a descoberta de agentes, permitindo que outros agentes ou clientes entendam o que um determinado agente pode fazer e como interagir com ele. Para o nosso "Hello World", o Cartão do Agente incluirá a habilidade "Hello, World!" e indicará que o agente está disponível em um `localhost` específico.

3.  **Agent Executor (Executor do Agente):** O Executor do Agente é a lógica central que processa as requisições recebidas pelo agente. Ele é responsável por mapear as requisições para as habilidades apropriadas e executar a lógica associada a essas habilidades. No nosso exemplo, o Executor do Agente receberá uma requisição para a habilidade "Hello, World!" e simplesmente retornará a string correspondente. Este componente encapsula a inteligência ou a funcionalidade do agente.

4.  **Servidor A2A:** O Servidor A2A é o ponto de entrada para as interações com o agente. Ele expõe um endpoint HTTP (geralmente `/agent`) onde as requisições A2A são recebidas. O servidor é responsável por rotear as requisições para o Executor do Agente apropriado e por formatar as respostas de acordo com o protocolo A2A. Para o "Hello World", o servidor será uma aplicação Flask simples que escutará em uma porta específica e responderá às requisições para a habilidade "Hello, World!".

## Interação entre Componentes

A interação entre esses componentes segue um fluxo claro:

1.  **Descoberta:** Um cliente (ou outro agente) deseja interagir com o agente "Hello World". Primeiro, ele pode consultar o Cartão do Agente (via um endpoint `.well-known/agent.json`) para descobrir as habilidades que o agente oferece e o endpoint onde ele pode ser contatado.

2.  **Requisição:** O cliente, sabendo o endpoint do agente e a habilidade desejada ("Hello, World!"), envia uma requisição HTTP POST para o Servidor A2A. Esta requisição incluirá os detalhes da habilidade a ser invocada.

3.  **Processamento:** O Servidor A2A recebe a requisição, a valida e a encaminha para o Executor do Agente. O Executor do Agente identifica a habilidade "Hello, World!" e executa sua lógica interna, que neste caso é simplesmente retornar a string "Hello, World!".

4.  **Resposta:** O Executor do Agente retorna o resultado para o Servidor A2A, que então formata a resposta de acordo com o protocolo A2A e a envia de volta ao cliente. O cliente recebe a resposta e pode processar a mensagem "Hello, World!".

Este fluxo demonstra a interoperabilidade básica do protocolo A2A, onde agentes podem anunciar suas capacidades e outros agentes/clientes podem invocá-las de forma padronizada.





# Princípios do Protocolo A2A

O protocolo A2A é um protocolo aberto que fornece uma maneira padrão para os agentes colaborarem entre si, independentemente da estrutura ou fornecedor subjacente. Os cinco princípios-chave são:

*   **Abrace as capacidades do agente**: O A2A se concentra em permitir que os agentes colaborem em suas modalidades naturais e não estruturadas, mesmo quando não compartilham memória, ferramentas e contexto. Isso permite cenários multiagente verdadeiros sem limitar um agente a uma "ferramenta."

*   **Construa sobre os padrões existentes:** O protocolo é construído sobre padrões existentes e populares, incluindo HTTP, SSE, JSON-RPC, o que significa que é mais fácil integrar com as pilhas de TI existentes que as empresas já usam diariamente.

*   **Seguro por padrão**: O A2A foi projetado para suportar autenticação e autorização de nível empresarial, com paridade com os esquemas de autenticação da OpenAPI no lançamento.

*   **Suporte para tarefas de longa duração:** Projetamos o A2A para ser flexível e suportar cenários em que ele se destaca na conclusão de tudo, desde tarefas rápidas até pesquisas aprofundadas que podem levar horas ou até dias quando os humanos estão envolvidos. Ao longo deste processo, o A2A pode fornecer feedback em tempo real, notificações e atualizações de estado para seus usuários.

*   **Agnóstico de modalidade:** O mundo agêntico não se limita apenas ao texto, e é por isso que projetamos o A2A para suportar várias modalidades, incluindo streaming de áudio e vídeo.





# Configuração e Uso

Este projeto demonstra um agente "Hello World" usando o protocolo A2A em Python. Siga as instruções abaixo para configurar e executar o projeto.

## Pré-requisitos

*   Python 3.10 ou superior.
*   Acesso a um terminal ou prompt de comando.
*   Git, para clonar o repositório.
*   Um editor de código (ex: Visual Studio Code) é recomendado.

## Estrutura do Projeto

```
a2a-hello-world/
├── .venv/                  # Ambiente virtual Python
├── agents/                 # Contém os agentes A2A
│   └── helloworld/         # Agente Hello World
│       ├── __init__.py     # Inicialização do módulo
│       ├── __main__.py     # Lógica principal do agente (skills, card, executor, server)
│       └── agent_executor.py # Implementação do executor do agente
├── client.py               # Script cliente para interagir com o agente
├── requirements.txt        # Dependências Python do projeto
├── README.md               # Documentação do projeto
└── todo.md                 # Lista de tarefas (já criada)
```

## Instalação

Recomendamos usar um ambiente virtual para projetos Python. O SDK Python do A2A usa `uv` para gerenciamento de dependências, mas você também pode usar `pip` com `venv`.

1.  **Crie e ative um ambiente virtual:**

    Usando `venv` (biblioteca padrão):

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Instale as dependências Python necessárias, incluindo o SDK A2A e suas dependências:**

    ```shell
    pip install -r requirements.txt
    ```

## Verificação da Instalação

Após a instalação, você deve ser capaz de importar o pacote `a2a` em um interpretador Python:

```shell
python3 -c "import a2a; print(\'A2A SDK importado com sucesso\')"
```

Se este comando for executado sem erros e imprimir a mensagem de sucesso, seu ambiente está configurado corretamente.

## Executando o Agente

Para iniciar o agente A2A, navegue até o diretório raiz do projeto (`a2a-hello-world/`) e execute o seguinte comando:

```bash
uvicorn agents.helloworld.__main__:app --host 0.0.0.0 --port 9999
```

Este comando iniciará o servidor A2A na porta `9999`.

## Interagindo com o Agente (Cliente)

Com o agente em execução, você pode usar o script `client.py` para interagir com ele. Abra um novo terminal (mantendo o agente em execução no primeiro terminal), navegue até o diretório raiz do projeto e execute:

```bash
python3 client.py
```

O `client.py` está configurado para:

*   Buscar o `AgentCard` público do agente.
*   Se suportado, buscar o `AgentCard` estendido (autenticado).
*   Enviar uma requisição para a habilidade `convert_currency` (ex: `convert 25 USD to BRL`).
*   Enviar uma requisição para a habilidade `super_hello_world`.

As respostas do agente serão impressas no terminal do cliente.



