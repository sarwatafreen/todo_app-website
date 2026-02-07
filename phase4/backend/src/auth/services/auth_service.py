from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from src.auth.models.user_model import User
from src.auth.utils.password_utils import verify_password


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.

    Args:
        session: Database session
        email: User's email address
        password: User's plain text password

    Returns:
        User object if authentication succeeds, None otherwise
    """
    # Query user by email
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if user and verify_password(password, user.hashed_password):
        return user

    return None