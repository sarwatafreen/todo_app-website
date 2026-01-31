from typing import List, Dict, Any
import random
import time
from src.models.message_model import MessageRead
from src.settings import settings


async def process_chat_message(messages: List[Dict[str, str]], user_id: str) -> str:
    """
    Process a chat message through a mock AI agent (to avoid OpenAI API dependency).

    Args:
        messages: List of message dictionaries with role and content
        user_id: The ID of the user sending the message

    Returns:
        The AI-generated response text
    """
    try:
        # Get the last user message to generate a relevant response
        last_user_message = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break

        # Generate a contextual response based on the user's message
        if "hello" in last_user_message.lower() or "hi" in last_user_message.lower():
            responses = [
                "Hello there! How can I assist you with your tasks today?",
                "Hi! I'm your AI assistant. What would you like to do?",
                "Greetings! How can I help you manage your tasks?"
            ]
        elif "task" in last_user_message.lower() or "todo" in last_user_message.lower():
            responses = [
                "I can help you manage your tasks. You can ask me to add, update, or list your tasks.",
                "Sure! I can help with your task management. What would you like to do with your tasks?",
                "For task management, you can ask me to create, update, or check your tasks."
            ]
        elif "add" in last_user_message.lower() or "create" in last_user_message.lower():
            responses = [
                "I can help you add tasks. Just tell me what task you'd like to add!",
                "Got it! Tell me the details of the task you want to create.",
                "Okay, what task would you like to add to your list?"
            ]
        else:
            responses = [
                "I understand. How else can I assist you?",
                "That sounds interesting. What would you like to do next?",
                "Thanks for sharing. Is there anything specific you'd like help with?",
                "I'm here to help with your tasks. What else would you like to do?",
                "Understood. Feel free to ask me to manage your tasks!"
            ]

        # Select a random response from the appropriate category
        response_text = random.choice(responses)

        return response_text

    except Exception as e:
        # Log the error
        print(f"Error processing chat message: {str(e)}")
        # Return a generic response in case of error
        return "I'm having trouble processing your request right now. Could you try rephrasing?"