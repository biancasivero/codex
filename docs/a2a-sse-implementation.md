# Server-Sent Events (SSE) no Protocolo A2A

## Visão Geral

O Server-Sent Events (SSE) é um dos quatro modos de interação do protocolo A2A, específicamente projetado para permitir comunicação em tempo real entre agentes com fluxo contínuo de dados. Esta implementação é fundamental para tarefas de longa duração que requerem atualizações de progresso em tempo real.

## Arquitetura SSE no A2A

### Componentes Principais

1. **A2AServer**: Servidor FastAPI que gerencia endpoints A2A
2. **TaskManager**: Gerencia tarefas e subscribers SSE
3. **EventSourceResponse**: Resposta HTTP para streaming de eventos
4. **A2AClient**: Cliente que consome streams SSE

### Fluxo de Dados

```
Cliente → SendTaskStreamingRequest → TaskManager → SSE Queue → EventSourceResponse → Cliente
```

## Implementação Detalhada

### 1. Configuração do Servidor

```python
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
from common.types import AgentCapabilities, AgentCard

# Configuração do Agent Card com streaming habilitado
capabilities = AgentCapabilities(streaming=True)
agent_card = AgentCard(
    name="HostAgent",
    description="Host agent with SSE support",
    capabilities=capabilities,
    defaultInputModes=["text", "text/plain"],
    defaultOutputModes=["text", "text/plain"]
)

# Servidor A2A com suporte a SSE
class A2AServer:
    def __init__(self, host="0.0.0.0", port=5000, agent_card: AgentCard = None):
        self.app = FastAPI()
        self.agent_card = agent_card
        self.task_manager = TaskManager()
        
        # Endpoint para processar requests A2A
        self.app.add_route("/", self._process_request, methods=["POST"])
        self.app.add_route("/.well-known/agent.json", self._get_agent_card, methods=["GET"])
```

### 2. Gerenciamento de Subscribers SSE

```python
import asyncio
from typing import AsyncIterable, List
from common.types import SendTaskStreamingResponse, TaskStatusUpdateEvent

class TaskManager:
    def __init__(self):
        self.tasks: dict[str, Task] = {}
        self.task_sse_subscribers: dict[str, List[asyncio.Queue]] = {}
        self.subscriber_lock = asyncio.Lock()

    async def setup_sse_consumer(self, task_id: str, is_resubscribe: bool = False):
        """Configura um novo consumer SSE para uma tarefa"""
        async with self.subscriber_lock:
            if task_id not in self.task_sse_subscribers:
                if is_resubscribe:
                    raise ValueError("Task not found for resubscription")
                else:
                    self.task_sse_subscribers[task_id] = []

            # Criar queue ilimitada para eventos SSE
            sse_event_queue = asyncio.Queue(maxsize=0)
            self.task_sse_subscribers[task_id].append(sse_event_queue)
            return sse_event_queue

    async def enqueue_events_for_sse(self, task_id: str, task_update_event):
        """Envia evento para todos os subscribers de uma tarefa"""
        async with self.subscriber_lock:
            if task_id not in self.task_sse_subscribers:
                return

            current_subscribers = self.task_sse_subscribers[task_id]
            for subscriber in current_subscribers:
                await subscriber.put(task_update_event)

    async def dequeue_events_for_sse(
        self, request_id: str, task_id: str, sse_event_queue: asyncio.Queue
    ) -> AsyncIterable[SendTaskStreamingResponse]:
        """Consome eventos da queue e envia via SSE"""
        try:
            while True:
                event = await sse_event_queue.get()
                
                if isinstance(event, JSONRPCError):
                    yield SendTaskStreamingResponse(id=request_id, error=event)
                    break
                
                yield SendTaskStreamingResponse(id=request_id, result=event)
                
                # Finaliza stream quando tarefa termina
                if isinstance(event, TaskStatusUpdateEvent) and event.final:
                    break
        finally:
            # Remove subscriber ao finalizar
            async with self.subscriber_lock:
                if task_id in self.task_sse_subscribers:
                    self.task_sse_subscribers[task_id].remove(sse_event_queue)
```

