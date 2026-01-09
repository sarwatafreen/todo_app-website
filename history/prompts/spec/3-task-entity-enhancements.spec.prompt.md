---
id: 3
title: task-entity-enhancements
stage: spec
date: '2025-01-01'
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-fullstack-web-app
branch: master
user: NLN
command: null
labels:
  - specification
  - architecture
  - task-entity
  - priority
  - tags
links:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
files:
  - specs/2-todo-fullstack-web-app/spec.md
  - specs/2-todo-fullstack-web-app/data-model.md
  - specs/2-todo-fullstack-web-app/contracts/api-contract.md
  - specs/2-todo-fullstack-web-app/tasks.md
  - specs/2-todo-fullstack-web-app/plan.md
  - README.md
tests: []
prompt: |
  # Phase II Specification – Full-Stack Todo App

  ## Domain Model

  ### Task
  - id: UUID
  - title: string (required)
  - description: string
  - completed: boolean
  - priority: enum (LOW | MEDIUM | HIGH)
  - tags: list[string]
  - created_at: datetime

  ## Persistence
  - PostgreSQL (Neon)
  - SQLModel used for schema & queries
  - Migrations handled automatically

  ## API Contract

  ### Create Task
  POST /api/tasks

  ### List Tasks
  GET /api/tasks
  Query Parameters:
  - search
  - completed
  - priority
  - tag
  - sort

  ### Update Task
  PUT /api/tasks/{id}

  ### Delete Task
  DELETE /api/tasks/{id}
response: |
  Updated all specifications to reflect the Task entity with priority and tags:

  1. spec.md: Updated to reflect Task entity instead of Todo, including priority and tags features
  2. data-model.md: Updated SQLModel definition to include priority (enum) and tags (JSON List[String]) fields
  3. api-contract.md: Updated API endpoints to use /api/tasks with query parameters for filtering by priority and tags
  4. tasks.md: Updated all tasks to reflect Task entity with priority and tags functionality
  5. plan.md: Updated architecture plan to include priority and tags in data model, repository, service, and API layers
  6. README.md: Updated to reflect Task entity with priority and tags features

  All specifications now consistently represent the Task entity with:
  - Priority field (enum: LOW, MEDIUM, HIGH)
  - Tags field (list of strings)
  - Updated API endpoints with filtering capabilities
  - Updated UI components to handle priority and tags
  - Updated business logic to handle priority and tags operations
outcome: Specifications updated to include Task entity with priority and tags features
evaluation: All specifications consistently updated to reflect the enhanced Task entity with priority and tags functionality, maintaining constitutional compliance and architectural patterns
---