import sqlite3
from typing import Optional, Dict, List

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
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS child_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            country_guideline TEXT NOT NULL DEFAULT 'WHO',
            gender TEXT,
            blood_group TEXT,
            allergies TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
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
    cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def authenticate_user(email: str, password: str) -> Optional[Dict]:
    user = get_user_by_email(email)
    if user and user['password'].strip() == password.strip():
        return user
    return None

def get_all_users() -> list:
    conn = get_user_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_child(name: str, date_of_birth: str, country_guideline: str, user_id: int,
              gender: Optional[str] = None, blood_group: Optional[str] = None, 
              allergies: Optional[str] = None) -> int:
    conn = get_user_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO child_profiles (user_id, name, date_of_birth, country_guideline, gender, blood_group, allergies)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, name, date_of_birth, country_guideline, gender, blood_group, allergies))
    child_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return child_id

def get_child(child_id: int) -> Optional[Dict]:
    conn = get_user_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM child_profiles WHERE id = ?", (child_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_children(user_id: Optional[int] = None) -> List[Dict]:
    conn = get_user_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT * FROM child_profiles WHERE user_id = ? ORDER BY name", (user_id,))
    else:
        cursor.execute("SELECT * FROM child_profiles ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_child(child_id: int, **kwargs) -> bool:
    conn = get_user_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    for key, value in kwargs.items():
        if key in ['name', 'date_of_birth', 'country_guideline', 'gender', 'blood_group', 'allergies']:
            fields.append(f"{key} = ?")
            values.append(value)
    if fields:
        fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(child_id)
        cursor.execute(f"UPDATE child_profiles SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
    conn.close()
    return True

def delete_child(child_id: int) -> bool:
    conn = get_user_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM child_profiles WHERE id = ?", (child_id,))
    conn.commit()
    conn.close()
    return True

init_user_database()
