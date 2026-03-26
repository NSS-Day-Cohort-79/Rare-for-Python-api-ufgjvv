import sqlite3
import json
import nss_handler


DATABASE = "db.sqlite3"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_tags():

    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT id, label FROM tags ORDER BY id ASC").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_tag(tag_id):

    conn = get_db_connection()
    try:
        row = conn.execute(
            "SELECT id, label FROM tags WHERE id = ?", (tag_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def create_tag(tag_data):

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

    conn = get_db_connection()
    try:
        cursor = conn.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
