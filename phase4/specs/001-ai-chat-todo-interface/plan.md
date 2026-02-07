# Implementation Plan: AI-Powered Chat Interface for Todo Management

**Branch**: `001-ai-chat-todo-interface` | **Date**: 2026-01-29 | **Spec**: specs/001-ai-chat-todo-interface/spec.md
**Input**: Feature specification from `/specs/001-ai-chat-todo-interface/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a stateless AI-powered chat interface that allows users to manage todos via natural language. The backend chat endpoint acts as an orchestration layer between the ChatKit frontend, the OpenAI Agents SDK, and persisted conversation state in the database. The system follows a strict stateless architecture where conversation context is reconstructed on every request from the database.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript for frontend
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, Next.js 16+ (App Router)
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application (Linux server + browser)
**Project Type**: web - determines source structure
**Performance Goals**: <5 second response time for 90% of interactions, 95% accuracy in natural language processing
**Constraints**: <200ms p95 for database operations, stateless operation, user isolation enforced
**Scale/Scope**: 10k users, persistent conversation history, real-time chat interface

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-Driven Development Compliance
- [x] All implementation must follow written specifications
- [x] Features must be derived from and traceable to written specifications

### Security-First Design Compliance
- [x] Authentication required on all protected endpoints using JWT
- [x] Task ownership enforced at every data operation
- [x] Database schema and ORM models reflect API contracts exactly
- [x] Frontend attaches valid JWT tokens to every backend request
- [x] Shared JWT secret configured via environment variables

### Technology Stack Compliance
- [x] Frontend uses Next.js 16+ (App Router)
- [x] Backend uses Python FastAPI
- [x] ORM uses SQLModel
- [x] Database uses Neon Serverless PostgreSQL
- [x] Authentication uses Better Auth with JWT

### API and Error Handling Compliance
- [x] All APIs follow RESTful design principles with consistent naming
- [x] Error handling is explicit with appropriate HTTP status codes (401, 403, 404, 422)
- [x] All endpoints reject unauthenticated requests with 401 Unauthorized
- [x] Only authenticated users access or modify their own data
- [x] Task ownership enforced across all CRUD operations

### Phase III Constitution Compliance
- [x] Agentic-First Architecture: Intelligence resides in AI agents, not backend routes
- [x] MCP as the Only Tool Interface: Task operations via MCP tools only
- [x] Stateless Server Rule: No in-memory state, context from database on each request
- [x] Explicit Separation of Concerns: Clear boundaries between UI, orchestration, agent, and MCP
- [x] Tool-Driven Task Management: All task operations via MCP tools (add_task, list_tasks, etc.)
- [x] Natural Language as Primary Interface: Users interact via natural language
- [x] Agent Behavior Rules: Agent confirms mutations, handles ambiguity, recovers from errors
- [x] Conversation Persistence: Stored in database with role, content, timestamp
- [x] Authentication & User Isolation: Every request authenticated, user-level data isolation

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chat-todo-interface/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task_model.py
│   │   ├── conversation_model.py      # New: Conversation entity
│   │   ├── message_model.py           # New: Message entity
│   │   └── __init__.py
│   ├── services/
│   │   ├── agent_service.py           # New: OpenAI Agent integration
│   │   └── conversation_service.py    # New: Conversation management
│   ├── api/
│   │   ├── task_endpoints.py
│   │   ├── chat_endpoints.py          # New: Chat interface endpoints
│   │   └── __init__.py
│   ├── middleware/
│   │   └── auth_middleware.py
│   ├── auth/
│   │   └── api/
│   │       └── auth_endpoints.py
│   ├── database.py
│   ├── main.py
│   └── settings.py
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   ├── Todo/
│   │   ├── Chat/                      # New: Chat UI components
│   │   └── ProtectedRoute.tsx
│   ├── pages/
│   ├── app/
│   │   ├── chat/                      # New: Chat page
│   │   ├── tasks/
│   │   ├── dashboard/
│   │   ├── login/
│   │   └── signup/
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── chat.ts                    # New: Chat API service
│   ├── context/
│   │   └── auth-context.tsx
│   └── lib/
└── tests/
```

## Phase 0: Research & Clarification

Based on the feature specification and constitution, all requirements are clearly defined. No additional clarification is needed as the following are specified:
- OpenAI ChatKit for frontend interface
- OpenAI Agents SDK for AI integration
- Stateless architecture with database-driven conversation reconstruction
- MCP tools for task operations
- User isolation and authentication requirements

## Phase 1: Design & Contracts

### Data Model Design

**Conversation Entity:**
- id: UUID primary key
- title: String (optional, auto-generated from first message if not provided)
- user_id: String (foreign key to user)
- created_at: DateTime
- updated_at: DateTime

**Message Entity:**
- id: UUID primary key
- conversation_id: UUID (foreign key to conversation)
- user_id: String (foreign key to user)
- role: Enum ('user' | 'assistant')
- content: String (message text)
- timestamp: DateTime
- order_index: Integer (for ordering messages in conversation)

### API Contract Design

**POST /api/{user_id}/chat**
- Request: `{ message: string, conversation_id?: string }`
- Response: `{ response: string, conversation_id: string, timestamp: string }`
- Headers: Authorization: Bearer {jwt_token}
- Authentication: JWT verification (user_id in path must match JWT token)
- Error Codes: 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 422 (Validation Error), 500 (Internal Server Error)

## Quickstart Guide

1. **Environment Setup**:
   - Install Python 3.11, Node.js 18+
   - Set up Neon PostgreSQL database
   - Configure environment variables (DATABASE_URL, JWT_SECRET)

2. **Backend Setup**:
   - Install dependencies: `pip install fastapi sqlmodel openai python-jose[cryptography] passlib[bcrypt]`
   - Create new models: conversation_model.py, message_model.py
   - Create new services: agent_service.py, conversation_service.py
   - Create new endpoints: chat_endpoints.py
   - Register chat router in main.py

3. **Frontend Setup**:
   - Create Chat component using OpenAI ChatKit
   - Create chat service for API communication
   - Add chat page at /chat route
   - Integrate with existing auth context

4. **Testing**:
   - Unit tests for new models and services
   - Integration tests for chat endpoints
   - End-to-end tests for complete chat flow

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multi-project structure | Web application requires separate frontend/backend | Single project insufficient for different tech stacks (Python/JS) |
| Additional dependencies | OpenAI Agents SDK required for AI functionality | Direct AI integration would violate agentic-first architecture |
