import sqlite3
import qrcode
import time
import os
from PIL import Image

def connect_db():
    return sqlite3.connect('users.db')

def create_wallet_table():
    """Create the wallet table if it doesn't exist."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS wallets (
    user_id INTEGER PRIMARY KEY,
    wallet_address TEXT NOT NULL,
    verification_image TEXT
);


    ''')
    conn.commit()
    conn.close()

def save_wallet_details(user_id, wallet_address=None, verification_image_path = None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO wallets (user_id, address, verification_image)
        VALUES (?, ?, ?)
    ''', (user_id, wallet_address, verification_image_path))
    conn.commit()
    conn.close()

def get_db_connection():
        DATABASE = 'users.db'
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

def get_wallet_address(user_id, wallet_address = None):
    conn = connect_db()
    cursor = conn.cursor()
    # Assuming you have a database connection established
    try:
        if user_id is None:
            print("Error: user_id is None. Cannot save wallet details.")
            return

        # Insert wallet details into the wallets table
        
        cursor.execute('''
            INSERT INTO wallets (user_id, address)
            VALUES (?, ?)
        ''', (user_id, wallet_address))
        
        # Commit the transaction
        conn.commit()
        print("Wallet details saved successfully.")

    except sqlite3.IntegrityError as e:
        print(f"An integrity error occurred: {e}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    return

# # Example call
# # Make sure you pass a valid user_id

# wallet_address = "user_wallet_address"
# save_wallet_details(user_id, wallet_address)
create_wallet_table()



#this piece of code is for esting purposes

QR_CODE_FOLDER = 'static/qrcodes'

# Ensure the QR code folder exists
os.makedirs(QR_CODE_FOLDER, exist_ok=True)

# Helper function to generate a QR code
def generate_qr_code(wallet_address, user_id):
    qr_code_path = os.path.join(QR_CODE_FOLDER, f'{user_id}_qrcode.png')
    img = qrcode.make(wallet_address)
    img.save(qr_code_path)
    return qr_code_path

