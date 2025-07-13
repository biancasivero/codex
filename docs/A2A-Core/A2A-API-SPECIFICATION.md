# A2A Protocol API - Especificação Técnica Completa

## Visão Geral

O A2A (Agent-to-Agent) Protocol é uma especificação para comunicação entre agentes de IA baseada em HTTP REST e JSON-RPC 2.0. Esta documentação cobre os endpoints principais, formatos de request/response, códigos de erro e exemplos práticos de uso.

**Versão do Protocolo:** A2A/1.0  
**Versão da API:** 2.0.0  
**Base URL:** `http://localhost:8080` (configurável)

## Headers Obrigatórios

### Para todos os endpoints:
```http
Content-Type: application/json
X-A2A-Protocol: 1.0
```

### Headers de resposta incluídos:
```http
X-A2A-Protocol: 1.0
X-Powered-By: BaseA2AServer/2.0
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Access-Control-Allow-Origin: *
```

## Endpoints Principais

### 1. Discovery Endpoint

**GET /discover**

Retorna as capacidades e informações do agente.

#### Request
```http
GET /discover HTTP/1.1
Host: localhost:8080
X-A2A-Protocol: 1.0
```

#### Response (200 OK)
```json
{
  "name": "HelloWorld Agent",
  "version": "1.0.0",
  "description": "Intelligent agent that provides contextual hello world responses",
  "protocolVersion": "0.2.5",
  "url": "http://localhost:8080",
  "defaultInputModes": ["text/plain", "application/json"],
  "defaultOutputModes": ["text/plain", "application/json"],
  "capabilities": {
    "pushNotifications": true,
    "streaming": true,
    "stateTransitionHistory": true,
    "extensions": []
  },
  "skills": [
    {
      "id": "hello_world",
      "name": "Hello World",
      "description": "Provides intelligent hello world responses",
      "tags": ["greeting", "hello", "basic"],
      "examples": [
        "Say hello",
        "Give me a super hello",
        "Simple hello world"
      ],
      "inputModes": ["text/plain"],
      "outputModes": ["text/plain", "application/json"]
    }
  ],
  "provider": {
    "organization": "A2A Project",
    "url": "https://github.com/a2aproject"
  }
}
```

#### Códigos de Erro
- **500 Internal Server Error**: Falha na descoberta de capacidades

---

### 2. Communication Endpoint

**POST /communicate**

Endpoint para comunicação direta com o agente usando JSON-RPC 2.0.

#### Request Structure
```http
POST /communicate HTTP/1.1
Host: localhost:8080
Content-Type: application/json
X-A2A-Protocol: 1.0

{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "request-123",
  "params": {
    "message": {
      "messageId": "msg-456",
      "role": "user",
      "kind": "message",
      "parts": [
        {
          "kind": "text",
          "text": "Hello World!"
        }
      ]
    },
    "configuration": {
      "acceptedOutputModes": ["text/plain", "application/json"],
      "blocking": true
    }
  }
}
```

#### Response Structure (200 OK)
```json
{
  "jsonrpc": "2.0",
  "id": "request-123",
  "result": {
    "kind": "task",
    "id": "task-789",
    "contextId": "context-012",
    "status": {
      "state": "completed",
      "timestamp": "2025-01-13T22:30:00Z",
      "message": {
        "messageId": "response-345",
        "role": "agent",
        "kind": "message",
        "parts": [
          {
            "kind": "text",
            "text": "Hello World! 👋"
          }
        ]
      }
    },
    "artifacts": [
      {
        "artifactId": "artifact-678",
        "name": "hello_world_result",
        "description": "HelloWorld intelligent response",
        "parts": [
          {
            "kind": "text",
            "text": "Hello World! 👋"
          }
        ]
      }
    ]
  }
}
```

#### Streaming Request (message/stream)
```json
{
  "jsonrpc": "2.0",
  "method": "message/stream",
  "id": "stream-123",
  "params": {
    "message": {
      "messageId": "msg-stream-456",
      "role": "user",
      "kind": "message",
      "parts": [
        {
          "kind": "text",
          "text": "Generate a long response"
        }
      ]
    },
    "configuration": {
      "acceptedOutputModes": ["text/plain"],
      "blocking": false
    }
  }
}
```

#### Códigos de Erro
- **500 Internal Server Error**: Falha na comunicação com o agente

---

