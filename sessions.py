import os
from db import get_connection

DB_PATH = os.path.join(os.path.dirname(__file__), 'boulder.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def log_session(location_id, duration_min, feel, notes=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sessions (location_id, duration_min, feel, notes) VALUES (?, ?, ?, ?)',(location_id, duration_min, feel, notes))
    conn.commit()
    session_id = cursor.lastrowid
    conn.close()    
    return session_id

def get_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT s.id, l.name AS location_name,s.date, s.duration_min, s.feel, s.notes FROM sessions s JOIN locations l ON s.location_id = l.id ORDER BY s.id DESC')
    sessions = cursor.fetchall()
    conn.close()
    return sessions

def update_session(session_id, location_id, duration_min, feel, notes):
    conn = get_connection()
    conn.execute(
        "UPDATE sessions SET location_id=?, duration_min=?, feel=?, notes=? WHERE id=?",
        (location_id, duration_min, feel, notes, session_id)
    )
    conn.commit()
    conn.close()

def delete_session(session_id):
    conn = get_connection()
    conn.execute("DELETE FROM climbs WHERE session_id=?", (session_id,))
    conn.execute("DELETE FROM sessions WHERE id=?", (session_id,))
    conn.commit()
    conn.close()