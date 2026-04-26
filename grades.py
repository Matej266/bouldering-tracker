from db import get_connection

def get_grades():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM grades')
    grades = cursor.fetchall()
    conn.close()
    return grades
