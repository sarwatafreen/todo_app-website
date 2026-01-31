"""
MCP (Model Context Protocol) tools for task management operations.
These tools provide the interface between the AI agent and the database.
All operations are stateless and persist changes in the database.
"""
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from datetime import datetime
from .models import Task, TaskCreate, TaskUpdate, TaskStatus


async def add_task(user_id: str, title: str, description: Optional[str] = None, due_date: Optional[datetime] = None) -> dict:
    """
    Add a new task for the specified user.

    Args:
        user_id: The ID of the user creating the task
        title: The task title
        description: Optional task description
        due_date: Optional due date for the task

    Returns:
        Dictionary with the created task information
    """
    from .database import get_async_session

    async with get_async_session() as session:
        # Create task with provided data
        task_data = TaskCreate(
            title=title,
            description=description,
            due_date=due_date
        )

        task = Task(**task_data.model_dump())
        task.owner_id = user_id

        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }


async def list_tasks(user_id: str, status: Optional[str] = None) -> List[dict]:
    """
    List all tasks for the specified user, optionally filtered by status.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        status: Optional status filter (pending, in_progress, completed)

    Returns:
        List of task dictionaries
    """
    from .database import get_async_session

    async with get_async_session() as session:
        # Build query based on status filter
        statement = select(Task).where(Task.owner_id == user_id)

        if status:
            try:
                status_enum = TaskStatus(status)
                statement = statement.where(Task.status == status_enum)
            except ValueError:
                # Invalid status provided, return all tasks
                pass

        result = await session.execute(statement)
        tasks = result.scalars().all()

        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]


async def complete_task(user_id: str, task_id: str) -> dict:
    """
    Mark a task as completed.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to complete

    Returns:
        Dictionary with the updated task information
    """
    from .database import get_async_session

    async with get_async_session() as session:
        # Find the task for this user
        statement = select(Task).where(Task.id == task_id).where(Task.owner_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found for user {user_id}")

        # Update task status to completed
        task.status = TaskStatus.completed
        task.updated_at = datetime.now()

        await session.commit()
        await session.refresh(task)

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }


async def update_task(user_id: str, task_id: str, title: Optional[str] = None,
                     description: Optional[str] = None, status: Optional[str] = None,
                     due_date: Optional[datetime] = None) -> dict:
    """
    Update an existing task for the specified user.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)
        status: New status (optional)
        due_date: New due date (optional)

    Returns:
        Dictionary with the updated task information
    """
    from .database import get_async_session

    async with get_async_session() as session:
        # Find the task for this user
        statement = select(Task).where(Task.id == task_id).where(Task.owner_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found for user {user_id}")

        # Update task fields
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            try:
                task.status = TaskStatus(status)
            except ValueError:
                raise ValueError(f"Invalid status: {status}")
        if due_date is not None:
            task.due_date = due_date

        task.updated_at = datetime.now()

        await session.commit()
        await session.refresh(task)

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }


async def delete_task(user_id: str, task_id: str) -> bool:
    """
    Delete a task for the specified user.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to delete

    Returns:
        True if task was deleted, False if not found
    """
    from .database import get_async_session

    async with get_async_session() as session:
        # Find the task for this user
        statement = select(Task).where(Task.id == task_id).where(Task.owner_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return False

        await session.delete(task)
        await session.commit()

        return True