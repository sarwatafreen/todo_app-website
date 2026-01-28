from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.jwt_handler import security, decode_and_validate_jwt


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get the current user from the JWT token in the Authorization header.

    Args:
        credentials: HTTP authorization credentials from the request

    Returns:
        User ID as string from the token payload

    Raises:
        HTTPException: If token is invalid, expired, or user ID not found
    """
    try:
        payload = decode_and_validate_jwt(credentials.credentials)
        user_id: str = payload.get("sub")

        if user_id is None:
            # Fallback to user_id if sub is not present
            user_id = payload.get("user_id")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: no user identifier found"
                )

        return user_id
    except HTTPException:
        # Re-raise HTTPExceptions (like expired/invalid token)
        raise
    except Exception:
        # Catch any other exception during token validation
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )