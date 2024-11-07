import sqlite3

def delete_finance_table(db_name='users.db'):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        
        # SQL command to drop the finance table
        cursor.execute("DROP TABLE IF EXISTS wallets")
        
        # Commit the changes
        connection.commit()
        
        print("Table 'finance' deleted successfully.")
    
    except sqlite3.Error as error:
        print("Error occurred while deleting the table:", error)
    
    finally:
        # Close the database connection
        if connection:
            connection.close()

# Call the function to delete the finance table
delete_finance_table()
