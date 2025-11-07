import sqlite3
import os

db_path = 'faithschool.db'
if not os.path.exists(db_path):
    print("Database does not exist!")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute('SELECT email, role, is_active FROM users')
    users = cursor.fetchall()
    print(f"Found {len(users)} users in database:")
    for email, role, is_active in users:
        print(f"  {email} - {role} - Active: {is_active}")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()