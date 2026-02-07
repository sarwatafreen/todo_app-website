<!--
Sync Impact Report:
Version change: N/A → 1.0.0
Added sections: Agent-First Development, Agentic Dev Stack Compliance, Local-Only Deployment, AI-Driven DevOps, Containerization Requirements, Helm-Based Deployment, Kubernetes Deployment, AI DevOps Operations
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Todo Chatbot Kubernetes Deployment Constitution

## Core Principles

### Agent-First Development
All infrastructure artifacts (Dockerfiles, Helm charts, Kubernetes resources) MUST be generated via AI tools. Manual authoring of Dockerfiles, YAMLs, or Helm templates is NOT allowed. This ensures consistent, AI-assisted development practices across all infrastructure components.

### Agentic Dev Stack Compliance
The workflow MUST strictly follow: `sp.specify → sp.plan → sp.tasks → sp.implement (Claude Code)`. Each stage must be documented and reviewable. This maintains consistency in the development lifecycle and ensures proper planning and implementation.

### Local-Only Deployment
Deployment must run on **Minikube**. No cloud providers (AWS, GCP, Azure) are permitted for this phase. This ensures reproducible local development and testing environments without external dependencies.

### AI-Driven DevOps
Kubernetes and Docker operations must be executed via: Docker AI Agent (Gordon), kubectl-ai, kagent. Direct CLI usage is allowed ONLY when AI tools are unavailable and must be justified. This promotes AI-assisted infrastructure management.

### Containerization Requirements
Frontend and Backend MUST be containerized separately. Dockerfiles MUST be generated using Docker AI (Gordon), or Claude Code prompts. Images must be tagged and usable by Kubernetes. This enables consistent deployment across environments.

### Helm-Based Deployment
Helm charts MUST be created for: Frontend and Backend. Charts MUST include: Deployment, Service, values.yaml. Charts MUST be generated via: kubectl-ai and/or kagent. This provides standardized packaging and configuration management for Kubernetes deployments.

## Kubernetes Deployment Standards

Applications MUST be deployed to Minikube. Services must expose: Frontend (NodePort or equivalent), Backend (ClusterIP or equivalent). Scaling MUST be demonstrated using AI tools. This ensures proper service exposure and scalability testing in the local environment.

## AI DevOps Operations Requirements

The following AI-powered operations MUST be demonstrated and logged: Docker AI (Gordon) for Dockerfile creation and image building, kubectl-ai for Kubernetes resource management, kagent for advanced orchestration tasks. This validates the AI-assisted DevOps workflow.

## Development Workflow

All development follows the Agentic Dev Stack methodology: Specification → Planning → Task Decomposition → Implementation. All code and infrastructure generated via AI agents with minimal manual intervention. Strict adherence to security-first design principles is maintained throughout.

## Governance

This constitution supersedes all other practices for the Todo Chatbot Kubernetes deployment project. Amendments require documentation, approval, and migration plan. All implementations must verify compliance with these principles. AI tools must be leveraged for all infrastructure operations as specified herein.

**Version**: 1.0.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05