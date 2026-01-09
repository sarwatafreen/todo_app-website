# Task API Contract

## Version
- API Version: 1.0
- Last Updated: 2025-01-01

## Base URL
- Development: `http://localhost:8000/api`
- Production: `<production-base-url>/api`

## Common Headers
- `Content-Type: application/json`
- `Accept: application/json`

## Authentication
- No authentication required for Phase II (public API)

## Response Format
All API responses follow this structure:

Success responses:
```json
{
  "data": { ... },
  "message": "Optional message"
}
```

Error responses:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Optional detailed error information"
  }
}
```

## Endpoints

### 1. Get All Tasks
- **Endpoint**: `GET /tasks`
- **Description**: Retrieve all tasks with optional filtering, sorting, and pagination
- **Query Parameters**:
  - `search` (optional): Search term for title/description
  - `completed` (optional): Filter by completion status (`all`, `active`, `completed`) - Default: `all`
  - `priority` (optional): Filter by priority level (`LOW`, `MEDIUM`, `HIGH`)
  - `tag` (optional): Filter by specific tag
  - `sort` (optional): Sort by (`created_at`, `title`, `priority`) - Default: `created_at`
  - `order` (optional): Sort order (`asc`, `desc`) - Default: `desc`
  - `page` (optional): Page number for pagination - Default: 1
  - `limit` (optional): Items per page - Default: 20, Max: 100

- **Response Codes**:
  - `200`: Success
  - `400`: Invalid query parameters
  - `500`: Server error

- **Success Response** (200):
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Sample task",
      "description": "Sample description",
      "completed": false,
      "priority": "HIGH",
      "tags": ["work", "urgent"],
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1,
    "pages": 1
  }
}
```

### 2. Create Task
- **Endpoint**: `POST /tasks`
- **Description**: Create a new task
- **Request Body**:
```json
{
  "title": "Task title (required, max 255 chars)",
  "description": "Task description (optional, max 1000 chars)",
  "priority": "MEDIUM", // Enum: LOW, MEDIUM, HIGH - Default: MEDIUM
  "tags": ["tag1", "tag2"] // Optional array of strings
}
```

- **Response Codes**:
  - `201`: Created successfully
  - `400`: Validation error
  - `500`: Server error

- **Success Response** (201):
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "New task",
    "description": "New description",
    "completed": false,
    "priority": "HIGH",
    "tags": ["work", "urgent"],
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
}
```

### 3. Get Task by ID
- **Endpoint**: `GET /tasks/{id}`
- **Description**: Retrieve a specific task by its ID
- **Path Parameters**:
  - `id`: UUID of the task (required)

- **Response Codes**:
  - `200`: Success
  - `404`: Task not found
  - `400`: Invalid ID format
  - `500`: Server error

- **Success Response** (200):
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Sample task",
    "description": "Sample description",
    "completed": false,
    "priority": "HIGH",
    "tags": ["work", "urgent"],
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
}
```

### 4. Update Task
- **Endpoint**: `PUT /tasks/{id}`
- **Description**: Update a specific task completely
- **Path Parameters**:
  - `id`: UUID of the task (required)

- **Request Body**:
```json
{
  "title": "Updated title (required, max 255 chars)",
  "description": "Updated description (optional, max 1000 chars)",
  "completed": true,
  "priority": "HIGH", // Enum: LOW, MEDIUM, HIGH
  "tags": ["updated", "tags"] // Optional array of strings
}
```

- **Response Codes**:
  - `200`: Updated successfully
  - `400`: Validation error or invalid ID format
  - `404`: Task not found
  - `500`: Server error

- **Success Response** (200):
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Updated task",
    "description": "Updated description",
    "completed": true,
    "priority": "HIGH",
    "tags": ["updated", "tags"],
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
}
```

### 5. Delete Task
- **Endpoint**: `DELETE /tasks/{id}`
- **Description**: Delete a specific task by its ID
- **Path Parameters**:
  - `id`: UUID of the task (required)

- **Response Codes**:
  - `204`: Deleted successfully (no content)
  - `404`: Task not found
  - `400`: Invalid ID format
  - `500`: Server error

### 6. Toggle Task Completion Status
- **Endpoint**: `PATCH /tasks/{id}/toggle`
- **Description**: Toggle the completion status of a specific task
- **Path Parameters**:
  - `id`: UUID of the task (required)

- **Response Codes**:
  - `200`: Toggled successfully
  - `404`: Task not found
  - `400`: Invalid ID format
  - `500`: Server error

- **Success Response** (200):
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Sample task",
    "description": "Sample description",
    "completed": true,
    "priority": "HIGH",
    "tags": ["work", "urgent"],
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request data validation failed |
| `RESOURCE_NOT_FOUND` | 404 | Requested resource does not exist |
| `INVALID_ID_FORMAT` | 400 | ID parameter is not a valid UUID |
| `INTERNAL_ERROR` | 500 | Internal server error occurred |

## Rate Limiting
- Default rate limit: 100 requests per minute per IP
- Exceeded rate limit returns HTTP 429

## Data Validation Rules
- Title: Required, 1-255 characters
- Description: Optional, 0-1000 characters
- Priority: Required, must be one of "LOW", "MEDIUM", "HIGH"
- Tags: Optional, must be an array of strings
- ID: Must be valid UUID format
- Boolean fields: Must be true or false