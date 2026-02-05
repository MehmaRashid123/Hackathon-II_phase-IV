"""
User service layer for business logic.

This module handles user-related operations including registration,
email uniqueness validation, and user retrieval.

Separation of Concerns:
- Models (user.py): Database schema
- Schemas (auth_schemas.py): API validation
- Services (user_service.py): Business logic (THIS FILE)
- API (auth.py): Route handlers
"""

from sqlmodel import Session, select
from typing import Optional
from fastapi import HTTPException, status

from src.models.user import User
from src.schemas.auth_schemas import UserCreate
from src.utils.security import hash_password


class UserService:
    """
    Service class for user management operations.

    All business logic for user operations should be implemented here,
    keeping route handlers thin and focused on HTTP concerns.
    """

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by email address.

        Args:
            session: Database session
            email: User's email address

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            session: Database session
            user_id: User's UUID as string

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        return user

    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:
        """
        Create a new user account.

        This method handles:
        1. Email uniqueness validation
        2. Password hashing
        3. User creation in database

        Args:
            session: Database session
            user_data: Validated user registration data

        Returns:
            User: Created user object

        Raises:
            HTTPException 400: If email already exists

        Example:
            >>> user_data = UserCreate(email="new@example.com", password="SecurePass123")
            >>> user = UserService.create_user(session, user_data)
            >>> user.email
            'new@example.com'
        """
        # Step 1: Check if email already exists
        existing_user = UserService.get_user_by_email(session, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered. Please use a different email or try logging in."
            )

        # Step 2: Hash the password (NEVER store plain-text passwords)
        hashed_password = hash_password(user_data.password)

        # Step 3: Create user object
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password
        )

        # Step 4: Save to database
        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # Get auto-generated fields (id, created_at)

        return new_user

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.

        Args:
            session: Database session
            email: User's email address
            password: Plain-text password to verify

        Returns:
            User object if credentials are valid, None otherwise

        Note:
            This method will be used in Phase 5 (Sign-In) but is defined here
            for service layer completeness.
        """
        from src.utils.security import verify_password

        # Get user by email
        user = UserService.get_user_by_email(session, email)
        if not user:
            return None

        # Verify password
        if not verify_password(password, user.hashed_password):
            return None

        return user
