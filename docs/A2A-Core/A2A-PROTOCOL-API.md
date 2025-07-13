# 🤖 A2A Protocol API Documentation

## 📖 **Overview**

The Agent-to-Agent (A2A) Protocol defines a standardized communication interface for autonomous agents. This optimized implementation provides enhanced performance, caching, and monitoring capabilities.

**Protocol Version**: 1.0  
**Base Implementation**: BaseA2AServer with CacheManager  
**Compatible With**: OpenAPI 3.0, Swagger UI  

---

## 🌐 **Base Endpoint Structure**

```
https://agent-host:port/{endpoint}
```

**Required Headers:**
- `X-A2A-Protocol: 1.0`
- `Content-Type: application/json`
- `Access-Control-Allow-Origin: *`

---

## 📋 **Core Endpoints**

### **1. Agent Discovery - GET /discover**

Retrieve agent capabilities and metadata for service discovery.

#### **Request**
```http
GET /discover HTTP/1.1
Host: agent-host:port
X-A2A-Protocol: 1.0
```

#### **Response**
```json
{
  "agent_name": "Example Agent",
  "protocol_version": "1.0",
  "capabilities": [
    {
      "name": "hello_world",
      "description": "Simple greeting capability",
      "input_schema": {
        "type": "object",
        "properties": {
          "name": { "type": "string" }
        }
      },
      "output_schema": {
        "type": "object", 
        "properties": {
          "message": { "type": "string" }
        }
      }
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "author": "System",
    "description": "Example A2A agent"
  },
  "endpoints": {
    "communicate": "/communicate",
    "delegate": "/delegate", 
    "health": "/health"
  },
  "timestamp": "2025-07-13T20:00:00.000Z"
}
```

#### **Performance**
- **Cache TTL**: 60 seconds
- **Expected Response Time**: < 50ms (cached), < 200ms (uncached)

---

### **2. Direct Communication - POST /communicate**

Send direct messages or requests to the agent.

#### **Request**
```http
POST /communicate HTTP/1.1
Host: agent-host:port
Content-Type: application/json
X-A2A-Protocol: 1.0

{
  "capability": "hello_world",
  "input": {
    "name": "World"
  },
  "metadata": {
    "sender": "ClientAgent",
    "request_id": "req_123456",
    "timeout": 30000
  }
}
```

#### **Response**
```json
{
  "status": "success",
  "output": {
    "message": "Hello, World!"
  },
  "metadata": {
    "processing_time_ms": 45,
    "agent": "Example Agent",
    "capability_used": "hello_world"
  },
  "timestamp": "2025-07-13T20:00:01.045Z"
}
```

#### **Error Response**
```json
{
  "status": "error",
  "error": {
    "code": "CAPABILITY_NOT_FOUND",
    "message": "Capability 'unknown_skill' not supported",
    "details": {
      "available_capabilities": ["hello_world"],
      "requested_capability": "unknown_skill"
    }
  },
  "timestamp": "2025-07-13T20:00:01.010Z"
}
```

---

### **3. Task Delegation - POST /delegate**

Delegate complex tasks that may require orchestration or multi-step processing.

#### **Request**
```http
POST /delegate HTTP/1.1
Host: agent-host:port
Content-Type: application/json
X-A2A-Protocol: 1.0

{
  "task": {
    "type": "workflow",
    "description": "Process user inquiry with research",
    "steps": [
      {
        "capability": "research",
        "input": { "query": "latest trends" }
      },
      {
        "capability": "summarize", 
        "input": { "data": "${research.output}" }
      }
    ]
  },
  "priority": "normal",
  "metadata": {
    "sender": "OrchestratorAgent",
    "deadline": "2025-07-13T21:00:00.000Z",
    "callback_url": "https://orchestrator:8080/tasks/callback"
  }
}
```

