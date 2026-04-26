import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'boulder.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with open(SCHEMA_PATH, 'r') as f:
        schema = f.read()
    conn = get_connection()
    conn.executescript(schema)
    conn.close()
    print('Database initialized.')
    
def seed_grades():
    grades = [
    ("5",0),
    ("6A",   1),
    ("6A+",  2),
    ("6B",   3),
    ("6B+",  4),
    ("6C",   5),
    ("6C+",  6),
    ("7A",   7),
    ("7A+",  8),
    ("7B",   9),
    ("7B+",  10),
    ("7C",   11),
    ("7C+",  12),
    ("8A",   13),
    ("8A+",  14),
    ("8B",   15),
    ("8B+",  16),
    ("8C",   17),
    ("8C+",  18),
    ("9A",   19),
    ("9A+",  20),
    ("9B",   21),
    ("9B+",  22),
    ("9C",   23),
    ("9C+",  24)]
    conn = get_connection()
    conn.executemany('INSERT OR IGNORE INTO grades (label, sort_order) VALUES (?, ?)', grades)
    conn.commit()
    conn.close()
    print('Grades seeded.')
    
def seed_locations():
    locations = [('Raca',),('Petrzalka',),('Prague',)]
    conn = get_connection()
    conn.executemany('INSERT OR IGNORE INTO locations (name) VALUES (?)', locations)
    conn.commit()
    conn.close()
    print('Locations seeded.')




if __name__ == '__main__':
    init_db()
    seed_grades()
    seed_locations()