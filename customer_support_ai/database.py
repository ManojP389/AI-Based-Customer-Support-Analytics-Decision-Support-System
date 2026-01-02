import sqlite3

def connect():
    return sqlite3.connect("support.db")

def create_tables():
    conn = connect()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        sentiment TEXT,
        issue TEXT,
        urgency TEXT,
        date TEXT
    )
    """)
    conn.commit()
    conn.close()
