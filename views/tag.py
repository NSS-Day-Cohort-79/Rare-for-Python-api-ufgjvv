import sqlite3
import json
from datetime import datetime

def get_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT * FROM tags
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        tags = []
        for row in query_results:
            tags.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_tags = json.dumps(tags)
        return serialized_tags