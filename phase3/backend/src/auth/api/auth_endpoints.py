from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta
from src.auth.models.user_model import User, UserCreate, UserLogin
from src.auth.schemas.auth_schemas import UserResponse
from src.auth.schemas.auth_schemas import LoginResponse, TokenRefresh
from src.auth.jwt_handler import create_access_token, create_refresh_token, decode_and_validate_jwt
from src.database import get_async_session
from src.auth.utils.password_utils import hash_password, verify_password
from src.auth.services.auth_service import authenticate_user
from src.auth.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Register a new user with secure password hashing.

    Args:
        user_data: User registration data including email and password
        session: Database session

    Returns:
        Created user information

    Raises:
        HTTPException: 400 if email already exists or validation fails
    """
    # Check if user with email already exists
    existing_user_statement = select(User).where(User.email == user_data.email)
    existing_user_result = await session.execute(existing_user_statement)
    existing_user = existing_user_result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate password confirmation
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create new user
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        role="user"  # Default role
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Convert to response model (excluding sensitive fields)
    response_user = UserResponse(
        id=str(user.id),  # Ensure ID is a string
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

    return response_user


@router.post("/login", response_model=LoginResponse)
async def login_user(
    user_credentials: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Authenticate user and return JWT tokens.

    Args:
        user_credentials: User login credentials (email and password)
        session: Database session

    Returns:
        JWT tokens and user information

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Query user by email
    user_statement = select(User).where(User.email == user_credentials.email)
    user_result = await session.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login time
    user.updated_at = datetime.now()
    session.add(user)
    await session.commit()

    # Create access and refresh tokens
    access_token_expires = timedelta(minutes=30)  # Use settings if available
    refresh_token_expires = timedelta(days=7)    # Use settings if available

    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )

    refresh_token = create_refresh_token(
        data={"sub": user.id},
        expires_delta=refresh_token_expires
    )

    # Create response
    user_response = UserResponse(
        id=str(user.id),  # Ensure ID is a string
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=1800,  # 30 minutes in seconds
        user=user_response
    )


@router.post("/refresh", response_model=dict)
async def refresh_token(
    token_data: TokenRefresh
):
    """
    Refresh access token using refresh token.

    Args:
        token_data: Refresh token

    Returns:
        New access token

    Raises:
        HTTPException: 401 if refresh token is invalid
    """
    try:
        # Decode and validate refresh token
        payload = decode_and_validate_jwt(token_data.refresh_token)

        # Check if token type is refresh
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: no user identifier found"
            )

        # Create new access token
        access_token_expires = timedelta(minutes=30)  # Use settings if available
        new_access_token = create_access_token(
            data={"sub": user_id},
            expires_delta=access_token_expires
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 1800  # 30 minutes in seconds
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get current user's profile information.

    Args:
        current_user_id: ID of the currently authenticated user
        session: Database session

    Returns:
        User profile information
    """
    # Get the user from the database
    user_statement = select(User).where(User.id == current_user_id)
    user_result = await session.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Return user response
    user_response = UserResponse(
        id=str(user.id),  # Ensure ID is a string
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

    return user_response