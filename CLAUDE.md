# Claude Code Configuration

## Build Commands
- `npm run build`: Build the project
- `npm run test`: Run the full test suite
- `npm run lint`: Run ESLint and format checks
- `npm run typecheck`: Run TypeScript type checking
- `./claude-flow --help`: Show all available commands

## SPARC Orchestration - Regras de Uso no Cursor Agent

### ✅ Status de Integração
**O SPARC Orchestration está totalmente funcional no Cursor Agent com algumas limitações específicas:**

### 🛠️ Comandos que Funcionam Perfeitamente
```bash
# Status e informações do sistema
./claude-flow status
./claude-flow sparc modes
./claude-flow sparc modes --verbose

# Sistema de memória persistente
./claude-flow memory store <key> "<data>"
./claude-flow memory get <key>
./claude-flow memory list
./claude-flow memory stats
./claude-flow memory export <file>
./claude-flow memory import <file>

# Configuração do sistema
./claude-flow config show
./claude-flow config get <key>
./claude-flow config set <key> <value>

# Gerenciamento de agentes (não-interativo)
./claude-flow agent list
./claude-flow agent status
```

### ⚠️ Limitações no Cursor Agent
```bash
# ❌ Comandos que NÃO funcionam (modo interativo/raw terminal):
./claude-flow sparc run ask "<pergunta>"         # Raw mode não suportado
./claude-flow start --ui                         # Interface web interativa
./claude-flow claude chat                        # Chat interativo
./claude-flow repl                               # REPL interativo

# ⚠️ Comandos com limitações:
./claude-flow sparc run <mode> "<task>"          # Alguns modos podem falhar
./claude-flow sparc tdd "<feature>"              # TDD interativo limitado
```

### 🎯 17 Modos SPARC Disponíveis
**Utilize os modos através do arquivo `.roomodes` ou comandos não-interativos:**

#### 🏗️ Core Orchestration (4 modos):
- **orchestrator** - Orquestração multi-agente com TodoWrite/Task/Memory
- **swarm-coordinator** - Coordenação avançada de enxame
- **workflow-manager** - Automação de processos e workflows
- **batch-executor** - Execução paralela de tarefas

#### 🔧 Development Modes (4 modos):
- **coder** - Geração autônoma de código com operações batch
- **architect** - Design de sistemas com coordenação via Memory
- **reviewer** - Revisão de código usando análise batch de arquivos
- **tdd** - Desenvolvimento orientado a testes com planejamento TodoWrite

#### 📊 Analysis & Research (3 modos):
- **researcher** - Pesquisa profunda com WebSearch/WebFetch paralelos
- **analyzer** - Análise de código e dados com processamento batch
- **optimizer** - Otimização de performance com análise sistemática

#### 🎨 Creative & Support (4 modos):
- **designer** - Design UI/UX com coordenação Memory
- **innovator** - Resolução criativa de problemas com WebSearch
- **documenter** - Documentação com operações batch de arquivos
- **debugger** - Debug sistemático com TodoWrite/Memory

#### 🧪 Testing & Quality (2 modos):
- **tester** - Testes abrangentes com execução paralela
- **memory-manager** - Gestão de conhecimento com ferramentas Memory

### 🚀 Boas Práticas para Uso no Cursor
1. **Use sempre comandos não-interativos** para máxima compatibilidade
2. **Aproveite o sistema de memória** para persistir informações entre sessões
3. **Configure modos via `.roomodes`** em vez de comandos interativos
4. **Use TodoWrite extensively** para coordenação de tarefas complexas
5. **Monitore status** com `./claude-flow status` regularmente

### 💾 Sistema de Memória Persistente
**O sistema de memória do SPARC está totalmente funcional e é ideal para:**
```bash
# Armazenar configurações do projeto
./claude-flow memory store "project_config" "A2A + SPARC integration setup"

# Persistir decisões arquiteturais
./claude-flow memory store "architecture" "Microservices with MCP integration"

# Manter histórico de desenvolvimento
./claude-flow memory store "development_log" "Integrated SPARC with existing A2A system"

# Recuperar informações quando necessário
./claude-flow memory get "project_config"
./claude-flow memory stats
```

### 🔗 Integração com Sistema A2A Existente
**O SPARC complementa perfeitamente o sistema A2A:**
- ✅ **Modos de desenvolvimento** para geração de código
- ✅ **Sistema de memória** para coordenação entre agentes
- ✅ **17 modos especializados** para diferentes tipos de tarefa
- ✅ **Configuração via `.roomodes`** para personalização
- ✅ **Compatibilidade total** com comandos não-interativos

