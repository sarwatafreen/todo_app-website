# Quickstart Guide: Authentication & Security

**Feature**: Authentication & Security
**Date**: 2026-01-27
**Author**: Claude Code

## Overview

This guide provides step-by-step instructions for setting up, configuring, and running the authentication and authorization system with JWT tokens, secure user signup/login, role-based access control (RBAC), and security best practices.

## Prerequisites

- Python 3.11+
- Pip package manager
- Existing backend API with database access
- Environment variables configured for JWT secrets

## Setup Instructions

### 1. Backend Setup (Extends existing backend)

#### Navigate to the backend directory:
```bash
cd backend
```

#### Install authentication-specific dependencies:
```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

#### Add authentication configuration to existing `.env` file:
```env
# JWT Configuration (if not already present)
JWT_SECRET_KEY=your-super-secret-jwt-key-here-at-least-32-chars-long
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Rate limiting
AUTH_RATE_LIMIT=5/minute
PASSWORD_MIN_LENGTH=8
```

#### Apply authentication database migrations:
```bash
# If using Alembic for migrations
alembic upgrade head
```

## Configuration

### Authentication Setup

1. **JWT Secret**: Generate a strong JWT secret (at least 32 characters) for the backend
2. **Rate Limiting**: Configure rate limits to prevent brute force attacks
3. **Password Policy**: Set minimum password strength requirements

### Database Configuration

1. Update the database with authentication-related tables (users, refresh_tokens, roles, auth_logs)
2. Ensure proper indexing for authentication queries
3. Set up any necessary database triggers or constraints for security

## Running the Authentication System

### Integration with Existing Backend
The authentication system integrates with the existing backend API:

1. **Start the existing backend server** (if not already running):
```bash
cd backend && uvicorn src.main:app --reload --port 8000
```

2. **Authentication endpoints** will be available as part of the existing API:
   - `POST /auth/signup` - Create new user account
   - `POST /auth/login` - Authenticate and get tokens
   - `POST /auth/refresh` - Refresh access token
   - `POST /auth/logout` - Logout and invalidate tokens
   - `GET /auth/me` - Get current user info
   - `GET /auth/users` - Get list of users (admin only)

### Authentication Endpoints

#### User Registration
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!"
  }'
```

#### User Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

#### Protected Resource Access
```bash
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer <access_token>"
```

#### Token Refresh
```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "<refresh_token>"
  }'
```

### Authentication Requirements
- All protected endpoints require a valid JWT token in the Authorization header
- Returns 401 Unauthorized if no valid token is present
- Returns 403 Forbidden for insufficient role permissions
- Rate limiting triggers after 5 failed login attempts per minute

## Security Notes

1. **JWT Validation**: All API endpoints require a valid JWT token in the Authorization header
2. **Password Security**: All passwords are securely hashed using bcrypt with salt
3. **Environment Variables**: Never commit secrets to version control
4. **HTTPS**: Use HTTPS in production for all authentication communications
5. **Rate Limiting**: Authentication endpoints are rate-limited to prevent brute force attacks

## Testing

Run authentication tests:
```bash
cd backend
pytest tests/auth/
```

Run specific test suites:
```bash
# Unit tests for authentication service
pytest tests/auth/test_auth_service.py

# Endpoint tests
pytest tests/auth/test_auth_endpoints.py

# RBAC tests
pytest tests/rbac/test_rbac_service.py
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Look for the `/auth/` endpoints in the API documentation.

## Troubleshooting

### Common Issues

1. **Authentication Failures**:
   - Verify JWT secrets match between services
   - Check that email/password combinations are correct
   - Ensure account is active and not locked

2. **Rate Limiting Issues**:
   - Check rate limit configuration
   - Verify that the same IP isn't making too many requests
   - Look for any caching issues that might affect rate tracking

3. **Database Connection Issues**:
   - Verify database connection string
   - Ensure authentication tables exist and are properly configured

### Security Testing
- Test that unauthorized users cannot access protected resources
- Verify that different roles have appropriate permissions
- Test rate limiting functionality
- Verify password strength requirements are enforced