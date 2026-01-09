from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ..models.task import Task, TaskBase
from ..repositories.task import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create_task(self, task_data: TaskBase) -> dict:
        """Create a new task with validation and return as dict for API"""
        # Validate priority
        if task_data.priority not in ["LOW", "MEDIUM", "HIGH"]:
            raise ValueError(f"Invalid priority: {task_data.priority}. Must be LOW, MEDIUM, or HIGH")

        # Validate tags if provided
        if task_data.tags is not None:
            if not isinstance(task_data.tags, list):
                raise ValueError("Tags must be a list of strings")
            for tag in task_data.tags:
                if not isinstance(tag, str):
                    raise ValueError(f"All tags must be strings, got: {type(tag)}")

        db_task = self.task_repository.create_task(task_data)
        return self._convert_task_to_dict(db_task)

    def get_task_by_id(self, task_id: UUID) -> Optional[dict]:
        """Get a task by its ID and return as dict for API"""
        db_task = self.task_repository.get_task_by_id(task_id)
        if db_task:
            return self._convert_task_to_dict(db_task)
        return None

    def get_all_tasks(
        self,
        search: Optional[str] = None,
        completed: Optional[str] = None,
        priority: Optional[str] = None,
        tag: Optional[str] = None,
        sort: Optional[str] = "created_at",
        order: Optional[str] = "desc"
    ) -> List[dict]:
        """Get all tasks with optional filtering, sorting, and search and return as dict for API"""
        db_tasks = self.task_repository.get_all_tasks(
            search=search,
            completed=completed,
            priority=priority,
            tag=tag,
            sort=sort,
            order=order
        )
        return [self._convert_task_to_dict(task) for task in db_tasks]

    def update_task(self, task_id: UUID, task_update: dict) -> Optional[dict]:
        """Update a task with validation and return as dict for API"""
        # Validate priority if provided
        if "priority" in task_update:
            if task_update["priority"] not in ["LOW", "MEDIUM", "HIGH"]:
                raise ValueError(f"Invalid priority: {task_update['priority']}. Must be LOW, MEDIUM, or HIGH")

        # Validate tags if provided
        if "tags" in task_update:
            if task_update["tags"] is not None:
                if not isinstance(task_update["tags"], list):
                    raise ValueError("Tags must be a list of strings")
                for tag in task_update["tags"]:
                    if not isinstance(tag, str):
                        raise ValueError(f"All tags must be strings, got: {type(tag)}")

        db_task = self.task_repository.update_task(task_id, task_update)
        if db_task:
            return self._convert_task_to_dict(db_task)
        return None

    def delete_task(self, task_id: UUID) -> bool:
        """Delete a task"""
        return self.task_repository.delete_task(task_id)

    def toggle_task_completion(self, task_id: UUID) -> Optional[dict]:
        """Toggle completion status of a task and return as dict for API"""
        db_task = self.task_repository.toggle_task_completion(task_id)
        if db_task:
            return self._convert_task_to_dict(db_task)
        return None

    def _convert_task_to_dict(self, task) -> dict:
        """Convert a Task model to a dictionary with string dates"""
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "tags": task.tags,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }