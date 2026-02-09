"""
Migration: Create tasks table

This migration creates the tasks table for storing user tasks that can be
managed through the AI assistant. Tasks include title, description, completion
status, and timestamps for tracking.

Revision ID: 003
Created: 2026-02-09
"""
from sqlalchemy import text


def upgrade(connection):
    """Create tasks table with proper indexes and constraints."""
    
    # Create tasks table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS tasks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    """))
    
    # Create index on user_id for multi-tenant isolation
    connection.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_tasks_user_id 
        ON tasks(user_id)
    """))
    
    # Create index on completed for filtering
    connection.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_tasks_completed 
        ON tasks(completed)
    """))
    
    # Create composite index for efficient user + completed queries
    connection.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_tasks_user_completed 
        ON tasks(user_id, completed)
    """))
    
    # Create index on created_at for sorting
    connection.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_tasks_created_at 
        ON tasks(created_at DESC)
    """))
    
    connection.commit()
    print("✓ Created tasks table with indexes")


def downgrade(connection):
    """Drop tasks table and its indexes."""
    
    connection.execute(text("DROP INDEX IF EXISTS idx_tasks_created_at"))
    connection.execute(text("DROP INDEX IF EXISTS idx_tasks_user_completed"))
    connection.execute(text("DROP INDEX IF EXISTS idx_tasks_completed"))
    connection.execute(text("DROP INDEX IF EXISTS idx_tasks_user_id"))
    connection.execute(text("DROP TABLE IF EXISTS tasks CASCADE"))
    
    connection.commit()
    print("✓ Dropped tasks table")


if __name__ == "__main__":
    """Run migration directly for testing."""
    from src.core.database import engine
    
    with engine.connect() as conn:
        print("Running migration 003: Create tasks table...")
        upgrade(conn)
        print("Migration completed successfully!")
