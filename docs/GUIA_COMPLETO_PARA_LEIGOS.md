# 🤖 HelloWorld


## 🎯 O que é este projeto?

Esse **assistente digital super inteligente** pode:
- Conversar com você em linguagem natural
- Se comunicar com outros assistentes
- Aprender e se adaptar às suas necessidades

- Conectar-se com outros agentes inteligentes
- Executar tarefas úteis diversas

Este é exatamente o que o **HelloWorld Agent** faz! Apesar do nome simples, é um sistema de agente profissional e completo.

---

## 🏗️ Como o Sistema Funciona?

### Analogia Simples: Uma Empresa de Assistentes

Pense no HelloWorld como uma **pequena empresa de assistentes digitais** onde cada componente tem uma função específica:

#### 🏢 **Recepção (Servidor A2A)**
- **Local**: Arquivo `__main__.py`
- **Função**: Como a recepção de uma empresa - recebe visitantes (outros agentes) e direciona para o assistente certo
- **Endereço**: `localhost:9999` (como o endereço da empresa)

#### 👨‍💼 **Gerente (Agent Executor)**
- **Local**: Arquivo `agent_executor.py`
- **Função**: O "cérebro" que decide o que fazer com cada pedido
- **Habilidades**: Lista de tarefas que sabe executar (chamadas de "skills")

#### 🧠 **Departamento de IA (Sistema MCP)**
- **Local**: Pasta `mcp/`
- **Função**: Conexão com inteligência artificial para tarefas complexas
- **Capacidades**: Através da linguagem natural, busca ferramentas, e dispinibiliza para os agentes.

#### 📋 **Cartão de Visitas (Agent Cards)**
- **Local**: Pasta `agent_cards/`
- **Função**: Como cartões de visita que explicam o que a empresa faz
- **Tipos**: Básico (publico geral) e Premium (apenas pagantes)

---

## 🛠️ O que o Assistente Sabe Fazer?

### 📚 **Habilidades Básicas**

#### 1. 👋 **Saudação Simples (hello_world)**
```
Você: "oi"
Assistente: "Hello World"
```
- **Para que serve**: Verificar se o assistente está funcionando
- **Como usar**: Digite "hi", "hello" ou "oi"

#### 2. 🎩 **Saudação Premium (super_hello_world)**
```
Você: "super hi"
Assistente: "Super Hello World! Bem-vindo usuário premium!"
```
- **Para que serve**: Versão especial para usuários autenticados
- **Restrição**: Precisa de "senha" (autenticação)

---

## 🔧 Como Funciona Por Dentro?

### 🎭 **O Cartão de Visitas Digital**

Quando alguém quer conhecer o assistente, ele mostra um "cartão de visitas" digital:

#### **Cartão Básico** (público - todos podem ver):
```json
{
    "nome": "Hello World Agent",
    "descrição": "Assistente digital amigável",
    "habilidades": [
        "Saudação simples",
        "Tarefas básicas de demonstração"
    ]
}
```

#### **Cartão Premium** (privado - só clientes especiais):
```json
{
    "nome": "Hello World Agent Pro",
    "descrição": "Assistente digital com IA avançada",
    "habilidades": [
        "Todas as básicas +",
        "Busca inteligente"
    ]
}
```

---

## 🚀 Como Usar o Sistema?

### 💻 **Opção 1: No Seu Computador**

#### Pré-requisitos:
- Python 3.10 ou mais novo
- UV (gerenciador de pacotes moderno)

#### Passos:
```bash
# 1. Entrar na pasta do projeto
cd /Users/agents/Desktop/codex/agents/helloworld

# 2. Instalar as dependências
uv sync

# 3. Iniciar o assistente
uv run .

# 4. Testar (em outro terminal)
uv run test_client.py
```

### 🐳 **Opção 2: Em Container (Mais Profissional)**

#### Pré-requisitos:
- Docker ou Podman

#### Passos:
```bash
# 1. Criar a "caixa" (container)
podman build . -t meu-assistente

# 2. Executar a "caixa"
podman run -p 9999:9999 meu-assistente

# 3. Seu assistente estará rodando em http://localhost:9999
```

### 🌐 **Opção 3: Teste Rápido via Navegador**

```bash
# Abra o navegador e vá para:
http://localhost:9999/.well-known/agent.json

# Você verá o "cartão de visitas" do seu assistente!
```

---

## 🔒 Segurança e Configuração

### 🔑 **Variáveis de Ambiente (Senhas e Configurações)**

Para usar todas as funcionalidades, você precisa configurar:

```bash
# Chave da IA do Google (para funcionalidades avançadas)
GOOGLE_API_KEY=sua_chave_aqui

# Localização do banco de dados
DATABASE_URL=sqlite:///./helloworld.db

# Onde o assistente vai "morar" na internet
HOST=0.0.0.0
PORT=9999
```

### ⚠️ **Avisos Importantes**

Este é um **projeto de demonstração**. Para usar em produção (empresas, clientes reais):

1. **🔐 Adicionar segurança real**: Senhas, criptografia, validação
2. **📊 Implementar logs**: Registrar tudo que acontece
3. **🚦 Controlar acesso**: Limitar quantas vezes alguém pode usar
4. **🛡️ Validar dados**: Verificar se as informações recebidas são seguras
5. **🏥 Adicionar monitoramento**: Saber quando algo dá errado


## 🔧 Dependências Principais Explicadas

### 📦 **O que o Sistema Precisa Para Funcionar**

```toml
# Framework principal para agentes
"a2a-sdk>=0.2.6"                    # Kit de ferramentas para criar agentes

# Inteligência Artificial
"langchain-google-genai"             # Conexão com IA do Google
"numpy>=1.24.0"                     # Matemática avançada
"pandas>=2.0.0"                     # Trabalhar com dados

# Comunicação web
"httpx>=0.28.1"                     # Fazer pedidos para internet
"uvicorn>=0.34.2"                   # Servidor web rápido

# Funcionalidades específicas
"python-dotenv>=1.1.0"              # Carregar configurações
```

---

## 🤝 Como Expandir o Sistema

### ➕ **Adicionando Nova Habilidade**

Quer ensinar algo novo para seu assistente? É fácil!

#### 1. **Adicione a função em `agent_executor.py`**:
```python
async def calculate_tip(self, context: RequestContext, event_queue: EventQueue) -> None:
    """Calcula gorjeta de restaurante."""
    # Seu código aqui
    event_queue.enqueue_event(new_agent_text_message(f"Gorjeta de 10%: R$ {tip_amount}"))
```

#### 2. **Registre a habilidade**:
```python
skill_functions = {
    "hello_world": self.hello_world,
    "super_hello_world": self.super_hello_world,
    "calculate_tip": self.calculate_tip,  # ← Nova habilidade
}
```

#### 3. **Atualize o cartão de visitas**:
```json
{
    "id": "calculate_tip",
    "name": "Calcular Gorjeta",
    "description": "Calcula gorjeta para restaurantes",
    "examples": ["calcule gorjeta de R$ 100", "quanto de gorjeta para R$ 50"]
}
```