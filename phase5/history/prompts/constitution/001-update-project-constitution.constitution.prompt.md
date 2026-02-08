---
id: 001
title: Update Project Constitution
stage: constitution
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Claude
command: /sp.constitution
labels: [constitution, governance, setup]
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

```text
# Project Constitution

## Core Principles
- Code must be clean, readable, and maintainable.
- 100% test coverage for business logic.
- No global state unless explicitly justified.
- Use TypeScript strict mode.
- Prefer functional over imperative style.

## Allowed Tech Stack
- Frontend: React 18+, Tailwind CSS
- Backend: Node.js 20+, Fastify
- Database: PostgreSQL + Prisma

## Non-Negotiables
- All features must have E2E tests.
- No console.log in production code.
- Follow conventional commits.
- Accessibility (WCAG 2.1 AA) required.

## Enforcement
Any generated plan or code that violates this constitution must be rejected and rewritten.
```

## Response snapshot

Updated the project constitution to include the specified principles, tech stack, and non-negotiables. The new constitution includes:

- Core Principles: Clean code, test coverage, state management, type safety, functional programming
- Allowed Tech Stack: React, Tailwind, Node.js, Fastify, PostgreSQL, Prisma
- Non-Negotiables: E2E tests, no console.log in production, conventional commits, accessibility
- Governance: Code enforcement of constitution compliance

Also updated dependent templates:
- plan-template.md: Added constitution check with specific requirements
- spec-template.md: Added constitution compliance success criteria
- tasks-template.md: Added constitution compliance tasks in polish phase

## Outcome

- ✅ Impact: Updated constitution with clear principles and governance structure
- 🧪 Tests: None required for this update
- 📁 Files: Updated constitution and 3 dependent templates
- 🔁 Next prompts: Ready to create features following the new constitution
- 🧠 Reflection: Clear governance structure established for the project

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature development following constitution