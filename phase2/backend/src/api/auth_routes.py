from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict
from ..database.database import get_session
from ..models.user import UserCreate, UserRead
from ..services.auth_service import AuthService
from ..utils.auth import verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRead)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user."""
    auth_service = AuthService(session)

    try:
        user_read = auth_service.register_user(user_create)
        return user_read
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)) -> Dict[str, str]:
    """Login a user and return an access token."""
    auth_service = AuthService(session)

    user = auth_service.authenticate_user(email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_service.create_access_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    """Logout a user."""
    # In a stateless JWT system, logout is typically handled on the client side
    # by removing the token. We can add server-side token blacklisting if needed.
    return {"message": "Logged out successfully"}