import requests
import json

# Test login endpoint directly
url = "http://localhost:8001/api/auth/login"
credentials = [
    {"username": "head@faithschool.rw", "password": "Head2024"},
    {"username": "teacher@faithschool.rw", "password": "Teacher2024"},
    {"username": "accounts@faithschool.rw", "password": "Accounts2024"},
    {"username": "parent@faithschool.rw", "password": "Parent2024"}
]

for cred in credentials:
    try:
        response = requests.post(url, data=cred)
        print(f"\nTesting {cred['username']}:")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS: Login successful!")
            data = response.json()
            print(f"User: {data['user']['full_name']} ({data['user']['role']})")
        else:
            print(f"FAILED: Login failed: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"ERROR: Cannot connect to backend server at {url}")
        print("Make sure the backend is running on port 8001")
        break
    except Exception as e:
        print(f"ERROR: {e}")