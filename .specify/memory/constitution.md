<!--
Sync Impact Report:
- Version change: N/A → 1.0.0
- Added principles: Spec-Driven Development, Agent Behavior Rules, Phase Governance, Technology Constraints, Quality Principles
- Added sections: Development Workflow, Technology Stack, Quality Standards
- Templates requiring updates: N/A
- Follow-up TODOs: None
-->

# Evolution of Todo Constitution

## Core Principles

### I. Spec-Driven Development (MANDATORY)
All development must follow the strict sequence: Constitution → Specifications → Plan → Tasks → Implementation. No agent may write code without approved specifications and tasks. All work must be traceable to approved requirements in the spec.

### II. Agent Behavior Rules
No manual coding by humans is permitted. No feature invention beyond approved specifications. No deviation from approved specifications. All refinement must occur at the specification level, not at the code level. Humans must only provide requirements, review specs, and approve changes.

### III. Phase Governance
Each phase is strictly scoped by its approved specification. Future-phase features must never leak into earlier phases. Architecture may evolve only through updated specifications and plans. Each phase must be completed before work begins on subsequent phases.

### IV. Technology Constraints
Backend development must use Python with FastAPI and SQLModel. Database must be Neon DB. Frontend (in later phases) must use Next.js. OpenAI Agents SDK and MCP must be used for agent functionality. Containerization with Docker is required. Future phases may include Kubernetes, Kafka, and Dapr for orchestration and messaging.

### V. Quality Principles
Clean architecture patterns must be followed with clear separation of concerns. Services must be stateless where possible. Code must be testable, maintainable, and well-documented. All code must pass automated tests before merging. Security and performance considerations must be addressed at the design phase.

### VI. Implementation Discipline
All implementations must follow the red-green-refactor cycle. Code must be accompanied by appropriate tests. Error handling must be comprehensive and consistent. Logging and observability must be built into all components from the start.

### VII. Reusable Intelligence & Agent Architecture
The system must be designed with reusable intelligence in mind. Agent skills and capabilities should be modular and composable to enable flexible task execution. Subagents must be architected to handle specialized functions while maintaining clear interfaces with the main agent system. Intelligence components must be designed for reusability across different contexts and scenarios.

## Technology Stack Requirements

The project must use the following technology stack:
- Backend: Python 3.10+, FastAPI, SQLModel
- Database: Neon DB (PostgreSQL-based)
- Frontend: Next.js (for phases that require UI)
- Agent Framework: OpenAI Agents SDK, Model Context Protocol (MCP)
- Containerization: Docker
- Infrastructure: Kubernetes (future phases), Kafka (future phases), Dapr (future phases)
- Development Tools: Claude Code for development assistance

## Development Workflow

All development must follow the Spec-Driven Development lifecycle:
1. Specifications must be created and approved before any implementation work
2. Technical plans must be created based on approved specifications
3. Implementation tasks must be derived from approved plans
4. Implementation must follow the tasks in sequence
5. All code changes must be reviewed and tested before merging

## Governance

This constitution supersedes all other development practices and guidelines. All project participants must comply with these principles. Amendments to this constitution require formal approval process and must be documented. All pull requests and code reviews must verify compliance with these principles. Deviations must be explicitly approved and documented.

The constitution must be referenced in all architectural decision records and implementation plans. Regular compliance reviews should be conducted to ensure adherence to these principles.

**Version**: 1.1.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2026-01-09
