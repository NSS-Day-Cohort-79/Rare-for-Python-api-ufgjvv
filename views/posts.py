import sqlite3
import json
from datetime import datetime


def post_post(post):
    """Insert a new post into the database along with its tags."""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                post["user_id"],
                post["category_id"],
                post["title"],
                datetime.now(),
                post["image_url"],
                post["content"],
                post["approved"],
            ),
        )
        post_id = db_cursor.lastrowid

        for tag in post.get("tags", []):
            db_cursor.execute("SELECT id FROM Tags WHERE id = ?", (tag,))
            result = db_cursor.fetchone()
            if result:
                tag_id = result["id"]
                db_cursor.execute(
                    "INSERT INTO PostTags (post_id, tag_id) VALUES (?, ?)",
                    (post_id, tag_id),
                )

        conn.commit()

    return json.dumps({"success": True})


def get_single_post(post_id):
    """Retrieve a single post with author and category info for Post Details page."""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            p.id,
            p.title,
            p.content,
            p.publication_date,
            p.image_url,
            u.first_name || ' ' || u.last_name AS full_name,
            c.label AS category
        FROM Posts p
        JOIN Users u ON p.user_id = u.id
        JOIN Categories c ON p.category_id = c.id
        WHERE p.id = ?
        """,
            (post_id,),
        )

        post = db_cursor.fetchone()
        if post is None:
            return json.dumps({"error": "Post not found"})

        return json.dumps(dict(post))


def get_user_posts(user_id):
    """Retrieve all posts for a specific user."""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            p.id,
            p.title,
            p.publication_date,
            p.image_url,
            u.first_name,
            u.last_name,
            c.label AS category
        FROM Posts p
        JOIN Users u ON p.user_id = u.id
        JOIN Categories c ON p.category_id = c.id
        WHERE p.user_id = ?
        ORDER BY p.id DESC
        """,
            (user_id,),
        )

        query_results = db_cursor.fetchall()
        posts = [dict(row) for row in query_results]
        return json.dumps(posts)


def get_posts(_unused=None):
    """Retrieve all posts with author and category information."""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            p.id,
            p.title,
            p.publication_date,
            p.image_url,
            u.first_name,
            u.last_name,
            c.label AS category
        FROM Posts p
        JOIN Users u ON p.user_id = u.id
        JOIN Categories c ON p.category_id = c.id
        ORDER BY p.id DESC
        """
        )

        query_results = db_cursor.fetchall()
        posts = [dict(row) for row in query_results]

        return json.dumps(posts)
