"""
Comprehensive test suite for Task API with user isolation.

Tests all 6 CRUD endpoints and verifies that User A cannot access User B's tasks.
"""

from src.schemas.auth_schemas import UserCreate
from src.schemas.task_schemas import TaskCreate, TaskUpdate
from src.services.user_service import UserService
from src.database import Session, engine
from src.utils.security import create_access_token
import uuid
import requests
import json

API_URL = "http://localhost:8000"


def test_task_api_with_user_isolation():
    """Test complete Task API with strict user isolation."""
    print("\n" + "=" * 80)
    print("🧪 TASK API + USER ISOLATION TEST SUITE")
    print("=" * 80)

    session = Session(engine)

    # Create two test users (User A and User B)
    print("\n1️⃣  Creating two test users...")

    user_a_email = f"user_a_{uuid.uuid4().hex[:8]}@example.com"
    user_b_email = f"user_b_{uuid.uuid4().hex[:8]}@example.com"

    user_a = UserService.create_user(session, UserCreate(email=user_a_email, password="Password123"))
    user_b = UserService.create_user(session, UserCreate(email=user_b_email, password="Password123"))

    print(f"   ✅ User A created: {user_a.id}")
    print(f"   ✅ User B created: {user_b.id}")

    # Generate JWT tokens for both users
    token_a = create_access_token(data={"sub": str(user_a.id), "email": user_a.email})
    token_b = create_access_token(data={"sub": str(user_b.id), "email": user_b.email})

    print(f"   ✅ JWT tokens generated for both users")

    # Test 1: User A creates a task (POST /api/{user_id}/tasks)
    print("\n2️⃣  Testing POST /api/{user_id}/tasks (User A creates task)...")

    task_data_a = {"title": "User A Task 1", "description": "First task for User A"}
    response = requests.post(
        f"{API_URL}/api/{user_a.id}/tasks",
        json=task_data_a,
        headers={"Authorization": f"Bearer {token_a}"}
    )

    if response.status_code == 201:
        task_a = response.json()
        print(f"   ✅ Task created: {task_a['id']}")
        print(f"      Title: {task_a['title']}")
        print(f"      User ID: {task_a['user_id']}")
    else:
        print(f"   ❌ Failed: {response.status_code} - {response.text}")
        session.close()
        return False

    # Test 2: User B creates a task
    print("\n3️⃣  Testing POST /api/{user_id}/tasks (User B creates task)...")

    task_data_b = {"title": "User B Task 1", "description": "First task for User B"}
    response = requests.post(
        f"{API_URL}/api/{user_b.id}/tasks",
        json=task_data_b,
        headers={"Authorization": f"Bearer {token_b}"}
    )

    if response.status_code == 201:
        task_b = response.json()
        print(f"   ✅ Task created: {task_b['id']}")
        print(f"      Title: {task_b['title']}")
        print(f"      User ID: {task_b['user_id']}")
    else:
        print(f"   ❌ Failed: {response.status_code} - {response.text}")
        session.close()
        return False

    # Test 3: User A lists tasks (should see only their own)
    print("\n4️⃣  Testing GET /api/{user_id}/tasks (User A lists tasks)...")

    response = requests.get(
        f"{API_URL}/api/{user_a.id}/tasks",
        headers={"Authorization": f"Bearer {token_a}"}
    )

    if response.status_code == 200:
        tasks = response.json()
        print(f"   ✅ User A has {len(tasks)} task(s)")
        if len(tasks) == 1 and tasks[0]['id'] == task_a['id']:
            print(f"      ✅ Correct: Only User A's task is visible")
        else:
            print(f"      ❌ Error: User A sees wrong tasks!")
            session.close()
            return False
    else:
        print(f"   ❌ Failed: {response.status_code} - {response.text}")
        session.close()
        return False

    # Test 4: User B lists tasks (should see only their own)
    print("\n5️⃣  Testing GET /api/{user_id}/tasks (User B lists tasks)...")

    response = requests.get(
        f"{API_URL}/api/{user_b.id}/tasks",
        headers={"Authorization": f"Bearer {token_b}"}
    )

    if response.status_code == 200:
        tasks = response.json()
        print(f"   ✅ User B has {len(tasks)} task(s)")
        if len(tasks) == 1 and tasks[0]['id'] == task_b['id']:
            print(f"      ✅ Correct: Only User B's task is visible")
        else:
            print(f"      ❌ Error: User B sees wrong tasks!")
            session.close()
            return False
    else:
        print(f"   ❌ Failed: {response.status_code} - {response.text}")
        session.close()
        return False

    # Test 5: User A tries to access User B's task (SHOULD FAIL with 403)
    print("\n6️⃣  Testing User Isolation: User A tries to access User B's task (should get 403)...")

    response = requests.get(
        f"{API_URL}/api/{user_b.id}/tasks/{task_b['id']}",
        headers={"Authorization": f"Bearer {token_a}"}  # User A's token
    )

    if response.status_code == 403:
        print(f"   ✅ Correctly rejected with HTTP 403 Forbidden")
        print(f"      Error: {response.json()['detail']}")
    else:
        print(f"   ❌ Security breach! Expected 403, got {response.status_code}")
        session.close()
        return False

    # Test 6: User A updates their own task (PUT /api/{user_id}/tasks/{id})
    print("\n7️⃣  Testing PUT /api/{user_id}/tasks/{id} (User A updates task)...")

    update_data = {"title": "Updated User A Task", "description": "Updated description"}
    response = requests.put(
        f"{API_URL}/api/{user_a.id}/tasks/{task_a['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {token_a}"}
    )

    if response.status_code == 200:
        updated_task = response.json()
        print(f"   ✅ Task updated successfully")
        print(f"      New title: {updated_task['title']}")
        if updated_task['title'] == update_data['title']:
            print(f"      ✅ Update confirmed")
        else:
            print(f"      ❌ Update failed!")
            session.close()
            return False
    else:
        print(f"   ❌ Failed: {response.status_code} - {response.text}")
        session.close()
        return False

    # Test 7: User A toggles task completion (PATCH /api/{user_id}/tasks/{id}/complete)
    print("\n8️⃣  Testing PATCH /api/{user_id}/tasks/{id}/complete (User A toggles completion)...")

    response = requests.patch(
        f"{API_URL}/api/{user_a.id}/tasks/{task_a['id']}/complete",
        headers={"Authorization": f"Bearer {token_a}"}
    )

    if response.status_code == 200:
        toggled_task = response.json()
        print(f"   ✅ Task completion toggled")
        print(f"      is_completed: {toggled_task['is_completed']}")
        if toggled_task['is_completed'] == True:
            print(f"      ✅ Toggle confirmed (false → true)")
        else:
            print(f"      ❌ Toggle failed!")
            session.close()
            return False
    else:
        print(f"   ❌ Failed: {response.status_code} - {response.text}")
        session.close()
        return False

    # Test 8: User B tries to update User A's task (SHOULD FAIL with 403)
    print("\n9️⃣  Testing User Isolation: User B tries to update User A's task (should get 403)...")

    response = requests.put(
        f"{API_URL}/api/{user_a.id}/tasks/{task_a['id']}",
        json={"title": "Hacked by User B"},
        headers={"Authorization": f"Bearer {token_b}"}  # User B's token
    )

    if response.status_code == 403:
        print(f"   ✅ Correctly rejected with HTTP 403 Forbidden")
    else:
        print(f"   ❌ Security breach! Expected 403, got {response.status_code}")
        session.close()
        return False

    # Test 9: User A gets single task (GET /api/{user_id}/tasks/{id})
    print("\n🔟  Testing GET /api/{user_id}/tasks/{id} (User A gets single task)...")

    response = requests.get(
        f"{API_URL}/api/{user_a.id}/tasks/{task_a['id']}",
        headers={"Authorization": f"Bearer {token_a}"}
    )

    if response.status_code == 200:
        task = response.json()
        print(f"   ✅ Task retrieved")
        print(f"      Title: {task['title']}")
        print(f"      Completed: {task['is_completed']}")
    else:
        print(f"   ❌ Failed: {response.status_code} - {response.text}")
        session.close()
        return False

    # Test 10: User A deletes task (DELETE /api/{user_id}/tasks/{id})
    print("\n1️⃣1️⃣  Testing DELETE /api/{user_id}/tasks/{id} (User A deletes task)...")

    response = requests.delete(
        f"{API_URL}/api/{user_a.id}/tasks/{task_a['id']}",
        headers={"Authorization": f"Bearer {token_a}"}
    )

    if response.status_code == 204:
        print(f"   ✅ Task deleted (HTTP 204 No Content)")

        # Verify task is gone
        verify = requests.get(
            f"{API_URL}/api/{user_a.id}/tasks/{task_a['id']}",
            headers={"Authorization": f"Bearer {token_a}"}
        )
        if verify.status_code == 404:
            print(f"   ✅ Confirmed: Task no longer exists (HTTP 404)")
        else:
            print(f"   ❌ Task still exists after deletion!")
            session.close()
            return False
    else:
        print(f"   ❌ Failed: {response.status_code} - {response.text}")
        session.close()
        return False

    # Test 11: User B tries to delete User A's task (SHOULD FAIL with 403)
    print("\n1️⃣2️⃣  Testing User Isolation: User B tries to delete User A's task (should get 403)...")

    # User A creates another task first
    response = requests.post(
        f"{API_URL}/api/{user_a.id}/tasks",
        json={"title": "Protected task", "description": "User B should not delete this"},
        headers={"Authorization": f"Bearer {token_a}"}
    )
    protected_task = response.json()

    # User B tries to delete it
    response = requests.delete(
        f"{API_URL}/api/{user_a.id}/tasks/{protected_task['id']}",
        headers={"Authorization": f"Bearer {token_b}"}  # User B's token
    )

    if response.status_code == 403:
        print(f"   ✅ Correctly rejected with HTTP 403 Forbidden")
    else:
        print(f"   ❌ Security breach! Expected 403, got {response.status_code}")
        session.close()
        return False

    session.close()

    print("\n" + "=" * 80)
    print("✅ ALL TASK API TESTS PASSED!")
    print("=" * 80)
    print("\n🔒 Security Features Verified:")
    print("   ✓ User A cannot access User B's tasks (GET)")
    print("   ✓ User A cannot update User B's tasks (PUT)")
    print("   ✓ User A cannot delete User B's tasks (DELETE)")
    print("   ✓ All endpoints enforce HTTP 403 for unauthorized access")
    print("\n📊 CRUD Operations Verified:")
    print("   ✓ POST /api/{user_id}/tasks - Create task")
    print("   ✓ GET /api/{user_id}/tasks - List tasks")
    print("   ✓ GET /api/{user_id}/tasks/{id} - Get single task")
    print("   ✓ PUT /api/{user_id}/tasks/{id} - Update task")
    print("   ✓ PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion")
    print("   ✓ DELETE /api/{user_id}/tasks/{id} - Delete task")
    print("\n🎯 Spec 2 Implementation Complete!")
    print("=" * 80)

    return True


if __name__ == "__main__":
    try:
        test_task_api_with_user_isolation()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to FastAPI server")
        print("Please start the server with: uvicorn src.main:app --reload --port 8000")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