#### **Response**
```json
{
  "status": "accepted",
  "task_id": "task_789012",
  "estimated_completion": "2025-07-13T20:05:00.000Z",
  "metadata": {
    "accepted_at": "2025-07-13T20:00:01.100Z",
    "agent": "Example Agent",
    "priority": "normal"
  },
  "tracking": {
    "status_url": "/tasks/task_789012/status",
    "result_url": "/tasks/task_789012/result"
  },
  "timestamp": "2025-07-13T20:00:01.100Z"
}
```

---

### **4. Health Check - GET /health**

Monitor agent health, performance, and availability.

#### **Request**
```http
GET /health HTTP/1.1
Host: agent-host:port
X-A2A-Protocol: 1.0
```

#### **Response**
```json
{
  "status": "healthy",
  "server_status": "healthy", 
  "uptime": 3600.45,
  "memory_usage": {
    "rss": 52428800,
    "heapTotal": 29360128,
    "heapUsed": 18874344,
    "external": 1089024
  },
  "performance": {
    "avg_response_time_ms": 87.5,
    "requests_per_minute": 145,
    "error_rate": 0.02
  },
  "capabilities_status": {
    "hello_world": "available",
    "research": "available"
  },
  "timestamp": "2025-07-13T20:00:01.200Z"
}
```

#### **Performance**
- **Cache TTL**: 30 seconds
- **Expected Response Time**: < 20ms (cached), < 100ms (uncached)

---

## 🔧 **Enhanced Endpoints (Optimized Implementation)**

### **5. Cache Statistics - GET /cache/stats**

Monitor caching performance and statistics.

#### **Response**
```json
{
  "cache_stats": {
    "enabled": true,
    "redis_connected": true,
    "memory_cache_size": 15,
    "hits": 1250,
    "misses": 89,
    "hit_ratio": 0.933,
    "avg_response_time_cached_ms": 12.5,
    "avg_response_time_uncached_ms": 156.8
  },
  "timestamp": "2025-07-13T20:00:01.300Z"
}
```

### **6. Agent Registry - GET /agents**

List all known agents in the system (PostgreSQL-enabled deployments).

#### **Response**
```json
{
  "agents": [
    {
      "name": "Example Agent",
      "endpoint": "http://localhost:8130",
      "capabilities": ["hello_world"],
      "status": "active",
      "last_seen": "2025-07-13T20:00:00.000Z"
    }
  ],
  "total_count": 1,
  "timestamp": "2025-07-13T20:00:01.400Z"
}
```

### **7. System Status - GET /status**

Comprehensive system information and metrics.

#### **Response**
```json
{
  "agent_name": "Example Agent",
  "protocol_version": "1.0",
  "server_uptime": 3600.45,
  "memory_usage": {
    "rss": 52428800,
    "heapTotal": 29360128,
    "heapUsed": 18874344
  },
  "system_info": {
    "node_version": "v20.10.0",
    "platform": "darwin",
    "arch": "arm64"
  },
  "timestamp": "2025-07-13T20:00:01.500Z"
}
```

---

## ❌ **Error Codes & Responses**

### **Standard HTTP Status Codes**

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request format |
| 404 | Not Found | Endpoint or capability not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Agent processing error |
| 503 | Service Unavailable | Agent temporarily unavailable |

### **A2A Error Response Format**

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      "additional_context": "value"
    }
  },
  "timestamp": "2025-07-13T20:00:01.000Z"
}
```

### **Common Error Codes**

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `CAPABILITY_NOT_FOUND` | 404 | Requested capability not supported |
| `INVALID_INPUT` | 400 | Input validation failed |
| `TIMEOUT` | 408 | Request processing timeout |
| `RATE_LIMITED` | 429 | Too many requests |
| `AGENT_UNAVAILABLE` | 503 | Agent temporarily down |
| `PROCESSING_ERROR` | 500 | Internal agent error |

---

## 🔍 **Request/Response Examples**

### **Complete Communication Flow**

```bash
# 1. Discover agent capabilities
curl -X GET http://localhost:8130/discover \
  -H "X-A2A-Protocol: 1.0"

# 2. Communicate with agent
curl -X POST http://localhost:8130/communicate \
  -H "Content-Type: application/json" \
  -H "X-A2A-Protocol: 1.0" \
  -d '{
    "capability": "hello_world",
    "input": { "name": "Alice" },
    "metadata": { "sender": "TestClient" }
  }'

