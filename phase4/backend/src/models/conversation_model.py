from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import DateTime, func
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .message_model import Message


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
    messages: list["Message"] = Relationship(back_populates="conversation")


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