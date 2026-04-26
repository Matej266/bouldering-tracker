from db import get_connection

def hardest_send():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT grades.label FROM climbs JOIN grades ON climbs.grade_id = grades.id WHERE sent = 1 ORDER BY grades.sort_order DESC LIMIT 1')
    label = cursor.fetchone()
    conn.close()
    return label['label'] if label else None

def sends_per_session():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT sessions.id, sessions.date, locations.name, COALESCE(SUM(climbs.sent), 0) AS sends FROM sessions JOIN locations ON sessions.location_id = locations.id LEFT JOIN climbs ON climbs.session_id = sessions.id GROUP BY sessions.id ORDER BY sessions.date DESC')
    data = cursor.fetchall()
    conn.close()
    return data

def attempts_by_grade():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT grades.label,SUM(climbs.tries) AS total_attempts, SUM(climbs.sent) AS total_sends FROM climbs JOIN grades ON climbs.grade_id = grades.id GROUP BY grades.id ORDER BY grades.sort_order')
    data = cursor.fetchall()
    conn.close()
    return data

def sends_per_grade():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT grades.label, SUM(climbs.sent) AS total_sends FROM climbs JOIN grades ON climbs.grade_id = grades.id GROUP BY grades.id ORDER BY grades.sort_order')
    data = cursor.fetchall()
    conn.close()
    return data

def total_climbs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) AS total_climbs FROM climbs WHERE sent = 1')
    total = cursor.fetchone()
    conn.close()
    return total['total_climbs']

def total_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) AS total_sessions FROM sessions')
    total = cursor.fetchone()
    conn.close()
    return total['total_sessions']

def progress_over_time():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT s.date, MAX(g.sort_order) AS best_sort_order, MAX(g.label) AS best_grade FROM sessions s JOIN climbs c ON s.id = c.session_id JOIN grades g ON c.grade_id = g.id WHERE c.sent =1 ORDER BY s.date')
    data = cursor.fetchall()
    conn.close()
    return data
