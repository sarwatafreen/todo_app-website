from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Session
from src.services.auth import AuthService
from src.models.user import UserCreate, UserRead


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBearer()


from typing import Generator
from src.database import get_session


def get_db_session() -> Generator[Session, None, None]:
    gen = get_session()
    db_session = next(gen)
    try:
        yield db_session
    finally:
        db_session.close()


def get_auth_service(session: Session = Depends(get_db_session)) -> AuthService:
    return AuthService(session)


@router.post("/signup", response_model=UserRead)
def signup(user_create: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    try:
        user = auth_service.register_user(user_create)
        return UserRead(
            id=user.id,
            email=user.email,
            created_at=user.created_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login(login_request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    user = auth_service.authenticate_user(
        login_request.email, login_request.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    token_data = auth_service.decode_token(credentials.credentials)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = auth_service.user_repo.get_user_by_email(token_data["email"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserRead(
        id=user.id,
        email=user.email,
        created_at=user.created_at.isoformat()
    )