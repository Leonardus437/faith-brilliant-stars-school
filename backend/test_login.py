import requests

url = "http://localhost:8001/api/auth/login"
data = {
    "username": "head@faithschool.rw",
    "password": "Head2024"
}

try:
    response = requests.post(url, data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
    print("Make sure backend is running on port 8001")
