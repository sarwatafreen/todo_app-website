"""
FastAPI backend for the AI Task Agent System
"""
from fastapi import FastAPI
from backend.api.tasks import router as tasks_router
from backend.api.agent import router as agent_router

app = FastAPI(title="AI Task Agent System API", version="1.0.0")


@app.get("/")
async def root():
    """Root endpoint for the API"""
    return {"message": "Welcome to the AI Task Agent System API"}


# Include the API routers
app.include_router(tasks_router)
app.include_router(agent_router)