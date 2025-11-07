import requests

# Test the minimal login endpoint
url = "http://localhost:8002/test-login"
credentials = {"username": "head@faithschool.rw", "password": "Head2024"}

try:
    response = requests.post(url, data=credentials)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("SUCCESS: Login working!")
        data = response.json()
        print(f"User: {data['user']['full_name']} ({data['user']['role']})")
    else:
        print(f"FAILED: {response.text}")
except Exception as e:
    print(f"ERROR: {e}")