"""
API routes for the AI agent in the AI Task Agent System
"""
from fastapi import APIRouter
from pydantic import BaseModel
from backend.agent.agent_instance import agent


router = APIRouter(prefix="/agent", tags=["agent"])


class AgentRequest(BaseModel):
    text: str


@router.post("/task")
def create_task_from_text(req: AgentRequest):
    result = agent.process(req.text)  # Using .process instead of .run since that's our method name
    return result