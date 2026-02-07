from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.background import BackgroundTask
from src.auth.jwt_handler import decode_and_validate_jwt
import re


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Global authentication middleware that validates JWT tokens for API routes.

    Applies to all /api/* paths, skips public endpoints like docs, health checks, etc.
    """

    async def dispatch(self, request: Request, call_next):
        # Define patterns for paths that should bypass authentication
        public_paths = [
            r"/docs",  # Swagger UI
            r"/redoc",  # ReDoc
            r"/openapi.json",  # OpenAPI schema
            r"/health",  # Health check
            r"/$",  # Root path
            r"/auth/signup",  # Auth endpoints
            r"/auth/login",  # Auth endpoints
            r"/auth/refresh",  # Auth endpoints
        ]

        # Check if the request path matches any public path pattern
        is_public = False
        for pattern in public_paths:
            if re.match(pattern, request.url.path):
                is_public = True
                break

        # Apply authentication only to API routes that are not public
        if request.url.path.startswith("/api/") and not is_public:
            # Extract authorization header
            auth_header = request.headers.get("authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated: Bearer token required"
                )

            # Extract the token
            token = auth_header[7:]  # Remove "Bearer " prefix

            try:
                # Decode and validate the JWT token
                payload = decode_and_validate_jwt(token)

                # Extract user_id from the token
                user_id = payload.get("sub")
                if user_id is None:
                    # Fallback to user_id if sub is not present
                    user_id = payload.get("user_id")
                    if user_id is None:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token: no user identifier found"
                        )

                # Attach the user_id to the request state for later use
                request.state.current_user = user_id

            except HTTPException:
                # Re-raise HTTP exceptions (like expired/invalid token)
                raise
            except Exception:
                # Catch any other exception during token validation
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )

        # Continue with the request
        response = await call_next(request)
        return response