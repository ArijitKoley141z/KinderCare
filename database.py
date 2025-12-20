import sqlite3
import os
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import json

DATABASE_PATH = "vaccination_health.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            country_guideline TEXT NOT NULL DEFAULT 'WHO',
            gender TEXT,
            blood_group TEXT,
            allergies TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vaccinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL,
            vaccine_name TEXT NOT NULL,
            vaccine_code TEXT,
            due_date DATE NOT NULL,
            administered_date DATE,
            status TEXT DEFAULT 'pending',
            notes TEXT,
            administered_by TEXT,
            batch_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            event_date DATE NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            severity TEXT,
            symptoms TEXT,
            treatment TEXT,
            doctor_name TEXT,
            hospital_clinic TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminder_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL,
            email_enabled INTEGER DEFAULT 0,
            email_address TEXT,
            sms_enabled INTEGER DEFAULT 0,
            phone_number TEXT,
            reminder_7_days INTEGER DEFAULT 1,
            reminder_1_day INTEGER DEFAULT 1,
            reminder_on_day INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sent_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vaccination_id INTEGER NOT NULL,
            reminder_type TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            channel TEXT NOT NULL,
            FOREIGN KEY (vaccination_id) REFERENCES vaccinations(id) ON DELETE CASCADE
        )
    """)
    
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

def add_child(name: str, date_of_birth: str, country_guideline: str, 
              gender: Optional[str] = None, blood_group: Optional[str] = None, 
              allergies: Optional[str] = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO children (name, date_of_birth, country_guideline, gender, blood_group, allergies)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, date_of_birth, country_guideline, gender, blood_group, allergies))
    child_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return child_id

def get_child(child_id: int) -> Optional[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM children WHERE id = ?", (child_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_children() -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM children ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_child(child_id: int, **kwargs) -> bool:
    conn = get_connection()
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
        cursor.execute(f"UPDATE children SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
    conn.close()
    return True

def delete_child(child_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM children WHERE id = ?", (child_id,))
    conn.commit()
    conn.close()
    return True

def add_vaccination(child_id: int, vaccine_name: str, vaccine_code: str, 
                   due_date: str, status: str = 'pending') -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vaccinations (child_id, vaccine_name, vaccine_code, due_date, status)
        VALUES (?, ?, ?, ?, ?)
    """, (child_id, vaccine_name, vaccine_code, due_date, status))
    vacc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return vacc_id

def get_vaccinations(child_id: int) -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM vaccinations WHERE child_id = ? ORDER BY due_date
    """, (child_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_vaccination_status(vacc_id: int, status: str, 
                               administered_date: Optional[str] = None,
                               notes: Optional[str] = None,
                               administered_by: Optional[str] = None,
                               batch_number: Optional[str] = None) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE vaccinations 
        SET status = ?, administered_date = ?, notes = ?, 
            administered_by = ?, batch_number = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, administered_date, notes, administered_by, batch_number, vacc_id))
    conn.commit()
    conn.close()
    return True

def delete_all_vaccinations(child_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vaccinations WHERE child_id = ?", (child_id,))
    conn.commit()
    conn.close()
    return True

def add_health_event(child_id: int, event_type: str, event_date: str, 
                     title: str, description: Optional[str] = None,
                     severity: Optional[str] = None, symptoms: Optional[str] = None,
                     treatment: Optional[str] = None, doctor_name: Optional[str] = None,
                     hospital_clinic: Optional[str] = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO health_events (child_id, event_type, event_date, title, 
                                   description, severity, symptoms, treatment,
                                   doctor_name, hospital_clinic)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (child_id, event_type, event_date, title, description, 
          severity, symptoms, treatment, doctor_name, hospital_clinic))
    event_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return event_id

def get_health_events(child_id: int, event_type: Optional[str] = None) -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    if event_type:
        cursor.execute("""
            SELECT * FROM health_events 
            WHERE child_id = ? AND event_type = ?
            ORDER BY event_date DESC
        """, (child_id, event_type))
    else:
        cursor.execute("""
            SELECT * FROM health_events 
            WHERE child_id = ? 
            ORDER BY event_date DESC
        """, (child_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_health_event(event_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM health_events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
    return True

def get_reminder_settings(child_id: int) -> Optional[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reminder_settings WHERE child_id = ?", (child_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def save_reminder_settings(child_id: int, email_enabled: bool, email_address: str,
                           sms_enabled: bool, phone_number: str,
                           reminder_7_days: bool, reminder_1_day: bool,
                           reminder_on_day: bool) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    existing = get_reminder_settings(child_id)
    if existing:
        cursor.execute("""
            UPDATE reminder_settings 
            SET email_enabled = ?, email_address = ?, sms_enabled = ?, phone_number = ?,
                reminder_7_days = ?, reminder_1_day = ?, reminder_on_day = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE child_id = ?
        """, (int(email_enabled), email_address, int(sms_enabled), phone_number,
              int(reminder_7_days), int(reminder_1_day), int(reminder_on_day), child_id))
    else:
        cursor.execute("""
            INSERT INTO reminder_settings (child_id, email_enabled, email_address, 
                                           sms_enabled, phone_number, reminder_7_days,
                                           reminder_1_day, reminder_on_day)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (child_id, int(email_enabled), email_address, int(sms_enabled), phone_number,
              int(reminder_7_days), int(reminder_1_day), int(reminder_on_day)))
    conn.commit()
    conn.close()
    return True

def record_sent_reminder(vaccination_id: int, reminder_type: str, channel: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sent_reminders (vaccination_id, reminder_type, channel)
        VALUES (?, ?, ?)
    """, (vaccination_id, reminder_type, channel))
    reminder_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return reminder_id

def get_sent_reminders(vaccination_id: int) -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM sent_reminders WHERE vaccination_id = ?
    """, (vaccination_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def register_user(name: str, email: str, password: str) -> bool:
    conn = get_connection()
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
    conn = get_connection()
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

init_database()
