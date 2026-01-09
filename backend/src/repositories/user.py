from sqlmodel import Session, select
from typing import Optional
from src.models.user import User, UserCreate


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_create: UserCreate, hashed_password: str) -> User:
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()