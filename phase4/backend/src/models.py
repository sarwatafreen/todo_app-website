"""
SQLModel database models for the Todo AI Chatbot application.
Contains Task, Conversation, and Message models with proper relationships.
"""
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import DateTime, func
from typing import Optional, List
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Enum as SQLEnum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskBase(SQLModel):
    """
    Base class for Task model containing common fields.
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.pending)
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
    status: Optional[TaskStatus] = Field(default=TaskStatus.pending)
    due_date: Optional[datetime] = Field(default=None)


class TaskUpdate(SQLModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[TaskStatus] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class ConversationBase(SQLModel):
    """
    Base class for Conversation model containing common fields.
    """
    title: Optional[str] = Field(default=None, max_length=255)
    user_id: str = Field(max_length=255)  # User ID from JWT


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a user's chat conversation.
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()))

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationRead(ConversationBase):
    """
    Schema for reading conversation data.
    """
    id: str
    created_at: datetime
    updated_at: datetime
    # Note: user_id is intentionally excluded from responses


class ConversationCreate(SQLModel):
    """
    Schema for creating a new conversation.
    """
    title: Optional[str] = Field(default=None, max_length=255)


class ConversationUpdate(SQLModel):
    """
    Schema for updating an existing conversation.
    """
    title: Optional[str] = Field(default=None, max_length=255)


class MessageBase(SQLModel):
    """
    Base class for Message model containing common fields.
    """
    conversation_id: str = Field(foreign_key="conversation.id", max_length=255)
    user_id: str = Field(max_length=255)  # User ID from JWT
    role: MessageRole = Field(sa_column=Column(SQLEnum(MessageRole), nullable=False))
    content: str = Field(min_length=1, max_length=10000)
    order_index: int = Field(default=0)


class Message(MessageBase, table=True):
    """
    Message model representing a message in a conversation.
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()))

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageRead(MessageBase):
    """
    Schema for reading message data.
    """
    id: str
    timestamp: datetime
    # Note: user_id is intentionally excluded from responses


class MessageCreate(SQLModel):
    """
    Schema for creating a new message.
    """
    conversation_id: str
    role: MessageRole
    content: str
    order_index: Optional[int] = 0


class MessageUpdate(SQLModel):
    """
    Schema for updating an existing message.
    """
    content: Optional[str] = Field(default=None, min_length=1, max_length=10000)
    order_index: Optional[int] = None