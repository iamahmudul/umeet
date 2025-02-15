import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = "1234"
DATABASE = "umeetdb"

def get_db_connection():
    return mysql.connector.connect(
        host=HOST,       # Change to your database host
        user=USER,            # Change to your MySQL username
        password=PASSWORD,    # Change to your MySQL password
        database=DATABASE      # Change to your database name
    )