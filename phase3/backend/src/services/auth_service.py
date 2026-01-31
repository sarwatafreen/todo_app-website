from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate, UserRead
from ..utils.auth import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from uuid import UUID

class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def register_user(self, user_create: UserCreate) -> UserRead:
        """Register a new user."""
        # Check if user already exists
        existing_user = self.session.exec(
            select(User).where(User.email == user_create.email)
        ).first()

        if existing_user:
            raise ValueError("Email already registered")

        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create the user
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password
        )

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        # Convert to UserRead model manually
        return UserRead(
            id=db_user.id,
            email=db_user.email,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        user = self.session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user or not verify_password(password, user.hashed_password):
            return None

        return user

    def create_access_token_for_user(self, user: User) -> str:
        """Create an access token for a user."""
        data = {"sub": str(user.id), "email": user.email}
        token = create_access_token(
            data=data,
            expires_delta=timedelta(minutes=30)
        )
        return token