### 📁 Arquivos de Configuração Criados
```
.claude/                    # Configurações do Claude-Flow
├── config.json            # Configuração principal
├── settings.json          # Configurações do sistema
└── settings.local.json    # Configurações locais

.roomodes                   # 17 modos SPARC pré-configurados
claude-flow                 # Wrapper script local
memory/                     # Diretório de memória persistente
└── backups/               # Backups automáticos
```

### ⚡ Exemplo de Uso Recomendado
```bash
# 1. Verificar status
./claude-flow status

# 2. Listar modos disponíveis  
./claude-flow sparc modes --verbose

# 3. Usar sistema de memória para coordenação
./claude-flow memory store "current_task" "Integrating SPARC with A2A system"

# 4. Verificar configuração
./claude-flow config show

# 5. Monitorar memória
./claude-flow memory stats
```

## Claude-Flow Complete Command Reference

### Core System Commands
- `./claude-flow start [--ui] [--port 3000] [--host localhost]`: Start orchestration system with optional web UI
- `./claude-flow status`: Show comprehensive system status
- `./claude-flow monitor`: Real-time system monitoring dashboard
- `./claude-flow config <subcommand>`: Configuration management (show, get, set, init, validate)

### Agent Management
- `./claude-flow agent spawn <type> [--name <name>]`: Create AI agents (researcher, coder, analyst, etc.)
- `./claude-flow agent list`: List all active agents
- `./claude-flow spawn <type>`: Quick agent spawning (alias for agent spawn)

### Task Orchestration
- `./claude-flow task create <type> [description]`: Create and manage tasks
- `./claude-flow task list`: View active task queue
- `./claude-flow workflow <file>`: Execute workflow automation files

### Memory Management
- `./claude-flow memory store <key> <data>`: Store persistent data across sessions
- `./claude-flow memory get <key>`: Retrieve stored information
- `./claude-flow memory list`: List all memory keys
- `./claude-flow memory export <file>`: Export memory to file
- `./claude-flow memory import <file>`: Import memory from file
- `./claude-flow memory stats`: Memory usage statistics
- `./claude-flow memory cleanup`: Clean unused memory entries

### SPARC Development Modes
- `./claude-flow sparc "<task>"`: Run orchestrator mode (default)
- `./claude-flow sparc run <mode> "<task>"`: Run specific SPARC mode
- `./claude-flow sparc tdd "<feature>"`: Test-driven development mode
- `./claude-flow sparc modes`: List all 17 available SPARC modes

Available SPARC modes: orchestrator, coder, researcher, tdd, architect, reviewer, debugger, tester, analyzer, optimizer, documenter, designer, innovator, swarm-coordinator, memory-manager, batch-executor, workflow-manager

### Swarm Coordination
- `./claude-flow swarm "<objective>" [options]`: Multi-agent swarm coordination
- `--strategy`: research, development, analysis, testing, optimization, maintenance
- `--mode`: centralized, distributed, hierarchical, mesh, hybrid
- `--max-agents <n>`: Maximum number of agents (default: 5)
- `--parallel`: Enable parallel execution
- `--monitor`: Real-time monitoring
- `--output <format>`: json, sqlite, csv, html

### MCP Server Integration
- `./claude-flow mcp start [--port 3000] [--host localhost]`: Start MCP server
- `./claude-flow mcp status`: Show MCP server status
- `./claude-flow mcp tools`: List available MCP tools

### Claude Integration
- `./claude-flow claude auth`: Authenticate with Claude API
- `./claude-flow claude models`: List available Claude models
- `./claude-flow claude chat`: Interactive chat mode

### Session Management
- `./claude-flow session`: Manage terminal sessions
- `./claude-flow repl`: Start interactive REPL mode

### Enterprise Features
- `./claude-flow project <subcommand>`: Project management (Enterprise)
- `./claude-flow deploy <subcommand>`: Deployment operations (Enterprise)
- `./claude-flow cloud <subcommand>`: Cloud infrastructure management (Enterprise)
- `./claude-flow security <subcommand>`: Security and compliance tools (Enterprise)
- `./claude-flow analytics <subcommand>`: Analytics and insights (Enterprise)

### Project Initialization
- `./claude-flow init`: Initialize Claude-Flow project
- `./claude-flow init --sparc`: Initialize with full SPARC development environment

## Quick Start Workflows

### Research Workflow
```bash
# Start a research swarm with distributed coordination
./claude-flow swarm "Research modern web frameworks" --strategy research --mode distributed --parallel --monitor

# Or use SPARC researcher mode for focused research
./claude-flow sparc run researcher "Analyze React vs Vue vs Angular performance characteristics"

# Store findings in memory for later use
./claude-flow memory store "research_findings" "Key insights from framework analysis"
```

