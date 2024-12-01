import sqlite3

def initialize_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect("DB/DrugsInventory.db")
    cursor = connection.cursor()

    # Read schema from file and execute it
    with open("DB/schema.sql", "r") as schema_file:
        schema = schema_file.read()
        cursor.executescript(schema)

    print("Database initialized successfully.")
    connection.commit()
    connection.close()

initialize_database()
