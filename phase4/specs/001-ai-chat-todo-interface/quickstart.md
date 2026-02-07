# Quickstart Guide: AI-Powered Chat Interface for Todo Management

## Prerequisites

- Python 3.11+
- Node.js 18+
- Neon PostgreSQL account and database
- OpenAI API key
- Git

## Environment Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd phase3
```

2. Set up environment variables in `.env` file:
```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
JWT_SECRET=your-super-secret-jwt-key-here
OPENAI_API_KEY=your-openai-api-key
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlmodel openai python-jose[cryptography] passlib[bcrypt] psycopg2-binary python-multipart python-dotenv
```

3. Create the new models:
```bash
# Create models directory if it doesn't exist
mkdir -p src/models
```

Create `src/models/conversation_model.py`:
```python
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime, func
from typing import Optional, List
from datetime import datetime
import uuid

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
```

Create `src/models/message_model.py`:
```python
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime, func
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum

class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class MessageBase(SQLModel):
    """
    Base class for Message model containing common fields.
    """
    conversation_id: str = Field(foreign_key="conversation.id", max_length=255)
    user_id: str = Field(max_length=255)  # User ID from JWT
    role: MessageRole = Field(sa_column=Column(Enum(MessageRole), nullable=False))
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
```

4. Create the agent service:
```bash
mkdir -p src/services
```

Create `src/services/agent_service.py`:
```python
from typing import List, Dict, Any
import openai
from src.models.message_model import MessageRead
from src.settings import settings

# Initialize OpenAI client
client = openai.OpenAI(api_key=settings.openai_api_key)

async def process_chat_message(messages: List[Dict[str, str]], user_id: str) -> str:
    """
    Process a chat message through the OpenAI agent.

    Args:
        messages: List of message dictionaries with role and content
        user_id: The ID of the user sending the message

    Returns:
        The AI-generated response text
    """
    try:
        # Format messages for OpenAI API
        openai_messages = []
        for msg in messages:
            openai_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # or another appropriate model
            messages=openai_messages,
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        # Log the error
        print(f"Error processing chat message: {str(e)}")
        raise e
```

5. Create the conversation service:
Create `src/services/conversation_service.py`:
```python
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from datetime import datetime
from uuid import UUID
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
```

6. Create the chat endpoints:
Create `src/api/chat_endpoints.py`:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Dict, Any
from datetime import datetime

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
from src.database import get_async_session
from pydantic import BaseModel

router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: str


@router.post("/", response_model=ChatResponse)
async def chat(
    user_id: str,
    chat_request: ChatRequest,
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
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
        conversation = await get_conversation_by_id(chat_request.conversation_id, user_id, session)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation = await create_new_conversation(user_id, None, session)

    # Save user message to database
    messages = await get_messages_for_conversation(conversation.id, user_id, session)
    next_order_index = len(messages)

    user_message = await save_message_to_conversation(
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
        ai_response = await process_chat_message(message_history, user_id)

        # Save AI response to database
        ai_message = await save_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role=MessageRole.assistant,
            content=ai_response,
            order_index=len(message_history),
            session=session
        )

        return ChatResponse(
            response=ai_response,
            conversation_id=conversation.id,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        # If agent processing fails, return a friendly error message
        error_response = "I'm sorry, I encountered an issue processing your request. Please try again."

        # Save error response to database
        error_message = await save_message_to_conversation(
            conversation_id=conversation.id,
            user_id=user_id,
            role=MessageRole.assistant,
            content=error_response,
            order_index=len(message_history),
            session=session
        )

        return ChatResponse(
            response=error_response,
            conversation_id=conversation.id,
            timestamp=datetime.now().isoformat()
        )
```

7. Update main.py to include the chat router:
```python
# Add this import near the top with other imports
from src.api.chat_endpoints import router as chat_router

# Add this line with the other router includes
app.include_router(chat_router)
```

## Frontend Setup

1. Navigate to frontend directory:
```bash
cd ../frontend
```

2. Install dependencies:
```bash
npm install @openai/chat-components react-markdown
```

3. Create the chat service:
```bash
mkdir -p src/services
```

