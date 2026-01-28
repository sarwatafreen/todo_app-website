# Todo Full-Stack Web Application

A secure, multi-user todo application with JWT-based authentication built using the Agentic Dev Stack methodology.

## Architecture

- **Frontend**: Next.js 16+ with App Router
- **Backend**: Python FastAPI
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Authentication**: Better Auth with JWT

## Features

- User registration and authentication
- Secure JWT-based authentication
- Personal todo management (CRUD operations)
- Data isolation - users can only access their own todos
- Responsive web interface

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login a user
- `POST /api/auth/logout` - Logout a user

### Todo Management
- `GET /api/users/{user_id}/todos` - Get all todos for a user
- `POST /api/users/{user_id}/todos` - Create a new todo for a user
- `GET /api/users/{user_id}/todos/{todo_id}` - Get a specific todo
- `PUT /api/users/{user_id}/todos/{todo_id}` - Update a specific todo
- `DELETE /api/users/{user_id}/todos/{todo_id}` - Delete a specific todo
- `PATCH /api/users/{user_id}/todos/{todo_id}/complete` - Toggle completion status

## Setup Instructions

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@localhost/todo_db
   JWT_SECRET_KEY=your-super-secret-key-change-in-production-keep-it-long-and-random
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables by creating a `.env.local` file:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```

## Security Features

- All API endpoints require valid JWT authentication
- Strict user data isolation - users can only access their own data
- Passwords are securely hashed using bcrypt
- User ID validation on every request to prevent cross-user access

## Development

This project was built using the Agentic Dev Stack methodology with Claude Code:
1. Specification → Planning → Task Decomposition → Implementation
2. All code generated via AI agents with minimal manual intervention
3. Strict adherence to security-first design principles

## Contributing

This project was generated using an automated process. For modifications, please follow the Agentic Dev Stack methodology:
1. Update the specification
2. Regenerate the plan
3. Update the tasks
4. Implement via Claude Code