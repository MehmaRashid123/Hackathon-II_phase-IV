"""
Authentication API endpoints.

This module defines routes for user authentication:
- POST /api/auth/signup - User registration
- POST /api/auth/signin - User login (Phase 5)
- GET /api/auth/me - Get current user (Phase 6)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.database import get_session
from src.schemas.auth_schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from src.services.user_service import UserService
from src.utils.security import create_access_token
from src.middleware.auth import get_current_user
from src.models.user import User


# Create router for authentication endpoints
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description="""
    Create a new user account with email and password.

    **Requirements:**
    - Email must be valid and unique (not already registered)
    - Password must be at least 8 characters
    - Password must contain at least one letter and one number

    **Returns:**
    - HTTP 201: User created successfully
    - HTTP 400: Email already exists or validation failed
    - HTTP 422: Invalid request data
    """
)
async def signup(
    user_data: UserCreate,
    session: Session = Depends(get_session)
) -> UserResponse:
    """
    Register a new user account.

    Args:
        user_data: User registration data (email, password)
        session: Database session (injected)

    Returns:
        UserResponse: Created user information (without password)

    Raises:
        HTTPException 400: If email already exists
        HTTPException 422: If validation fails (handled by Pydantic)

    Example Request:
        POST /api/auth/signup
        {
            "email": "newuser@example.com",
            "password": "SecurePassword123"
        }

    Example Response (201):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "newuser@example.com",
            "created_at": "2024-01-01T12:00:00Z"
        }
    """
    # Create user via service layer (handles validation and business logic)
    user = UserService.create_user(session, user_data)

    # Return user data (password is excluded by UserResponse schema)
    return UserResponse.model_validate(user)


@router.post(
    "/signin",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Sign in to existing account",
    description="""
    Authenticate with email and password to receive a JWT access token.

    **Note:** This endpoint will be fully implemented in Phase 5.
    """
)
async def signin(
    credentials: UserLogin,
    session: Session = Depends(get_session)
) -> TokenResponse:
    """
    Sign in to an existing account.

    This is a placeholder for Phase 5 implementation.

    Args:
        credentials: User login credentials (email, password)
        session: Database session (injected)

    Returns:
        TokenResponse: JWT access token and user information

    Raises:
        HTTPException 401: If credentials are invalid
    """
    # Authenticate user
    user = UserService.authenticate_user(
        session,
        credentials.email,
        credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Create JWT token with user information (sub: user_id, email: user_email)
    # This allows backend to verify identity independently in Phase 6
    access_token = create_access_token(
        data={
            "sub": str(user.id),  # Subject: user's UUID
            "email": user.email,   # Include email for convenience
            "type": "access"       # Token type
        }
    )

    # Return token and user info
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user",
    description="""
    Retrieve information about the currently authenticated user.

    **Requires**: Valid JWT token in Authorization header

    **Returns:**
    - HTTP 200: Current user information
    - HTTP 401: If token is missing, invalid, or expired

    **Authorization**: Bearer {jwt_token}
    """
)
async def get_me(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Get current authenticated user details.

    This is a protected endpoint that demonstrates JWT verification middleware.
    It will be the foundation for user isolation in Spec 2 (Task API).

    Args:
        current_user: Authenticated user (injected by middleware)

    Returns:
        UserResponse: Current user information (without password)

    Example Request:
        GET /api/auth/me
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

    Example Response (200):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com",
            "created_at": "2024-01-01T12:00:00Z"
        }
    """
    return UserResponse.model_validate(current_user)
