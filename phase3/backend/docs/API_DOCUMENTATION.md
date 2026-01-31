# Todo API Documentation

## Authentication

All endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer {jwt_token}
```

## Endpoints

### Authentication

#### Register User
- **POST** `/api/auth/register`
- Request Body:
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password"
  }
  ```
- Response: User object with ID, email, and timestamps

#### Login User
- **POST** `/api/auth/login`
- Form Data:
  - `email`: user@example.com
  - `password`: secure_password
- Response:
  ```json
  {
    "access_token": "jwt_token",
    "token_type": "bearer"
  }
  ```

#### Logout User
- **POST** `/api/auth/logout`
- Response: Success message

### Todo Management

#### Get User Todos
- **GET** `/api/users/{user_id}/todos`
- Headers: Authorization Bearer token
- Response: Array of Todo objects

#### Create Todo
- **POST** `/api/users/{user_id}/todos`
- Headers: Authorization Bearer token
- Request Body:
  ```json
  {
    "title": "Todo title",
    "description": "Optional description",
    "due_date": "2023-12-31T23:59:59Z"
  }
  ```
- Response: Created Todo object

#### Get Specific Todo
- **GET** `/api/users/{user_id}/todos/{todo_id}`
- Headers: Authorization Bearer token
- Response: Todo object

#### Update Todo
- **PUT** `/api/users/{user_id}/todos/{todo_id}`
- Headers: Authorization Bearer token
- Request Body: Any of the todo fields to update
- Response: Updated Todo object

#### Delete Todo
- **DELETE** `/api/users/{user_id}/todos/{todo_id}`
- Headers: Authorization Bearer token
- Response: Success message

#### Toggle Todo Completion
- **PATCH** `/api/users/{user_id}/todos/{todo_id}/complete`
- Headers: Authorization Bearer token
- Request Body:
  ```json
  {
    "is_completed": true
  }
  ```
- Response: Updated Todo object

## Error Responses

- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User attempting to access another user's data
- `404 Not Found`: Resource does not exist
- `422 Unprocessable Entity`: Invalid request data

## Security

- User ID validation on all requests to prevent cross-user data access
- JWT token validation on all protected endpoints
- Passwords are hashed using bcrypt
- All user data is isolated by user ID