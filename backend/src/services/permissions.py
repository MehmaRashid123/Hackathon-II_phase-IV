"""
Permissions service for workspace access control.

Implements role-based access control (RBAC) for workspace features.
"""

from sqlmodel import Session, select
from typing import Optional
import uuid

from src.models.workspace_member import WorkspaceMember, WorkspaceRole
from src.models.user import User


class PermissionService:
    """Service for workspace permission checks."""

    @staticmethod
    def get_user_workspace_role(
        db: Session,
        user_id: uuid.UUID,
        workspace_id: uuid.UUID
    ) -> Optional[WorkspaceRole]:
        """
        Get user's role in a workspace.

        Args:
            db: Database session
            user_id: User ID
            workspace_id: Workspace ID

        Returns:
            WorkspaceRole if user is a member, None otherwise
        """
        statement = select(WorkspaceMember).where(
            WorkspaceMember.user_id == user_id,
            WorkspaceMember.workspace_id == workspace_id
        )
        membership = db.exec(statement).first()

        return membership.role if membership else None

    @staticmethod
    def user_has_workspace_access(
        db: Session,
        user_id: uuid.UUID,
        workspace_id: uuid.UUID,
        required_role: Optional[WorkspaceRole] = None
    ) -> bool:
        """
        Check if user has access to workspace with optional minimum role requirement.

        Args:
            db: Database session
            user_id: User ID
            workspace_id: Workspace ID
            required_role: Minimum role required (None = any member access)

        Returns:
            True if user has access, False otherwise
        """
        role = PermissionService.get_user_workspace_role(db, user_id, workspace_id)

        if role is None:
            return False

        if required_role is None:
            return True

        # Role hierarchy: OWNER > ADMIN > MEMBER > VIEWER
        role_hierarchy = {
            WorkspaceRole.VIEWER: 0,
            WorkspaceRole.MEMBER: 1,
            WorkspaceRole.ADMIN: 2,
            WorkspaceRole.OWNER: 3,
        }

        return role_hierarchy.get(role, 0) >= role_hierarchy.get(required_role, 0)

    @staticmethod
    def user_can_edit_task(
        db: Session,
        user_id: uuid.UUID,
        workspace_id: uuid.UUID
    ) -> bool:
        """
        Check if user can create/edit tasks in workspace.

        Requires MEMBER role or higher.
        """
        return PermissionService.user_has_workspace_access(
            db, user_id, workspace_id, WorkspaceRole.MEMBER
        )

    @staticmethod
    def user_can_manage_workspace(
        db: Session,
        user_id: uuid.UUID,
        workspace_id: uuid.UUID
    ) -> bool:
        """
        Check if user can manage workspace settings.

        Requires ADMIN role or higher.
        """
        return PermissionService.user_has_workspace_access(
            db, user_id, workspace_id, WorkspaceRole.ADMIN
        )

    @staticmethod
    def user_can_delete_workspace(
        db: Session,
        user_id: uuid.UUID,
        workspace_id: uuid.UUID
    ) -> bool:
        """
        Check if user can delete workspace.

        Requires OWNER role.
        """
        return PermissionService.user_has_workspace_access(
            db, user_id, workspace_id, WorkspaceRole.OWNER
        )

    @staticmethod
    def get_user_workspaces(
        db: Session,
        user_id: uuid.UUID
    ) -> list[tuple[uuid.UUID, WorkspaceRole]]:
        """
        Get all workspaces user has access to with their roles.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            List of (workspace_id, role) tuples
        """
        statement = select(WorkspaceMember).where(
            WorkspaceMember.user_id == user_id
        )
        memberships = db.exec(statement).all()

        return [(m.workspace_id, m.role) for m in memberships]
