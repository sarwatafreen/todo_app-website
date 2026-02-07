# Todo AI Chatbot - Phase 3

A stateless AI-powered todo management system with natural language chat interface built using Python FastAPI backend and Next.js frontend.

## Features

- **AI-Powered Chat Interface**: Natural language interaction to manage todos
- **Stateless Architecture**: All conversation state stored in database
- **Secure Authentication**: JWT-based authentication with user isolation
- **MCP Tools Integration**: AI agent uses MCP tools for task operations
- **Production Ready**: Docker-ready deployment configuration

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: Neon PostgreSQL with SQLModel ORM
- **AI Integration**: OpenAI Agents SDK
- **Authentication**: JWT-based with Better Auth patterns
- **Language**: Python 3.11

### Frontend
- **Framework**: Next.js 16+ with App Router
- **UI Components**: Custom ChatKit implementation
- **Styling**: Tailwind CSS
- **API Client**: Axios
- **Language**: TypeScript

## Architecture

The system follows a strict separation of concerns:

- **Chat UI**: User interaction layer
- **FastAPI**: Request orchestration
- **AI Agent**: Reasoning & tool selection
- **MCP Tools**: Task execution
- **Database**: Source of truth

## Project Structure

```
phase-3/
├─ backend/
│   ├─ src/
│   │   ├─ main.py                    # FastAPI app + chat endpoint registration
│   │   ├─ models.py                  # SQLModel: Task, Conversation, Message
│   │   ├─ mcp_tools.py               # MCP tools (add, list, complete, update, delete)
│   │   ├─ agents.py                  # OpenAI Agents SDK setup & runner
│   │   ├─ dependencies.py            # DB, auth, JWT dependencies
│   │   ├─ utils.py                   # Helper functions
│   │   ├─ database.py                # Database setup
│   │   ├─ settings.py                # App settings
│   │   ├─ middleware/
│   │   │   └─ auth_middleware.py   # Authentication middleware
│   │   ├─ api/
│   │   │   ├─ chat_endpoints.py     # Chat interface endpoints
│   │   │   └─ task_endpoints.py     # Task CRUD endpoints
│   │   └─ auth/
│   │       └─ api/
│   │           └─ auth_endpoints.py # Authentication endpoints
│   ├─ requirements.txt               # Dependencies including openai
│   └─ .env                         # Environment variables
│
├─ frontend/
│   ├─ src/
│   │   ├─ app/
│   │   │   └─ index.tsx             # Chat page
│   │   ├─ components/
│   │   │   └─ ChatKit/
│   │   │       └─ ChatInterface.tsx # Chat interface component
│   │   └─ services/
│   │       └─ chatApi.ts            # API service for agent-backed endpoint
│   └─ package.json                 # Dependencies
│
├─ specs/
│   ├─ sp.constitution.md            # Phase III constitution
│   ├─ spec-4-chat-interface.md      # Chat interface spec
│   ├─ spec-5-mcp-tools.md           # MCP tools spec
│   └─ spec-6-agent-behavior.md      # Agent behavior spec
│
├─ migrations/                       # DB migration scripts
└─ README.md                        # This file
```

## Installation & Setup

### Backend Setup

1. **Clone the repository**
```bash
git clone <repo-url>
cd phase-3/backend
```

2. **Create virtual environment and install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start the backend server**
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the frontend development server**
```bash
npm run dev
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database
JWT_SECRET_KEY=your-super-secret-key-change-in-production
OPENAI_API_KEY=your-openai-api-key
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## API Endpoints

### Chat Endpoint
- **POST** `/api/{user_id}/chat` - Process chat messages with AI agent

### Task Endpoints
- **GET** `/api/{user_id}/tasks` - Get all tasks for user
- **POST** `/api/{user_id}/tasks` - Create a new task
- **GET** `/api/{user_id}/tasks/{task_id}` - Get specific task
- **PUT** `/api/{user_id}/tasks/{task_id}` - Update a task
- **DELETE** `/api/{user_id}/tasks/{task_id}` - Delete a task
- **PATCH** `/api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

### Auth Endpoints
- **POST** `/auth/register` - Register new user
- **POST** `/auth/login` - Login user
- **GET** `/auth/profile` - Get user profile

## MCP Tools Available to AI Agent

- `add_task(user_id, title, description)` - Add a new task
- `list_tasks(user_id, status)` - List tasks, optionally filtered by status
- `complete_task(user_id, task_id)` - Mark a task as completed
- `update_task(user_id, task_id, title, description, status)` - Update a task
- `delete_task(user_id, task_id)` - Delete a task

## Docker Deployment

Coming soon - Docker configuration files will be added for easy containerized deployment.

## Development

### Running Tests
Backend tests:
```bash
cd backend
python -m pytest tests/
```

Frontend tests:
```bash
cd frontend
npm run test
```

### Running Linting
Backend:
```bash
cd backend
flake8 .
black --check .
```

Frontend:
```bash
cd frontend
npm run lint
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository.