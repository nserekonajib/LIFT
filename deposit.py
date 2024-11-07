from flask import Flask, render_template, request, redirect, url_for, flash, session
import qrcode
import sqlite3
import os
from paymentdetails import save_wallet_details
# Database setup (you may already have this)

def depositnow():
    app = Flask(__name__)
     # Ensure to set your secret key
    DATABASE = 'users.db'

    # Helper function to get database connection
    def get_db_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @app.route('/deposit', methods=['GET', 'POST'])
    def deposit():
        if request.method == 'POST':
            user_id = session.get('user_id')
            if not user_id:
                return redirect(url_for('login'))

            full_name = request.form['full_name']
            wallet_address = request.form['wallet_address']
            password = request.form['password']
            amount = float(request.form['amount'])

            # Step 1: Validate Full Name and Wallet Address
            if not full_name or not wallet_address:
                flash("Please enter all required details.")
                return redirect(url_for('deposit'))

            # Save wallet details if valid
            save_wallet_details(user_id, wallet_address)

            # Step 2: Validate Password and Amount Range Based on Plan
            # Retrieve the user and finance data to validate
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if not user or user['password'] != password:
                flash("Invalid password.")
                return redirect(url_for('deposit'))

            # Validate amount within the range for the user's selected plan
            finance = conn.execute("SELECT * FROM finance WHERE user_id = ?", (user_id,)).fetchone()
            if not finance or amount < finance['min_investment'] or amount > finance['max_investment']:
                flash(f"Please enter an amount within the range: {finance['min_investment']} - {finance['max_investment']}.")
                return redirect(url_for('deposit'))

            # Redirect to next step after validation
            session['amount'] = amount  # Save amount for use in the next step
            return redirect(url_for('next_step'))

        return render_template('deposit.html')

    @app.route('/next_step')
    def next_step():
        user_id = session.get('user_id')
        amount = session.get('amount')
        if not user_id or not amount:
            return redirect(url_for('deposit'))

        # Generate QR code for payment
        qr_code_path = f'static/qrcodes/{user_id}_qrcode.png'
        wallet_address = "user_wallet_address"  # Retrieve this from the database as needed
        img = qrcode.make(wallet_address)
        img.save(qr_code_path)

        # Clear previous QR codes for this user
        old_files = [f for f in os.listdir('static/qrcodes') if f.startswith(f'{user_id}_') and f != qr_code_path]
        for f in old_files:
            os.remove(f'static/qrcodes/{f}')

        return render_template('next_step.html', qr_code_path=qr_code_path, wallet_address=wallet_address)

    @app.route('/upload_payment_verification', methods=['POST'])
    def upload_payment_verification():
        if 'verification_image' not in request.files:
            flash('No file uploaded.')
            return redirect(url_for('next_step'))

        file = request.files['verification_image']
        if file.filename == '':
            flash('No file selected.')
            return redirect(url_for('next_step'))

        user_id = session.get('user_id')
        file_path = f'static/verification/{user_id}_verification.png'
        file.save(file_path)

        # Save payment transaction to database as pending
        conn = get_db_connection()
        conn.execute("INSERT INTO finance (user_id, amount, status, verification_image) VALUES (?, ?, ?, ?)",
                    (user_id, session.get('amount'), 'pending', file_path))
        conn.commit()
        conn.close()

        flash("Verification uploaded successfully.")
        return redirect(url_for('home'))

   
