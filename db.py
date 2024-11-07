import sqlite3
from werkzeug.security import generate_password_hash

def connect_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect('users.db')
    return conn

def create_user_table():
    """Create the users table in the database if it does not already exist."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullName TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(full_name, password, email):
    """Insert a new user into the database."""
    hashed_password = generate_password_hash(password)
    conn = connect_db()
    cursor = conn.cursor()
    # Include all three parameters in the insert statement
    cursor.execute('INSERT INTO users (fullName, password, email) VALUES (?, ?, ?)', (full_name, hashed_password, email))
    conn.commit()
    conn.close()

def find_user(email):
    """Find a user by email."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

    
  
