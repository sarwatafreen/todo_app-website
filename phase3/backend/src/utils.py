"""
Utility functions for the Todo AI Chatbot application.
Helper functions for common operations.
"""
import uuid
from datetime import datetime
from typing import Dict, List, Any
from .models import Message, MessageRead


def generate_uuid() -> str:
    """
    Generate a new UUID string.

    Returns:
        str: A new UUID string
    """
    return str(uuid.uuid4())


def format_timestamp(dt: datetime) -> str:
    """
    Format a datetime object as an ISO string.

    Args:
        dt: The datetime object to format

    Returns:
        str: ISO formatted timestamp string
    """
    return dt.isoformat()


def convert_message_to_dict(message: Message) -> Dict[str, Any]:
    """
    Convert a Message object to a dictionary.

    Args:
        message: The Message object to convert

    Returns:
        Dict[str, Any]: Dictionary representation of the message
    """
    return {
        "id": message.id,
        "conversation_id": message.conversation_id,
        "user_id": message.user_id,
        "role": message.role.value,
        "content": message.content,
        "timestamp": message.timestamp.isoformat(),
        "order_index": message.order_index
    }


def convert_message_read_to_dict(message: MessageRead) -> Dict[str, Any]:
    """
    Convert a MessageRead object to a dictionary.

    Args:
        message: The MessageRead object to convert

    Returns:
        Dict[str, Any]: Dictionary representation of the message
    """
    return {
        "id": message.id,
        "conversation_id": message.conversation_id,
        "role": message.role.value,
        "content": message.content,
        "timestamp": message.timestamp.isoformat(),
        "order_index": message.order_index
    }


def sort_messages_by_order_and_time(messages: List[Message]) -> List[Message]:
    """
    Sort messages by order_index and then by timestamp.

    Args:
        messages: List of messages to sort

    Returns:
        List[Message]: Sorted list of messages
    """
    return sorted(messages, key=lambda msg: (msg.order_index, msg.timestamp))


def create_assistant_message(content: str, conversation_id: str, user_id: str, order_index: int) -> Dict[str, Any]:
    """
    Create an assistant message dictionary.

    Args:
        content: The message content
        conversation_id: The conversation ID
        user_id: The user ID
        order_index: The order index for the message

    Returns:
        Dict[str, Any]: Dictionary representing the assistant message
    """
    return {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "role": "assistant",
        "content": content,
        "order_index": order_index,
        "timestamp": datetime.now().isoformat()
    }


def create_user_message(content: str, conversation_id: str, user_id: str, order_index: int) -> Dict[str, Any]:
    """
    Create a user message dictionary.

    Args:
        content: The message content
        conversation_id: The conversation ID
        user_id: The user ID
        order_index: The order index for the message

    Returns:
        Dict[str, Any]: Dictionary representing the user message
    """
    return {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "role": "user",
        "content": content,
        "order_index": order_index,
        "timestamp": datetime.now().isoformat()
    }


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing potentially harmful content.

    Args:
        text: The input text to sanitize

    Returns:
        str: Sanitized input text
    """
    if not text:
        return ""

    # Remove potentially dangerous characters/sequences
    sanitized = text.replace("<script", "&lt;script").replace("javascript:", "javascript_")

    return sanitized.strip()


def validate_conversation_id(conversation_id: str) -> bool:
    """
    Validate a conversation ID format.

    Args:
        conversation_id: The conversation ID to validate

    Returns:
        bool: True if the conversation ID is valid, False otherwise
    """
    try:
        # Try to parse as UUID
        uuid.UUID(conversation_id)
        return True
    except ValueError:
        return False


def prepare_message_history_for_agent(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Prepare message history for the agent by formatting appropriately.

    Args:
        messages: List of message dictionaries

    Returns:
        List[Dict[str, str]]: Formatted message history for the agent
    """
    # Ensure messages are in the correct format for the agent
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", "")
        })

    return formatted_messages