# Research: Backend API & Data Layer (FastAPI + SQLModel + Neon)

**Feature**: Backend API & Data Layer
**Date**: 2026-01-26
**Author**: Claude Code

## Executive Summary

This research document outlines the technical decisions, architecture patterns, and implementation strategies for building a secure, stateless REST API using FastAPI that enforces JWT authentication and user ownership with persistent task storage in Neon PostgreSQL using SQLModel.

## Architecture Decisions

### Decision: FastAPI Framework
**Rationale**: FastAPI provides automatic API documentation, type validation, high performance, and excellent support for asynchronous operations. Its dependency injection system is ideal for authentication middleware and database session management.

**Alternatives considered**:
- Flask: Would require more manual setup for validation and documentation
- Django: Would be overly complex for a pure API service

### Decision: SQLModel ORM
**Rationale**: SQLModel provides type hints, combines SQLAlchemy and Pydantic functionality, and ensures database schema and API contracts align perfectly as required by the constitution.

**Alternatives considered**:
- SQLAlchemy Core: Would lack Pydantic integration and type safety
- Tortoise ORM: Would not integrate as well with FastAPI's Pydantic models

### Decision: Neon Serverless PostgreSQL
**Rationale**: Neon provides serverless PostgreSQL with auto-scaling, branching, and built-in connection pooling. It's designed for modern applications with variable loads.

**Alternatives considered**:
- Standard PostgreSQL: Would require manual scaling and connection management
- Other cloud databases: Would not align with the specified technology stack

## Technology Patterns

### API Patterns
- **Dependency Injection**: For database sessions, authentication context
- **Pydantic Models**: For request/response validation and serialization
- **FastAPI Middlewares**: For authentication and request processing
- **SQLModel Models**: For database schema definitions with validation

### Security Patterns
- **JWT Middleware**: For token validation on protected routes
- **User Identity Extraction**: From JWT payload to enforce ownership
- **Parameterized Queries**: To prevent SQL injection
- **Input Validation**: Using Pydantic models for all API inputs

### Database Patterns
- **Connection Pooling**: Through Neon's built-in connection pooling
- **Session Management**: Per-request database sessions using FastAPI dependencies
- **Transaction Management**: Automatic transaction handling for each request
- **Relationship Mapping**: Using SQLModel's relationship features

## API Design Patterns

### RESTful Endpoint Structure
- `/api/{user_id}/tasks`: Operations on a user's tasks
- `/api/{user_id}/tasks/{task_id}`: Operations on specific task
- Standard HTTP methods: GET, POST, PUT, DELETE, PATCH
- Consistent error responses with appropriate status codes

### Authentication Flow
1. Client presents JWT token in Authorization header
2. FastAPI middleware validates token signature using shared secret
3. Middleware extracts user identity from token payload
4. Middleware validates that user_id in path matches JWT identity
5. Request proceeds with authenticated context attached

## Database Design Considerations

### Task Model
- ID (primary key, UUID)
- Title (required, string, max 255 chars)
- Description (optional, string, max 1000 chars)
- Completed (boolean, default false)
- Owner ID (foreign key to user, UUID)
- Created timestamp (auto-generated)
- Updated timestamp (auto-updated)

### Indexing Strategy
- Index on owner_id for efficient user-scoped queries
- Index on completed status for filtering
- Composite indexes as needed for common query patterns

## Error Handling Strategy

### HTTP Status Codes
- 200: Successful GET/PUT/PATCH requests
- 201: Successful POST requests
- 204: Successful DELETE requests
- 400: Bad request (validation errors)
- 401: Unauthorized (missing or invalid JWT)
- 403: Forbidden (user ID mismatch in path vs JWT)
- 404: Not found (resource doesn't exist)
- 422: Validation errors (request body validation failed)
- 500: Internal server errors

### Error Response Format
```json
{
  "detail": "Human-readable error message",
  "code": "machine-readable-error-code"
}
```

## Performance Considerations

### Backend Optimization
- Connection pooling with Neon's built-in pooling
- Efficient indexing for user-specific queries
- Caching strategies for frequently accessed data
- Async processing for non-critical operations

### API Design
- Pagination for collection endpoints
- Filtering and sorting parameters
- Efficient serialization with Pydantic
- Minimal database queries per request

## Deployment Considerations

### Environment Configuration
- Separate environments for development, staging, and production
- Environment-specific configuration for database URLs and JWT secrets
- Secure handling of sensitive configuration values

### Containerization
- Docker configuration for consistent deployments
- Environment variable management
- Health check endpoints
- Resource limits and scaling configuration