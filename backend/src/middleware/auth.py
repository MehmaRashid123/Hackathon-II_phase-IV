"""
Authentication middleware for JWT token verification.

This module provides FastAPI dependencies for securing endpoints
and extracting the current authenticated user from JWT tokens.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from typing import Optional
import uuid

from src.database import get_session
from src.models.user import User
from src.services.user_service import UserService
from src.utils.security import verify_token


# HTTP Bearer token scheme for Authorization header
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    FastAPI dependency that extracts and validates JWT token from Authorization header.

    This is the core authentication middleware used to protect routes.
    It performs the following steps:
    1. Extract Bearer token from Authorization header
    2. Verify JWT signature and expiration
    3. Extract user ID from 'sub' claim
    4. Fetch user from database
    5. Return authenticated user object

    Args:
        credentials: HTTP Bearer token from Authorization header
        session: Database session (injected)

    Returns:
        User: Authenticated user object

    Raises:
        HTTPException 401: If token is missing, invalid, expired, or user not found

    Usage:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id}
    """
    # Step 1: Get token from credentials
    token = credentials.credentials

    # Step 2: Verify JWT token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token. Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Step 3: Extract user ID from 'sub' claim
    user_id_str: Optional[str] = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identifier (sub claim). Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Step 4: Validate user ID format (UUID)
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identifier format in token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Step 5: Fetch user from database
    user = UserService.get_user_by_id(session, str(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found. Account may have been deleted.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Step 6: Return authenticated user
    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    session: Session = Depends(get_session)
) -> Optional[User]:
    """
    Optional authentication - returns user if token is valid, None otherwise.

    Useful for endpoints that have different behavior for authenticated vs unauthenticated users.

    Args:
        credentials: Optional HTTP Bearer token
        session: Database session (injected)

    Returns:
        User object if authenticated, None otherwise
    """
    if not credentials:
        return None

    try:
        return await get_current_user(credentials, session)
    except HTTPException:
        return None


def require_auth(user: User = Depends(get_current_user)) -> User:
    """
    Simplified dependency for routes that require authentication.

    Usage:
        @app.get("/protected")
        def protected_route(user: User = Depends(require_auth)):
            return {"user_id": user.id}
    """
    return user


async def validate_user_id(
    user_id: str,
    current_user: User = Depends(get_current_user)
) -> str:
    """
    FastAPI dependency that validates URL user_id matches authenticated user.

    This is critical for user isolation in the Task API. It ensures that users
    can only access their own resources by comparing the user_id in the URL
    with the authenticated user's ID from the JWT token.

    Args:
        user_id: User ID from URL path parameter
        current_user: Authenticated user from JWT token (injected)

    Returns:
        str: Validated user_id (matches authenticated user)

    Raises:
        HTTPException 403: If URL user_id does not match authenticated user

    Usage:
        @app.get("/api/{user_id}/tasks")
        def get_tasks(
            user_id: str = Depends(validate_user_id)
        ):
            # user_id is guaranteed to match authenticated user
            return TaskService.get_user_tasks(user_id)

    Security:
        - User A with token for ID "123" cannot access /api/456/tasks
        - Returns HTTP 403 Forbidden if user_id mismatch
        - This prevents horizontal privilege escalation attacks
    """
    # Validate UUID format of path parameter
    try:
        path_user_id = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format in URL path"
        )

    # Compare URL user_id with authenticated user's ID
    if path_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this user's resources. "
                   "You can only access your own tasks."
        )

    # Return validated user_id as string
    return str(path_user_id)
