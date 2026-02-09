"""
Migration runner script

Executes all database migrations in order.
Run this script to set up or update the database schema.

Usage:
    python run_migrations.py
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.database import engine
from migrations.versions import (
    _001_create_conversations_table as migration_001,
    _002_create_messages_table as migration_002,
    _003_create_tasks_table as migration_003,
)


def run_all_migrations():
    """Run all migrations in order."""
    migrations = [
        ("001", "Create conversations table", migration_001),
        ("002", "Create messages table", migration_002),
        ("003", "Create tasks table", migration_003),
    ]
    
    print("=" * 60)
    print("Running Database Migrations")
    print("=" * 60)
    
    with engine.connect() as conn:
        for revision, description, migration in migrations:
            print(f"\n[{revision}] {description}")
            print("-" * 60)
            try:
                migration.upgrade(conn)
                print(f"✓ Migration {revision} completed successfully")
            except Exception as e:
                print(f"✗ Migration {revision} failed: {e}")
                raise
    
    print("\n" + "=" * 60)
    print("All migrations completed successfully!")
    print("=" * 60)


def rollback_all_migrations():
    """Rollback all migrations in reverse order."""
    migrations = [
        ("003", "Create tasks table", migration_003),
        ("002", "Create messages table", migration_002),
        ("001", "Create conversations table", migration_001),
    ]
    
    print("=" * 60)
    print("Rolling Back Database Migrations")
    print("=" * 60)
    
    with engine.connect() as conn:
        for revision, description, migration in migrations:
            print(f"\n[{revision}] {description}")
            print("-" * 60)
            try:
                migration.downgrade(conn)
                print(f"✓ Migration {revision} rolled back successfully")
            except Exception as e:
                print(f"✗ Migration {revision} rollback failed: {e}")
                # Continue with other rollbacks
    
    print("\n" + "=" * 60)
    print("All migrations rolled back!")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database migration runner")
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Rollback all migrations instead of applying them"
    )
    
    args = parser.parse_args()
    
    if args.rollback:
        rollback_all_migrations()
    else:
        run_all_migrations()
