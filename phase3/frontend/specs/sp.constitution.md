# Phase III – Todo AI Chatbot Constitution

## Core Principles

### 1. Agentic-First Architecture
- All intelligence and decision-making must reside in **AI agents**.
- Backend routes must not contain business logic for task decisions.
- The agent decides **what to do**, tools decide **how to do it**.

### 2. MCP as the Only Tool Interface
- Task operations **must only be exposed via MCP tools**.
- FastAPI routes are forbidden from directly manipulating tasks.
- MCP tools must be:
  - Stateless
  - Deterministic
  - Side-effect limited to database operations

### 3. Stateless Server Rule
- No in-memory state is allowed on the server.
- Each chat request must:
  1. Fetch conversation history from database
  2. Run agent with full context
  3. Persist outputs back to database
- Server must be restart-safe without losing context.

### 4. Explicit Separation of Concerns

| Layer | Responsibility |
|------|---------------|
| Chat UI | User interaction only |
| FastAPI | Request orchestration |
| Agent | Reasoning & tool selection |
| MCP Server | Task execution |
| Database | Source of truth |

Cross-layer shortcuts are **not allowed**.

### 5. Tool-Driven Task Management
- All task CRUD operations must occur via MCP tools:
  - add_task
  - list_tasks
  - update_task
  - complete_task
  - delete_task
- The agent **must never fabricate task state**.
- Tool results are the single source of truth.

### 6. Natural Language as Primary Interface
- Users interact exclusively through natural language.
- No command syntax or special keywords are required.
- The agent must infer intent from conversational input.

### 7. Agent Behavior Rules
- The agent must:
  - Confirm all task mutations in natural language
  - Handle ambiguity by asking clarifying questions
  - Gracefully recover from tool errors
- The agent must not expose internal tool schemas to users.

### 8. Conversation Persistence
- Conversations and messages must be stored in the database.
- Each message must record:
  - role (user / assistant)
  - content
  - timestamp
- Conversation context must be reconstructable at any time.

### 9. Authentication & User Isolation
- Every chat request must be associated with an authenticated user.
- MCP tools must enforce user-level data isolation.
- Cross-user data access is strictly forbidden.

### 10. Spec-Driven Development
- No implementation may begin without:
  - sp.specify
  - sp.plan
  - sp.tasks
- Manual coding is discouraged.
- Claude Code must be used to generate implementation artifacts.

## Phase III Success Criteria

Phase III is considered complete when:

- Users can manage todos entirely via natural language
- The agent correctly selects and invokes MCP tools
- Conversations persist across requests and restarts
- The system demonstrates clean agent–tool separation
- The chatbot behaves predictably, safely, and helpfully

## Non-Goals (Explicitly Out of Scope)

- UI-heavy chat customization
- Long-term memory beyond database persistence
- Multi-agent collaboration
- Voice or multimodal inputs

## Amendment Policy

This constitution may only be updated:
- At the beginning of a new phase
- Or with explicit justification documented in the specs

All Phase III specs must reference this constitution.