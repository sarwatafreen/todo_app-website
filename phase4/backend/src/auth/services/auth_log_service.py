from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime, func
import json
import uuid


class AuthEventType(str, Enum):
    """
    Enum for authentication event types.
    """
    LOGIN_ATTEMPT = "login_attempt"
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"
    TOKEN_REFRESH = "token_refresh"
    AUTH_ERROR = "auth_error"


class AuthLogBase(SQLModel):
    """
    Base class for authentication log entries.
    """
    user_id: Optional[str] = Field(default=None)
    event_type: str = Field(max_length=50)
    success: bool = Field(default=False)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None)
    details: Optional[dict] = Field(default={})


class AuthLog(AuthLogBase, table=True):
    """
    Authentication log model for tracking authentication events.
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(sa_column_kwargs={"server_default": func.now()})

    class Config:
        arbitrary_types_allowed = True


async def log_auth_event(
    user_id: Optional[str] = None,
    event_type: AuthEventType = AuthEventType.LOGIN_ATTEMPT,
    success: bool = False,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[dict] = None
):
    """
    Log an authentication event for security monitoring.

    Args:
        user_id: ID of the user involved in the event (optional)
        event_type: Type of authentication event
        success: Whether the event was successful
        ip_address: IP address of the request (optional)
        user_agent: User agent string of the request (optional)
        details: Additional details about the event (optional)
    """
    # In a real implementation, this would log to a database or logging service
    # For now, we'll just print to console for demonstration purposes
    print(f"Auth Event: {event_type.value} | User: {user_id} | Success: {success} | IP: {ip_address}")

    # This is a placeholder implementation - in a real system, you would:
    # 1. Save to database
    # 2. Send to logging service
    # 3. Trigger alerts for suspicious activity
    pass