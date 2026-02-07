# Data Model: Authentication & Security

**Feature**: Authentication & Security
**Date**: 2026-01-27
**Author**: Claude Code

## Overview

This document defines the data models for the authentication and authorization system using JWT tokens, with secure user signup/login, role-based access control (RBAC), and security best practices. The models implement the key entities identified in the feature specification and enforce the data integrity requirements specified in the constitution.

## Entity Definitions

### User Entity

**Purpose**: Represents an authenticated user with credentials and role information for access control

**Fields**:
- `id` (UUID): Primary key, unique identifier for the user
- `email` (String): User's email address (unique, required)
- `hashed_password` (String): BCrypt-hashed password (required, stored securely)
- `role` (String): User's role (e.g., "user", "admin") (default: "user")
- `is_active` (Boolean): Whether the account is active (default: true)
- `is_verified` (Boolean): Whether the email has been verified (default: false)
- `failed_login_attempts` (Integer): Count of failed login attempts (default: 0)
- `last_failed_login` (DateTime): Timestamp of last failed login attempt (nullable)
- `account_locked_until` (DateTime): When account lock expires (nullable)
- `created_at` (DateTime): Timestamp when the user was created (auto-generated)
- `updated_at` (DateTime): Timestamp when the user was last updated (auto-updates)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Hashed password must be properly formatted bcrypt hash
- Role must be one of the predefined values ("user", "admin", etc.)
- Failed login attempts must be non-negative
- Account lock time must be in the future if set

**Access Control**:
- Users can only view/update their own profile information (except role)
- Admins can view/update any user's information
- Password changes require proper authentication

### Refresh Token Entity

**Purpose**: Stores refresh tokens for extending session duration securely

**Fields**:
- `id` (UUID): Primary key, unique identifier for the token
- `token` (String): The refresh token value (encrypted, indexed)
- `user_id` (UUID): Foreign key linking to the user (required)
- `expires_at` (DateTime): When the token expires (required)
- `is_revoked` (Boolean): Whether the token has been revoked (default: false)
- `created_at` (DateTime): Timestamp when the token was created (auto-generated)

**Validation Rules**:
- Token must be unique across all refresh tokens
- User ID must reference a valid user
- Expiration time must be in the future
- Revoked tokens cannot be used for refreshing

**Access Control**:
- Only the associated user can use their refresh tokens
- Admins may revoke user refresh tokens

### Role Entity

**Purpose**: Defines roles and their associated permissions in the system

**Fields**:
- `id` (UUID): Primary key, unique identifier for the role
- `name` (String): Role name (e.g., "user", "admin", "moderator") (unique, required)
- `description` (String): Human-readable description of the role (optional)
- `permissions` (JSON): List of permissions associated with this role (required)
- `created_at` (DateTime): Timestamp when the role was created (auto-generated)
- `updated_at` (DateTime): Timestamp when the role was last updated (auto-updates)

**Validation Rules**:
- Role name must be unique
- Permissions must be a valid JSON array of permission strings
- Permissions must be from the predefined list of valid permissions

### Authentication Log Entity

**Purpose**: Tracks authentication events for security monitoring and audit trails

**Fields**:
- `id` (UUID): Primary key, unique identifier for the log entry
- `user_id` (UUID): Foreign key linking to the user (nullable for failed login attempts with invalid email)
- `event_type` (String): Type of authentication event (login, logout, failed_login, etc.)
- `success` (Boolean): Whether the authentication attempt was successful
- `ip_address` (String): IP address of the request (nullable)
- `user_agent` (String): User agent string from the request (nullable)
- `timestamp` (DateTime): When the event occurred (auto-generated)
- `details` (JSON): Additional details about the authentication event (optional)

**Validation Rules**:
- Event type must be one of the predefined values
- Success flag must be boolean
- Timestamp must be current time or past

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    failed_login_attempts INTEGER DEFAULT 0,
    last_failed_login TIMESTAMP WITH TIME ZONE,
    account_locked_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active);
```

### Refresh Tokens Table
```sql
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token VARCHAR(255) NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_refresh_tokens_token ON refresh_tokens(token);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
```

### Roles Table
```sql
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_roles_name ON roles(name);
```

### Authentication Logs Table
```sql
CREATE TABLE auth_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    event_type VARCHAR(50) NOT NULL,
    success BOOLEAN NOT NULL,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    details JSONB
);

CREATE INDEX idx_auth_logs_user_id ON auth_logs(user_id);
CREATE INDEX idx_auth_logs_event_type ON auth_logs(event_type);
CREATE INDEX idx_auth_logs_timestamp ON auth_logs(timestamp);
CREATE INDEX idx_auth_logs_success ON auth_logs(success);
```

## State Transitions

### User Account States
- `inactive` → `active`: When user registers and verifies email
- `active` → `locked`: When failed login attempts exceed threshold
- `locked` → `active`: When account lock period expires or admin intervention
- `active` → `deactivated`: When user requests account deactivation

### Authentication Event States
- `attempt` → `success` | `failure`: Based on credential validation result
- `success` → `logout`: When user explicitly logs out
- `failure` → `lockout`: When consecutive failures trigger account lock

## Query Patterns

### Common Queries
1. Authenticate user by email and password
2. Get user by JWT token subject
3. Check user role permissions
4. Record authentication event
5. Invalidate refresh token
6. Lock account after failed attempts

### Security Enforcement
- All authentication-related queries must respect privacy and security requirements
- Sensitive data (password hashes) should not be returned in responses
- Authentication logs must be comprehensive for security monitoring

## API Representation

### User Request Objects
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!"
}
```

### User Response Object (without sensitive data)
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "role": "user",
  "is_active": true,
  "is_verified": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Login Request Object
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

### Login Response Object
```json
{
  "access_token": "jwt-token-string",
  "refresh_token": "refresh-token-string",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "role": "user"
  }
}
```

### Token Refresh Request/Response
```json
// Request
{
  "refresh_token": "refresh-token-string"
}

// Response
{
  "access_token": "new-jwt-token-string",
  "token_type": "bearer",
  "expires_in": 1800
}
```