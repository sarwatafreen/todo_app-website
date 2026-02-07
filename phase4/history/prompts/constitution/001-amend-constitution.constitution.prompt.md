---
id: 001
title: Amend Constitution
stage: constitution
date: 2026-01-26
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, setup, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests:
  - none
---

## Prompt

/sp.constitution

Project: Phase II – Todo Full-Stack Web Application (Agentic Dev Stack)

Core principles:
- Spec-driven development (all implementation must follow written specs)
- Security-first design (authentication, authorization, and data isolation)
- Separation of concerns (frontend, backend, and auth layers clearly defined)
- Automation over manual coding (Claude Code executes all implementation)
- Maintainability and scalability (clean architecture, modular components)

Key standards:
- All features must be derived from and traceable to written specifications
- RESTful API design with consistent naming, HTTP methods, and responses
- Authentication required on all protected endpoints using JWT
- Task ownership enforced at every data operation
- Database schema and ORM models must reflect API contracts exactly
- Frontend must attach valid JWT tokens to every backend request
- Error handling must be explicit (401, 403, 404, 422)

Constraints:
- Technology stack:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth with JWT
- No manual coding: all implementation via Agentic Dev Stack workflow
- Persistent storage required (no in-memory or file-based storage)
- API must follow the defined endpoints and HTTP verbs
- Shared JWT secret must be configured via environment variables
- Only authenticated users may access or modify their own data

Success criteria:
- All 5 Basic Level features implemented as a working web application
- REST API fully functional and secured with JWT authentication
- Each user can only see, create, update, and delete their own tasks
- Frontend and backend successfully verify authentication independently
- All endpoints reject unauthenticated requests with 401 Unauthorized
- Task ownership is enforced across all CRUD operations
- Application is deployable with persistent database storage
- Implementation strictly follows the written specifications without deviation

## Response snapshot

Updated the project constitution to reflect the specific requirements for the Phase II Todo Full-Stack Web Application. Created a comprehensive constitution document with:

1. Core Principles section covering spec-driven development, security-first design, separation of concerns, automation over manual coding, and maintainability
2. Key Standards section detailing RESTful API design, authentication requirements, error handling, and data integrity
3. Constraints section specifying the technology stack, storage requirements, API compliance, and access control
4. Success Criteria section outlining feature implementation, API functionality, data isolation, and deployment readiness
5. Governance section establishing constitutional authority

Also updated the plan, spec, and tasks templates to align with the new constitution by incorporating specific compliance checks and requirements.

## Outcome

- ✅ Impact: Created comprehensive constitution for Todo Full-Stack Web Application project with aligned templates
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md, .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
- 🔁 Next prompts: Continue with spec development for the Todo application
- 🧠 Reflection: The constitution now properly captures all the requirements and constraints specified by the user, with corresponding template updates to ensure compliance throughout the development process.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on the new constitution