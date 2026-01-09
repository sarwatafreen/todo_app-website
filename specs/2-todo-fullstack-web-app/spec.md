# Todo Full-Stack Web Application - Specification

## 1. Overview

### 1.1 Purpose
Transform the existing console-based todo application into a production-grade full-stack web application using Next.js, FastAPI, SQLModel, and Neon Serverless PostgreSQL. The application will now be called a "Task" management system with enhanced features.

### 1.2 Scope
- **In Scope**: Full-stack web application with CRUD operations for tasks, responsive UI, API layer, database layer, repository pattern, service layer, priority levels, tagging system
- **Out of Scope**: AI chatbot, Kubernetes deployment, email notifications, advanced analytics

### 1.3 Success Criteria
- All task operations (create, read, update, delete) work through the web interface
- Responsive UI that works on desktop and mobile devices
- Proper separation of concerns between frontend and backend
- All business logic encapsulated in the backend service layer
- Clean architecture following repository and service patterns
- Support for task priorities and tagging system

## 2. Functional Requirements

### 2.1 Core Task Operations
- **FR-001**: Users must be able to create new tasks with title, description, priority, and tags
- **FR-002**: Users must be able to view all tasks in a dashboard
- **FR-003**: Users must be able to update tasks (title, description, completion status, priority, tags)
- **FR-004**: Users must be able to delete tasks
- **FR-005**: Users must be able to mark tasks as completed/incomplete

### 2.2 Search, Filter & Sort Features
- **FR-006**: Users must be able to search tasks by keyword across title and description fields
- **FR-007**: Users must be able to filter tasks by completion status (all, active, completed)
- **FR-008**: Users must be able to filter tasks by priority (LOW, MEDIUM, HIGH)
- **FR-009**: Users must be able to filter tasks by tags
- **FR-010**: Users must be able to sort tasks by creation date (ascending/descending)
- **FR-011**: Users must be able to sort tasks by priority (LOW, MEDIUM, HIGH)
- **FR-012**: Users must be able to sort tasks alphabetically by title
- **FR-013**: Users must be able to combine multiple filters simultaneously (completion status, priority, tags)
- **FR-014**: Sorting functionality must work correctly with active filters applied

### 2.3 API Requirements
- **FR-011**: Backend must expose REST APIs for all task operations
- **FR-012**: APIs must follow REST conventions with proper HTTP methods and status codes
- **FR-013**: APIs must return JSON responses with appropriate error handling

## 3. Non-Functional Requirements

### 3.1 Performance
- **NFR-001**: API responses should be under 500ms for standard operations
- **NFR-002**: UI should be responsive with no noticeable lag for user interactions

### 3.2 Security
- **NFR-003**: No authentication required for Phase II (public task app)
- **NFR-004**: Input validation must be performed on both frontend and backend

### 3.3 Reliability
- **NFR-005**: Application should handle database connection issues gracefully
- **NFR-006**: Proper error handling and user feedback for all operations

## 4. Architecture

### 4.1 Technology Stack
- **Frontend**: Next.js 16 (App Router), TailwindCSS
- **Backend**: FastAPI (Python 3.13+)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Dependency Management**: `uv`

### 4.2 Layered Architecture
```
┌─────────────────┐
│   Frontend      │ ← Next.js with React components
├─────────────────┤
│   API Layer     │ ← FastAPI REST endpoints
├─────────────────┤
│   Service Layer │ ← Business logic and validation
├─────────────────┤
│ Repository Layer│ ← Data access and persistence
├─────────────────┤
│   Database      │ ← Neon PostgreSQL
└─────────────────┘
```

### 4.3 Data Model
- **Task Entity**:
  - id: UUID (Primary Key)
  - title: String (Required, max 255 chars)
  - description: String (Optional, max 1000 chars)
  - completed: Boolean (Default: false)
  - priority: String enum (LOW, MEDIUM, HIGH) (Default: MEDIUM)
  - tags: JSON List[String] (Optional)
  - created_at: DateTime (Auto-generated)
  - updated_at: DateTime (Auto-generated)

## 5. API Specification

### 5.1 Task Endpoints
- `GET /api/tasks` - Retrieve all tasks with optional search, filter, and sort parameters
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Retrieve a specific task
- `PUT /api/tasks/{id}` - Update a specific task
- `DELETE /api/tasks/{id}` - Delete a specific task
- `PATCH /api/tasks/{id}/toggle` - Toggle completion status

### 5.2 Query Parameters for GET /api/tasks
- `search` (string) - Keyword search across title and description fields
- `completed` (string) - Filter by completion status (all, active, completed)
- `priority` (string) - Filter by priority level (LOW, MEDIUM, HIGH)
- `tag` (string) - Filter by specific tag
- `sort` (string) - Sort by field (created_at, title, priority) - Default: created_at
- `order` (string) - Sort order (asc, desc) - Default: desc
- `page` (integer) - Page number for pagination - Default: 1
- `limit` (integer) - Items per page - Default: 20, Max: 100

### 5.3 Request/Response Examples
```
GET /api/tasks?search=meeting&completed=active&priority=HIGH&sort=created_at&order=desc
Response: [
  {
    "id": "uuid-string",
    "title": "Team meeting",
    "description": "Weekly team sync",
    "completed": false,
    "priority": "HIGH",
    "tags": ["work", "meeting"],
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
]
```

## 6. User Interface Requirements

