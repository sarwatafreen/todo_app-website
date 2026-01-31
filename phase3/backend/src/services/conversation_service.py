from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from datetime import datetime
import uuid

from src.models.conversation_model import Conversation, ConversationCreate
from src.models.message_model import Message, MessageCreate, MessageRole
from src.database import get_async_session


async def get_conversation_by_id(conversation_id: str, user_id: str, session: AsyncSession) -> Optional[Conversation]:
    """
    Retrieve a conversation by its ID for a specific user.

    Args:
        conversation_id: The ID of the conversation to retrieve
        user_id: The ID of the user requesting the conversation
        session: Database session

    Returns:
        The conversation if found and owned by the user, None otherwise
    """
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def create_new_conversation(user_id: str, title: Optional[str], session: AsyncSession) -> Conversation:
    """
    Create a new conversation for a user.

    Args:
        user_id: The ID of the user creating the conversation
        title: Optional title for the conversation
        session: Database session

    Returns:
        The newly created conversation
    """
    conversation_data = ConversationCreate(title=title)
    conversation = Conversation(**conversation_data.model_dump())
    conversation.user_id = user_id

    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)

    return conversation


async def get_messages_for_conversation(conversation_id: str, user_id: str, session: AsyncSession) -> List[Message]:
    """
    Retrieve all messages for a specific conversation belonging to a user.

    Args:
        conversation_id: The ID of the conversation
        user_id: The ID of the user requesting messages
        session: Database session

    Returns:
        List of messages in chronological order
    """
    statement = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.user_id == user_id
    ).order_by(Message.order_index, Message.timestamp)

    result = await session.execute(statement)
    return result.scalars().all()


async def save_message_to_conversation(
    conversation_id: str,
    user_id: str,
    role: MessageRole,
    content: str,
    order_index: int,
    session: AsyncSession
) -> Message:
    """
    Save a message to a conversation.

    Args:
        conversation_id: The ID of the conversation
        user_id: The ID of the user sending the message
        role: The role of the message sender (user/assistant)
        content: The message content
        order_index: The position of the message in the conversation
        session: Database session

    Returns:
        The saved message
    """
    message_data = MessageCreate(
        conversation_id=conversation_id,
        role=role,
        content=content,
        order_index=order_index
    )

    message = Message(**message_data.model_dump())
    message.user_id = user_id

    session.add(message)
    await session.commit()
    await session.refresh(message)

    return message