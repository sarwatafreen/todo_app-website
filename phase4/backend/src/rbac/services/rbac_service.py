from enum import Enum
from typing import List, Dict, Any
from src.auth.models.user_model import User


class Permission(str, Enum):
    """
    Enum for defining available permissions in the system.
    """
    TASK_READ = "task:read"
    TASK_CREATE = "task:create"
    TASK_UPDATE = "task:update"
    TASK_DELETE = "task:delete"
    USER_MANAGE = "user:manage"
    ADMIN_ACCESS = "admin:access"


class Role(str, Enum):
    """
    Enum for defining available roles in the system.
    """
    USER = "user"
    ADMIN = "admin"


class RBACService:
    """
    Role-Based Access Control service for managing permissions.
    """

    # Define role permissions mapping
    ROLE_PERMISSIONS: Dict[Role, List[Permission]] = {
        Role.USER: [
            Permission.TASK_READ,
            Permission.TASK_CREATE,
            Permission.TASK_UPDATE,
            Permission.TASK_DELETE
        ],
        Role.ADMIN: [
            Permission.TASK_READ,
            Permission.TASK_CREATE,
            Permission.TASK_UPDATE,
            Permission.TASK_DELETE,
            Permission.USER_MANAGE,
            Permission.ADMIN_ACCESS
        ]
    }

    @classmethod
    def get_permissions_for_role(cls, role: str) -> List[Permission]:
        """
        Get all permissions for a given role.

        Args:
            role: The role string

        Returns:
            List of permissions for the role
        """
        role_enum = Role(role.lower()) if role.lower() in Role.__members__ else Role.USER
        return cls.ROLE_PERMISSIONS.get(role_enum, [])

    @classmethod
    def user_has_permission(cls, user: User, permission: Permission) -> bool:
        """
        Check if a user has a specific permission.

        Args:
            user: The user object
            permission: The permission to check

        Returns:
            True if user has the permission, False otherwise
        """
        user_permissions = cls.get_permissions_for_role(user.role)
        return permission in user_permissions

    @classmethod
    def user_has_role(cls, user: User, role: Role) -> bool:
        """
        Check if a user has a specific role.

        Args:
            user: The user object
            role: The role to check

        Returns:
            True if user has the role, False otherwise
        """
        return user.role.lower() == role.value.lower()