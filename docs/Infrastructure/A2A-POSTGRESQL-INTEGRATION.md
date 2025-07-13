# 🗄️ A2A PostgreSQL Integration Guide

## 🎯 **Overview**

Integrate PostgreSQL persistence with the optimized A2A system, extending the BaseA2AServer and CacheManager with enterprise-grade data persistence.

---

## 📊 **Current A2A Architecture + PostgreSQL**

```
BaseA2AServer (Optimized)
├── CacheManager (Redis + Memory)
├── Agent Discovery (/discover)
├── Agent Communication (/communicate) 
└── NEW: PostgreSQL Persistence Layer
    ├── Agent State Persistence
    ├── Task History Storage
    ├── Communication Logs
    └── Performance Metrics
```

---

## 🏗️ **A2A PostgreSQL Schema**

### **Core A2A Tables**

```sql
-- A2A Agent Registry
CREATE TABLE a2a_agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    endpoint VARCHAR(255) NOT NULL,
    capabilities JSONB NOT NULL DEFAULT '[]',
    status VARCHAR(50) DEFAULT 'active', -- active, inactive, error
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    discovery_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- A2A Communication Sessions
CREATE TABLE a2a_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    initiator_agent_id UUID REFERENCES a2a_agents(id),
    target_agent_id UUID REFERENCES a2a_agents(id),
    session_type VARCHAR(50) NOT NULL, -- discover, communicate, delegate
    status VARCHAR(50) DEFAULT 'active', -- active, completed, failed
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'
);

-- A2A Messages Log
CREATE TABLE a2a_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES a2a_sessions(id) ON DELETE CASCADE,
    sender_agent_id UUID REFERENCES a2a_agents(id),
    receiver_agent_id UUID REFERENCES a2a_agents(id),
    message_type VARCHAR(50) NOT NULL, -- request, response, error
    content JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    response_time_ms INTEGER,
    status_code INTEGER
);

-- A2A Task Queue (for delegation)
CREATE TABLE a2a_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES a2a_sessions(id),
    delegator_agent_id UUID REFERENCES a2a_agents(id),
    assigned_agent_id UUID REFERENCES a2a_agents(id),
    task_data JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, in_progress, completed, failed
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    result JSONB,
    error_message TEXT
);

-- A2A Performance Metrics
CREATE TABLE a2a_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES a2a_agents(id),
    metric_type VARCHAR(100) NOT NULL, -- response_time, discovery_latency, error_rate
    metric_value DECIMAL(10,3) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

-- Performance Indexes
CREATE INDEX idx_a2a_agents_status ON a2a_agents(status);
CREATE INDEX idx_a2a_agents_last_seen ON a2a_agents(last_seen DESC);
CREATE INDEX idx_a2a_sessions_status ON a2a_sessions(status);
CREATE INDEX idx_a2a_sessions_started_at ON a2a_sessions(started_at DESC);
CREATE INDEX idx_a2a_messages_timestamp ON a2a_messages(timestamp DESC);
CREATE INDEX idx_a2a_messages_session_id ON a2a_messages(session_id);
CREATE INDEX idx_a2a_tasks_status ON a2a_tasks(status);
CREATE INDEX idx_a2a_tasks_assigned_agent ON a2a_tasks(assigned_agent_id);
CREATE INDEX idx_a2a_metrics_agent_timestamp ON a2a_metrics(agent_id, timestamp DESC);
```

---

## 🔧 **A2A PostgreSQL Manager**

### **Enhanced BaseA2AServer with PostgreSQL**

```javascript
// ui/shared/PostgreSQLA2AServer.js
const BaseA2AServer = require('./BaseA2AServer');
const { Pool } = require('pg');

class PostgreSQLA2AServer extends BaseA2AServer {
  constructor(config = {}) {
    super(config);
    
    this.dbConfig = {
      host: config.db?.host || process.env.POSTGRES_HOST || 'localhost',
      port: config.db?.port || process.env.POSTGRES_PORT || 5432,
      database: config.db?.database || process.env.POSTGRES_DB || 'a2a_system',
      user: config.db?.user || process.env.POSTGRES_USER || 'a2a',
      password: config.db?.password || process.env.POSTGRES_PASSWORD,
      max: config.db?.max || 20,
      idleTimeoutMillis: config.db?.idleTimeout || 30000,
      connectionTimeoutMillis: config.db?.connectionTimeout || 2000,
      ...config.db
    };
    
    this.dbPool = null;
    this.initializeDatabase();
  }

  async initializeDatabase() {
    try {
      this.dbPool = new Pool(this.dbConfig);
      
      // Test connection
      const client = await this.dbPool.connect();
      await client.query('SELECT NOW()');
      client.release();
      
      console.log('✅ PostgreSQL connection established');
      
      // Register this agent in the database
      await this.registerAgent();
      
    } catch (error) {
      console.error('❌ PostgreSQL connection failed:', error);
      // Fallback to in-memory operation
      this.dbPool = null;
    }
  }

  async registerAgent() {
    if (!this.dbPool) return;

    try {
      const discovery = await this.agent.discover();
      
      await this.dbPool.query(`
        INSERT INTO a2a_agents (name, endpoint, capabilities, discovery_data)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (name) 
        DO UPDATE SET 
          endpoint = EXCLUDED.endpoint,
          capabilities = EXCLUDED.capabilities,
          discovery_data = EXCLUDED.discovery_data,
          last_seen = CURRENT_TIMESTAMP,
          updated_at = CURRENT_TIMESTAMP
      `, [
        this.config.agentName,
        `http://localhost:${this.config.port}`,
        JSON.stringify(discovery.capabilities || []),
        JSON.stringify(discovery)
      ]);

      console.log(`📝 Agent ${this.config.agentName} registered in database`);
    } catch (error) {
      console.warn('⚠️  Failed to register agent:', error.message);
    }
  }

  async logCommunication(type, targetAgent, requestData, responseData, responseTime) {
    if (!this.dbPool) return;

    try {
      // Create or get session
      const sessionResult = await this.dbPool.query(`
        INSERT INTO a2a_sessions (initiator_agent_id, session_type, metadata)
        SELECT id, $1, $2 FROM a2a_agents WHERE name = $3
        RETURNING id
      `, [type, JSON.stringify({ target_agent: targetAgent }), this.config.agentName]);

      const sessionId = sessionResult.rows[0]?.id;
      if (!sessionId) return;

      // Log the message
      await this.dbPool.query(`
        INSERT INTO a2a_messages (
          session_id, sender_agent_id, message_type, 
          content, response_time_ms, status_code
        )
        SELECT $1, id, $2, $3, $4, $5
        FROM a2a_agents WHERE name = $6
      `, [
        sessionId,
        type,
        JSON.stringify({ request: requestData, response: responseData }),
        responseTime,
        responseData?.status || 200,
        this.config.agentName
      ]);

      // Record performance metric
      await this.recordMetric('response_time', responseTime);

    } catch (error) {
      console.warn('⚠️  Failed to log communication:', error.message);
    }
  }

  async recordMetric(type, value, metadata = {}) {
    if (!this.dbPool) return;

    try {
      await this.dbPool.query(`
        INSERT INTO a2a_metrics (agent_id, metric_type, metric_value, metadata)
        SELECT id, $1, $2, $3 FROM a2a_agents WHERE name = $4
      `, [type, value, JSON.stringify(metadata), this.config.agentName]);
    } catch (error) {
      console.warn('⚠️  Failed to record metric:', error.message);
    }
  }

  // Override setupRoutes to add PostgreSQL logging
  setupRoutes() {
    super.setupRoutes();

    // Add database statistics endpoint
    this.app.get('/db/stats', async (req, res) => {
      if (!this.dbPool) {
        return res.json({ error: 'Database not connected' });
      }

      try {
        const stats = await this.getDatabaseStats();
        res.json(stats);
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    // Add agent discovery from database
    this.app.get('/agents', async (req, res) => {
      if (!this.dbPool) {
        return res.json({ error: 'Database not connected' });
      }

      try {
        const result = await this.dbPool.query(`
          SELECT name, endpoint, capabilities, status, last_seen
          FROM a2a_agents 
          WHERE status = 'active'
          ORDER BY last_seen DESC
        `);
        
        res.json({
          agents: result.rows,
          timestamp: new Date().toISOString()
        });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });
  }

  async getDatabaseStats() {
    const stats = {};

    try {
      // Agent counts
      const agentStats = await this.dbPool.query(`
        SELECT status, COUNT(*) as count 
        FROM a2a_agents 
        GROUP BY status
      `);
      stats.agents = Object.fromEntries(
        agentStats.rows.map(row => [row.status, parseInt(row.count)])
      );

      // Session stats (last 24h)
      const sessionStats = await this.dbPool.query(`
        SELECT session_type, COUNT(*) as count
        FROM a2a_sessions 
        WHERE started_at > NOW() - INTERVAL '24 hours'
        GROUP BY session_type
      `);
      stats.sessions_24h = Object.fromEntries(
        sessionStats.rows.map(row => [row.session_type, parseInt(row.count)])
      );

      // Performance metrics
      const perfStats = await this.dbPool.query(`
        SELECT 
          metric_type,
          AVG(metric_value) as avg_value,
          MIN(metric_value) as min_value,
          MAX(metric_value) as max_value
        FROM a2a_metrics 
        WHERE timestamp > NOW() - INTERVAL '1 hour'
        GROUP BY metric_type
      `);
      stats.performance_1h = Object.fromEntries(
        perfStats.rows.map(row => [row.metric_type, {
          avg: parseFloat(row.avg_value),
          min: parseFloat(row.min_value),
          max: parseFloat(row.max_value)
        }])
      );

      stats.timestamp = new Date().toISOString();
      return stats;

    } catch (error) {
      throw new Error(`Database stats error: ${error.message}`);
    }
  }

  async stop() {
    // Mark agent as inactive before stopping
    if (this.dbPool) {
      try {
        await this.dbPool.query(`
          UPDATE a2a_agents 
          SET status = 'inactive', updated_at = CURRENT_TIMESTAMP
          WHERE name = $1
        `, [this.config.agentName]);
      } catch (error) {
        console.warn('⚠️  Failed to mark agent as inactive:', error.message);
      }
    }

    await super.stop();
    
    if (this.dbPool) {
      await this.dbPool.end();
    }
  }
}

module.exports = PostgreSQLA2AServer;
```

---

## 🚀 **Usage Example**

### **Migrating to PostgreSQL A2A Server**

```javascript
// Before: Basic A2A Server
const BaseA2AServer = require('../shared/BaseA2AServer');
const MyAgent = require('./agents/my_agent');

const server = new BaseA2AServer({
  port: 8080,
  agentClass: MyAgent,
  agentName: 'My Agent'
});

// After: PostgreSQL-enabled A2A Server
const PostgreSQLA2AServer = require('../shared/PostgreSQLA2AServer');
const MyAgent = require('./agents/my_agent');

const server = new PostgreSQLA2AServer({
  port: 8080,
  agentClass: MyAgent,
  agentName: 'My Agent',
  db: {
    host: 'localhost',
    database: 'a2a_system',
    user: 'a2a_user',
    password: 'secure_password'
  },
  cache: {
    enabled: true,
    redis: null // Use Redis if available
  }
});
```

---

## 📋 **Setup Checklist**

### **1. Database Setup**
```bash
# Create PostgreSQL database
createdb a2a_system

# Run schema creation
psql a2a_system < schemas/a2a_postgresql_schema.sql

# Set environment variables
export POSTGRES_HOST=localhost
export POSTGRES_DB=a2a_system
export POSTGRES_USER=a2a_user
export POSTGRES_PASSWORD=secure_password
```

### **2. Dependencies**
```json
{
  "dependencies": {
    "pg": "^8.11.0",
    "pg-connection-string": "^2.6.0"
  }
}
```

### **3. Configuration Update**
```javascript
// config/a2a-unified.json
{
  "global_defaults": {
    "protocol_version": "1.0",
    "database": {
      "enabled": true,
      "host": "localhost",
      "database": "a2a_system"
    }
  }
}
```

---

## 📊 **New Endpoints**

| Endpoint | Description | Example Response |
|----------|-------------|------------------|
| `GET /db/stats` | Database statistics | Agent counts, session stats, performance |
| `GET /agents` | Active agents from DB | List of registered A2A agents |
| `GET /sessions` | Recent sessions | Communication history |
| `GET /metrics` | Performance metrics | Response times, error rates |

---

## 🔄 **Migration Strategy**

### **Phase 1: Parallel Operation**
- Run both in-memory and PostgreSQL systems
- Compare results for consistency
- Gradual migration of agents

### **Phase 2: Full Migration**
- Switch all agents to PostgreSQL
- Disable in-memory fallbacks
- Monitor performance

### **Phase 3: Optimization**
- Tune database queries
- Implement advanced caching
- Add analytics dashboards

---

## 📈 **Benefits**

- ✅ **Persistent agent discovery**
- ✅ **Communication history tracking**
- ✅ **Performance monitoring**
- ✅ **Task delegation persistence**
- ✅ **Enterprise-grade reliability**
- ✅ **Advanced analytics capabilities**

---

## ⚠️ **Considerations**

- **Performance**: Database calls add latency (~10-50ms)
- **Complexity**: Additional configuration required
- **Dependencies**: PostgreSQL server needed
- **Monitoring**: Database health monitoring required

---

*A2A PostgreSQL Integration - Part of A2A Optimization Suite*  
*Compatible with BaseA2AServer and CacheManager*