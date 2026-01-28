from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class RoleBase(SQLModel):
    """
    Base class for Role model containing common fields.
    """
    name: str = Field(unique=True, nullable=False, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)


class Role(RoleBase, table=True):
    """
    Role model representing user roles and their permissions.
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    permissions: List[str] = Field(default=[], sa_column_kwargs={"server_default": "'[]'::jsonb"})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class RoleCreate(RoleBase):
    """
    Schema for creating a new role.
    """
    permissions: List[str] = []


class RoleRead(RoleBase):
    """
    Schema for reading role data.
    """
    id: str
    permissions: List[str]
    created_at: datetime
    updated_at: datetime


class RoleUpdate(SQLModel):
    """
    Schema for updating role information.
    """
    name: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    permissions: Optional[List[str]] = []