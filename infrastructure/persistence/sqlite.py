import sqlite3

def get_connection():
    conn = sqlite3.connect("data.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mercadolivre (
            id TEXT PRIMARY KEY,
            affiliate_link TEXT NOT NULL
        )
    """)
    return conn
