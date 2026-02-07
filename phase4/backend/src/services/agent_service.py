from typing import List, Dict, Any
import random


def process_chat_message(messages: List[Dict[str, str]], user_id: str) -> str:
    """
    Process a chat message through a mock AI agent (to avoid OpenAI API dependency).

    Args:
        messages: List of message dictionaries with role and content
        user_id: The ID of the user sending the message

    Returns:
        The AI-generated response text
    """
    # Simple hardcoded response to bypass any potential issues
    responses = [
        "Hello! I'm your AI assistant. How can I help you today?",
        "Hi there! I'm ready to help you with your tasks.",
        "Greetings! What would you like to do today?",
        "I'm your AI assistant. How can I assist you?",
        "Nice to meet you! How can I help?",
        "Hello! What can I do for you today?"
    ]

    print(f"DEBUG: Agent service called with {len(messages)} messages for user {user_id}")
    print(f"DEBUG: Messages: {messages}")

    response = random.choice(responses)
    print(f"DEBUG: Returning response: {response}")

    return response