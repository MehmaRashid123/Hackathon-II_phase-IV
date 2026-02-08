"""
Pydantic schemas for authentication endpoints.

This module defines request and response models for authentication operations.
Schemas are used for API validation and serialization, separate from database models.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import uuid
import re


class UserCreate(BaseModel):
    """
    Request schema for user registration.

    Validates email format and password requirements before processing.
    """

    email: EmailStr = Field(
        ...,
        description="User's email address (must be valid and unique)",
        examples=["user@example.com"]
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User's password (minimum 8 characters, must contain at least one letter and one number)",
        examples=["SecurePass123"]
    )

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength requirements.

        Requirements:
        - Minimum 8 characters
        - At least one letter (a-z or A-Z)
        - At least one number (0-9)

        Args:
            v: Password string to validate

        Returns:
            str: Validated password

        Raises:
            ValueError: If password doesn't meet requirements
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        if not re.search(r'[a-zA-Z]', v):
            raise ValueError('Password must contain at least one letter')

        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')

        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "newuser@example.com",
                "password": "SecurePassword123"
            }
        }


class UserResponse(BaseModel):
    """
    Response schema for user data.

    Returns user information without sensitive data (no password).
    """

    id: uuid.UUID = Field(
        ...,
        description="Unique user identifier"
    )

    email: str = Field(
        ...,
        description="User's email address"
    )

    created_at: datetime = Field(
        ...,
        description="Account creation timestamp (UTC)"
    )

    class Config:
        from_attributes = True  # Allow conversion from SQLModel/ORM objects
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2024-01-01T00:00:00Z"
            }
        }


class UserLogin(BaseModel):
    """
    Request schema for user login.

    Used for sign-in endpoint (Phase 5).
    """

    email: EmailStr = Field(
        ...,
        description="User's email address"
    )

    password: str = Field(
        ...,
        description="User's password"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123"
            }
        }


class TokenResponse(BaseModel):
    """
    Response schema for authentication tokens.

    Returned after successful login (Phase 5).
    """

    access_token: str = Field(
        ...,
        description="JWT access token"
    )

    token_type: str = Field(
        default="bearer",
        description="Token type (always 'bearer')"
    )

    user: UserResponse = Field(
        ...,
        description="Authenticated user information"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com",
                    "created_at": "2024-01-01T00:00:00Z"
                }
            }
        }
