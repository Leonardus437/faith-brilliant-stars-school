import sqlite3
import bcrypt

conn = sqlite3.connect('faithschool.db')
cursor = conn.cursor()

# Generate proper password hashes
passwords = {
    'head@faithschool.rw': 'Head2024',
    'teacher@faithschool.rw': 'Teacher2024',
    'accounts@faithschool.rw': 'Accounts2024',
    'parent@faithschool.rw': 'Parent2024'
}

for email, password in passwords.items():
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cursor.execute("UPDATE users SET hashed_password = ? WHERE email = ?", (hashed, email))
    print(f"Updated password for {email}")

conn.commit()
conn.close()
print("All passwords updated successfully!")
