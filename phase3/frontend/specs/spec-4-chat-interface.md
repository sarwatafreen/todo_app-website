# Spec-4: AI Chat Interface

## Objective

Build a **stateless AI-powered chat interface** that allows users to manage todos via natural language, where the **frontend chat UI is directly integrated with an AI agent–driven backend**.

The backend chat endpoint acts as an orchestration layer between:
- the ChatKit frontend
- the OpenAI Agents SDK
- persisted conversation state in the database

## Scope

This spec covers:

- Chat UI integration using **ChatKit components**
- Direct integration of frontend with **agent-backed chat API**
- Stateless `/api/{user_id}/chat` endpoint
- Conversation & message persistence
- Conversation reconstruction per request
- End-to-end request → agent → response lifecycle

## Out of Scope (Handled in Other Specs)

- MCP tool implementations (Spec-5)
- Agent reasoning and tool-selection rules (Spec-6)
- Authentication and authorization logic (Spec-7)

## Functional Requirements

### 1. AI-Integrated Chat UI

- The frontend must use **ChatKit components** to provide a conversational interface.
- The UI must communicate directly with the **agent-backed chat endpoint**.
- The frontend must:
  - Send user messages to the backend
  - Receive AI-generated responses
  - Reuse `conversation_id` to maintain continuity
- The frontend must NOT:
  - Contain AI logic
  - Call MCP tools directly
  - Manage conversation state locally beyond UI rendering

### 2. Agent-Backed Stateless Chat Endpoint

**Endpoint**: `POST /api/{user_id}/chat`

**Behavior**
- Receive user message from ChatKit UI
- Restore conversation context from database
- Invoke OpenAI Agent via Agents SDK
- Persist assistant response
- Return AI response to frontend

⚠️ The endpoint must act as a **thin orchestration layer** and remain fully stateless.

### 3. Conversation Management

- If `conversation_id` is provided:
  - Load the conversation and messages from database
- If `conversation_id` is not provided:
  - Create a new conversation entry
- Conversation context must be reconstructed **on every request**.

### 4. Message Persistence

Each message must be stored with:
- user_id
- conversation_id
- role (`user` or `assistant`)
- content
- timestamp

The database is the **single source of truth** for conversation state.

### 5. Agent Invocation Boundary

- The chat endpoint must:
  - Build the full message history
  - Pass messages to the OpenAI Agents SDK
- The endpoint must NOT:
  - Contain task logic
  - Decide which MCP tool to call
  - Modify task data directly

### 6. Error Handling

- Gracefully handle:
  - Invalid conversation IDs
  - Agent execution failures
  - Database errors
- Always return a friendly assistant-style response to the frontend.

## Success Criteria

- Frontend chat UI is fully integrated with AI agent backend
- Users interact only through natural language
- Conversations persist across requests and server restarts
- Server remains stateless
- Clear separation between UI, agent orchestration, and task execution