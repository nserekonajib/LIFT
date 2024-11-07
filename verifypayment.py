import sqlite3

# Example to create table in your Flask app setup or a migration script
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Subscription table with a foreign key to the user
cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscription (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        plan TEXT,
        status TEXT DEFAULT 'pending',
        amount REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
''')
conn.commit()
conn.close()

def get_plan_amount(plan):
    # Dictionary to store plan prices
    plan_prices = {
        "starter": 10.0,
        "bronze": 20.0,
        "gold": 30.0
    }
    
    # Return the amount for the specified plan, or 0 if the plan is not found
    return plan_prices.get(plan.lower(), 0.0)

