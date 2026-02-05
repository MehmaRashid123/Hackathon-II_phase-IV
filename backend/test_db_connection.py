"""
Test script to verify database connection and users table.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from sqlmodel import Session, select
from src.database import engine
from src.models.user import User

# Load environment
load_dotenv()

def test_database_connection():
    """Test database connection and verify users table exists."""
    print("🔍 Testing database connection...")

    try:
        # Create a session
        with Session(engine) as session:
            # Try to query the users table (should return empty list)
            statement = select(User)
            results = session.exec(statement).all()

            print(f"✅ Database connection successful!")
            print(f"✅ Users table exists and is accessible")
            print(f"📊 Current user count: {len(results)}")

            if len(results) == 0:
                print("ℹ️  No users in database yet (expected for fresh install)")
            else:
                print(f"ℹ️  Found {len(results)} existing user(s)")
                for user in results:
                    print(f"   - {user.email} (ID: {user.id})")

            return True

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
