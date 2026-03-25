import sqlite3
import json

def add_post_tags(post_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        for tag_id in post_tag['tag_ids']:
            db_cursor.execute("""
                INSERT INTO PostTags (post_id, tag_id) VALUES (?, ?)
            """, (post_tag['post_id'], tag_id))

        conn.commit()

        return json.dumps({'success': True})