from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    """
    Base class for Task model containing common fields.
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)
    owner_id: str = Field(max_length=255)  # User ID from JWT
    due_date: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    """
    Task model representing a user's personal task data.
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()))


class TaskRead(TaskBase):
    """
    Schema for reading task data, excludes sensitive fields.
    """
    id: str
    created_at: datetime
    updated_at: datetime
    # Note: owner_id is intentionally excluded from responses


class TaskCreate(SQLModel):
    """
    Schema for creating a new task.
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)


class TaskUpdate(SQLModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: Optional[bool] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)