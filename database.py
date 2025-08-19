import sqlite3

DB_NAME = "fitness.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                client_name TEXT,
                client_chat_id INTEGER
            )
        """)
        conn.commit()

def add_booking(date, time, client_name, chat_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO schedule (date, time, client_name, client_chat_id)
            VALUES (?, ?, ?, ?)
        """, (date, time, client_name, chat_id))
        conn.commit()

def get_bookings():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schedule")
        return cursor.fetchall()

def delete_booking(date, time):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM schedule WHERE date = ? AND time = ?", (date, time))
        conn.commit()

def get_booking_by_datetime(date, time):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schedule WHERE date = ? AND time = ?", (date, time))
        return cursor.fetchone()
