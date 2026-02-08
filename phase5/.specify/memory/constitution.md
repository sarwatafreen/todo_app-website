<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Modified principles: N/A (completely new constitution)
Added sections: All sections (Core Principles, Allowed Tech Stack, Non-Negotiables, Governance)
Removed sections: None (template replaced entirely)
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ✅ reviewed
Follow-up TODOs: None
-->

# Project Constitution

## Core Principles

### Code Quality
Code must be clean, readable, and maintainable.

### Test Coverage
100% test coverage for business logic.

### State Management
No global state unless explicitly justified.

### Type Safety
Use TypeScript strict mode.

### Functional Programming
Prefer functional over imperative style.

## Allowed Tech Stack

### Frontend
React 18+, Tailwind CSS

### Backend
Node.js 20+, Fastify

### Database
PostgreSQL + Prisma

## Non-Negotiables

### Testing Requirements
All features must have E2E tests.

### Logging Policy
No console.log in production code.

### Commit Standards
Follow conventional commits.

### Accessibility Compliance
Accessibility (WCAG 2.1 AA) required.

## Governance

Any generated plan or code that violates this constitution must be rejected and rewritten.

**Version**: 1.0.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07