### 3. Endpoint SSE

```python
from starlette.requests import Request
from starlette.responses import JSONResponse

class A2AServer:
    async def _process_request(self, request: Request):
        try:
            body = await request.json()
            json_rpc_request = A2ARequest.validate_python(body)

            # Processa requisição de streaming
            if isinstance(json_rpc_request, SendTaskStreamingRequest):
                result = await self.task_manager.on_send_task_subscribe(json_rpc_request)
                return self._create_response(result)
            
            # Outros tipos de requisição...
            
        except Exception as e:
            return self._handle_exception(e)

    def _create_response(self, result: Any) -> JSONResponse | EventSourceResponse:
        if isinstance(result, AsyncIterable):
            # Gerador de eventos SSE
            async def event_generator(result) -> AsyncIterable[dict[str, str]]:
                async for item in result:
                    yield {"data": item.model_dump_json(exclude_none=True)}

            return EventSourceResponse(event_generator(result))
        elif isinstance(result, JSONRPCResponse):
            return JSONResponse(result.model_dump(exclude_none=True))
        else:
            raise ValueError(f"Unexpected result type: {type(result)}")
```

### 4. Processamento de Streaming Request

```python
from common.types import SendTaskStreamingRequest, TaskSendParams

class TaskManager:
    async def on_send_task_subscribe(
        self, request: SendTaskStreamingRequest
    ) -> AsyncIterable[SendTaskStreamingResponse]:
        """Processa requisição de streaming e configura SSE"""
        
        task_params: TaskSendParams = request.params
        
        # Criar nova tarefa
        task = await self.create_task(task_params)
        task_id = task.id
        
        # Configurar consumer SSE
        sse_event_queue = await self.setup_sse_consumer(task_id)
        
        # Executar tarefa de forma assíncrona
        asyncio.create_task(self.execute_task_with_updates(task))
        
        # Retornar stream de eventos
        return self.dequeue_events_for_sse(request.id, task_id, sse_event_queue)

    async def execute_task_with_updates(self, task: Task):
        """Executa tarefa e envia atualizações via SSE"""
        task_id = task.id
        
        try:
            # Simular processamento com atualizações
            for progress in [25, 50, 75, 100]:
                await asyncio.sleep(1)  # Simular trabalho
                
                # Criar evento de progresso
                progress_event = TaskStatusUpdateEvent(
                    task_id=task_id,
                    progress=progress,
                    message=f"Processando... {progress}%",
                    final=(progress == 100)
                )
                
                # Enviar para todos os subscribers
                await self.enqueue_events_for_sse(task_id, progress_event)
                
        except Exception as e:
            # Enviar erro via SSE
            error_event = TaskErrorEvent(task_id=task_id, error=str(e))
            await self.enqueue_events_for_sse(task_id, error_event)
```

## Cliente SSE

### Implementação Python

```python
import httpx
from httpx_sse import connect_sse
from typing import AsyncIterable
import json

class A2AClient:
    def __init__(self, url: str):
        self.url = url

    async def send_task_streaming(
        self, payload: dict[str, Any]
    ) -> AsyncIterable[SendTaskStreamingResponse]:
        """Envia tarefa e recebe atualizações via SSE"""
        
        request = SendTaskStreamingRequest(params=payload)
        
        with httpx.Client(timeout=None) as client:
            with connect_sse(
                client, "POST", self.url, json=request.model_dump()
            ) as event_source:
                try:
                    for sse in event_source.iter_sse():
                        response = SendTaskStreamingResponse(**json.loads(sse.data))
                        yield response
                        
                        # Parar quando tarefa finalizar
                        if (response.result and 
                            isinstance(response.result, TaskStatusUpdateEvent) and
                            response.result.final):
                            break
                            
                except json.JSONDecodeError as e:
                    raise A2AClientJSONError(str(e)) from e
                except httpx.RequestError as e:
                    raise A2AClientHTTPError(400, str(e)) from e
```

