import requests
import json

url = "http://localhost:8000/api/auth/signup"
data = {
    "email": "test_cors@example.com",
    "password": "Test1234"
}

# Test OPTIONS request (CORS preflight)
print("Testing OPTIONS request (CORS preflight)...")
try:
    options_response = requests.options(url, headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type"
    })
    print(f"OPTIONS Status: {options_response.status_code}")
    print(f"OPTIONS Headers: {dict(options_response.headers)}")
except Exception as e:
    print(f"OPTIONS Error: {e}")

print("\nTesting POST request...")
try:
    response = requests.post(url, json=data, headers={
        "Origin": "http://localhost:3000"
    })
    print(f"POST Status Code: {response.status_code}")
    print(f"POST Response: {response.text}")
    print(f"POST Headers: {dict(response.headers)}")
except Exception as e:
    print(f"POST Error: {e}")
