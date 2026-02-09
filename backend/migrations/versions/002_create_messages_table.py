"""
Migration: Create messages table

This migration creates the messages table for storing individual messages
within conversations. Messages have roles (user, assistant, tool) and are
linked to both conversations and users for multi-tenant isolation.

Revision ID: 002
Depends on: 001
Created: 2026-02-09
"""
from sqlalchemy import text


def upgrade(connection):
    """Create messages table with proper indexes and constraints."""
    
    # Create messages table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS messages (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'tool')),
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """))
    
    # Create index on conversation_id for efficient message retrieval
    connection.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_messages_conversation_id 
        ON messages(conversation_id)
    """))
    
    # Create index on user_id for multi-tenant isolation
    connection.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_messages_user_id 
        ON messages(user_id)
    """))
    
    # Create composite index for efficient conversation + user queries
    connection.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_messages_conversation_user 
        ON messages(conversation_id, user_id)
    """))
    
    # Create index on created_at for message ordering
    connection.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_messages_created_at 
        ON messages(created_at ASC)
    """))
    
    connection.commit()
    print("✓ Created messages table with indexes and role constraint")


def downgrade(connection):
    """Drop messages table and its indexes."""
    
    connection.execute(text("DROP INDEX IF EXISTS idx_messages_created_at"))
    connection.execute(text("DROP INDEX IF EXISTS idx_messages_conversation_user"))
    connection.execute(text("DROP INDEX IF EXISTS idx_messages_user_id"))
    connection.execute(text("DROP INDEX IF EXISTS idx_messages_conversation_id"))
    connection.execute(text("DROP TABLE IF EXISTS messages CASCADE"))
    
    connection.commit()
    print("✓ Dropped messages table")


if __name__ == "__main__":
    """Run migration directly for testing."""
    from src.core.database import engine
    
    with engine.connect() as conn:
        print("Running migration 002: Create messages table...")
        upgrade(conn)
        print("Migration completed successfully!")