### Uso do Cliente

```python
async def main():
    client = A2AClient("http://localhost:10008")
    
    # Payload da tarefa
    task_payload = {
        "id": "task-123",
        "type": "document_analysis",
        "content": "Analyze this large document..."
    }
    
    # Processar com streaming
    async for update in client.send_task_streaming(task_payload):
        if update.error:
            print(f"Erro: {update.error}")
            break
        elif update.result:
            if isinstance(update.result, TaskStatusUpdateEvent):
                print(f"Progresso: {update.result.progress}% - {update.result.message}")
                
                if update.result.final:
                    print("Tarefa completada!")
                    break
```

## Implementação JavaScript/Frontend

```javascript
// Conectar ao endpoint SSE
const eventSource = new EventSource('/api/a2a/stream');

// Handler para eventos de progresso
eventSource.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    
    if (data.error) {
        console.error('Erro:', data.error);
        eventSource.close();
        return;
    }
    
    if (data.result) {
        const result = data.result;
        
        // Atualizar UI com progresso
        if (result.progress !== undefined) {
            updateProgressBar(result.progress);
            showStatusMessage(result.message);
        }
        
        // Finalizar quando tarefa completar
        if (result.final) {
            console.log('Tarefa completada!');
            eventSource.close();
        }
    }
});

// Handler para erros de conexão
eventSource.addEventListener('error', (event) => {
    console.error('Erro na conexão SSE:', event);
    eventSource.close();
});

// Função para atualizar barra de progresso
function updateProgressBar(progress) {
    const progressBar = document.getElementById('progress-bar');
    progressBar.style.width = `${progress}%`;
    progressBar.textContent = `${progress}%`;
}

// Função para mostrar mensagem de status
function showStatusMessage(message) {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = message;
}
```

## Tipos de Eventos SSE

### 1. TaskStatusUpdateEvent
```python
class TaskStatusUpdateEvent:
    task_id: str
    progress: int  # 0-100
    message: str
    final: bool    # True quando tarefa finalizar
    timestamp: str
```

### 2. TaskArtifactUpdateEvent
```python
class TaskArtifactUpdateEvent:
    task_id: str
    artifact_id: str
    artifact_type: str  # "text", "image", "file"
    content: str
    metadata: dict
```

### 3. TaskErrorEvent
```python
class TaskErrorEvent:
    task_id: str
    error_code: str
    error_message: str
    timestamp: str
```

## Vantagens da Implementação SSE

### 1. **Performance**
- Conexão HTTP persistente
- Menor overhead que WebSockets
- Suporte nativo a reconexão automática

### 2. **Simplicidade**
- Protocolo HTTP padrão
- Fácil implementação no frontend
- Compatível com proxies e load balancers

### 3. **Escalabilidade**
- Suporte a múltiplos subscribers por tarefa
- Gerenciamento eficiente de memória
- Limpeza automática de subscribers

### 4. **Confiabilidade**
- Garantia de ordem de eventos
- Suporte a retry automático
- Tratamento robusto de erros

## Considerações de Produção

### 1. **Gerenciamento de Recursos**
```python
# Configurar limites para evitar memory leaks
MAX_SUBSCRIBERS_PER_TASK = 100
MAX_QUEUE_SIZE = 1000
CONNECTION_TIMEOUT = 30  # segundos

# Cleanup periódico de subscribers órfãos
async def cleanup_stale_subscribers():
    current_time = time.time()
    for task_id, subscribers in self.task_sse_subscribers.items():
        for subscriber in subscribers[:]:  # Criar cópia para iterar
            if current_time - subscriber.last_activity > CONNECTION_TIMEOUT:
                subscribers.remove(subscriber)
```

