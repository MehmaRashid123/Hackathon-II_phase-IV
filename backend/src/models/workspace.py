"""
Workspace SQLModel for multi-tenant organization.

This module defines the Workspace entity for workspace-level data isolation.
Each workspace can have multiple users with different roles.
"""

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List
import uuid
from enum import Enum


class WorkspaceRole(str, Enum):
    """Roles for workspace members with hierarchical permissions."""
    OWNER = "OWNER"      # Full control: delete workspace, manage all settings
    ADMIN = "ADMIN"      # Manage members, projects, tasks
    MEMBER = "MEMBER"    # Create/edit own tasks, view workspace data
    VIEWER = "VIEWER"    # Read-only access


class Workspace(SQLModel, table=True):
    """
    Workspace model representing an organizational boundary for tasks and projects.

    **Schema Design**:
    - Many-to-many relationship with users via WorkspaceMember association table
    - One-to-many with projects and tasks (workspace owns these entities)
    - Indexes on created_at for sorting

    **Fields**:
    - id: UUID primary key
    - name: Workspace name (1-255 characters, required)
    - created_at: Timestamp of workspace creation (UTC)
    - updated_at: Timestamp of last update (UTC)
    """

    __tablename__ = "workspaces"

    # Primary key
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        description="Unique identifier for the workspace"
    )

    # Workspace details
    name: str = Field(
        max_length=255,
        nullable=False,
        description="Workspace name (1-255 characters)"
    )

    # Timestamps (UTC)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Timestamp of workspace creation (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp of last update (UTC)",
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    # Relationships
    members: List["WorkspaceMember"] = Relationship(
        back_populates="workspace",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    projects: List["Project"] = Relationship(
        back_populates="workspace",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    tasks: List["Task"] = Relationship(
        back_populates="workspace",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    activities: List["Activity"] = Relationship(
        back_populates="workspace",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class WorkspaceMember(SQLModel, table=True):
    """
    Association table for many-to-many relationship between users and workspaces.

    **Schema Design**:
    - Composite primary key on (workspace_id, user_id) ensures unique membership
    - Role-based access control (RBAC) via role field
    - Indexes on both foreign keys for efficient queries

    **Fields**:
    - workspace_id: Foreign key to workspaces.id
    - user_id: Foreign key to users.id
    - role: WorkspaceRole enum (OWNER, ADMIN, MEMBER, VIEWER)
    - joined_at: Timestamp when user was added to workspace
    """

    __tablename__ = "workspace_members"

    # Composite primary key
    workspace_id: uuid.UUID = Field(
        foreign_key="workspaces.id",
        primary_key=True,
        nullable=False,
        description="Foreign key to workspaces.id"
    )

    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        primary_key=True,
        nullable=False,
        description="Foreign key to users.id"
    )

    # Role-based access control
    role: WorkspaceRole = Field(
        default=WorkspaceRole.MEMBER,
        nullable=False,
        description="User's role in the workspace (OWNER, ADMIN, MEMBER, VIEWER)"
    )

    # Timestamp
    joined_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when user was added to workspace (UTC)"
    )

    # Relationships
    workspace: Workspace = Relationship(back_populates="members")
    user: "User" = Relationship(back_populates="workspace_memberships")
