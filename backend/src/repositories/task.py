from sqlmodel import SQLModel, Session, select, Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from ..models.task import Task, TaskBase


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task: TaskBase) -> Task:
        """Create a new task"""
        db_task = Task.model_validate(task)
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task

    def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        """Get a task by its ID"""
        return self.session.get(Task, task_id)

    def get_all_tasks(
        self,
        search: Optional[str] = None,
        completed: Optional[str] = None,
        priority: Optional[str] = None,
        tag: Optional[str] = None,
        sort: Optional[str] = "created_at",
        order: Optional[str] = "desc"
    ) -> List[Task]:
        """Get all tasks with optional filtering, sorting, and search"""
        statement = select(Task)

        # Apply filters
        if search:
            statement = statement.where(
                Task.title.contains(search) | Task.description.contains(search)
            )
        if completed:
            if completed.lower() == "active":
                statement = statement.where(Task.completed == False)
            elif completed.lower() == "completed":
                statement = statement.where(Task.completed == True)
        if priority:
            statement = statement.where(Task.priority == priority.upper())
        if tag:
            # For JSONB tags column, we'd use JSON operators in a real implementation
            # For this prototype, we'll do a simple contains check
            statement = statement.where(Task.tags.contains([tag]))

        # Apply sorting
        if sort == "title":
            if order == "asc":
                statement = statement.order_by(Task.title.asc())
            else:
                statement = statement.order_by(Task.title.desc())
        elif sort == "priority":
            if order == "asc":
                statement = statement.order_by(Task.priority.asc())
            else:
                statement = statement.order_by(Task.priority.desc())
        else:  # Default to created_at
            if order == "asc":
                statement = statement.order_by(Task.created_at.asc())
            else:
                statement = statement.order_by(Task.created_at.desc())

        return self.session.exec(statement).all()

    def update_task(self, task_id: UUID, task_update: dict) -> Optional[Task]:
        """Update a task by ID"""
        task = self.session.get(Task, task_id)
        if not task:
            return None

        for field, value in task_update.items():
            if hasattr(task, field):
                setattr(task, field, value)

        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: UUID) -> bool:
        """Delete a task by ID"""
        task = self.session.get(Task, task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    def toggle_task_completion(self, task_id: UUID) -> Optional[Task]:
        """Toggle completion status of a task"""
        task = self.session.get(Task, task_id)
        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task