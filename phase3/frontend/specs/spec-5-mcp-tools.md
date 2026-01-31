# Spec-5: MCP Tools

## Objective

Define and implement **stateless MCP (Model Context Protocol) tools** that provide the interface between the AI agent and the database for all task management operations.

## Scope

This spec covers:

- MCP tool definitions for add_task, list_tasks, complete_task, update_task, delete_task
- Stateless implementation of all tools
- Database persistence for all operations
- User isolation enforcement in all tools

## Out of Scope (Handled in Other Specs)

- AI agent implementation (Spec-6)
- Frontend integration (Spec-4)
- Authentication implementation (Spec-7)

## Functional Requirements

### 1. add_task(user_id, title, description)

- **Purpose**: Add a new task for the specified user
- **Parameters**:
  - user_id (string): ID of the user creating the task
  - title (string): Title of the task
  - description (string, optional): Description of the task
- **Returns**: Dictionary with the created task information
- **Behavior**:
  - Creates a new task record in the database
  - Sets owner_id to the provided user_id
  - Sets status to "pending" by default
  - Returns the created task data

### 2. list_tasks(user_id, status)

- **Purpose**: List all tasks for the specified user
- **Parameters**:
  - user_id (string): ID of the user whose tasks to retrieve
  - status (string, optional): Filter by status (pending, in_progress, completed)
- **Returns**: List of task dictionaries
- **Behavior**:
  - Queries tasks filtered by owner_id to enforce user isolation
  - Optionally filters by status if provided
  - Returns all matching tasks with their details

### 3. complete_task(user_id, task_id)

- **Purpose**: Mark a task as completed
- **Parameters**:
  - user_id (string): ID of the user
  - task_id (string): ID of the task to complete
- **Returns**: Dictionary with the updated task information
- **Behavior**:
  - Verifies that the task belongs to the user
  - Updates the task status to "completed"
  - Returns the updated task data

### 4. update_task(user_id, task_id, title, description, status)

- **Purpose**: Update an existing task
- **Parameters**:
  - user_id (string): ID of the user
  - task_id (string): ID of the task to update
  - title (string, optional): New title for the task
  - description (string, optional): New description for the task
  - status (string, optional): New status for the task
- **Returns**: Dictionary with the updated task information
- **Behavior**:
  - Verifies that the task belongs to the user
  - Updates only the provided fields
  - Returns the updated task data

### 5. delete_task(user_id, task_id)

- **Purpose**: Delete a task
- **Parameters**:
  - user_id (string): ID of the user
  - task_id (string): ID of the task to delete
- **Returns**: Boolean indicating success
- **Behavior**:
  - Verifies that the task belongs to the user
  - Deletes the task from the database
  - Returns True if successful, False if task not found

### 6. Statelessness Requirement

- All MCP tools must be stateless
- No in-memory state or session data allowed
- All operations must persist changes to the database
- Tools must work correctly after server restart

### 7. User Isolation Requirement

- All MCP tools must enforce user isolation
- Each tool must verify that the user owns the resources being accessed
- No cross-user data access allowed

### 8. Error Handling

- MCP tools must handle database errors gracefully
- Return appropriate error messages for invalid inputs
- Maintain transaction integrity for all operations

## Success Criteria

- All MCP tools are implemented and functioning
- Tools are stateless and persist changes to database
- User isolation is enforced in all operations
- Tools return appropriate responses for all scenarios
- Tools integrate properly with the AI agent