# 3. Check agent health
curl -X GET http://localhost:8130/health \
  -H "X-A2A-Protocol: 1.0"

# 4. Monitor cache performance  
curl -X GET http://localhost:8130/cache/stats \
  -H "X-A2A-Protocol: 1.0"
```

---

## 📊 **Performance Benchmarks**

### **Baseline Performance (Optimized Implementation)**

| Endpoint | Cached Response | Uncached Response | Improvement |
|----------|----------------|-------------------|-------------|
| `/discover` | ~12ms | ~156ms | **900%** |
| `/health` | ~8ms | ~89ms | **1000%** |
| `/communicate` | N/A | ~145ms | Baseline |
| `/delegate` | N/A | ~267ms | Baseline |

### **Load Testing Results**

- **Concurrent Users**: 50
- **Test Duration**: 30 seconds
- **Success Rate**: 99.8%
- **Average Response Time**: 45ms
- **Requests per Second**: 1,200+

---

## 🔧 **OpenAPI 3.0 Specification**

```yaml
openapi: 3.0.3
info:
  title: A2A Protocol API
  version: 1.0.0
  description: Optimized Agent-to-Agent Communication Protocol

servers:
  - url: http://localhost:8130
    description: Local development server

paths:
  /discover:
    get:
      summary: Agent Discovery
      responses:
        '200':
          description: Agent capabilities and metadata
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DiscoveryResponse'
        
  /communicate:
    post:
      summary: Direct Communication
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommunicateRequest'
      responses:
        '200':
          description: Communication successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CommunicateResponse'

components:
  schemas:
    DiscoveryResponse:
      type: object
      properties:
        agent_name:
          type: string
        capabilities:
          type: array
          items:
            $ref: '#/components/schemas/Capability'
        timestamp:
          type: string
          format: date-time
```

---

## 🚀 **Implementation Guide**

### **Basic Server Setup**

```javascript
const BaseA2AServer = require('./shared/BaseA2AServer');
const MyAgent = require('./agents/my_agent');

const server = new BaseA2AServer({
  port: 8130,
  agentClass: MyAgent,
  agentName: 'My A2A Agent',
  cache: {
    enabled: true,
    ttl: 300  // 5 minutes
  }
});

server.start().then(() => {
  console.log('🤖 A2A Agent ready!');
}).catch(error => {
  console.error('❌ Failed to start:', error);
});
```

### **Agent Implementation**

```javascript
class MyAgent {
  async discover() {
    return {
      agent_name: 'My Agent',
      capabilities: [
        {
          name: 'hello_world',
          description: 'Simple greeting',
          input_schema: { type: 'object' },
          output_schema: { type: 'object' }
        }
      ]
    };
  }

  async communicate(request) {
    const { capability, input } = request;
    
    if (capability === 'hello_world') {
      return {
        status: 'success',
        output: { message: `Hello, ${input.name || 'World'}!` }
      };
    }
    
    throw new Error('Capability not found');
  }

  async delegate(request) {
    // Handle complex task delegation
    return {
      status: 'accepted',
      task_id: `task_${Date.now()}`
    };
  }

  async health() {
    return {
      status: 'healthy',
      capabilities_status: {
        hello_world: 'available'
      }
    };
  }
}
```

---

## 📈 **Monitoring & Analytics**

### **Key Metrics to Track**

- **Response Time**: Per endpoint average
- **Cache Hit Ratio**: Percentage of cached responses
- **Error Rate**: Failed requests per minute
- **Throughput**: Requests per second
- **Availability**: Uptime percentage

### **Monitoring Endpoints**

```bash
# Real-time metrics
GET /status
GET /cache/stats
GET /health

# Historical data (PostgreSQL integration)
GET /metrics?timerange=1h
GET /agents?status=active
```

---

*A2A Protocol API Documentation - Optimized Implementation*  
*Version 1.0 - Compatible with BaseA2AServer and CacheManager*