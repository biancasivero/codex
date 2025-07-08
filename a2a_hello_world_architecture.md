
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

