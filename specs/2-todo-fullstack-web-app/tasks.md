# Task Full-Stack Web Application - Tasks

## Phase 0: Implementation Rules

### Task 0.1: Understand Backend Rules
- **Objective**: Ensure understanding of backend architecture and implementation rules
- **Acceptance Criteria**:
  - FastAPI routers → Services → Repositories pattern is understood
  - SQLModel only used inside repositories for database operations
  - Neon DB connection via environment variables (NEON_DATABASE_URL)
  - Clear separation between API, service, and repository layers is maintained
- **Tests**:
  - [ ] FastAPI router → service → repository pattern is followed
  - [ ] SQLModel is only used inside repositories
  - [ ] Database connection uses environment variables
  - [ ] Layer separation is maintained throughout implementation

### Task 0.2: Understand Frontend Rules
- **Objective**: Ensure understanding of frontend architecture and implementation rules
- **Acceptance Criteria**:
  - Next.js App Router pattern is understood
  - Server Components are preferred over Client Components where possible
  - No direct database access from frontend - all operations through backend APIs
  - Frontend communicates with backend through API endpoints only
- **Tests**:
  - [ ] Next.js App Router pattern is followed
  - [ ] Server Components are used where possible
  - [ ] No client-side database access is implemented
  - [ ] All data operations go through backend APIs

### Task 0.3: Understand Error Handling Rules
- **Objective**: Ensure understanding of error handling implementation rules
- **Acceptance Criteria**:
  - All API endpoints return structured JSON errors with consistent format
  - User interface displays friendly error messages derived from API responses
  - Server-side validation with proper error responses to frontend
  - Error boundaries are implemented for graceful error handling in UI
- **Tests**:
  - [ ] API endpoints return structured JSON errors
  - [ ] UI displays friendly error messages
  - [ ] Server-side validation is implemented
  - [ ] Error boundaries handle errors gracefully

### Task 0.4: Understand Iteration Rule
- **Objective**: Ensure understanding of the iteration and refinement process
- **Acceptance Criteria**:
  - If generated code/output is incorrect, specifications are refined and regenerated
  - No manual patching of code - always update specifications first
  - When specs are refined, all affected components are regenerated
  - Generated output is validated against specifications before proceeding
- **Tests**:
  - [ ] Specifications are refined when output is incorrect
  - [ ] No manual code patches are made
  - [ ] Affected components are regenerated when specs change
  - [ ] Output is validated against specifications

## Phase 1: Project Setup and Database Layer

### Task 1.1: Initialize Project Structure
- **Objective**: Set up Next.js frontend and FastAPI backend projects
- **Acceptance Criteria**:
  - Next.js app with App Router is created
  - FastAPI backend project is set up
  - Dependency management with `uv` is configured
  - Basic project structure follows specification
  - Implementation follows Phase II Implementation Rules
- **Tests**:
  - [ ] Can run Next.js development server
  - [ ] Can run FastAPI development server
  - [ ] Dependencies are properly managed with `uv`
  - [ ] Implementation follows backend rules (Task 0.1)
  - [ ] Implementation follows frontend rules (Task 0.2)
  - [ ] Error handling rules are considered (Task 0.3)

### Task 1.2: Set up Database Connection
- **Objective**: Configure Neon PostgreSQL connection with SQLModel
- **Acceptance Criteria**:
  - Database connection is established via environment variables
  - SQLModel is properly configured and only used in repositories
  - Connection pooling is set up
  - Implementation follows Phase II Implementation Rules
- **Tests**:
  - [ ] Database connection can be established via environment variables
  - [ ] Connection handles disconnections gracefully
  - [ ] SQLModel is configured for repository layer only
  - [ ] Implementation follows backend rules (Task 0.1)

### Task 1.3: Create Task Entity Model
- **Objective**: Implement the Task SQLModel entity with priority and tags
- **Acceptance Criteria**:
  - Task entity matches specification with priority and tags fields
  - Proper field types and constraints are applied (priority enum, tags as JSON)
  - Created_at and updated_at fields auto-populate
  - Implementation follows Phase II Implementation Rules
