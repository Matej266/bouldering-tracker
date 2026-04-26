from db import get_connection

def get_locations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM locations')
    locations = cursor.fetchall()
    conn.close()
    return locations
