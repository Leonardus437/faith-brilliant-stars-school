import sqlite3

conn = sqlite3.connect('faithschool.db')
cursor = conn.cursor()

# Check current roles
cursor.execute("SELECT email, role FROM users")
users = cursor.fetchall()
print("Current user roles:")
for email, role in users:
    print(f"  {email}: {role}")

# Update roles to match enum values
role_mapping = {
    'head_teacher': 'HEAD_TEACHER',
    'teacher': 'TEACHER', 
    'accountant': 'ACCOUNTANT',
    'parent': 'PARENT',
    'student': 'STUDENT'
}

for old_role, new_role in role_mapping.items():
    cursor.execute("UPDATE users SET role = ? WHERE role = ?", (new_role, old_role))
    print(f"Updated {old_role} -> {new_role}")

conn.commit()

# Verify changes
cursor.execute("SELECT email, role FROM users")
users = cursor.fetchall()
print("\nUpdated user roles:")
for email, role in users:
    print(f"  {email}: {role}")

conn.close()
print("Role fix completed")