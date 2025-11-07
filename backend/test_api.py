import requests

# Login
response = requests.post(
    "http://localhost:8001/api/auth/login",
    data={"username": "admin@faithschool.rw", "password": "Admin2024"}
)
print("Login:", response.status_code)
if response.status_code == 200:
    token = response.json()["access_token"]
    print("Token received")
    
    # Get students
    headers = {"Authorization": f"Bearer {token}"}
    students_response = requests.get("http://localhost:8001/api/students/", headers=headers)
    print(f"Students: {students_response.status_code}")
    if students_response.status_code == 200:
        students = students_response.json()
        print(f"Found {len(students)} students")
        if students:
            print(f"First student: {students[0]}")
    else:
        print(f"Error: {students_response.text}")
else:
    print(f"Login failed: {response.text}")
