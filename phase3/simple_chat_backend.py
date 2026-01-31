import requests
import json
import os

def get_user_input():
    """Get user ID and message from input"""
    print("=== AI Chat Assistant - Connected to Backend ===")
    print("Note: You need a valid User ID from logging into the main application")
    print()

    user_id = input("Enter your User ID: ").strip()
    if not user_id:
        print("User ID is required!")
        return None, None

    print("\nType 'exit' to quit\n")
    message = input("You: ").strip()
    if message.lower() == 'exit':
        return None, None

    return user_id, message

def send_message_to_backend(user_id, message, conversation_id=None):
    """Send message to the backend API"""
    try:
        # Backend API URL (using the WSL IP that we know works)
        api_url = f"http://172.28.224.12:8000/api/{user_id}/chat/"

        # Prepare the request
        headers = {
            'Content-Type': 'application/json',
            # If you have a stored token, you can add it here:
            # 'Authorization': f'Bearer {your_stored_token}',
        }

        payload = {
            "message": message,
            "conversation_id": conversation_id
        }

        # Send the request to the backend
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data.get('response', 'No response received'), data.get('conversation_id')
        else:
            error_detail = response.json().get('detail', 'Unknown error') if response.headers.get('content-type', '').startswith('application/json') else 'Server error'
            return f"Error: {error_detail}", conversation_id

    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to the server. Make sure the backend is running.", conversation_id
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}", conversation_id

def main():
    print("AI Chat Assistant - Connected to Backend API")
    print("=" * 50)
    print("This connects to the backend API we verified is working")
    print("You need a valid User ID from logging into the main application")
    print()

    conversation_id = None

    while True:
        user_id, message = get_user_input()

        if user_id is None or message is None:
            print("Goodbye!")
            break

        if not message:
            print("🤖 AI: Please enter a message")
            continue

        # Send message to backend
        ai_response, conversation_id = send_message_to_backend(user_id, message, conversation_id)

        # Display response
        print(f"🤖 AI: {ai_response}")
        print()

if __name__ == "__main__":
    main()