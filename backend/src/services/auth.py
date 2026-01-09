from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session
from src.models.user import User, UserCreate
from src.repositories.user import UserRepository
import os


class AuthService:
    def __init__(self, session: Session):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("SECRET_KEY", "secret123")  # In production, use a strong secret
        self.algorithm = "HS256"
        self.user_repo = UserRepository(session)

    def hash_password(self, password: str) -> str:
        # bcrypt has a maximum password length of 72 bytes
        # Truncate if necessary, though in practice you might want to reject long passwords
        if len(password.encode('utf-8')) > 72:
            password = password[:72]  # Conservative truncation
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)  # Default to 1 hour
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_repo.get_user_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    def register_user(self, user_create: UserCreate) -> User:
        # Check if user already exists
        existing_user = self.user_repo.get_user_by_email(user_create.email)
        if existing_user:
            raise ValueError("Email already registered")

        # Hash the password and create the user
        hashed_password = self.hash_password(user_create.password)
        return self.user_repo.create_user(user_create, hashed_password)

    def decode_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email: str = payload.get("sub")
            if email is None:
                return None
            return {"email": email}
        except JWTError:
            return None