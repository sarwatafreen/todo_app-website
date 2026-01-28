# Quickstart Guide: Backend API & Data Layer

**Feature**: Backend API & Data Layer
**Date**: 2026-01-26
**Author**: Claude Code

## Overview

This guide provides step-by-step instructions for setting up, configuring, and running the secure, user-scoped REST API using FastAPI, SQLModel, and Neon PostgreSQL.

## Prerequisites

- Python 3.11+
- Pip package manager
- Neon Serverless PostgreSQL account
- Environment variables configured for JWT secrets

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup

#### Navigate to the backend directory:
```bash
cd backend
```

#### Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```

#### Set up environment variables:
Create a `.env` file in the backend directory with the following variables:
```env
DATABASE_URL="your-neon-database-url"
JWT_SECRET_KEY="your-jwt-secret-key-here-at-least-32-characters-long"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Run database migrations:
```bash
# If using Alembic for migrations
alembic upgrade head
```

#### Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`.

## Configuration

### Authentication Setup

1. **JWT Secret**: Generate a strong JWT secret (at least 32 characters) for the backend
2. **Database**: Ensure your Neon PostgreSQL database is properly configured with the correct connection string

### Database Configuration

1. Update the `DATABASE_URL` in your backend `.env` file to point to your Neon database
2. Ensure the database has the correct permissions for the application
3. Run the initial migrations to create the required tables

## Running the Application

### Development Mode

Start the backend in development mode:

1. **Backend**: `cd backend && uvicorn src.main:app --reload`

The service will auto-reload on code changes.

### Production Mode

Build and run the application in production mode:

1. **Backend**: Deploy using a WSGI/ASGI server like Gunicorn
```bash
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## API Endpoints

### Task Endpoints
- `GET /api/{user_id}/tasks` - Retrieve all tasks for the user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get details of a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task content/metadata
- `DELETE /api/{user_id}/tasks/{id}` - Remove a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

### Authentication Requirements
- All endpoints require a valid JWT token in the Authorization header
- User ID in the URL path must match the user ID in the JWT token
- Returns 401 Unauthorized if no valid token is present
- Returns 403 Forbidden if user ID in path doesn't match JWT identity

## Security Notes

1. **JWT Validation**: All API endpoints require a valid JWT token in the Authorization header
2. **User Isolation**: Users can only access their own data based on owner_id
3. **Environment Variables**: Never commit secrets to version control
4. **HTTPS**: Use HTTPS in production for all communications

## Testing

Run backend tests:
```bash
cd backend
pytest
```

Run specific test suites:
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Contract tests
pytest tests/contract/
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Verify your Neon PostgreSQL connection string
   - Check that the database is accessible from your network

2. **Authentication Failures**:
   - Ensure JWT secrets match between systems
   - Verify that user IDs in requests match JWT identities

3. **CORS Issues**:
   - Configure CORS settings in the FastAPI backend to allow frontend origin

### Development Tips

1. **Hot Reload**: Backend supports hot reloading during development with `--reload` flag
2. **Logging**: Check backend logs for API request information and errors
3. **Debugging**: Use FastAPI's built-in validation and error reporting