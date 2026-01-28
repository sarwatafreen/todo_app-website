# Data Model: Todo Full-Stack Web Application

**Feature**: Todo Full-Stack Web Application
**Date**: 2026-01-26
**Author**: Claude Code

## Overview

This document defines the data models for the secure, multi-user todo web application. The models implement the key entities identified in the feature specification and enforce the data integrity requirements specified in the constitution.

## Entity Definitions

### User Entity

**Purpose**: Represents a registered user of the application with authentication credentials and identity claims

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier for the user
- `email` (String, unique): User's email address, used for identification
- `hashed_password` (String): BCrypt hashed password for authentication
- `created_at` (DateTime): Timestamp when the user account was created
- `updated_at` (DateTime): Timestamp when the user account was last updated
- `is_active` (Boolean): Whether the account is active (default: true)

**Relationships**:
- One-to-Many: User has many Todos (user.todos)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Email cannot be empty
- Password must meet minimum security requirements (handled during registration)

**Access Control**:
- Only the user themselves can access their own account information
- All operations require valid JWT authentication matching the user ID

### Todo Entity

**Purpose**: Represents a personal task item owned by a specific user, with properties like title, description, completion status, and timestamps

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier for the todo
- `title` (String): Title of the todo item (required)
- `description` (String, optional): Detailed description of the task
- `is_completed` (Boolean): Whether the task is completed (default: false)
- `user_id` (UUID/Integer): Foreign key linking to the owning user
- `created_at` (DateTime): Timestamp when the todo was created
- `updated_at` (DateTime): Timestamp when the todo was last updated
- `due_date` (DateTime, optional): Optional deadline for the task

**Relationships**:
- Many-to-One: Todo belongs to one User (todo.user)

**Validation Rules**:
- Title cannot be empty
- Title must be between 1-255 characters
- Description must be between 0-1000 characters if provided
- User ID must correspond to an existing user
- is_completed must be boolean value

**Access Control**:
- Only the owning user can access, modify, or delete this todo
- All operations require valid JWT authentication matching the todo's user ID
- Users cannot access todos belonging to other users

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_email ON users(email);
```

### Todos Table
```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_is_completed ON todos(is_completed);
```

## State Transitions

### Todo Status Transitions
- `incomplete` → `completed`: When user marks todo as complete
- `completed` → `incomplete`: When user unmarks todo as complete

### User Account Transitions
- `inactive` → `active`: When user confirms email/registers
- `active` → `deactivated`: When user deactivates account
- `deactivated` → `active`: When user reactivates account

## Query Patterns

### Common Queries
1. Get all todos for a specific user (filtered by user_id)
2. Get a specific todo by ID (with user_id verification)
3. Create new todo for a specific user
4. Update todo status for a specific user's todo
5. Delete a specific user's todo

### Security Enforcement
- All queries must filter by user_id to enforce data isolation
- User ID in JWT token must match user_id in query conditions
- No cross-user data access is allowed

## API Representation

### User Response Object
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "is_active": true
}
```

### Todo Request Object
```json
{
  "title": "Task title",
  "description": "Task description",
  "is_completed": false,
  "due_date": "2023-12-31T23:59:59Z"
}
```

### Todo Response Object
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "is_completed": false,
  "user_id": "user-uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "due_date": "2023-12-31T23:59:59Z"
}
```