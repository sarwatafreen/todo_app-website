from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.api.task_endpoints import router as tasks_router
from src.auth.api.auth_endpoints import router as auth_router
from src.database import async_engine
from src.middleware.auth_middleware import AuthMiddleware
from typing import Dict, Any


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the application.
    Handles startup and shutdown events.
    """
    # Startup
    print("Starting up the application...")

    # Shutdown
    yield

    # Close the database engine
    await async_engine.dispose()
    print("Application shutdown complete")


# Create FastAPI app instance
app = FastAPI(
    title="Backend API & Data Layer",
    description="Secure, user-scoped REST API with JWT authentication and Neon PostgreSQL storage",
    version="1.0.0",
    lifespan=lifespan
)


# Add the authentication middleware
app.add_middleware(AuthMiddleware)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the auth and tasks routers
app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
async def root():
    """
    Root endpoint for basic health check.
    """
    return {"message": "Backend API is running"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is operational.
    """
    return {"status": "healthy", "service": "backend-api"}


# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Global handler for HTTP exceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    Global handler for request validation errors.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": [
                {
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "type": error["type"]
                }
                for error in exc.errors()
            ]
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Global handler for general exceptions.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)