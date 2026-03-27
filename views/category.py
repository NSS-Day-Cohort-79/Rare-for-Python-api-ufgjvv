import sqlite3
import json
from datetime import datetime

def get_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT * FROM categories ORDER BY label ASC
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        categories = []
        for row in query_results:
            categories.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_categories = json.dumps(categories)
        return serialized_categories

def get_category(pk):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                id,
                label
            FROM categories
            WHERE id = ?
        """, (pk,))

        query_result = db_cursor.fetchone()

        if query_result is None:
            return json.dumps(None)

        return json.dumps(dict(query_result))


def create_category(category):
    """Adds a new category to the database
 
    Args:
        category (dict): Contains the label for the new category
 
    Returns:
        json string: The newly created category with its id and label
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
 
        db_cursor.execute("""
            INSERT INTO Categories (label) VALUES (?)
        """, (category['label'],))
 
        id = db_cursor.lastrowid
 
        return json.dumps({
            'id': id,
            'label': category['label']
        })

def update_category(category):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE categories
        SET label = ?
        WHERE id = ?
        """, (category["label"], category["id"],))

        conn.commit()

        return json.dumps({"success": True})

def delete_category(id):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM categories
        WHERE id = ?
        """, (id,))

        conn.commit()

        return json.dumps({"success": True})
