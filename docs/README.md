# 📚 Documentação do Projeto - Organizada por Clusters SPARC

> **🔄 Reorganização SPARC:** 77 documentos categorizados e organizados em estrutura modular otimizada

## 🎯 **Overview**

Esta documentação foi **completamente reorganizada** usando **SPARC Orchestration** em 6 clusters temáticos principais + suporte, facilitando a navegação e manutenção do sistema integrado de agentes que combina:

- **Sistema A2A (Agent-to-Agent)**: Comunicação otimizada com BaseA2AServer e cache
- **SPARC Orchestration**: 17 modos especializados para desenvolvimento e análise
- **MCP Integration**: Model Context Protocol com ferramentas avançadas
- **Infrastructure**: PostgreSQL, Docker e monitoramento enterprise

## 📂 **Estrutura de Clusters**

A documentação está organizada em **6 clusters principais + suporte** com **77 documentos** reorganizados:

### **🚀 1. A2A Core** - Sistema Principal
📁 [`A2A-Core/`](./A2A-Core/) - **10 documentos**

**Arquitetura, API e componentes principais do sistema A2A otimizado**

| Documento | Descrição |
|-----------|-----------|
| [A2A-ARCHITECTURE.md](./A2A-Core/A2A-ARCHITECTURE.md) | Arquitetura completa do sistema A2A |
| [A2A-PROTOCOL-API.md](./A2A-Core/A2A-PROTOCOL-API.md) | Especificação técnica da API A2A |
| [A2A-MIGRATION-GUIDE.md](./A2A-Core/A2A-MIGRATION-GUIDE.md) | Guia de migração para BaseA2AServer |
| [A2A-UNIFIED-SYSTEM.md](./A2A-Core/A2A-UNIFIED-SYSTEM.md) | Sistema unificado A2A |

---

### **🔌 2. MCP Integration** - Integrações MCP  
📁 [`MCP-Integration/`](./MCP-Integration/) - **8 documentos**

**Model Context Protocol, ferramentas e bridges**

| Documento | Descrição |
|-----------|-----------|
| [MCP_TOOLS_INTEGRATION.md](./MCP-Integration/MCP_TOOLS_INTEGRATION.md) | Integração de ferramentas MCP |
| [CLAUDE_CODE_A2A_BRIDGE_MCP_TOOLS.md](./MCP-Integration/CLAUDE_CODE_A2A_BRIDGE_MCP_TOOLS.md) | Bridge Claude Code ↔ A2A |
| [DIEGOTOOLS_INTEGRATION.md](./MCP-Integration/DIEGOTOOLS_INTEGRATION.md) | Integração Diego Tools |

---

### **🤖 3. Agent Systems** - Sistemas de Agentes
📁 [`Agent-Systems/`](./Agent-Systems/) - **13 documentos**

**Orchestrator, agentes especializados e sistemas autônomos**

| Documento | Descrição |
|-----------|-----------|
| [ORCHESTRATOR_AGENT_GUIDE.md](./Agent-Systems/ORCHESTRATOR_AGENT_GUIDE.md) | Guia completo do Orchestrator |
| [GUARDIAN-SISTEMA-COMPLETO.md](./Agent-Systems/GUARDIAN-SISTEMA-COMPLETO.md) | Sistema Guardian completo |
| [AGENTE-ORGANIZADOR-AUTONOMO.md](./Agent-Systems/AGENTE-ORGANIZADOR-AUTONOMO.md) | Agente organizador autônomo |

---

### **🏗️ 4. Infrastructure** - Infraestrutura
📁 [`Infrastructure/`](./Infrastructure/) - **11 documentos**

**Docker, deployment, banco de dados e monitoramento**

| Documento | Descrição |
|-----------|-----------|
| [A2A-POSTGRESQL-INTEGRATION.md](./Infrastructure/A2A-POSTGRESQL-INTEGRATION.md) | Integração PostgreSQL A2A |
| [DOCKER-COMPOSE-UNIFICADO.md](./Infrastructure/DOCKER-COMPOSE-UNIFICADO.md) | Docker Compose unificado |
| [ENHANCED-MONITOR-GUIDE.md](./Infrastructure/ENHANCED-MONITOR-GUIDE.md) | Guia de monitoramento avançado |

---

### **📖 5. Guides & Tutorials** - Guias e Tutoriais
📁 [`Guides-Tutorials/`](./Guides-Tutorials/) - **16 documentos**

**Documentação de uso, configuração e procedimentos**

| Documento | Descrição |
|-----------|-----------|
| [GUIA_COMPLETO_PARA_LEIGOS.md](./Guides-Tutorials/GUIA_COMPLETO_PARA_LEIGOS.md) | Guia completo para iniciantes |
| [CONFIGURACAO_COMPLETA.md](./Guides-Tutorials/CONFIGURACAO_COMPLETA.md) | Configuração completa do sistema |
| [COMANDOS_RAPIDOS.md](./Guides-Tutorials/COMANDOS_RAPIDOS.md) | Comandos rápidos de uso |

---

### **📦 6. Legacy** - Arquivos Históricos
📁 [`Legacy/`](./Legacy/) - **8 documentos**

**Documentos de versões anteriores e otimizações concluídas**

| Documento | Descrição |
|-----------|-----------|
| [A2A-OPTIMIZATION-FINAL-REPORT.md](./Legacy/A2A-OPTIMIZATION-FINAL-REPORT.md) | Relatório final otimização A2A |
| [A2A-OPTIMIZATION-COMPLETE.md](./Legacy/A2A-OPTIMIZATION-COMPLETE.md) | Otimização A2A completa |

