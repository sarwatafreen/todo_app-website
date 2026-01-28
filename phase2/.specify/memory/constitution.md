<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Modified principles: None (new constitution)
Added sections: All sections as per user requirements
Removed sections: Template placeholders
Templates requiring updates: ✅ Updated
Follow-up TODOs: None
-->
# Phase II – Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven Development
All implementation must follow written specifications. Features must be derived from and traceable to written specifications. No implementation without a corresponding spec.

### Security-First Design
Security is paramount in all design and implementation decisions. Authentication, authorization, and data isolation must be implemented at every layer. All protected endpoints must use JWT authentication. Task ownership must be enforced at every data operation.

### Separation of Concerns
Frontend, backend, and auth layers must be clearly defined and separated. Each layer has distinct responsibilities and interfaces. Clear API contracts must exist between layers.

### Automation Over Manual Coding
Claude Code executes all implementation through the Agentic Dev Stack workflow. No manual coding is allowed; all implementation must follow the automated workflow process.

### Maintainability and Scalability
Clean architecture and modular components must be maintained throughout the codebase. Code must be designed for long-term maintenance and scaling requirements.

## Key Standards

### RESTful API Design
All APIs must follow RESTful design principles with consistent naming, HTTP methods, and responses. Endpoints must follow predictable URL patterns and return appropriate HTTP status codes.

### Authentication Requirements
Authentication must be required on all protected endpoints using JWT. Frontend must attach valid JWT tokens to every backend request. Shared JWT secret must be configured via environment variables.

### Error Handling
Error handling must be explicit with appropriate HTTP status codes (401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable Entity). All endpoints must reject unauthenticated requests with 401 Unauthorized status.

### Data Integrity
Database schema and ORM models must reflect API contracts exactly. Only authenticated users may access or modify their own data. Task ownership must be enforced across all CRUD operations.

## Constraints

### Technology Stack
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT

### Storage Requirements
Persistent storage is required - no in-memory or file-based storage allowed. Application must be deployable with persistent database storage.

### API Compliance
API must follow the defined endpoints and HTTP verbs exactly. All implementation must strictly follow written specifications without deviation.

### Access Control
Only authenticated users may access or modify their own data. Each user can only see, create, update, and delete their own tasks.

## Success Criteria

### Feature Implementation
All 5 Basic Level features must be implemented as a working web application. Each feature must be fully functional and properly integrated.

### API Functionality
REST API must be fully functional and secured with JWT authentication. Frontend and backend must successfully verify authentication independently.

### Data Isolation
Each user must only be able to see, create, update, and delete their own tasks. Task ownership must be enforced across all CRUD operations.

### Deployment Readiness
Application must be deployable with persistent database storage and all security measures in place.

## Governance

All implementation must strictly follow written specifications without deviation. Changes to this constitution require explicit approval and documentation. Code reviews must verify compliance with all constitutional principles. This constitution supersedes all other development practices and guidelines.

**Version**: 1.0.0 | **Ratified**: 2026-01-26 | **Last Amended**: 2026-01-26