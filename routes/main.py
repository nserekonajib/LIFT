from flask import Blueprint, render_template

# Blueprint setup for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

