import sqlite3 
import json

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
        """, (category['name'],))
 
        id = db_cursor.lastrowid
 
        return json.dumps({
            'id': id,
            'label': category['name']
        })