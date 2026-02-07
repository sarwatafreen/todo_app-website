"""
Dependency functions for the Todo AI Chatbot application.
Includes database, authentication, JWT, and Better Auth dependencies.
"""
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from .database import get_async_session
from .auth.jwt_handler import decode_and_validate_jwt


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session dependency.

    Yields:
        AsyncSession: Database session for the request
    """
    async with get_async_session() as session:
        yield session


def get_current_user(token: str = Depends(lambda: None)) -> str:
    """
    Get current user from JWT token.

    Args:
        token: JWT token from Authorization header

    Returns:
        str: User ID from the JWT token

    Raises:
        HTTPException: 401 if token is invalid or expired
        HTTPException: 403 if user is not authorized
    """
    # This function would typically be called with Depends(oauth2_scheme)
    # For now, we'll implement the core logic
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Decode and validate the JWT token
        payload = decode_and_validate_jwt(token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_user_access(user_id: str, requested_user_id: str) -> None:
    """
    Verify that the authenticated user has access to the requested resource.

    Args:
        user_id: The ID of the authenticated user
        requested_user_id: The ID of the user resource being accessed

    Raises:
        HTTPException: 403 if user does not have access to the resource
    """
    if user_id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )


def get_bearer_token(authorization: str = None) -> str:
    """
    Extract the Bearer token from the Authorization header.

    Args:
        authorization: Authorization header value

    Returns:
        str: The extracted token

    Raises:
        HTTPException: 401 if Authorization header is missing or invalid
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )