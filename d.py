modules = [
    "Flask",
    "Flask-SQLAlchemy",
    "Flask-Session",
    "Flask-WTF",
    "Flask-Login",
    "Flask-Flash",
    "Flask-Bcrypt",
    "pymysql",
    "requests",
    "sqlite3",
    "qrcode",
    "Pillow",
    "datetime",
    "platformdirs",
    "os",
    "Werkzeug",
    "gunicorn",
    "waitress"
]

# Create the requirements.txt file
with open('requirements.txt', 'w') as f:
    for module in modules:
        f.write(module + '\n')

print("requirements.txt file created successfully.")
