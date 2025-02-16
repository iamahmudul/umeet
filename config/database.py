import mysql.connector
import os

HOST = "localhost"
USER = "root"
PASSWORD = "1234"
DATABASE = "umeetdb"

def get_db_connection():
    return mysql.connector.connect(
        host=HOST, 
        user=USER, 
        password=PASSWORD, 
        database=DATABASE,
        ssl_disabled=True  # Disable SSL if not required
    )