### 6.1 UI Components
- **Task List**: Component to display all tasks with visual indicators for completion status, priority levels, and tags
- **Add Task Form**: Component for creating new tasks with fields for title, description, priority selector, and tags input
- **Edit Task Modal**: Modal component for editing existing tasks with all fields including priority and tags
- **Delete Confirmation**: Confirmation dialog component for delete operations
- **Priority Selector**: Component for selecting priority level (LOW, MEDIUM, HIGH)
- **Tags Input**: Component for adding and managing tags (list of strings)

### 6.2 Dashboard View
- Display list of all tasks using Task List component
- Show completion status with visual indicators
- Show priority levels with visual indicators
- Show tags with visual indicators
- Include action buttons for edit/delete
- Show filters for all/active/completed tasks
- Show filters for priority levels
- Show filters for tags

### 6.3 Form Components
- Create new task form using Add Task Form component (with priority and tags)
- Edit task form using Edit Task Modal component (with priority and tags)

### 6.4 UI Behavior
- All actions call backend APIs (no direct database access)
- UI refreshes automatically after API operations
- Validation handled server-side with appropriate error feedback to user
- Page refresh maintains data persistence through Neon DB

### 6.5 Responsive Design
- Mobile-first approach
- Properly sized touch targets
- Responsive grid/list layout

## 7. Implementation Rules

### 7.1 Backend Rules
- **FastAPI Architecture**: Use FastAPI routers → Services → Repositories pattern
- **SQLModel Usage**: SQLModel only used inside repositories for database operations
- **DB Connection**: Neon DB connection via environment variables (NEON_DATABASE_URL)
- **Layer Separation**: Maintain clear separation between API, service, and repository layers

### 7.2 Frontend Rules
- **Next.js App Router**: Use Next.js App Router pattern for navigation
- **Component Types**: Server Components preferred over Client Components where possible
- **No Client-Side DB Logic**: No direct database access from frontend - all operations through backend APIs
- **API Integration**: Frontend communicates with backend through API endpoints only

### 7.3 Error Handling Rules
- **API Responses**: All API endpoints return structured JSON errors with consistent format
- **UI Messages**: User interface displays friendly error messages derived from API responses
- **Validation Errors**: Server-side validation with proper error responses to frontend
- **Error Boundaries**: Implement error boundaries for graceful error handling in UI

### 7.4 Iteration Rule
- **Incorrect Output Handling**: If generated code/output is incorrect, refine specifications and regenerate
- **No Manual Patching**: Never manually patch code - always update specifications first
- **Regeneration Process**: When specs are refined, regenerate all affected components
- **Validation Loop**: Validate generated output against specifications before proceeding

### 7.5 Architecture Constraints
- Must follow repository pattern for data access (mandatory as per constitution)
- Must implement service layer for business logic (mandatory as per constitution)
- Frontend must not contain business logic (mandatory as per constitution)
- All database access must go through repositories (mandatory as per constitution)
- Backend must expose REST APIs only (mandatory as per constitution)

### 7.6 Technology Constraints
- No hardcoded data (non-negotiable as per constitution)
- No direct database queries outside repository layer (non-negotiable as per constitution)
- All changes must be driven by specifications (no manual code edits) (non-negotiable as per constitution)
- Must use mandatory technology stack as specified in constitution

### 7.7 Constitutional Compliance
- Spec-driven development only (all changes via spec refinements) (non-negotiable)
- No manual code edits allowed (non-negotiable)
- All implementation must follow architectural rules specified in constitution
- Repository pattern and service layer are mandatory requirements (non-negotiable)
- Frontend must never contain business logic (non-negotiable)
- Backend must expose REST APIs only (non-negotiable)

## 8. Acceptance Criteria

### 8.1 Core Functionality
- [ ] Users can create new tasks through the web interface using Add Task Form component
- [ ] Users can view all tasks in a dashboard using Task List component
- [ ] Users can update tasks (title, description, status, priority, tags) using Edit Task Modal component
- [ ] Users can delete tasks with Delete Confirmation component
- [ ] Users can mark tasks as completed/incomplete
- [ ] Tasks persist in Neon DB and page refresh does not lose data

### 8.2 Advanced Features
- [ ] Users can filter tasks by completion status
- [ ] Users can filter tasks by priority (LOW, MEDIUM, HIGH) using Priority Selector component
- [ ] Users can filter tasks by tags using Tags Input component
- [ ] Users can sort tasks by creation date (ascending/descending)
- [ ] Users can sort tasks by priority (LOW, MEDIUM, HIGH)
- [ ] Users can sort tasks alphabetically by title
- [ ] Users can search tasks by keyword across title and description fields
- [ ] Users can combine multiple filters simultaneously (completion status, priority, tags)
- [ ] Sorting functionality works correctly with active filters applied

### 8.3 UI Behavior Requirements
- [ ] All actions call backend APIs (no direct database access)
- [ ] UI refreshes automatically after API operations
- [ ] Validation handled server-side with appropriate error feedback to user
- [ ] Page refresh maintains data persistence through Neon DB

### 8.4 Quality Requirements
- [ ] All API endpoints return proper HTTP status codes
- [ ] Frontend properly handles API errors
- [ ] Application follows the layered architecture
- [ ] Responsive design works on different screen sizes
- [ ] No business logic exists in the frontend layer
- [ ] All specified UI components are implemented and functional

## 9. Dependencies
- Next.js 16 with App Router
- FastAPI
- SQLModel
- Neon PostgreSQL
- uv for dependency management
- TailwindCSS for styling