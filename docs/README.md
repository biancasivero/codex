# Documentação do Sistema Codex

> Sistema integrado de agentes A2A com orquestração SPARC e integração MCP

## 📋 Visão Geral

Este repositório contém a documentação completa do Sistema Codex, uma plataforma avançada de orquestração de agentes que combina:

- **Sistema A2A (Agent-to-Agent)**: Comunicação e coordenação entre agentes autônomos
- **SPARC Orchestration**: 17 modos especializados de desenvolvimento e análise
- **Integração MCP**: Model Context Protocol para extensibilidade de ferramentas
- **Interface Web**: Dashboard de monitoramento e controle em tempo real

## 🗂️ Estrutura da Documentação

A documentação está organizada em **7 clusters temáticos** com **72 documentos** especializados:

### [📡 A2A-Core](./A2A-Core/README.md) 
Arquitetura central e especificações do protocolo A2A
- Especificações da API e protocolos de comunicação
- Arquitetura do sistema e padrões de integração
- Guias de migração e modos de interação

### [🤖 Agent-Systems](./Agent-Systems/README.md)
Sistemas de agentes e orquestração
- Agentes especializados (Auto-commit, Organizador, Guardian)
- Orchestrator e coordenação multi-agente
- Estados de tarefas e monitoramento de agentes

### [📚 Guides-Tutorials](./Guides-Tutorials/README.md)
Guias práticos e tutoriais passo-a-passo
- Guia completo para iniciantes
- Configurações e comandos rápidos
- Integrações de UI e TypeScript

### [🏗️ Infrastructure](./Infrastructure/README.md)
Infraestrutura, banco de dados e containerização
- PostgreSQL e sistemas de memória híbrida
- Docker Compose e monitoramento
- Adaptações Mem0-OSS

### [🔧 MCP-Integration](./MCP-Integration/README.md)
Model Context Protocol e integrações de ferramentas
- Bridge MCP Tools e DiegoTools
- Simplificação de ferramentas e testes
- Distinções entre MCP e Agents

### [🆘 Support](./Support/README.md)
Documentação de suporte e coordenação
- Resolução de problemas e debugging
- Organizações e scores de qualidade
- Coordenação e bancos de memória

### [📦 Legacy](./Legacy/README.md)
Documentos de versões anteriores e otimizações
- Relatórios de otimização A2A
- Implementações de TaskStatus
- Melhorias de protocolo

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