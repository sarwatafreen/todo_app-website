"""
OpenAI Agents SDK setup and runner for the Todo AI Chatbot.
Handles stateless context reconstruction and agent-tool interaction.
"""
from typing import List, Dict, Any, Optional
import openai
from .mcp_tools import add_task, list_tasks, complete_task, update_task, delete_task
from .models import MessageRole
from .settings import settings


class TodoAgent:
    """
    Todo Agent class that manages interactions with the OpenAI Agents API.
    Handles stateless context reconstruction and tool selection.
    """

    def __init__(self):
        """
        Initialize the Todo Agent with OpenAI client.
        """
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.tools = self._define_tools()

    def _define_tools(self) -> List[Dict[str, Any]]:
        """
        Define the tools available to the agent.

        Returns:
            List of tool definitions in OpenAI format
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The ID of the user"
                            },
                            "title": {
                                "type": "string",
                                "description": "The title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional description of the task"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "Optional due date in ISO format (YYYY-MM-DDTHH:MM:SS.ssssss)"
                            }
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for the user, optionally filtered by status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The ID of the user"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"],
                                "description": "Optional status filter"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The ID of the user"
                            },
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to complete"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The ID of the user"
                            },
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title for the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description for the task"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"],
                                "description": "New status for the task"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "New due date in ISO format (YYYY-MM-DDTHH:MM:SS.ssssss)"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The ID of the user"
                            },
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to delete"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

    async def run_agent(self, messages: List[Dict[str, str]], user_id: str) -> str:
        """
        Run the agent with the provided messages and user context.

        Args:
            messages: List of message dictionaries with role and content
            user_id: The ID of the user interacting with the agent

        Returns:
            The AI-generated response text
        """
        try:
            # Prepare messages for OpenAI API
            openai_messages = []
            for msg in messages:
                openai_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            # Call OpenAI API with tools
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Can be upgraded to gpt-4-turbo if available
                messages=openai_messages,
                tools=self.tools,
                tool_choice="auto",  # Let the model decide when to use tools
                temperature=0.7,
                max_tokens=1000
            )

            # Process the response
            response_message = response.choices[0].message

            # If the model decided to call a tool
            tool_calls = response_message.tool_calls
            if tool_calls:
                # Execute the tool calls
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = eval(tool_call.function.arguments)

                    # Add user_id to function arguments if not present
                    if "user_id" not in function_args:
                        function_args["user_id"] = user_id

                    # Execute the appropriate tool
                    result = await self._execute_tool(function_name, function_args)

                    # Add the result to the messages for follow-up
                    openai_messages.append({
                        "role": "tool",
                        "content": str(result),
                        "tool_call_id": tool_call.id
                    })

                # Get final response after tool execution
                final_response = await self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=openai_messages,
                    temperature=0.7,
                    max_tokens=1000
                )

                return final_response.choices[0].message.content
            else:
                # No tool calls, return the original response
                return response_message.content

        except Exception as e:
            # Log the error
            print(f"Error processing agent request: {str(e)}")
            return "I'm sorry, I encountered an issue processing your request. Please try again."

    async def _execute_tool(self, function_name: str, function_args: Dict[str, Any]) -> Any:
        """
        Execute the specified tool with the provided arguments.

        Args:
            function_name: Name of the tool to execute
            function_args: Arguments for the tool

        Returns:
            Result of the tool execution
        """
        try:
            if function_name == "add_task":
                return await add_task(**function_args)
            elif function_name == "list_tasks":
                return await list_tasks(**function_args)
            elif function_name == "complete_task":
                return await complete_task(**function_args)
            elif function_name == "update_task":
                return await update_task(**function_args)
            elif function_name == "delete_task":
                return await delete_task(**function_args)
            else:
                raise ValueError(f"Unknown tool: {function_name}")
        except Exception as e:
            # Return error message as string
            return f"Error executing {function_name}: {str(e)}"