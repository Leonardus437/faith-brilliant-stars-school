import sqlite3
import bcrypt

conn = sqlite3.connect('faithschool.db')
cursor = conn.cursor()

# Test user exists
user = cursor.execute('SELECT email, hashed_password, role FROM users WHERE email = ?', ('head@faithschool.rw',)).fetchone()
if user:
    email, hashed_pw, role = user
    print(f"User found: {email} ({role})")
    
    # Test password
    test_password = 'Head2024'
    is_valid = bcrypt.checkpw(test_password.encode(), hashed_pw.encode())
    print(f"Password test: {'PASS' if is_valid else 'FAIL'}")
    
    if is_valid:
        print("\nCredentials are correct!")
        print(f"Email: {email}")
        print(f"Password: {test_password}")
else:
    print("User not found!")

conn.close()
