import sqlite3

# เชื่อมต่อ database
conn = sqlite3.connect("rooms.db")
cursor = conn.cursor()

# กำหนด username และ password
username = "nim"
password = "140933"

# เพิ่ม user ใหม่ (ถ้า username ซ้ำจะไม่เพิ่ม)
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", (username, password))

conn.commit()
conn.close()

print(f"✅ User '{username}' ถูกสร้างเรียบร้อยแล้ว")
