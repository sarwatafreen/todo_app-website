from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func
from typing import Optional
from datetime import datetime
import uuid


class UserBase(SQLModel):
    """
    Base class for User model containing common fields.
    """
    email: str = Field(unique=True, nullable=False, max_length=255)
    role: str = Field(default="user", max_length=50)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    failed_login_attempts: int = Field(default=0)
    last_failed_login: Optional[datetime] = Field(default=None)
    account_locked_until: Optional[datetime] = Field(default=None)


class User(UserBase, table=True):
    """
    User model representing an authenticated user with credentials and role information.
    """
    __tablename__ = "users"  # Specify table name to avoid conflicts
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()))


class UserRead(UserBase):
    """
    Schema for reading user data, excludes sensitive fields.
    """
    id: str
    created_at: datetime
    updated_at: datetime
    # Note: hashed_password is intentionally excluded from responses


class UserCreate(UserBase):
    """
    Schema for creating a new user, includes password.
    """
    password: str
    confirm_password: str


class UserLogin(SQLModel):
    """
    Schema for user login.
    """
    email: str
    password: str


class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    email: Optional[str] = Field(default=None, max_length=255)
    role: Optional[str] = Field(default=None, max_length=50)
    is_active: Optional[bool] = Field(default=None)
    is_verified: Optional[bool] = Field(default=None)


class UserResponse(SQLModel):
    """
    Response schema for user information without sensitive data.
    """
    id: str
    email: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime