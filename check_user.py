import sqlite3

conn = sqlite3.connect("rooms.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

conn.close()

print("Users in DB:")
for u in users:
    print(u)
