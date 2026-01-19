import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db():#connection to the DB

    return sqlite3.connect(os.path.join(BASE_DIR,"issues.db"))



def init_db():#creats the issues table
    conn = get_db()
    cur = conn.cursor()

  
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()



def init_users():#creats the users table for authentication
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


