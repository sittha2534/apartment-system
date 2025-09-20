from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")

# ใช้ environment variable สำหรับ DB ไฟล์
DB_FILE = os.environ.get("DB_FILE", "rooms.db")

# ------------------------------
# สร้างฐานข้อมูลและ user เริ่มต้น ถ้าไม่มี
# ------------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.executescript("""
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

    INSERT OR IGNORE INTO settings (id, site_name, welcome_text, default_rooms)
    VALUES (1, 'Apartment System', 'ยินดีต้อนรับ', '');

    INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '1234');
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized")

# ------------------------------
# ฟังก์ชันเชื่อมต่อ DB
# ------------------------------
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------------------
# สร้าง DB ถ้ายังไม่มี
# ------------------------------
if not os.path.exists(DB_FILE):
    init_db()

# ------------------------------
# Routes
# ------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            flash("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    rooms = [dict(r) for r in cursor.fetchall()]

    for room in rooms:
        cursor.execute(
            "SELECT electricity_unit, water_unit, recorded_at FROM room_meters WHERE room_id=? ORDER BY recorded_at DESC LIMIT 1",
            (room['id'],)
        )
        meter = cursor.fetchone()
        if meter:
            meter = dict(meter)
            room['electricity_unit'] = meter['electricity_unit']
            room['water_unit'] = meter['water_unit']
            room['recorded_at'] = meter['recorded_at'][:7] if meter['recorded_at'] else None
        else:
            room['electricity_unit'] = None
            room['water_unit'] = None
            room['recorded_at'] = None

    cursor.execute("SELECT * FROM settings WHERE id=1")
    config = cursor.fetchone()
    conn.close()

    default_rooms = []
    if config and config['default_rooms']:
        default_rooms = [r.strip() for r in config['default_rooms'].split(',') if r.strip()]

    return render_template('index.html', rooms=rooms, config=config, default_rooms=default_rooms)

@app.route('/update_meter/<int:room_id>', methods=['POST'])
def update_meter(room_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    electricity_unit = int(request.form.get('electricity_unit'))
    water_unit = int(request.form.get('water_unit'))
    recorded_month = request.form.get('recorded_month')  # YYYY-MM

    try:
        recorded_at = datetime.strptime(recorded_month + "-01", "%Y-%m-%d").date()
    except:
        flash("กรุณาเลือกเดือนให้ถูกต้อง", "danger")
        return redirect(url_for('home'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM room_meters 
        WHERE room_id = ? AND strftime('%Y-%m', recorded_at) = ?
    """, (room_id, recorded_month))
    exists = cursor.fetchone()

    if exists:
        flash("มีข้อมูลเดือนนี้แล้ว ไม่สามารถบันทึกซ้ำได้", "warning")
    else:
        cursor.execute(
            "INSERT INTO room_meters (room_id, electricity_unit, water_unit, recorded_at) VALUES (?, ?, ?, ?)",
            (room_id, electricity_unit, water_unit, recorded_at)
        )
        conn.commit()
        flash("บันทึกข้อมูลประจำเดือนสำเร็จ", "success")

    conn.close()
    return redirect(url_for('home'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'name' in request.form:
            # เพิ่มห้อง
            name = request.form['name']
            status = request.form['status']
            tenant_name = request.form.get('tenant_name', '')
            room_price = float(request.form.get('room_price', 0))
            water_rate = float(request.form.get('water_rate', 0))
            electricity_rate = float(request.form.get('electricity_rate', 0))

            cursor.execute("""
                INSERT INTO rooms (name, status, tenant_name, room_price, water_rate, electricity_rate)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, status, tenant_name, room_price, water_rate, electricity_rate))
            conn.commit()
            flash("เพิ่มห้องสำเร็จ", "success")
        else:
            # อัพเดต settings
            site_name = request.form['site_name']
            welcome_text = request.form['welcome_text']
            default_rooms = request.form.get('default_rooms', '')

            cursor.execute("""
                UPDATE settings SET site_name=?, welcome_text=?, default_rooms=? WHERE id=1
            """, (site_name, welcome_text, default_rooms))
            conn.commit()
            flash("บันทึกตั้งค่าสำเร็จ", "success")

        return redirect(url_for('settings'))

    cursor.execute("SELECT * FROM settings WHERE id=1")
    config = cursor.fetchone()
    cursor.execute("SELECT * FROM rooms")
    rooms = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return render_template('settings.html', config=config, rooms=rooms)

@app.route('/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM room_meters WHERE room_id=?", (room_id,))
    cursor.execute("DELETE FROM rooms WHERE id=?", (room_id,))
    conn.commit()
    conn.close()
    flash("ลบห้องเรียบร้อยแล้ว", "warning")
    return redirect(url_for('settings'))

@app.route('/receipt/<int:room_id>')
def print_receipt(room_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()

    row = cursor.execute("SELECT * FROM rooms WHERE id=?", (room_id,)).fetchone()
    room = dict(row) if row else None

    cursor.execute("""
        SELECT * FROM room_meters 
        WHERE room_id=? 
        ORDER BY recorded_at DESC 
        LIMIT 2
    """, (room_id,))
    meters = [dict(m) for m in cursor.fetchall()]

    latest = meters[0] if len(meters) >= 1 else None
    previous = meters[1] if len(meters) >= 2 else None

    if latest and latest['recorded_at']:
        latest['recorded_at'] = latest['recorded_at'][:7]
    if previous and previous['recorded_at']:
        previous['recorded_at'] = previous['recorded_at'][:7]

    conn.close()
    return render_template('receipt.html', room=room, latest=latest, previous=previous, now=datetime.now())

@app.route('/edit_latest_meter/<int:room_id>', methods=['POST'])
def edit_latest_meter(room_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        water_unit = int(request.form.get('water_unit'))
        electricity_unit = int(request.form.get('electricity_unit'))
        recorded_month = request.form.get('recorded_month')
        recorded_at = datetime.strptime(recorded_month + "-01", "%Y-%m-%d").date()
    except:
        flash("ข้อมูลไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง", "danger")
        return redirect(url_for('print_receipt', room_id=room_id))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM room_meters
        WHERE room_id = ?
        ORDER BY recorded_at DESC
        LIMIT 1
    """, (room_id,))
    row = cursor.fetchone()

    if row:
        meter_id = row['id']
        cursor.execute("""
            UPDATE room_meters 
            SET water_unit = ?, electricity_unit = ?, recorded_at = ?
            WHERE id = ?
        """, (water_unit, electricity_unit, recorded_at, meter_id))
        conn.commit()
        flash("แก้ไขหน่วยล่าสุดสำเร็จ", "success")
    else:
        flash("ไม่พบข้อมูลหน่วยล่าสุดที่จะแก้ไข", "danger")

    conn.close()
    return redirect(url_for('print_receipt', room_id=room_id))

@app.route('/test_db')
def test_db():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        return f"✅ Database Connected!<br>Tables: {tables}<br>Users: {users}"
    except Exception as e:
        return f"❌ Cannot connect to DB: {e}"

# ------------------------------
# Run
# ------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