### 3. Delegation Endpoint

**POST /delegate**

Endpoint para delegação de tarefas e gerenciamento de task lifecycle.

#### Task Management Methods

##### Get Task (tasks/get)
```json
{
  "jsonrpc": "2.0",
  "method": "tasks/get",
  "id": "get-task-123",
  "params": {
    "id": "task-789",
    "historyLength": 10
  }
}
```

##### Cancel Task (tasks/cancel)
```json
{
  "jsonrpc": "2.0",
  "method": "tasks/cancel",
  "id": "cancel-123",
  "params": {
    "id": "task-789"
  }
}
```

##### Push Notification Config (tasks/pushNotificationConfig/set)
```json
{
  "jsonrpc": "2.0",
  "method": "tasks/pushNotificationConfig/set",
  "id": "push-config-123",
  "params": {
    "taskId": "task-789",
    "pushNotificationConfig": {
      "url": "https://client.example.com/notifications",
      "authentication": {
        "schemes": ["Bearer"],
        "credentials": "token-xyz"
      }
    }
  }
}
```

#### Response Structure
```json
{
  "jsonrpc": "2.0",
  "id": "get-task-123",
  "result": {
    "kind": "task",
    "id": "task-789",
    "contextId": "context-012",
    "status": {
      "state": "completed",
      "timestamp": "2025-01-13T22:30:00Z"
    },
    "history": [
      {
        "messageId": "msg-1",
        "role": "user",
        "kind": "message",
        "parts": [{"kind": "text", "text": "Hello"}]
      },
      {
        "messageId": "msg-2", 
        "role": "agent",
        "kind": "message",
        "parts": [{"kind": "text", "text": "Hello World!"}]
      }
    ],
    "artifacts": [
      {
        "artifactId": "artifact-678",
        "name": "hello_world_result",
        "parts": [{"kind": "text", "text": "Hello World!"}]
      }
    ]
  }
}
```

#### Códigos de Erro
- **500 Internal Server Error**: Falha na delegação de tarefa

---

### 4. Health Check Endpoint

**GET /health**

Verifica o status de saúde do agente e infraestrutura.

#### Request
```http
GET /health HTTP/1.1
Host: localhost:8080
X-A2A-Protocol: 1.0
```

#### Response (200 OK)
```json
{
  "status": "healthy",
  "agent": {
    "name": "HelloWorld Agent",
    "status": "running",
    "uptime": 3600
  },
  "server": {
    "uptime": 3600,
    "memory": {
      "rss": 52428800,
      "heapUsed": 25165824,
      "heapTotal": 41943040
    },
    "pid": 12345
  },
  "cache": {
    "status": "connected",
    "health": "healthy",
    "connections": {
      "active": 1,
      "idle": 4,
      "total": 5
    },
    "stats": {
      "hits": 150,
      "misses": 45,
      "hitRate": "76.92%"
    }
  },
  "timestamp": "2025-01-13T22:30:00Z"
}
```

#### Response (500 Internal Server Error)
```json
{
  "error": "Health check failed",
  "status": "unhealthy",
  "timestamp": "2025-01-13T22:30:00Z"
}
```

---

## Endpoints Auxiliares

### Agent Card

**GET /agent.json**

Retorna o cartão do agente com informações detalhadas.

#### Response (200 OK)
```json
{
  "name": "HelloWorld Agent",
  "version": "1.0.0",
  "description": "Intelligent agent that provides contextual hello world responses",
  "protocolVersion": "0.2.5",
  "url": "http://localhost:8080",
  "defaultInputModes": ["text/plain", "application/json"],
  "defaultOutputModes": ["text/plain", "application/json"],
  "capabilities": {
    "pushNotifications": true,
    "streaming": true
  },
  "skills": [
    {
      "id": "hello_world",
      "name": "Hello World",
      "description": "Provides intelligent hello world responses",
      "tags": ["greeting"]
    }
  ]
}
```

### Cache Management

**GET /cache/stats**
```json
{
  "cache": {
    "hits": 250,
    "misses": 50,
    "hitRate": "83.33%",
    "operations": 300
  },
  "redis": {
    "status": "connected",
    "connections": {
      "active": 2,
      "idle": 3,
      "total": 5
    }
  },
  "timestamp": "2025-01-13T22:30:00Z"
}
```

**POST /cache/invalidate**

