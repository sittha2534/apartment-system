import sqlite3

# เชื่อมต่อ (ถ้าไม่มีไฟล์ rooms.db มันจะสร้างให้)
conn = sqlite3.connect("rooms.db")
cursor = conn.cursor()

# สร้างตารางทั้งหมด
cursor.executescript("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    tenant_name TEXT,
    room_price REAL,
    water_rate REAL,
    electricity_rate REAL
);

CREATE TABLE IF NOT EXISTS room_meters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER,
    electricity_unit INTEGER,
    water_unit INTEGER,
    recorded_at DATE,
    FOREIGN KEY(room_id) REFERENCES rooms(id)
);

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    site_name TEXT,
    welcome_text TEXT,
    default_rooms TEXT
);

-- ค่า default settings
INSERT OR IGNORE INTO settings (id, site_name, welcome_text, default_rooms)
VALUES (1, 'Apartment System', 'ยินดีต้อนรับ', '');
""")

# เพิ่ม user เริ่มต้น (admin / 1234)
cursor.execute("""
INSERT OR IGNORE INTO users (username, password) 
VALUES (?, ?)
""", ("admin", "1234"))

conn.commit()
conn.close()

print("✅ สร้างฐานข้อมูล rooms.db พร้อม user admin/1234 สำเร็จ")
