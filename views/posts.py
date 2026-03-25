import sqlite3
import json
from datetime import datetime

def post_post(post):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved')
                          VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            post["user_id"],
            post["category_id"],
            post["title"],
            datetime.now(),
            post["image_url"],
            post["content"],
            post["approved"],
        ),)
        post_id = db_cursor.lastrowid

        for tag in post["tags"]:
            db_cursor.execute("""
            SELECT id FROM tags WHERE id = ?
            """, (tag,))
            tag_id = db_cursor.fetchone()[0]

            db_cursor.execute("""
        INSERT INTO posttags ('post_id', 'tag_id') 
                              VALUES (?, ?)   
        """, (post_id, tag_id))
            
        conn.commit()

        return json.dumps({"success": True})
    
def get_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                p.id,
                p.user_id,
                p.category_id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved
            FROM Posts p
        """)

        posts = [dict(row) for row in db_cursor.fetchall()]
        return json.dumps(posts)
    
def get_single_post(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                p.id,
                p.user_id,
                p.category_id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved
            FROM Posts p
            WHERE p.id = ?
        """, (pk,))

        post = dict(db_cursor.fetchone())

        db_cursor.execute("""
            SELECT
                t.id,
                t.label
            FROM Tags t
            JOIN PostTags pt ON pt.tag_id = t.id
            WHERE pt.post_id = ?
        """, (pk,))

        post['tags'] = [dict(row) for row in db_cursor.fetchall()]

        return json.dumps(post) 