### Development Workflow
```bash
# Start orchestration system with web UI
./claude-flow start --ui --port 3000

# Run TDD workflow for new feature
./claude-flow sparc tdd "User authentication system with JWT tokens"

# Development swarm for complex projects
./claude-flow swarm "Build e-commerce API with payment integration" --strategy development --mode hierarchical --max-agents 8 --monitor

# Check system status
./claude-flow status
```

### Analysis Workflow
```bash
# Analyze codebase performance
./claude-flow sparc run analyzer "Identify performance bottlenecks in current codebase"

# Data analysis swarm
./claude-flow swarm "Analyze user behavior patterns from logs" --strategy analysis --mode mesh --parallel --output sqlite

# Store analysis results
./claude-flow memory store "performance_analysis" "Bottlenecks identified in database queries"
```

### Maintenance Workflow
```bash
# System maintenance with safety controls
./claude-flow swarm "Update dependencies and security patches" --strategy maintenance --mode centralized --monitor

# Security review
./claude-flow sparc run reviewer "Security audit of authentication system"

# Export maintenance logs
./claude-flow memory export maintenance_log.json
```

## Integration Patterns

### Memory-Driven Coordination
Use Memory to coordinate information across multiple SPARC modes and swarm operations:

```bash
# Store architecture decisions
./claude-flow memory store "system_architecture" "Microservices with API Gateway pattern"

# All subsequent operations can reference this decision
./claude-flow sparc run coder "Implement user service based on system_architecture in memory"
./claude-flow sparc run tester "Create integration tests for microservices architecture"
```

### Multi-Stage Development
Coordinate complex development through staged execution:

```bash
# Stage 1: Research and planning
./claude-flow sparc run researcher "Research authentication best practices"
./claude-flow sparc run architect "Design authentication system architecture"

# Stage 2: Implementation
./claude-flow sparc tdd "User registration and login functionality"
./claude-flow sparc run coder "Implement JWT token management"

# Stage 3: Testing and deployment
./claude-flow sparc run tester "Comprehensive security testing"
./claude-flow swarm "Deploy authentication system" --strategy maintenance --mode centralized
```

### Enterprise Integration
For enterprise environments with additional tooling:

```bash
# Project management integration
./claude-flow project create "authentication-system"
./claude-flow project switch "authentication-system"

# Security compliance
./claude-flow security scan
./claude-flow security audit

# Analytics and monitoring
./claude-flow analytics dashboard
./claude-flow deploy production --monitor
```

## Advanced Batch Tool Patterns

### TodoWrite Coordination
Always use TodoWrite for complex task coordination:

```javascript
TodoWrite([
  {
    id: "architecture_design",
    content: "Design system architecture and component interfaces",
    status: "pending",
    priority: "high",
    dependencies: [],
    estimatedTime: "60min",
    assignedAgent: "architect"
  },
  {
    id: "frontend_development", 
    content: "Develop React components and user interface",
    status: "pending",
    priority: "medium",
    dependencies: ["architecture_design"],
    estimatedTime: "120min",
    assignedAgent: "frontend_team"
  }
]);
```

### Task and Memory Integration
Launch coordinated agents with shared memory:

```javascript
// Store architecture in memory
Task("System Architect", "Design architecture and store specs in Memory");

// Other agents use memory for coordination
Task("Frontend Team", "Develop UI using Memory architecture specs");
Task("Backend Team", "Implement APIs according to Memory specifications");
```

## Code Style Preferences
- Use ES modules (import/export) syntax
- Destructure imports when possible
- Use TypeScript for all new code
- Follow existing naming conventions
- Add JSDoc comments for public APIs
- Use async/await instead of Promise chains
- Prefer const/let over var

## Workflow Guidelines
- Always run typecheck after making code changes
- Run tests before committing changes
- Use meaningful commit messages
- Create feature branches for new functionality
- Ensure all tests pass before merging

## Important Notes
- **Use TodoWrite extensively** for all complex task coordination
- **Leverage Task tool** for parallel agent execution on independent work
- **Store all important information in Memory** for cross-agent coordination
- **Use batch file operations** whenever reading/writing multiple files
- **Check .claude/commands/** for detailed command documentation
- **All swarm operations include automatic batch tool coordination**
- **Monitor progress** with TodoRead during long-running operations
- **Enable parallel execution** with --parallel flags for maximum efficiency

This configuration ensures optimal use of Claude Code's batch tools for swarm orchestration and parallel task execution with full Claude-Flow capabilities.