Request:
```json
{
  "pattern": "discovery"
}
```

Response:
```json
{
  "success": true,
  "pattern": "discovery",
  "invalidated": 5,
  "timestamp": "2025-01-13T22:30:00Z"
}
```

### Server Metrics

**GET /metrics**
```json
{
  "server": {
    "uptime": 7200,
    "requests": 1250,
    "errors": 12,
    "errorRate": "0.96%",
    "memory": {
      "rss": "50MB",
      "heapUsed": "24MB",
      "heapTotal": "40MB"
    }
  },
  "cache": {
    "hits": 340,
    "misses": 85,
    "hitRate": "80.0%"
  },
  "timestamp": "2025-01-13T22:30:00Z"
}
```

### Server Information

**GET /info**
```json
{
  "server": "BaseA2AServer",
  "version": "2.0.0",
  "agent": "HelloWorld Agent",
  "port": 8080,
  "protocol": "A2A/1.0",
  "features": {
    "redis_cache": true,
    "compression": true,
    "cache_warmup": true
  },
  "endpoints": {
    "core": ["/discover", "/communicate", "/delegate", "/health", "/agent.json"],
    "cache": ["/cache/stats", "/cache/invalidate", "/cache/warmup"],
    "monitoring": ["/metrics", "/info"]
  },
  "uptime": 7200,
  "timestamp": "2025-01-13T22:30:00Z"
}
```

---

## Códigos de Erro JSON-RPC

### Códigos Padrão JSON-RPC 2.0
| Código | Nome | Descrição |
|--------|------|-----------|
| -32700 | Parse error | JSON inválido recebido pelo servidor |
| -32600 | Invalid Request | Objeto de request JSON-RPC inválido |
| -32601 | Method not found | Método não existe ou não está disponível |
| -32602 | Invalid params | Parâmetros de método inválidos |
| -32603 | Internal error | Erro interno do servidor JSON-RPC |

### Códigos Específicos A2A
| Código | Nome | Descrição |
|--------|------|-----------|
| -32001 | Task not found | ID de tarefa solicitado não foi encontrado |
| -32002 | Task not cancelable | Tarefa está em estado que não pode ser cancelado |
| -32003 | Push Notification not supported | Agente não suporta push notifications |
| -32004 | Unsupported operation | Operação solicitada não é suportada pelo agente |
| -32005 | Content type not supported | Tipos de conteúdo incompatíveis entre request e agente |
| -32006 | Invalid agent response | Agente retornou resposta inválida para o método atual |

### Exemplo de Erro Response
```json
{
  "jsonrpc": "2.0",
  "id": "request-123",
  "error": {
    "code": -32001,
    "message": "Task not found",
    "data": {
      "taskId": "task-nonexistent",
      "timestamp": "2025-01-13T22:30:00Z"
    }
  }
}
```

---

## Task States (Estados de Tarefa)

| Estado | Descrição |
|--------|-----------|
| `submitted` | Tarefa foi submetida e aguarda processamento |
| `working` | Tarefa está sendo processada pelo agente |
| `input-required` | Tarefa requer input adicional do usuário |
| `completed` | Tarefa foi completada com sucesso |
| `canceled` | Tarefa foi cancelada pelo usuário |
| `failed` | Tarefa falhou durante o processamento |
| `rejected` | Tarefa foi rejeitada pelo agente |
| `auth-required` | Tarefa requer autenticação adicional |
| `unknown` | Estado da tarefa é desconhecido |

---

## Estruturas de Dados Principais

### Message
```typescript
interface Message {
  messageId: string;
  role: "user" | "agent";
  kind: "message";
  contextId?: string;
  taskId?: string;
  parts: Part[];
  metadata?: Record<string, any>;
  referenceTaskIds?: string[];
  extensions?: string[];
}
```

### Part
```typescript
type Part = TextPart | FilePart | DataPart;

interface TextPart {
  kind: "text";
  text: string;
  metadata?: Record<string, any>;
}

interface FilePart {
  kind: "file";
  file: FileWithBytes | FileWithUri;
  metadata?: Record<string, any>;
}

interface DataPart {
  kind: "data";
  data: Record<string, any>;
  metadata?: Record<string, any>;
}
```

### Task
```typescript
interface Task {
  id: string;
  contextId: string;
  kind: "task";
  status: TaskStatus;
  history?: Message[];
  artifacts?: Artifact[];
  metadata?: Record<string, any>;
}
```

