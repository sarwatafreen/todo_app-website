# Todo Full-Stack Web Application - Quickstart Guide

## Prerequisites

- Node.js 18+ (for Next.js frontend)
- Python 3.13+ (for FastAPI backend)
- `uv` package manager (install with `pip install uv`)
- A Neon PostgreSQL account (for serverless database)

## Environment Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd todo-fullstack-web-app
```

### 2. Set up Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Install dependencies with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install fastapi sqlmodel python-multipart "uvicorn[standard]"
```

### 3. Set up Frontend (Next.js)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Configuration

### 1. Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL="your-neon-database-connection-string"
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Database Setup
The application will automatically create tables on startup using SQLModel's create_engine and create_all method.

## Running the Application

### 1. Start the Backend
```bash
# In backend directory
uvicorn main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
# In frontend directory
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Documentation: http://localhost:8000/docs

## Project Structure

```
todo-fullstack-web-app/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── models/                 # SQLModel entity definitions
│   ├── repositories/           # Data access layer
│   ├── services/               # Business logic layer
│   ├── api/                    # API endpoints
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── app/                    # Next.js app router pages
│   ├── components/             # React components
│   ├── lib/                    # Utility functions
│   └── package.json            # Node.js dependencies
└── docs/                       # Documentation
```

## API Endpoints

### Todo Management
- `GET /api/todos` - Get all todos with optional filters
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a specific todo
- `DELETE /api/todos/{id}` - Delete a specific todo
- `PATCH /api/todos/{id}/toggle` - Toggle completion status

## Development Commands

### Backend
```bash
# Run with auto-reload
uvicorn main:app --reload

# Run tests
python -m pytest

# Format code
black .
```

### Frontend
```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Format code
npm run format
```

## Database Migrations

The application uses SQLModel's automatic table creation. For production, consider implementing Alembic for migration management:

```bash
# Install alembic
pip install alembic

# Initialize alembic
alembic init alembic

# Generate migration
alembic revision --autogenerate -m "Migration message"

# Apply migration
alembic upgrade head
```