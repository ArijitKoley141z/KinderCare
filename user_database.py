import sqlite3
from typing import Optional, Dict

USER_DATABASE_PATH = "user_database.db"

def get_user_connection():
    conn = sqlite3.connect(USER_DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_user_database():
    conn = get_user_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def register_user(name: str, email: str, password: str) -> bool:
    conn = get_user_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        """, (name, email, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def get_user_by_email(email: str) -> Optional[Dict]:
    conn = get_user_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def authenticate_user(email: str, password: str) -> Optional[Dict]:
    user = get_user_by_email(email)
    if user and user['password'] == password:
        return user
    return None

def get_all_users() -> list:
    conn = get_user_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

init_user_database()
