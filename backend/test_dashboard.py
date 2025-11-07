import requests

response = requests.post(
    "http://localhost:8001/api/auth/login",
    data={"username": "admin@faithschool.rw", "password": "Admin2024"}
)
token = response.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}
dashboard_response = requests.get("http://localhost:8001/api/analytics/dashboard", headers=headers)
print(f"Dashboard: {dashboard_response.status_code}")
if dashboard_response.status_code == 200:
    import json
    print(json.dumps(dashboard_response.json(), indent=2))
else:
    print(f"Error: {dashboard_response.text}")