---

### **🛠️ 7. Support** - Documentos de Suporte
📁 [`Support/`](./Support/) - **15 documentos**

**Configurações, reports e documentos auxiliares**

| Documento | Descrição |
|-----------|-----------|
| [CLAUDE.md](./Support/CLAUDE.md) | Configuração Claude Code |
| [UNIVERSAL-ORGANIZATION-GUIDE.md](./Support/UNIVERSAL-ORGANIZATION-GUIDE.md) | Guia de organização universal |

## 🧭 Navegação Rápida

### Por Tipo de Usuário

**👩‍💻 Desenvolvedores**
- [Guia Completo](./Guides-Tutorials/GUIA_COMPLETO_PARA_LEIGOS.md)
- [Configuração Completa](./Guides-Tutorials/CONFIGURACAO_COMPLETA.md)
- [TypeScript](./Guides-Tutorials/TYPESCRIPT.md)

**🏗️ Arquitetos de Sistema**
- [Arquitetura A2A](./A2A-Core/A2A-ARCHITECTURE.md)
- [Sistema Unificado](./A2A-Core/A2A-UNIFIED-SYSTEM.md)
- [Orquestrador](./Agent-Systems/ORCHESTRATOR_AGENT_GUIDE.md)

**🔧 DevOps/Infraestrutura**
- [Docker Compose](./Infrastructure/DOCKER-COMPOSE-UNIFICADO.md)
- [PostgreSQL](./Infrastructure/01-POSTGRESQL.md)
- [Monitoramento](./Infrastructure/ENHANCED-MONITOR-GUIDE.md)

**🚀 Usuários Finais**
- [Comandos Rápidos](./Guides-Tutorials/COMANDOS_RAPIDOS.md)
- [Executar Sistema](./Guides-Tutorials/EXECUTAR_SISTEMA.md)
- [UI Configuration](./Guides-Tutorials/UI_CONFIGURACAO_MELHORADA.md)

### Por Funcionalidade

**🔗 Integrações**
- [MCP Tools](./MCP-Integration/MCP_TOOLS_INTEGRATION.md)
- [DiegoTools](./MCP-Integration/DIEGOTOOLS_INTEGRATION.md)
- [Claude Flow](./Support/CLAUDE-FLOW-DISAMBIGUATION.md)

**🧠 Sistema de Memória**
- [Memória Híbrida](./Infrastructure/HYBRID_MEMORY_SYSTEM.md)
- [Banco de Memória](./Support/memory-bank.md)
- [Mem0-OSS](./Infrastructure/MEM0-OSS-IMPLEMENTATION-SUMMARY.md)

**📊 Monitoramento**
- [Monitor Enhanced](./Infrastructure/ENHANCED-MONITOR-SUMMARY.md)
- [Sistemas de Guardian](./Agent-Systems/GUARDIAN-SISTEMA-COMPLETO.md)
- [Coordenação](./Support/coordination.md)

## 🏃‍♂️ Quick Start

1. **Instalação Básica**: [Guia Completo para Leigos](./Guides-Tutorials/GUIA_COMPLETO_PARA_LEIGOS.md)
2. **Configuração**: [Configuração Completa](./Guides-Tutorials/CONFIGURACAO_COMPLETA.md)
3. **Primeiro Agent**: [HelloWorld Agent](./Agent-Systems/HELLOWORLD_AGENT_TASKSTATE_COMPLETED.md)
4. **Interface Web**: [Integração UI](./Guides-Tutorials/INTEGRACAO_UI.md)

## 🔍 Busca e Navegação

### Encontrar por Palavra-chave
- **A2A/Agents**: [A2A-Core](./A2A-Core/) + [Agent-Systems](./Agent-Systems/)
- **MCP/Tools**: [MCP-Integration](./MCP-Integration/)
- **Docker/Infra**: [Infrastructure](./Infrastructure/)
- **Tutoriais**: [Guides-Tutorials](./Guides-Tutorials/)
- **Suporte**: [Support](./Support/)

### Documentos Mais Acessados
1. [Guia Completo para Leigos](./Guides-Tutorials/GUIA_COMPLETO_PARA_LEIGOS.md)
2. [Arquitetura A2A](./A2A-Core/A2A-ARCHITECTURE.md)
3. [Orchestrator Guide](./Agent-Systems/ORCHESTRATOR_AGENT_GUIDE.md)
4. [MCP Tools Integration](./MCP-Integration/MCP_TOOLS_INTEGRATION.md)
5. [Docker Compose Unificado](./Infrastructure/DOCKER-COMPOSE-UNIFICADO.md)

## 📝 Contribuindo

Para adicionar ou modificar documentação:

1. **Identifique o cluster apropriado** baseado no conteúdo
2. **Siga o padrão de nomenclatura** existente
3. **Atualize os READMEs** do cluster correspondente
4. **Adicione links cruzados** para documentos relacionados
5. **Use commits convencionais** conforme [guia](./Guides-Tutorials/CONVENTIONAL-COMMITS-AUTO.md)

## 🎯 Roadmap de Documentação

- [ ] Tutoriais interativos para SPARC modes
- [ ] Documentação de API automatizada
- [ ] Guias de troubleshooting expandidos
- [ ] Vídeos tutoriais para casos complexos

## 📊 Estatísticas

- **Total de Documentos**: 72
- **Clusters Organizados**: 7
- **Idiomas**: Português (principal), Inglês (técnico)
- **Última Atualização**: 2025-01-13

---

📌 **Dica**: Use `Ctrl+F` para buscar rapidamente por termos específicos ou navegue pelos clusters temáticos para exploração estruturada.