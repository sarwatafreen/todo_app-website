# Task Full-Stack Web Application - Plan

## 1. Architecture Overview

### 1.1 System Architecture
The application will follow a clean architecture pattern with clear separation of concerns:

- **Presentation Layer**: Next.js frontend with React components
- **API Layer**: FastAPI REST endpoints
- **Business Logic Layer**: Service layer with business rules
- **Data Access Layer**: Repository pattern for database operations
- **Data Layer**: Neon PostgreSQL database

### 1.2 Technology Stack Decision
- **Frontend**: Next.js 16 with App Router chosen for modern React development and built-in routing
- **Backend**: FastAPI selected for its speed, automatic API documentation, and excellent Python type hints support
- **ORM**: SQLModel chosen as it combines SQLAlchemy and Pydantic, providing both database modeling and validation
- **Database**: Neon Serverless PostgreSQL selected for its serverless capabilities and compatibility with PostgreSQL
- **Dependency Management**: `uv` for fast Python package management

## 2. Data Layer Design

### 2.1 Database Schema
The database will contain a single main table for tasks:

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    tags JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 2.2 SQLModel Entity
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List
import json

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "MEDIUM"  # Enum: LOW, MEDIUM, HIGH
    tags: Optional[List[str]] = None

class Task(TaskBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## 3. Repository Layer Design

### 3.1 Repository Interface
All repositories will follow a common interface pattern with standard CRUD operations:

- `create(entity)`: Create a new entity
- `get_by_id(id)`: Retrieve entity by ID
- `get_all(filters)`: Retrieve all entities with optional filters
- `update(id, updates)`: Update entity by ID
- `delete(id)`: Delete entity by ID

### 3.2 Task Repository
The TaskRepository will implement the repository interface with SQLModel-specific operations for the Task entity, including methods for filtering by priority and tags.

## 4. Service Layer Design

### 4.1 Service Responsibilities
- Implement business logic for task operations
- Validate input data (including priority enum and tags format)
- Coordinate between repositories and other services
- Handle transactions where needed
- Implement filtering by completion status, priority, and tags
- Implement sorting by creation date, title, and priority

### 4.2 Task Service
The TaskService will contain methods for:
- Creating tasks with validation for priority and tags
- Retrieving tasks with filtering/sorting/search capabilities
- Updating task status, priority, and tags
- Deleting tasks
- Filtering by completion status, priority, and tags
- Sorting by creation date, title, and priority

## 5. API Layer Design

### 5.1 REST API Endpoints
The API will follow REST conventions with proper HTTP methods and status codes:

- `GET /api/tasks` - Retrieve tasks with optional query parameters for filtering (search, completed, priority, tag, sort, order)
- `POST /api/tasks` - Create a new task with priority and tags
- `GET /api/tasks/{id}` - Retrieve a specific task
- `PUT /api/tasks/{id}` - Update a specific task with priority and tags
- `DELETE /api/tasks/{id}` - Delete a specific task
- `PATCH /api/tasks/{id}/toggle` - Toggle completion status

### 5.2 Request/Response Models
Pydantic models will be used for request/response validation and serialization, including validation for priority enum and tags array.

## 6. Frontend Architecture

### 6.1 Next.js App Structure
Using the App Router pattern:
```
app/
├── layout.tsx
├── page.tsx (dashboard)
├── globals.css
└── api/
    └── tasks/
        └── route.ts (proxy to backend if needed)
```

### 6.2 Component Structure
- Reusable components for task items with priority and tag indicators
- Form components for creating/editing tasks with priority and tags
- Filter/sort components for priority and tags
- Layout components

### 6.3 State Management
- Client-side state for UI interactions
- API integration for data persistence
- Error handling and loading states
- State management for priority and tags

## 7. Development Approach

### 7.1 Implementation Order
1. Set up project structure and dependencies
2. Implement database layer and models with priority and tags
3. Create repository layer with priority and tags filtering
4. Build service layer with priority and tags business logic
5. Develop API endpoints with priority and tags support
6. Create frontend components with priority and tags UI
7. Integrate frontend with backend APIs
8. Testing and validation

### 7.2 Testing Strategy
- Unit tests for repository and service layers including priority and tags functionality
- Integration tests for API endpoints with all new features
- Frontend component tests for priority and tags UI
- End-to-end tests for critical user flows including priority and tags

## 8. Configuration and Deployment

### 8.1 Environment Variables
- Database connection string (Neon)
- API configuration
- Development/production settings

### 8.2 Dependency Management
- Use `uv` for fast dependency installation
- Maintain proper dependency versions
- Create requirements files for different environments

## 9. Constitutional Compliance

### 9.1 Spec-Driven Development Requirements
- All implementation must follow spec-driven development methodology (non-negotiable)
- No manual code edits allowed - all changes must be driven by specifications
- Implementation must strictly adhere to architectural rules in constitution

### 9.2 Technology Stack Compliance
- Frontend must use Next.js 16 (App Router) and TailwindCSS as mandated
- Backend must use FastAPI with Python 3.13+ as mandated
- ORM must be SQLModel as specified
- Database must be Neon Serverless PostgreSQL as required
- Dependency management must use `uv` as specified

### 9.3 Architectural Pattern Compliance
- Repository pattern is mandatory and must be implemented for all data access
- Service layer is mandatory and must contain all business logic
- Frontend must never contain business logic
- Backend must expose REST APIs only

## 10. Implementation Rules

### 10.1 Backend Rules
- **FastAPI Architecture**: Use FastAPI routers → Services → Repositories pattern
- **SQLModel Usage**: SQLModel only used inside repositories for database operations
- **DB Connection**: Neon DB connection via environment variables (NEON_DATABASE_URL)
- **Layer Separation**: Maintain clear separation between API, service, and repository layers

### 10.2 Frontend Rules
- **Next.js App Router**: Use Next.js App Router pattern for navigation
- **Component Types**: Server Components preferred over Client Components where possible
- **No Client-Side DB Logic**: No direct database access from frontend - all operations through backend APIs
- **API Integration**: Frontend communicates with backend through API endpoints only

### 10.3 Error Handling Rules
- **API Responses**: All API endpoints return structured JSON errors with consistent format
- **UI Messages**: User interface displays friendly error messages derived from API responses
- **Validation Errors**: Server-side validation with proper error responses to frontend
- **Error Boundaries**: Implement error boundaries for graceful error handling in UI

### 10.4 Iteration Rule
- **Incorrect Output Handling**: If generated code/output is incorrect, refine specifications and regenerate
- **No Manual Patching**: Never manually patch code - always update specifications first
- **Regeneration Process**: When specs are refined, regenerate all affected components
- **Validation Loop**: Validate generated output against specifications before proceeding

## 11. Risk Analysis and Mitigation

### 11.1 Technical Risks
- **Database connection issues**: Implement proper connection pooling and error handling
- **API performance**: Monitor response times and optimize queries, especially for tags filtering
- **Frontend performance**: Implement proper data fetching and caching strategies
- **Tags filtering performance**: Optimize GIN indexes on tags column for efficient tag-based queries

### 11.2 Constitutional Compliance Risks
- **Deviation from spec-driven approach**: Regular validation against specifications
- **Technology stack violations**: Strict adherence to mandated technologies
- **Architecture pattern violations**: Regular code reviews for compliance

### 11.3 Mitigation Strategies
- Comprehensive error handling at all layers
- Proper logging and monitoring setup
- Performance testing during development
- Regular validation against constitutional requirements