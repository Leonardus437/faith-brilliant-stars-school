import sqlite3

conn = sqlite3.connect('faithschool.db')
cursor = conn.cursor()

# Get current table schema
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
print("Current columns:")
for col in columns:
    print(f"  {col[1]} - {col[2]}")

existing_columns = [col[1] for col in columns]

# Add missing columns
if 'photo_url' not in existing_columns:
    cursor.execute('ALTER TABLE users ADD COLUMN photo_url TEXT')
    print("Added photo_url column")

if 'language_preference' not in existing_columns:
    cursor.execute('ALTER TABLE users ADD COLUMN language_preference TEXT DEFAULT "en"')
    print("Added language_preference column")
else:
    # Update existing rows to have default value
    cursor.execute('UPDATE users SET language_preference = "en" WHERE language_preference IS NULL')
    print("Updated language_preference default values")

conn.commit()
conn.close()
print("Schema fix completed")