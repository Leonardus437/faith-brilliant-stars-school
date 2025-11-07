from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Test login
response = client.post(
    "/api/auth/login",
    data={"username": "head@faithschool.rw", "password": "Head2024"}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# List all routes
print("\nRegistered routes:")
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"  {route.path}")
