import sqlite3
import json

DATABASE = "db.sqlite3"


def get_db_connection():
    """Open a connection to the SQLite database and configure row_factory."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Rows behave like dicts
    return conn


def get_tags():
    """
    Return all tags as a list of dicts.

    SQL: SELECT id, label FROM tags ORDER BY id ASC
    Response shape: [{"id": 1, "label": "Python"}, ...]
    """
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT id, label FROM tags ORDER BY id ASC").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_tag(tag_id):
    """
    Return a single tag by ID, or None if not found.

    SQL: SELECT id, label FROM tags WHERE id = ?
    Response shape: {"id": 1, "label": "Python"} or None
    """
    conn = get_db_connection()
    try:
        row = conn.execute(
            "SELECT id, label FROM tags WHERE id = ?", (tag_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def create_tag(tag_data):
    """
    Insert a new tag and return the created tag (with its auto-generated id).

    Expected tag_data: {"label": "Python"}
    Response shape:    {"id": 5, "label": "Python"}

    Raises ValueError if 'label' is missing or empty.
    """
    label = (tag_data.get("label") or "").strip()
    if not label:
        raise ValueError("Tag 'label' is required and cannot be blank.")

    conn = get_db_connection()
    try:
        cursor = conn.execute("INSERT INTO tags (label) VALUES (?)", (label,))
        conn.commit()
        new_id = cursor.lastrowid
        return {"id": new_id, "label": label}
    finally:
        conn.close()


def update_tag(tag_id, tag_data):
    """
    Update an existing tag's label by ID.

    Expected tag_data: {"label": "New Label"}
    Returns the updated tag dict, or None if the tag was not found.

    Raises ValueError if 'label' is missing or empty.
    """
    label = (tag_data.get("label") or "").strip()
    if not label:
        raise ValueError("Tag 'label' is required and cannot be blank.")

    conn = get_db_connection()
    try:
        cursor = conn.execute("UPDATE tags SET label = ? WHERE id = ?", (label, tag_id))
        conn.commit()
        if cursor.rowcount == 0:
            return None  # No row matched — tag doesn't exist
        return {"id": tag_id, "label": label}
    finally:
        conn.close()


def delete_tag(tag_id):
    """
    Delete a tag by ID.

    Returns True if a row was deleted, False if the tag was not found.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
