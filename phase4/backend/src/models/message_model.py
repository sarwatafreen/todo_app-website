from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import DateTime, func
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Enum as SQLEnum

if TYPE_CHECKING:
    from .conversation_model import Conversation


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


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