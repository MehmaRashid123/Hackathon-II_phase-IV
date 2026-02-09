"""
Migration: Create conversations table

This migration creates the conversations table for storing chat conversations
between users and the AI assistant. Each conversation belongs to a user and
contains metadata like title and timestamps.

Revision ID: 001
Created: 2026-02-09
"""
from sqlalchemy import text


def upgrade(connection):
    """Create conversations table with proper indexes and constraints."""
    
    # Create conversations table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS conversations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            title VARCHAR(255),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """))
    
    # Create index on user_id for efficient queries
    connection.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_conversations_user_id 
        ON conversations(user_id)
    """))
    
    # Create index on created_at for sorting
    connection.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_conversations_created_at 
        ON conversations(created_at DESC)
    """))
    
    connection.commit()
    print("✓ Created conversations table with indexes")


def downgrade(connection):
    """Drop conversations table and its indexes."""
    
    connection.execute(text("DROP INDEX IF EXISTS idx_conversations_created_at"))
    connection.execute(text("DROP INDEX IF EXISTS idx_conversations_user_id"))
    connection.execute(text("DROP TABLE IF EXISTS conversations CASCADE"))
    
    connection.commit()
    print("✓ Dropped conversations table")


if __name__ == "__main__":
    """Run migration directly for testing."""
    from src.core.database import engine
    
    with engine.connect() as conn:
        print("Running migration 001: Create conversations table...")
        upgrade(conn)
        print("Migration completed successfully!")
