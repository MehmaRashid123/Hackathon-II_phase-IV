"""
Test script for user registration endpoint.

Tests the POST /api/auth/signup endpoint with various scenarios.
"""

import requests
import json
from datetime import datetime


BASE_URL = "http://localhost:8000"


def test_successful_registration():
    """Test successful user registration."""
    print("\n🧪 Test 1: Successful Registration")
    print("=" * 50)

    # Generate unique email using timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    test_email = f"testuser_{timestamp}@example.com"

    payload = {
        "email": test_email,
        "password": "SecurePassword123"
    }

    response = requests.post(f"{BASE_URL}/api/auth/signup", json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 201:
        print("✅ PASS: User registered successfully")
        return response.json()
    else:
        print("❌ FAIL: Registration failed")
        return None


def test_duplicate_email(email):
    """Test duplicate email registration (should fail)."""
    print("\n🧪 Test 2: Duplicate Email Registration")
    print("=" * 50)

    payload = {
        "email": email,
        "password": "AnotherPassword456"
    }

    response = requests.post(f"{BASE_URL}/api/auth/signup", json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 400:
        print("✅ PASS: Duplicate email correctly rejected")
    else:
        print("❌ FAIL: Duplicate email should return 400")


def test_weak_password():
    """Test weak password (should fail validation)."""
    print("\n🧪 Test 3: Weak Password Validation")
    print("=" * 50)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    test_email = f"weakpass_{timestamp}@example.com"

    payload = {
        "email": test_email,
        "password": "weak"  # Too short, no number
    }

    response = requests.post(f"{BASE_URL}/api/auth/signup", json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 422:
        print("✅ PASS: Weak password correctly rejected")
    else:
        print("❌ FAIL: Weak password should return 422")


def test_invalid_email():
    """Test invalid email format (should fail validation)."""
    print("\n🧪 Test 4: Invalid Email Format")
    print("=" * 50)

    payload = {
        "email": "not-an-email",
        "password": "SecurePassword123"
    }

    response = requests.post(f"{BASE_URL}/api/auth/signup", json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 422:
        print("✅ PASS: Invalid email correctly rejected")
    else:
        print("❌ FAIL: Invalid email should return 422")


def main():
    """Run all registration tests."""
    print("\n" + "=" * 50)
    print("🚀 User Registration Endpoint Tests")
    print("=" * 50)
    print(f"Testing API at: {BASE_URL}")
    print("Make sure the FastAPI server is running!")
    print("=" * 50)

    try:
        # Test 1: Successful registration
        user = test_successful_registration()

        if user:
            # Test 2: Duplicate email
            test_duplicate_email(user["email"])

        # Test 3: Weak password
        test_weak_password()

        # Test 4: Invalid email
        test_invalid_email()

        print("\n" + "=" * 50)
        print("✅ All tests completed!")
        print("=" * 50)

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to FastAPI server")
        print("Please start the server with: uvicorn src.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    main()
