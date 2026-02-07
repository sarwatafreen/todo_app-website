from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """
    Schema for user creation.
    """
    email: str
    password: str
    confirm_password: str

    @validator('email')
    def validate_email(cls, email):
        """Validate email format."""
        if '@' not in email or '.' not in email.split('@')[1]:
            raise ValueError('Invalid email format')
        return email

    @validator('password')
    def validate_password(cls, password):
        """Validate password strength."""
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in password):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in password):
            raise ValueError('Password must contain at least one digit')
        return password

    @validator('confirm_password')
    def passwords_match(cls, confirm_password, values):
        """Verify that passwords match."""
        if 'password' in values and confirm_password != values['password']:
            raise ValueError('Passwords do not match')
        return confirm_password


class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    email: str
    password: str


class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    """
    Schema for token refresh request.
    """
    refresh_token: str


class TokenData(BaseModel):
    """
    Schema for token data.
    """
    user_id: str
    username: Optional[str] = None


class UserResponse(BaseModel):
    """
    Schema for user response without sensitive data.
    """
    id: str
    email: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class LoginResponse(BaseModel):
    """
    Schema for login response.
    """
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user: UserResponse