from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List
from src.models.task_model import Task, TaskRead, TaskCreate, TaskUpdate
from src.auth.dependencies import get_current_user
from src.database import get_session
from datetime import datetime


router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskRead])
def get_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the specified user.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        current_user: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        List of tasks owned by the user

    Raises:
        HTTPException: 403 if user_id doesn't match current_user
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Query tasks filtered by owner_id to enforce ownership
    statement = select(Task).where(Task.owner_id == user_id)
    result = session.execute(statement)
    tasks = result.scalars().all()

    return tasks


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user.

    Args:
        user_id: The ID of the user creating the task
        task_data: Task creation data
        current_user: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        Created task

    Raises:
        HTTPException: 403 if user_id doesn't match current_user
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Create task with owner_id set to the authenticated user
    task = Task(**task_data.model_dump())
    task.owner_id = user_id

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    user_id: str,
    task_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the specified user.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to retrieve
        current_user: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        The requested task

    Raises:
        HTTPException: 403 if user_id doesn't match current_user or task not owned by user
        HTTPException: 404 if task not found for this user
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Query task by ID and owner_id to enforce ownership
    statement = select(Task).where(Task.id == task_id).where(Task.owner_id == user_id)
    result = session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    user_id: str,
    task_id: str,
    task_data: TaskUpdate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the specified user.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        task_data: Task update data
        current_user: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        Updated task

    Raises:
        HTTPException: 403 if user_id doesn't match current_user or task not owned by user
        HTTPException: 404 if task not found for this user
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Query task by ID and owner_id to enforce ownership
    statement = select(Task).where(Task.id == task_id).where(Task.owner_id == user_id)
    result = session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields
    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    task.updated_at = datetime.now()

    session.commit()
    session.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the specified user.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to delete
        current_user: The ID of the currently authenticated user (from JWT)
        session: Database session

    Raises:
        HTTPException: 403 if user_id doesn't match current_user or task not owned by user
        HTTPException: 404 if task not found for this user
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Query task by ID and owner_id to enforce ownership
    statement = select(Task).where(Task.id == task_id).where(Task.owner_id == user_id)
    result = session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()


from pydantic import BaseModel

class TaskCompletionUpdate(BaseModel):
    is_completed: bool

@router.patch("/{task_id}/complete", response_model=TaskRead)
def update_task_completion(
    user_id: str,
    task_id: str,
    completion_update: TaskCompletionUpdate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the specified user.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        completion_update: Object containing the new completion status
        current_user: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        Updated task

    Raises:
        HTTPException: 403 if user_id doesn't match current_user or task not owned by user
        HTTPException: 404 if task not found for this user
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Query task by ID and owner_id to enforce ownership
    statement = select(Task).where(Task.id == task_id).where(Task.owner_id == user_id)
    result = session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update completion status
    task.is_completed = completion_update.is_completed
    task.updated_at = datetime.now()

    session.commit()
    session.refresh(task)

    return task