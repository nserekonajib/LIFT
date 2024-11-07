# financedata.py
from flask import *
import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect('users.db')

def create_finance_table():
    """Create the finance table if it doesn't exist, linking it to the users table via user_id."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS finance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('deposit', 'withdraw')),  -- Ensure only valid types
        status TEXT NOT NULL,
        subscription_plan TEXT,  -- New column for subscription plan
        required_amount REAL,     -- New column for required investment amount
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')
    conn.commit()
    conn.close()


# financedata.py
def get_finance_data(user_id):
    """Retrieve a summary of finance data for the specified user, considering only completed transactions."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch completed deposits only
    cursor.execute('SELECT SUM(amount) FROM finance WHERE user_id = ?  AND status = "completed"', (user_id,))
    investment = cursor.fetchone()[0] or 0

    # Calculate earnings as 2% of the total completed deposits
    earnings = investment * 0.02

    # Fetch completed withdrawals only
    cursor.execute('SELECT SUM(amount) FROM finance WHERE user_id = ? AND type = "withdraw" AND status = "completed"', (user_id,))
    withdrawn = cursor.fetchone()[0] or 0

    # Calculate the balance as investment + earnings - withdrawn
    balance = (investment + earnings) - withdrawn

    conn.close()
    
    return {
        'investment': investment,
        'earnings': earnings,
        'withdrawn': withdrawn,
        'balance': balance
    }

def get_transactions(user_id):
    """Retrieve all transactions for a specific user."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT date, amount, status FROM finance WHERE user_id = ?', (user_id,))
    transactions = [{'date': row[0], 'amount': row[1], 'status': row[2]} for row in cursor.fetchall()]
    conn.close()
    return transactions

def insert_finance_data(user_id, amount, trans_type, status='pending'):
    """Insert a new finance transaction for a specific user."""
    conn = connect_db()
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO finance (user_id, date, amount, type, status) VALUES (?, ?, ?, ?, ?)',
                   (user_id, date, amount, trans_type, status))
    conn.commit()
    print('data inserted successifully')
    conn.close()

def get_user_subscription(user_id):
    """Retrieve the subscription plan and required amount for the specified user."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT subscription_plan, required_amount FROM finance WHERE user_id = ?', (user_id,))
    subscription = cursor.fetchone()
    conn.close()
    return subscription if subscription else (None, None)  # Return None if no subscription