- **Tests**:
  - [ ] Task entity can be instantiated with valid data
  - [ ] Entity validation works correctly for all fields
  - [ ] Auto-generated fields work as expected
  - [ ] Priority field validates enum values (LOW, MEDIUM, HIGH)
  - [ ] Tags field accepts and stores array of strings
  - [ ] Implementation follows backend rules (Task 0.1)

## Phase 2: Repository and Service Layer

### Task 2.1: Implement Task Repository
- **Objective**: Create TaskRepository with CRUD operations and advanced filtering/sorting/search
- **Acceptance Criteria**:
  - Repository follows the defined interface
  - All CRUD operations are implemented
  - Proper error handling is in place
  - Filtering by completion status, priority and tags is supported
  - Sorting by creation date, title, and priority is supported
  - Search by title and description is supported
  - Multiple filters can be combined simultaneously
  - Sorting works correctly with active filters applied
- **Tests**:
  - [ ] Can create tasks through repository
  - [ ] Can read tasks through repository
  - [ ] Can update tasks through repository
  - [ ] Can delete tasks through repository
  - [ ] Repository handles database errors gracefully
  - [ ] Repository supports filtering by completion status
  - [ ] Repository supports filtering by priority
  - [ ] Repository supports filtering by tags
  - [ ] Repository supports sorting by creation date
  - [ ] Repository supports sorting by title
  - [ ] Repository supports sorting by priority
  - [ ] Repository supports search by title and description
  - [ ] Repository supports combining multiple filters simultaneously
  - [ ] Repository supports sorting with active filters applied

### Task 2.2: Implement Task Service
- **Objective**: Create TaskService with business logic and advanced filtering/sorting/search
- **Acceptance Criteria**:
  - Service implements all required business logic
  - Input validation is performed for all fields
  - Filtering by completion status, priority, and tags is implemented
  - Sorting by creation date, title, and priority is implemented
  - Search by title and description is implemented
  - Multiple filters can be combined simultaneously
  - Sorting works correctly with active filters applied
  - Implementation follows Phase II Implementation Rules
- **Tests**:
  - [ ] Service validates task creation input
  - [ ] Service supports filtering by completion status
  - [ ] Service supports filtering by priority (LOW, MEDIUM, HIGH)
  - [ ] Service supports filtering by tags
  - [ ] Service supports sorting by creation date/title/priority
  - [ ] Service supports searching by title/description
  - [ ] Service supports combining multiple filters simultaneously
  - [ ] Service supports sorting with active filters applied
  - [ ] Implementation follows backend rules (Task 0.1)
  - [ ] Service layer maintains clear separation from API and repository layers (Task 0.1)

## Phase 3: API Layer

### Task 3.1: Create Task API Endpoints
- **Objective**: Implement REST API endpoints for task operations
- **Acceptance Criteria**:
  - All required endpoints are implemented
  - Proper HTTP status codes are returned
  - Request/response validation is in place
  - Query parameters for filtering/sorting/searching are supported
  - Implementation follows Phase II Implementation Rules
- **Tests**:
  - [ ] GET /api/tasks returns list of tasks with filtering options
  - [ ] POST /api/tasks creates a new task with priority and tags
  - [ ] GET /api/tasks/{id} returns specific task
  - [ ] PUT /api/tasks/{id} updates a specific task
  - [ ] DELETE /api/tasks/{id} deletes a specific task
  - [ ] PATCH /api/tasks/{id}/toggle toggles completion status
  - [ ] API supports query parameters: search, completed, priority, tag, sort, order
  - [ ] Implementation follows backend rules (Task 0.1)
  - [ ] API returns structured JSON errors with consistent format (Task 0.3)

### Task 3.2: API Error Handling
- **Objective**: Implement comprehensive error handling for API
- **Acceptance Criteria**:
  - Proper error responses for validation failures
  - Error responses for not found resources
  - Error responses for server-side issues
  - Validation errors for priority enum and tags format
  - Implementation follows Phase II Implementation Rules
- **Tests**:
  - [ ] API returns 400 for invalid input
  - [ ] API returns 400 for invalid priority values
  - [ ] API returns 400 for invalid tags format
  - [ ] API returns 404 for non-existent resources
  - [ ] API returns 500 for server errors with appropriate messages
  - [ ] Implementation follows backend rules (Task 0.1)
  - [ ] API returns structured JSON errors with consistent format (Task 0.3)

## Phase 4: Frontend Implementation

### Task 4.1: Create Task Dashboard UI
- **Objective**: Build the main dashboard to display tasks using Task List component
- **Acceptance Criteria**:
  - Responsive layout that works on mobile/desktop
  - Uses Task List component to display tasks with completion status, priority, and tags
  - Shows action buttons for each task
  - Visual indicators for priority levels
  - Visual indicators for tags
  - UI refreshes automatically after API operations
  - Implementation follows Phase II Implementation Rules
  - All UI components behave according to specified behavior requirements
- **Tests**:
  - [ ] Dashboard renders properly on desktop
  - [ ] Dashboard renders properly on mobile
  - [ ] Tasks are displayed with correct information using Task List component
  - [ ] Visual indicators show completion status
  - [ ] Visual indicators show priority levels
  - [ ] Visual indicators show tags
  - [ ] UI refreshes automatically after API operations
  - [ ] Implementation follows frontend rules (Task 0.2)
  - [ ] All actions call backend APIs (no direct database access) (Task 0.2)
  - [ ] UI components follow behavior requirements (Task 0.2)
  - [ ] Page refresh maintains data persistence through Neon DB (Task 0.2)

### Task 4.2: Implement Task Creation Form
- **Objective**: Create Add Task Form component for adding new tasks
- **Acceptance Criteria**:
  - Form includes fields for title, description, priority, and tags
  - Form validation is implemented for all fields
  - Form integrates with backend API
  - Uses Add Task Form component as specified
  - All actions call backend APIs (no direct database access)
  - Implementation follows Phase II Implementation Rules
- **Tests**:
  - [ ] Form validates required fields
  - [ ] Form validates priority field (LOW, MEDIUM, HIGH)
  - [ ] Form accepts tags input
  - [ ] Form submits data to backend API
  - [ ] New task appears in dashboard after creation
  - [ ] Add Task Form component functions as specified
  - [ ] Implementation follows frontend rules (Task 0.2)
  - [ ] Form calls backend API for all operations (Task 0.2)
  - [ ] Server-side validation errors are properly displayed (Task 0.3)

### Task 4.3: Implement Task Update Functionality
- **Objective**: Create Edit Task Modal component for updating existing tasks
- **Acceptance Criteria**:
  - Uses Edit Task Modal component to edit task title, description, priority, and tags
  - Users can toggle completion status
  - Changes are persisted to backend
  - All actions call backend APIs (no direct database access)
- **Tests**:
  - [ ] Task title can be updated
  - [ ] Task description can be updated
  - [ ] Task priority can be updated
  - [ ] Task tags can be updated
  - [ ] Completion status can be toggled
  - [ ] Changes are saved to backend
  - [ ] Edit Task Modal component functions as specified

### Task 4.4: Implement Task Deletion
- **Objective**: Implement task deletion with Delete Confirmation component
- **Acceptance Criteria**:
  - Delete button is available for each task
  - Uses Delete Confirmation component for delete operations
  - Deletion is processed through backend API
  - All actions call backend APIs (no direct database access)
- **Tests**:
  - [ ] Delete button is visible for each task
  - [ ] Confirmation prevents accidental deletion using Delete Confirmation component
  - [ ] Task is removed from UI after deletion
  - [ ] Backend API processes deletion correctly

### Task 4.5: Implement Priority Selector Component
- **Objective**: Create Priority Selector component for selecting priority levels
- **Acceptance Criteria**:
  - Component allows selection of priority level (LOW, MEDIUM, HIGH)
  - Component is used in Add Task Form and Edit Task Modal
  - Proper validation for priority values
- **Tests**:
  - [ ] Priority Selector component allows selection of LOW, MEDIUM, HIGH
  - [ ] Component is integrated in Add Task Form
  - [ ] Component is integrated in Edit Task Modal
  - [ ] Proper validation for priority values