### TaskStatus
```typescript
interface TaskStatus {
  state: TaskState;
  timestamp?: string; // ISO 8601
  message?: Message;
}
```

### Artifact
```typescript
interface Artifact {
  artifactId: string;
  name?: string;
  description?: string;
  parts: Part[];
  metadata?: Record<string, any>;
  extensions?: string[];
}
```

---

## Compatibilidade OpenAPI/Swagger

A API A2A Protocol pode ser documentada usando OpenAPI 3.0. Exemplo de definição:

```yaml
openapi: 3.0.0
info:
  title: A2A Protocol API
  description: Agent-to-Agent Communication Protocol
  version: 2.0.0
  
servers:
  - url: http://localhost:8080
    description: Local development server

paths:
  /discover:
    get:
      summary: Get agent capabilities
      tags: [Core]
      responses:
        '200':
          description: Agent capabilities
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AgentCard'
        '500':
          description: Discovery failed
          
  /communicate:
    post:
      summary: Communicate with agent
      tags: [Core]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/JSONRPCRequest'
      responses:
        '200':
          description: Communication response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/JSONRPCResponse'
                
  /delegate:
    post:
      summary: Delegate tasks to agent
      tags: [Core]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/JSONRPCRequest'
      responses:
        '200':
          description: Delegation response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/JSONRPCResponse'
                
  /health:
    get:
      summary: Check agent health
      tags: [Monitoring]
      responses:
        '200':
          description: Health status
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HealthResponse'

components:
  schemas:
    JSONRPCRequest:
      type: object
      required: [jsonrpc, method, id]
      properties:
        jsonrpc:
          type: string
          enum: ["2.0"]
        method:
          type: string
        id:
          oneOf:
            - type: string
            - type: number
        params:
          type: object
          
    JSONRPCResponse:
      type: object
      required: [jsonrpc, id]
      properties:
        jsonrpc:
          type: string
          enum: ["2.0"]
        id:
          oneOf:
            - type: string
            - type: number
        result:
          type: object
        error:
          $ref: '#/components/schemas/JSONRPCError'
```

---

## Autenticação e Segurança

O A2A Protocol suporta múltiplos esquemas de autenticação:

### API Key Authentication
```http
Authorization: Bearer your-api-key-here
```

### HTTP Basic Authentication
```http
Authorization: Basic base64(username:password)
```

### OAuth 2.0
```http
Authorization: Bearer oauth-access-token
```

### Headers de Segurança Incluídos
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

---

## Performance e Cache

### Cache Redis
- Cache automático para endpoints `/discover` e `/health`
- TTL configurável (padrão: 300 segundos)
- Connection pooling para alta performance
- Estatísticas de cache disponíveis em `/cache/stats`

### Compressão
- Compressão gzip automática para responses > 1KB
- Nível de compressão configurável (padrão: 6)

### Métricas
- Tempo de resposta em header `X-Response-Time`
- Contadores de request/erro disponíveis em `/metrics`
- Monitoramento de memória e uptime

---

## Exemplos de Integração

### Cliente JavaScript
```javascript
class A2AClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }
  
  async discover() {
    const response = await fetch(`${this.baseUrl}/discover`, {
      headers: { 'X-A2A-Protocol': '1.0' }
    });
    return response.json();
  }
  
  async sendMessage(message) {
    const response = await fetch(`${this.baseUrl}/communicate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-A2A-Protocol': '1.0'
      },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'message/send',
        id: Date.now(),
        params: { message }
      })
    });
    return response.json();
  }
}
```

### Cliente Python
```python
import requests

class A2AClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {'X-A2A-Protocol': '1.0'}
    
    def discover(self):
        response = requests.get(f"{self.base_url}/discover", headers=self.headers)
        return response.json()
    
    def send_message(self, message):
        payload = {
            "jsonrpc": "2.0",
            "method": "message/send", 
            "id": "python-client-1",
            "params": {"message": message}
        }
        response = requests.post(
            f"{self.base_url}/communicate",
            json=payload,
            headers={**self.headers, "Content-Type": "application/json"}
        )
        return response.json()
```

---

Esta documentação cobre a especificação completa da API A2A Protocol v2.0 com todos os endpoints, formatos de dados, códigos de erro e exemplos práticos de uso.