Create `src/services/chat.ts`:
```typescript
import axios, { AxiosResponse } from 'axios';
import { authService } from './auth';

interface ChatRequest {
  message: string;
  conversation_id?: string;
}

interface ChatResponse {
  response: string;
  conversation_id: string;
  timestamp: string;
}

class ChatService {
  private API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  async sendMessage(userId: string, message: string, conversationId?: string): Promise<ChatResponse> {
    try {
      const requestData: ChatRequest = {
        message: message,
        conversation_id: conversationId
      };

      const response: AxiosResponse<ChatResponse> = await axios.post(
        `${this.API_BASE_URL}/api/${userId}/chat`,
        requestData,
        { headers: authService.getAuthHeaders() }
      );

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response) {
          // Server responded with error status
          const message = error.response.data?.detail || error.response.data?.message || 'An error occurred';
          throw new Error(message);
        } else if (error.request) {
          // Request was made but no response received
          throw new Error('Network error - could not reach server');
        } else {
          // Something else happened while setting up the request
          throw new Error(error.message || 'An unexpected error occurred');
        }
      } else {
        // Non-Axios error
        throw new Error(error instanceof Error ? error.message : 'An unexpected error occurred');
      }
    }
  }
}

export const chatService = new ChatService();
```

4. Create the chat component:
```bash
mkdir -p src/components/Chat
```

Create `src/components/Chat/ChatInterface.tsx`:
```tsx
'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../../context/auth-context';
import { chatService } from '../../services/chat';
import { Todo } from '../Todo/TodoList';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

const ChatInterface: React.FC = () => {
  const { user } = useAuth();
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages when they update
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !user || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    // Add user message to UI immediately
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await chatService.sendMessage(
        user.id,
        inputMessage,
        conversationId
      );

      // Update conversation ID if it changed
      if (response.conversation_id !== conversationId) {
        setConversationId(response.conversation_id);
      }

      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: `Error: ${(error as Error).message || 'Failed to send message'}`,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!user) {
    return <div>Please log in to use the chat interface.</div>;
  }

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      <div className="bg-white shadow rounded-lg mb-4">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-800">AI Todo Assistant</h2>
          <p className="text-sm text-gray-600 mt-1">
            Chat naturally to manage your tasks. Try "Add a task to buy groceries" or "Show my tasks".
          </p>
        </div>

        <div className="p-4 h-96 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full text-gray-500">
              <p>Start a conversation with the AI assistant...</p>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200 text-gray-800'
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{message.content}</div>
                    <div className={`text-xs mt-1 ${message.role === 'user' ? 'text-blue-100' : 'text-gray-500'}`}>
                      {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-200 text-gray-800">
                    <div>Thinking...</div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        <div className="p-4 border-t border-gray-200">
          <div className="flex space-x-2">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type your message here..."
              className="flex-1 border border-gray-300 rounded-lg p-2 resize-none h-16 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
```

5. Create the chat page:
```bash
mkdir -p src/app/chat
```

Create `src/app/chat/page.tsx`:
```tsx
'use client';

import React from 'react';
import ProtectedRoute from '../../components/ProtectedRoute';
import ChatInterface from '../../components/Chat/ChatInterface';
import Head from 'next/head';

const ChatPage: React.FC = () => {
  return (
    <ProtectedRoute>
      <Head>
        <title>AI Todo Chat | Todo App</title>
      </Head>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">AI Todo Assistant</h1>
        <ChatInterface />
      </div>
    </ProtectedRoute>
  );
};

export default ChatPage;
```

## Running the Application

1. Start the backend:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn src.main:app --reload --port 8000
```

2. In a new terminal, start the frontend:
```bash
cd frontend
npm run dev
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs
   - Chat page: http://localhost:3000/chat

## Testing the Chat Interface

1. Register and log in to the application
2. Navigate to the /chat page
3. Try natural language commands like:
   - "Add a task to buy milk"
   - "Show me my tasks"
   - "Mark my meeting task as complete"
   - "What did I ask you earlier?"

The AI assistant should process these commands and interact with your todo list appropriately.