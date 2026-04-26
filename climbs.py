from db import get_connection

def log_climb(session_id, grade_id,tries, sent, notes=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO climbs (session_id, grade_id, tries, sent, notes) VALUES(?, ?, ?, ?, ?)',(session_id, grade_id, tries, sent, notes))
    conn.commit()
    climb_id = cursor.lastrowid
    conn.close()
    return climb_id

def get_climbs(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT c.id, g.label AS grade_label, c.sent, c.tries, c.notes FROM climbs c JOIN grades g ON c.grade_id = g.id WHERE c.session_id = ? ORDER BY g.sort_order',(session_id,))
    climbs = cursor.fetchall()
    conn.close()
    return climbs

