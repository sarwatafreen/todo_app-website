"""
Task model for the Todo Console Application.

This module defines the Task data model with properties and string representation.
"""

class Task:
    """
    Represents a single todo task with ID, description, and completion status.
    """
    def __init__(self, task_id, description):
        self.id = task_id
        self.description = description
        self.completed = False  # Default to incomplete

    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{self.id}. [{status}] {self.description}"

    def to_dict(self):
        """Convert task to dictionary representation."""
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from a dictionary."""
        task = cls(data['id'], data['description'])
        task.completed = data.get('completed', False)
        return task