### Task 4.6: Implement Tags Input Component
- **Objective**: Create Tags Input component for managing tags
- **Acceptance Criteria**:
  - Component allows adding and managing tags (list of strings)
  - Component is used in Add Task Form and Edit Task Modal
  - Proper validation for tags format
- **Tests**:
  - [ ] Tags Input component allows adding tags
  - [ ] Tags Input component allows managing tags
  - [ ] Component is integrated in Add Task Form
  - [ ] Component is integrated in Edit Task Modal
  - [ ] Proper validation for tags format

## Phase 5: Advanced Features

### Task 5.1: Implement Filtering
- **Objective**: Add filtering by completion status, priority, and tags
- **Acceptance Criteria**:
  - Filter options are available (all, active, completed)
  - Priority filter options are available (LOW, MEDIUM, HIGH)
  - Tag filter options are available
  - Tasks are filtered based on selection
  - Filtered state is reflected in UI
  - Multiple filters can be combined simultaneously (completion status, priority, tags)
  - Implementation follows Phase II Implementation Rules
- **Tests**:
  - [ ] "All" filter shows all tasks
  - [ ] "Active" filter shows only incomplete tasks
  - [ ] "Completed" filter shows only completed tasks
  - [ ] Priority filters work correctly
  - [ ] Tag filters work correctly
  - [ ] Multiple filters can be applied simultaneously
  - [ ] Combined filters work correctly together
  - [ ] Implementation follows frontend rules (Task 0.2)
  - [ ] All filtering operations call backend API (Task 0.2)

### Task 5.2: Implement Sorting
- **Objective**: Add sorting functionality for tasks
- **Acceptance Criteria**:
  - Tasks can be sorted by creation date
  - Tasks can be sorted by title
  - Tasks can be sorted by priority
  - Sorting options are available in UI
  - Sorting works correctly with active filters applied
  - Implementation follows Phase II Implementation Rules
- **Tests**:
  - [ ] Tasks sort by creation date ascending/descending
  - [ ] Tasks sort by title alphabetically
  - [ ] Tasks sort by priority (LOW, MEDIUM, HIGH)
  - [ ] Sorting works correctly when filters are applied
  - [ ] Sorting maintains filter state when changing sort order
  - [ ] Implementation follows frontend rules (Task 0.2)
  - [ ] All sorting operations call backend API (Task 0.2)

### Task 5.3: Implement Search
- **Objective**: Add search functionality for tasks
- **Acceptance Criteria**:
  - Search input field is available
  - Tasks are filtered based on search term
  - Search works on title and description
  - Search works with active filters and sorting applied
  - Implementation follows Phase II Implementation Rules
- **Tests**:
  - [ ] Search filters tasks by title
  - [ ] Search filters tasks by description
  - [ ] Search is case-insensitive
  - [ ] Search works with active filters applied
  - [ ] Search works with active sorting applied
  - [ ] Implementation follows frontend rules (Task 0.2)
  - [ ] All search operations call backend API (Task 0.2)

## Phase 6: Integration and Testing

### Task 6.1: Frontend-Backend Integration
- **Objective**: Connect frontend to backend API with proper UI behavior
- **Acceptance Criteria**:
  - All frontend operations call backend API (no direct database access)
  - API responses are properly handled
  - Error states are handled gracefully with server-side validation feedback
  - UI refreshes automatically after API operations
  - Page refresh maintains data persistence through Neon DB
  - All new features (priority, tags, search, filter, sort) work end-to-end
  - Multiple filters can be combined simultaneously
  - Sorting works correctly with active filters applied
- **Tests**:
  - [ ] Create operation calls backend API with priority and tags
  - [ ] Read operations call backend API
  - [ ] Update operations call backend API with priority and tags
  - [ ] Delete operations call backend API
  - [ ] All filtering, sorting, and search operations work with API
  - [ ] UI refreshes automatically after API operations
  - [ ] Page refresh maintains data persistence through Neon DB
  - [ ] Server-side validation errors are properly displayed to user
  - [ ] Search functionality works end-to-end
  - [ ] Filtering by completion status works end-to-end
  - [ ] Filtering by priority works end-to-end
  - [ ] Filtering by tags works end-to-end
  - [ ] Multiple filters can be combined simultaneously end-to-end
  - [ ] Sorting by creation date works end-to-end
  - [ ] Sorting by title works end-to-end
  - [ ] Sorting by priority works end-to-end
  - [ ] Sorting works correctly with active filters applied

### Task 6.2: End-to-End Testing
- **Objective**: Test complete user workflows including UI behavior
- **Acceptance Criteria**:
  - Full CRUD operations work end-to-end
  - Advanced features work correctly
  - Error handling works throughout
  - Priority and tags features work end-to-end
  - Search, filter, and sort features work end-to-end
  - Multiple filters can be combined simultaneously
  - Sorting works correctly with active filters applied
  - All UI components function as specified
  - Tasks persist in Neon DB and page refresh does not lose data
- **Tests**:
  - [ ] User can complete full CRUD workflow with priority and tags
  - [ ] User can search tasks by keyword across title and description
  - [ ] User can filter tasks by completion status
  - [ ] User can filter tasks by priority (LOW, MEDIUM, HIGH)
  - [ ] User can filter tasks by tags
  - [ ] User can sort tasks by creation date (ascending/descending)
  - [ ] User can sort tasks by priority (LOW, MEDIUM, HIGH)
  - [ ] User can sort tasks alphabetically by title
  - [ ] User can combine multiple filters simultaneously (completion status, priority, tags)
  - [ ] Sorting functionality works correctly with active filters applied
  - [ ] User can manage task priorities
  - [ ] User can manage task tags
  - [ ] Error states are handled gracefully
  - [ ] All UI components (Task List, Add Task Form, Edit Task Modal, Delete Confirmation, Priority Selector, Tags Input) function correctly
  - [ ] Tasks persist in Neon DB and page refresh does not lose data

## Phase 7: Validation and Deployment Preparation

### Task 7.1: Final Validation
- **Objective**: Ensure all requirements from spec are met
- **Acceptance Criteria**:
  - All functional requirements are satisfied
  - All non-functional requirements are met
  - Architecture follows specified patterns
  - New features (priority, tags) are fully implemented
  - All UI components are implemented and functional
  - UI behavior requirements are met (all actions call backend APIs, UI refreshes automatically, validation handled server-side)
  - Tasks persist in Neon DB and page refresh does not lose data
  - All UI components and behaviors match the specified requirements
- **Tests**:
  - [ ] All FR requirements from spec are implemented
  - [ ] All NFR requirements from spec are met
  - [ ] Architecture follows layered pattern
  - [ ] No business logic in frontend layer
  - [ ] Priority feature is fully implemented
  - [ ] Tags feature is fully implemented
  - [ ] All UI components (Task List, Add Task Form, Edit Task Modal, Delete Confirmation, Priority Selector, Tags Input) are implemented and functional
  - [ ] All actions call backend APIs (no direct database access)
  - [ ] UI refreshes automatically after API operations
  - [ ] Validation handled server-side with appropriate error feedback to user
  - [ ] Page refresh maintains data persistence through Neon DB
  - [ ] Tasks persist in Neon DB and page refresh does not lose data
  - [ ] Task List component displays tasks with completion status, priority, and tags
  - [ ] Add Task Form component includes fields for title, description, priority, and tags with validation
  - [ ] Edit Task Modal component allows editing all task properties with validation
  - [ ] Delete Confirmation component prevents accidental deletions
  - [ ] Priority Selector component allows selection of LOW, MEDIUM, HIGH priority
  - [ ] Tags Input component allows adding and managing tags
  - [ ] All UI components follow behavior requirements (call APIs, refresh automatically, handle validation)

### Task 7.2: Performance Testing
- **Objective**: Validate performance requirements
- **Acceptance Criteria**:
  - API responses are under 500ms
  - UI is responsive during operations
  - No performance bottlenecks exist
  - Filtering by tags and priority is performant
- **Tests**:
  - [ ] API endpoints respond within 500ms
  - [ ] UI remains responsive during operations
  - [ ] Loading states are properly implemented
  - [ ] Filtering by tags performs well with large datasets