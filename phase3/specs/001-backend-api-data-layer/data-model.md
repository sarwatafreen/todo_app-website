# Data Model: Backend API & Data Layer

**Feature**: Backend API & Data Layer
**Date**: 2026-01-26
**Author**: Claude Code

## Overview

This document defines the data models for the secure, user-scoped REST API using SQLModel for database operations with Neon PostgreSQL. The models implement the key entities identified in the feature specification and enforce the data integrity requirements specified in the constitution.

## Entity Definitions

### User Entity (Virtual/Reference)

**Purpose**: Represents an authenticated user with identity claims extracted from JWT tokens, serving as the basis for data access control

**Fields** (as referenced in JWT):
- `id` (UUID): Unique identifier for the user (extracted from JWT payload)
- `email` (String): User's email address (extracted from JWT payload)
- `identity_claims` (JSON): Additional identity information from JWT

**Relationships**:
- One-to-Many: User has many Tasks (via owner_id foreign key)

**Access Control**:
- User identity is extracted from JWT token during authentication
- All operations require valid JWT authentication matching the user ID
- No direct database storage of user records (identity comes from JWT provider)

### Task Entity

**Purpose**: Represents a user's personal task data that must be stored, retrieved, updated, and deleted with strict ownership enforcement

**Fields**:
- `id` (UUID): Primary key, unique identifier for the task
- `title` (String): Title of the task (required, max 255 characters)
- `description` (String, optional): Detailed description of the task (max 1000 characters)
- `is_completed` (Boolean): Whether the task is completed (default: false)
- `owner_id` (UUID): Foreign key linking to the task owner (user ID from JWT)
- `created_at` (DateTime): Timestamp when the task was created (auto-generated)
- `updated_at` (DateTime): Timestamp when the task was last updated (auto-updates)
- `due_date` (DateTime, optional): Optional deadline for the task

**Relationships**:
- Many-to-One: Task belongs to one User (via owner_id foreign key)

**Validation Rules**:
- Title cannot be empty
- Title must be between 1-255 characters
- Description must be between 0-1000 characters if provided
- Owner ID must be a valid UUID format
- is_completed must be boolean value
- Due date must be a valid date/time if provided

**Access Control**:
- Only the owning user can access, modify, or delete this task
- All operations require valid JWT authentication matching the task's owner_id
- Users cannot access tasks belonging to other users

## Database Schema

### Tasks Table
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    owner_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_tasks_owner_id ON tasks(owner_id);
CREATE INDEX idx_tasks_is_completed ON tasks(is_completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

## State Transitions

### Task Status Transitions
- `incomplete` → `completed`: When user marks task as complete
- `completed` → `incomplete`: When user unmarks task as complete

## Query Patterns

### Common Queries
1. Get all tasks for a specific user (filtered by owner_id)
2. Get a specific task by ID (with owner_id verification)
3. Create new task for a specific user
4. Update task status for a specific user's task
5. Delete a specific user's task

### Security Enforcement
- All queries must filter by owner_id to enforce data isolation
- User ID in JWT token must match owner_id in query conditions
- No cross-user data access is allowed

## API Representation

### Task Request Object
```json
{
  "title": "Task title",
  "description": "Task description",
  "is_completed": false,
  "due_date": "2023-12-31T23:59:59Z"
}
```

### Task Response Object
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "is_completed": false,
  "owner_id": "user-uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "due_date": "2023-12-31T23:59:59Z"
}
```

### Task Update Object
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "is_completed": true,
  "due_date": "2023-12-31T23:59:59Z"
}
```