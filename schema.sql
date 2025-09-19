CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
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

-- ค่า default สำหรับ settings
INSERT OR IGNORE INTO settings (id, site_name, welcome_text, default_rooms)
VALUES (1, 'Apartment System', 'ยินดีต้อนรับ', '');
