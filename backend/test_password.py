from app.core.security import get_password_hash, verify_password
import sqlite3

# Test password hashing
test_password = "Head2024"
hashed = get_password_hash(test_password)
print(f"Original: {test_password}")
print(f"Hashed: {hashed}")
print(f"Verification: {verify_password(test_password, hashed)}")

# Check what's actually in the database
conn = sqlite3.connect('faithschool.db')
cursor = conn.cursor()
cursor.execute('SELECT email, hashed_password FROM users WHERE email = ?', ('head@faithschool.rw',))
result = cursor.fetchone()
if result:
    email, db_hash = result
    print(f"\nDatabase hash for {email}: {db_hash}")
    print(f"Verification against DB hash: {verify_password(test_password, db_hash)}")
else:
    print("User not found in database")
conn.close()