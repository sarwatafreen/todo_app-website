# Quickstart Guide: Todo Full-Stack Web Application

**Feature**: Todo Full-Stack Web Application
**Date**: 2026-01-26
**Author**: Claude Code

## Overview

This guide provides step-by-step instructions for setting up, configuring, and running the secure, multi-user todo web application. The application consists of a Next.js frontend and a FastAPI backend with Neon Serverless PostgreSQL database and Better Auth for authentication.

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- Git for version control
- A Neon Serverless PostgreSQL account
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
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
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

### 3. Frontend Setup

#### Navigate to the frontend directory:
```bash
cd frontend
```

#### Install dependencies:
```bash
npm install
```

#### Set up environment variables:
Create a `.env.local` file in the frontend directory with the following variables:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
NEXTAUTH_SECRET="your-nextauth-secret"
NEXTAUTH_URL=http://localhost:3000
```

#### Start the frontend development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Configuration

### Authentication Setup

1. **JWT Secret**: Generate a strong JWT secret (at least 32 characters) for both frontend and backend
2. **Better Auth**: Configure Better Auth with your preferred authentication methods (email/password, social logins)
3. **Database**: Ensure your Neon PostgreSQL database is properly configured with the correct connection string

### Database Configuration

1. Update the `DATABASE_URL` in your backend `.env` file to point to your Neon database
2. Ensure the database has the correct permissions for the application
3. Run the initial migrations to create the required tables

## Running the Application

### Development Mode

Start both the backend and frontend in development mode:

1. **Backend**: `cd backend && uvicorn src.main:app --reload`
2. **Frontend**: `cd frontend && npm run dev`

Both services will auto-reload on code changes.

### Production Mode

Build and run the application in production mode:

1. **Backend**: Deploy using a WSGI/ASGI server like Gunicorn
2. **Frontend**: Build with `npm run build` and serve with a web server

## API Endpoints

### Authentication Endpoints
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Authenticate a user
- `POST /auth/logout` - Logout a user

### Todo Endpoints
- `GET /users/{user_id}/todos` - Get all todos for a user
- `POST /users/{user_id}/todos` - Create a new todo for a user
- `GET /users/{user_id}/todos/{todo_id}` - Get a specific todo
- `PUT /users/{user_id}/todos/{todo_id}` - Update a specific todo
- `PATCH /users/{user_id}/todos/{todo_id}/complete` - Toggle todo completion status
- `DELETE /users/{user_id}/todos/{todo_id}` - Delete a specific todo

## Security Notes

1. **JWT Validation**: All API endpoints require a valid JWT token in the Authorization header
2. **User Isolation**: Users can only access their own data
3. **Environment Variables**: Never commit secrets to version control
4. **HTTPS**: Use HTTPS in production for all communications

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Verify your Neon PostgreSQL connection string
   - Check that the database is accessible from your network

2. **Authentication Failures**:
   - Ensure JWT secrets match between frontend and backend
   - Verify that user IDs in requests match JWT identities

3. **CORS Issues**:
   - Configure CORS settings in the FastAPI backend to allow frontend origin

### Development Tips

1. **Hot Reload**: Both frontend and backend support hot reloading during development
2. **Logging**: Check backend logs for API request information and errors
3. **Frontend Console**: Monitor browser console for client-side errors

## Testing

Run backend tests:
```bash
cd backend
pytest
```

Run frontend tests:
```bash
cd frontend
npm run test
```

## Next Steps

1. Complete user registration and login flow
2. Implement the full todo management interface
3. Add additional security measures as needed
4. Deploy to your preferred hosting platform