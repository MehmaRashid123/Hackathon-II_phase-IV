"""Add workspace models and relationships

Revision ID: 001_workspace_models
Revises:
Create Date: 2026-02-05

This migration adds:
- workspaces table
- workspace_members table (many-to-many association)
- activities table for audit logging
- Updates tasks table with workspace_id, created_by, assigned_to
- Updates projects table with workspace_id
- Composite indexes for performance
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '001_workspace_models'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create workspaces table
    op.create_table(
        'workspaces',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()'), onupdate=sa.text('NOW()')),
    )
    op.create_index('ix_workspaces_created_at', 'workspaces', ['created_at'])

    # Create workspace_members table (association table)
    op.create_table(
        'workspace_members',
        sa.Column('workspace_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='MEMBER'),
        sa.Column('joined_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('workspace_id', 'user_id'),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Create activities table
    op.create_table(
        'activities',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('workspace_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('activity_type', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=False),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_activities_workspace_id', 'activities', ['workspace_id'])
    op.create_index('ix_activities_user_id', 'activities', ['user_id'])
    op.create_index('ix_activities_task_id', 'activities', ['task_id'])
    op.create_index('ix_activities_project_id', 'activities', ['project_id'])
    op.create_index('ix_activities_created_at', 'activities', ['created_at'])
    # Composite index for efficient activity feed queries
    op.create_index('ix_activities_workspace_created', 'activities', ['workspace_id', 'created_at'])

    # Add workspace_id to tasks table
    op.add_column('tasks', sa.Column('workspace_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key('fk_tasks_workspace', 'tasks', 'workspaces', ['workspace_id'], ['id'], ondelete='CASCADE')
    op.create_index('ix_tasks_workspace_id', 'tasks', ['workspace_id'])

    # Add created_by and assigned_to to tasks table
    op.add_column('tasks', sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('tasks', sa.Column('assigned_to', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key('fk_tasks_created_by', 'tasks', 'users', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('fk_tasks_assigned_to', 'tasks', 'users', ['assigned_to'], ['id'], ondelete='SET NULL')
    op.create_index('ix_tasks_created_by', 'tasks', ['created_by'])
    op.create_index('ix_tasks_assigned_to', 'tasks', ['assigned_to'])

    # Add workspace_id to projects table
    op.add_column('projects', sa.Column('workspace_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key('fk_projects_workspace', 'projects', 'workspaces', ['workspace_id'], ['id'], ondelete='CASCADE')
    op.create_index('ix_projects_workspace_id', 'projects', ['workspace_id'])

    # Create composite indexes for analytics performance
    op.create_index('ix_tasks_workspace_status', 'tasks', ['workspace_id', 'status'])
    op.create_index('ix_tasks_workspace_priority', 'tasks', ['workspace_id', 'priority'])
    op.create_index('ix_tasks_workspace_created', 'tasks', ['workspace_id', 'created_at'])


def downgrade() -> None:
    # Drop composite indexes
    op.drop_index('ix_tasks_workspace_created', 'tasks')
    op.drop_index('ix_tasks_workspace_priority', 'tasks')
    op.drop_index('ix_tasks_workspace_status', 'tasks')

    # Remove workspace_id from projects
    op.drop_index('ix_projects_workspace_id', 'projects')
    op.drop_constraint('fk_projects_workspace', 'projects', type_='foreignkey')
    op.drop_column('projects', 'workspace_id')

    # Remove created_by and assigned_to from tasks
    op.drop_index('ix_tasks_assigned_to', 'tasks')
    op.drop_index('ix_tasks_created_by', 'tasks')
    op.drop_constraint('fk_tasks_assigned_to', 'tasks', type_='foreignkey')
    op.drop_constraint('fk_tasks_created_by', 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'assigned_to')
    op.drop_column('tasks', 'created_by')

    # Remove workspace_id from tasks
    op.drop_index('ix_tasks_workspace_id', 'tasks')
    op.drop_constraint('fk_tasks_workspace', 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'workspace_id')

    # Drop activities table
    op.drop_index('ix_activities_workspace_created', 'activities')
    op.drop_index('ix_activities_created_at', 'activities')
    op.drop_index('ix_activities_project_id', 'activities')
    op.drop_index('ix_activities_task_id', 'activities')
    op.drop_index('ix_activities_user_id', 'activities')
    op.drop_index('ix_activities_workspace_id', 'activities')
    op.drop_table('activities')

    # Drop workspace_members table
    op.drop_table('workspace_members')

    # Drop workspaces table
    op.drop_index('ix_workspaces_created_at', 'workspaces')
    op.drop_table('workspaces')
