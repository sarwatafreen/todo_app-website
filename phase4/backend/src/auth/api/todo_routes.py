from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..database.database import get_session
from ..middleware.auth import get_current_user
from ..middleware.user_validation import validate_user_id_match
from ..models.todo import TodoCreate, TodoRead, TodoUpdate
from ..services.todo_service import TodoService

router = APIRouter(prefix="/users/{user_id}", tags=["Todos"])

@router.get("/todos", response_model=List[TodoRead])
def get_user_todos(
    user_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all todos for the specified user."""
    # Validate that the requested user matches the authenticated user
    validate_user_id_match(str(user_id), current_user)

    todo_service = TodoService(session)
    return todo_service.get_todos_by_user(user_id)


@router.post("/todos", response_model=TodoRead)
def create_todo(
    user_id: UUID,
    todo_create: TodoCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new todo for the specified user."""
    # Validate that the requested user matches the authenticated user
    validate_user_id_match(str(user_id), current_user)

    todo_service = TodoService(session)
    return todo_service.create_todo(todo_create, user_id)


@router.get("/todos/{todo_id}", response_model=TodoRead)
def get_todo(
    user_id: UUID,
    todo_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific todo for the specified user."""
    # Validate that the requested user matches the authenticated user
    validate_user_id_match(str(user_id), current_user)

    todo_service = TodoService(session)
    todo = todo_service.get_todo_by_id(todo_id, user_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo


@router.put("/todos/{todo_id}", response_model=TodoRead)
def update_todo(
    user_id: UUID,
    todo_id: UUID,
    todo_update: TodoUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific todo for the specified user."""
    # Validate that the requested user matches the authenticated user
    validate_user_id_match(str(user_id), current_user)

    todo_service = TodoService(session)
    todo = todo_service.update_todo(todo_id, todo_update, user_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo


@router.delete("/todos/{todo_id}")
def delete_todo(
    user_id: UUID,
    todo_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific todo for the specified user."""
    # Validate that the requested user matches the authenticated user
    validate_user_id_match(str(user_id), current_user)

    todo_service = TodoService(session)
    success = todo_service.delete_todo(todo_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return {"message": "Todo deleted successfully"}


@router.patch("/todos/{todo_id}/complete", response_model=TodoRead)
def toggle_todo_completion(
    user_id: UUID,
    todo_id: UUID,
    is_completed: bool,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a specific todo for the specified user."""
    # Validate that the requested user matches the authenticated user
    validate_user_id_match(str(user_id), current_user)

    todo_service = TodoService(session)
    todo = todo_service.toggle_todo_completion(todo_id, user_id, is_completed)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo