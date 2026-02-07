from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session
from typing import List, Dict, Any
from datetime import datetime
import uuid

from src.models.conversation_model import Conversation
from src.models.message_model import Message, MessageRead, MessageRole
from src.services.agent_service import process_chat_message
from src.services.conversation_service import (
    get_conversation_by_id,
    create_new_conversation,
    get_messages_for_conversation,
    save_message_to_conversation
)
from src.auth.dependencies import get_current_user
from src.database import get_session
from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: str


router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
def chat(
    user_id: str,
    chat_request: ChatRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Process a chat message and return AI-generated response.

    Args:
        user_id: The ID of the user (from path)
        chat_request: The chat request containing message and optional conversation_id
        current_user: The authenticated user (from JWT)
        session: Database session

    Returns:
        ChatResponse containing AI response, conversation_id, and timestamp
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Validate input
    if not chat_request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    # Get or create conversation
    conversation: Conversation
    if chat_request.conversation_id:
        # Load existing conversation
        conversation = get_conversation_by_id(chat_request.conversation_id, user_id, session)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation = create_new_conversation(user_id, None, session)

    # Save user message to database
    messages = get_messages_for_conversation(conversation.id, user_id, session)
    next_order_index = len(messages)

    user_message = save_message_to_conversation(
        conversation_id=conversation.id,
        user_id=user_id,
        role=MessageRole.user,
        content=chat_request.message,
        order_index=next_order_index,
        session=session
    )

    # Prepare messages for agent (including history)
    message_history = []
    for msg in messages:
        message_history.append({
            "role": msg.role.value,
            "content": msg.content
        })

    # Add the new user message
    message_history.append({
        "role": "user",
        "content": chat_request.message
    })

    try:
        # Process message with AI agent
        print(f"DEBUG: Calling agent service with {len(message_history)} messages")
        ai_response = process_chat_message(message_history, user_id)
        print(f"DEBUG: Agent service returned: {ai_response}")

        # Save AI response to database
        print(f"DEBUG: Attempting to save AI response to DB")
        ai_message = save_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role=MessageRole.assistant,
            content=ai_response,
            order_index=len(message_history),
            session=session
        )
        print(f"DEBUG: AI response saved successfully")

        return ChatResponse(
            response=ai_response,
            conversation_id=conversation.id,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        # Log the specific error for debugging
        import traceback
        print(f"DEBUG: Chat endpoint error: {str(e)}")
        print(f"DEBUG: Error type: {type(e).__name__}")
        print(f"DEBUG: Traceback: {traceback.format_exc()}")

        # If agent processing fails, return a friendly error message
        error_response = "I'm sorry, I encountered an issue processing your request. Please try again."

        # Save error response to database
        print(f"DEBUG: Saving error response to DB")
        error_message = save_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role=MessageRole.assistant,
            content=error_response,
            order_index=len(message_history),
            session=session
        )
        print(f"DEBUG: Error response saved")

        return ChatResponse(
            response=error_response,
            conversation_id=conversation.id,
            timestamp=datetime.now().isoformat()
        )