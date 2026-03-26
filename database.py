import sqlite3
from datetime import datetime

DATABASE = "db.sqlite3"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection