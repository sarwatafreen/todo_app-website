"""
Task Manager service for the Todo Console Application.

This module handles all business logic for task operations including:
- Adding tasks
- Retrieving tasks
- Updating tasks
- Deleting tasks
- Marking tasks as complete/incomplete
"""

from src.models.task import Task


class TaskManager:
    """
    Manages the collection of tasks in memory.
    Handles all data operations for tasks.
    """
    def __init__(self):
        self.tasks = []  # In-memory storage for tasks
        self.next_id = 1  # Sequential ID generator starting from 1

    def add_task(self, description):
        """Add a new task with a unique ID."""
        task = Task(self.next_id, description)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_task_by_id(self, task_id):
        """Find and return a task by its ID, or None if not found."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self):
        """Return all tasks."""
        return self.tasks

    def update_task(self, task_id, new_description):
        """Update the description of a task by its ID."""
        task = self.get_task_by_id(task_id)
        if task:
            task.description = new_description
            return True
        return False

    def delete_task(self, task_id):
        """Delete a task by its ID."""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def mark_task_complete(self, task_id):
        """Mark a task as complete by its ID."""
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = True
            return True
        return False

    def mark_task_incomplete(self, task_id):
        """Mark a task as incomplete by its ID."""
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = False
            return True
        return False

    def get_next_id(self):
        """Get the next available ID for a new task."""
        return self.next_id