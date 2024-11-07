from flask import *
from platformdirs import user_data_dir
from db import connect_db, create_user_table, find_user
from auth import register_user, login_user, logout_user
from financedata import create_finance_table, insert_finance_data, get_finance_data, get_transactions
import bcrypt
from paymentdetails import *
import qrcode
import os
from verifypayment import *
from deposit import *
from waitress import serve


app = Flask(__name__)
app.secret_key = '6796098789077896759987587687696'  # Change this to a secure random key
#create_finance_table()
#insert_demo_data()
#create_wallet_table()

#making a global variable
wallet_address = '53453tfgdjfkjfbdfhsjhfior78965783465439853gugfsdf876t734'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    # Assume user_id is stored in session after login

    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))  # Redirect if not logged in

    finance_data = get_finance_data(user_id)
    transactions = get_transactions(user_id)
    
    return render_template('home.html', finance=finance_data, transactions=transactions)

# Example usage of insert_finance_data for Deposit/Withdrawal actions
# @app.route('/deposit', methods=['POST'])
# def deposit():
#     user_id = session.get('user_id')
#     amount = request.form.get('amount')
#     insert_finance_data(user_id, amount, 'investment', 'approved')
#     return redirect(url_for('home'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('fullName')
        password = request.form.get('password')
        email = request.form.get('email')

        try:
        
            if register_user(username, password, email):
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Username already exists. Please choose another.', 'error')
        except:
            print('error occured')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # Get email from the form
        password = request.form.get('password')  # Get password from the form
        
        if login_user(email, password):
            user = find_user(email=email)

            if user:
                id, name, hashed_password, email = user
                session['user_id'] = id  # Save UID in the session    
                #flash('Login successful!', 'success')  # Flash success message
                return redirect(url_for('home'))  # Redirect to the dashboard or another page
            
        else:
             # Flash error message
            redirect(url_for('login'))
            flash('Invalid email or password.', 'danger')   # Redirect back to the login page

    return render_template('login.html')  # Render the login page for GET requests


@app.route('/logout', methods = ['POST'])
def logout():
    return logout_user()

@app.route('/subscribe/<plan>', methods=['POST', 'GET'])
def subscribe(plan):
    user_id = session.get('user_id')  # Ensure user is logged in
    amount = get_plan_amount(plan)     # Retrieve the plan amount based on the selected plan
    
    # Save the subscription data
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO subscription (user_id, plan, amount) VALUES (?, ?, ?)', 
                   (user_id, plan, amount))
    conn.commit()
    conn.close()

    # Redirect to the next step for payment
    return render_template('deposit.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            flash("Please log in to continue.")
            return redirect(url_for('login'))

        amount = request.form.get('amount')
        type = request.form.get('type')

        # Static wallet address (you may replace this with the actual user's wallet address)
        wallet_address = '53453tfgdjfkjfbdfhsjhfior78965783465439853gugfsdf876t734'

        # Generate the QR code
        qr_code_path = generate_qr_code(wallet_address, user_id)

        # Insert transaction data into finance table with 'pending' status
        insert_finance_data(user_id, amount, type, status='completed')

        #flash("Deposit initiated. Please complete payment on the next page.")
        return redirect(url_for('pay', qr_code_path=qr_code_path))

    return render_template('deposit.html')

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    qr_code_path = 'wallet_qr.png'
    wallet_address = '53453tfgdjfkjfbdfhsjhfior78965783465439853gugfsdf876t734'  # This should be fetched dynamically

    return render_template('next_step.html', qr_code_path=qr_code_path, wallet_address=wallet_address)


from datetime import datetime

@app.route('/withdraw', methods=['POST', 'GET'])
def withdraw():
    if request.method == 'GET':
        return render_template('withdraw.html')
    
    user_id = session.get('user_id')
    if not user_id:
        flash("You must be logged in to withdraw funds.")
        return redirect(url_for('login'))

    # Get the requested withdrawal amount
    try:
        amount = float(request.form.get('amount'))
    except ValueError:
        flash("Invalid amount entered.")
        return redirect(url_for('withdraw'))

    # Connect to the database and retrieve deposits and withdrawals
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Get total completed deposits for the user
    cursor.execute('SELECT SUM(amount) FROM finance WHERE user_id = ? AND status = "completed" ', (user_id,))
    deposits = cursor.fetchone()[0] or 0

    # Calculate earnings as 2% of total deposits
    earnings = deposits * 0.02

    # Get total completed withdrawals
    cursor.execute('SELECT SUM(amount) FROM finance WHERE user_id = ? AND type = "withdraw" AND status = "completed"', (user_id,))
    withdrawals = cursor.fetchone()[0] or 0

    # Calculate available earnings balance
    available_earnings = earnings - withdrawals

    # Check if requested amount exceeds available earnings
    if available_earnings < 0:
        available_earnings = 0  # Ensure balance can't be negative for display

    if amount > available_earnings:
        flash(f"Insufficient earnings. You can only withdraw up to {available_earnings:.2f}.")
        conn.close()
        return redirect(url_for('withdraw'))

    # Record the withdrawal request as "pending" with the current date and time
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO finance (user_id, amount, type, status, date) VALUES (?, ?, "withdraw", "completed", ?)', 
                   (user_id, amount, current_date))
    conn.commit()
    conn.close()

    flash("Withdrawal request submitted successfully and is pending approval.")
    return redirect(url_for('home'))

    

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)