import sqlite3
import json
from datetime import datetime

def get_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT * FROM categories
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        categories = []
        for row in query_results:
            categories.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_categories = json.dumps(categories)
        return serialized_categories