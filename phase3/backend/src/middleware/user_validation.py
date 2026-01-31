from fastapi import HTTPException, status
from typing import Dict
from uuid import UUID
from ..middleware.auth import get_current_user

def validate_user_id_match(requested_user_id: str, current_user: Dict) -> bool:
    """
    Validate that the requested user ID matches the current authenticated user ID.

    Args:
        requested_user_id: The user ID from the request path/params
        current_user: The current authenticated user (from JWT)

    Returns:
        bool: True if the IDs match, raises HTTPException otherwise
    """
    if str(current_user["user_id"]) != str(requested_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's resources"
        )
    return True