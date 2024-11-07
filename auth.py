from db import insert_user, find_user
from werkzeug.security import check_password_hash
from flask import render_template, session, redirect, url_for, flash

def register_user(username, password, email):
    if find_user(email):
        return False  # User already exists
    insert_user(username, password, email)
    return True

def login_user(email, password):
    """Log in a user by email and password."""
    user = find_user(email=email)  # Find user by email
    
    if user and check_password_hash(user[2], password):  # Assuming the password is at index 2
        return True  # Login successful
    return False  # Login failed

def find(email):
    find_user(email=email)
    
def logout_user():
    """Logs out the current user by clearing their session."""
    session.pop('user_id', None)  # Remove user ID from the session to log out
    flash('You have been logged out successfully.', 'info')  # Inform the user
    redirect(url_for('login'))
    return render_template('login.html')  # Redirect to login page
