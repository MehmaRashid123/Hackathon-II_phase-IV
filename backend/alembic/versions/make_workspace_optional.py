"""make workspace_id optional for personal tasks

Revision ID: workspace_optional_001
Revises: 
Create Date: 2026-02-08

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'workspace_optional_001'
down_revision = None  # Update this with your latest revision ID
branch_labels = None
depends_on = None


def upgrade():
    # Make workspace_id nullable for personal tasks
    op.alter_column('task', 'workspace_id',
                    existing_type=sa.UUID(),
                    nullable=True)


def downgrade():
    # Revert workspace_id to NOT NULL
    op.alter_column('task', 'workspace_id',
                    existing_type=sa.UUID(),
                    nullable=False)
