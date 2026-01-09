"""
API routes for tasks in the AI Task Agent System
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from backend.agent.agent_instance import agent


router = APIRouter(prefix="/tasks", tags=["tasks"])


# Data models
class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[str] = None
    priority: str = "medium"
    language: Optional[str] = None
    created_at: str = datetime.now().isoformat()


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[str] = None  # Using string to allow partial updates


# In-memory storage (for demo purposes)
tasks_db = []


@router.get("")
async def get_tasks():
    """Get all tasks"""
    return {"tasks": tasks_db}


@router.post("")
async def create_task(task_create: TaskCreate):
    """Create a new task with AI processing"""
    # Process the task through the agent to extract additional info
    processed_data = agent.process(task_create.title)
    
    # Create the task object
    task = Task(
        id=str(uuid.uuid4()),
        title=processed_data.get("title", task_create.title),
        description=task_create.description,
        due_date=processed_data.get("due_date"),
        priority=processed_data.get("priority", "medium"),
        language=processed_data.get("language")
    )
    
    tasks_db.append(task)
    return task


@router.get("/{task_id}")
async def get_task(task_id: str):
    """Get a specific task by ID"""
    for task in tasks_db:
        if task.id == task_id:
            return task
    
    raise HTTPException(status_code=404, detail="Task not found")


@router.put("/{task_id}")
async def update_task(task_id: str, task_update: TaskUpdate):
    """Update a specific task by ID"""
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            if task_update.title is not None:
                tasks_db[i].title = task_update.title
            if task_update.description is not None:
                tasks_db[i].description = task_update.description
            if task_update.completed is not None:
                tasks_db[i].completed = task_update.completed == "true"
            
            return tasks_db[i]
    
    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Delete a specific task by ID"""
    global tasks_db
    initial_length = len(tasks_db)
    tasks_db = [task for task in tasks_db if task.id != task_id]
    
    if len(tasks_db) == initial_length:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully"}