### 2. **Monitoramento**
```python
import logging
from prometheus_client import Counter, Histogram, Gauge

# Métricas
sse_connections_total = Counter('sse_connections_total', 'Total SSE connections')
sse_events_sent_total = Counter('sse_events_sent_total', 'Total SSE events sent')
sse_connection_duration = Histogram('sse_connection_duration_seconds', 'SSE connection duration')
active_sse_connections = Gauge('active_sse_connections', 'Active SSE connections')

# Logging
logger = logging.getLogger(__name__)

class TaskManager:
    async def setup_sse_consumer(self, task_id: str):
        sse_connections_total.inc()
        active_sse_connections.inc()
        logger.info(f"New SSE connection for task {task_id}")
        
        # ... implementação
```

### 3. **Segurança**
```python
# Autenticação para conexões SSE
async def authenticate_sse_request(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPException(401, "Missing authentication")
    
    # Validar token
    token = auth_header.replace('Bearer ', '')
    if not validate_jwt_token(token):
        raise HTTPException(401, "Invalid token")

# Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@limiter.limit("10/minute")
async def process_sse_request(request: Request):
    # ... processamento
```

## Casos de Uso Práticos

### 1. **Análise de Documentos**
- Upload de PDF grande
- Atualizações de progresso de OCR
- Resultados parciais de análise

### 2. **Processamento de Imagens**
- Geração de imagens por IA
- Filtros e transformações
- Feedback visual em tempo real

### 3. **Workflows Complexos**
- Orquestração de múltiplos agentes
- Estados de execução
- Logs de processamento

### 4. **Integração com Sistemas Legados**
- Migração de dados
- Sincronização de sistemas
- Relatórios de progresso

## Troubleshooting

### 1. **Conexões Órfãs**
```python
# Detectar e limpar conexões órfãs
async def health_check_subscribers():
    for task_id, subscribers in self.task_sse_subscribers.items():
        for subscriber in subscribers[:]:
            try:
                # Testar se subscriber ainda está ativo
                await subscriber.put(HealthCheckEvent())
            except:
                # Remover subscriber inativo
                subscribers.remove(subscriber)
```

### 2. **Memory Leaks**
```python
# Monitorar uso de memória
import psutil

def monitor_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    
    if memory_info.rss > MAX_MEMORY_THRESHOLD:
        logger.warning(f"High memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
        # Implementar limpeza agressiva
```

### 3. **Reconexão Automática**
```javascript
// Cliente JavaScript com reconexão
class ReconnectingEventSource {
    constructor(url, options = {}) {
        this.url = url;
        this.options = options;
        this.reconnectInterval = 5000; // 5 segundos
        this.maxReconnectAttempts = 10;
        this.reconnectAttempts = 0;
        this.connect();
    }
    
    connect() {
        this.eventSource = new EventSource(this.url);
        
        this.eventSource.onopen = () => {
            this.reconnectAttempts = 0;
            console.log('SSE conectado');
        };
        
        this.eventSource.onerror = () => {
            this.eventSource.close();
            this.attemptReconnect();
        };
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Tentativa de reconexão ${this.reconnectAttempts}`);
            
            setTimeout(() => {
                this.connect();
            }, this.reconnectInterval);
        }
    }
}
```

## Conclusão

A implementação SSE no protocolo A2A oferece uma solução robusta e escalável para comunicação em tempo real entre agentes. A arquitetura baseada em queues assíncronas, combinada com o padrão EventSource, permite:

- **Feedback em tempo real** para operações longas
- **Escalabilidade** para múltiplos clientes simultâneos
- **Confiabilidade** com reconexão automática
- **Simplicidade** de implementação e manutenção

Esta implementação serve como base sólida para sistemas de agentes A2A que requerem interação contínua e atualizações de progresso em tempo real.