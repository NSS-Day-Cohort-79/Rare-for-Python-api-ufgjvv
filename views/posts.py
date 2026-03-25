import sqlite3
import json
from datetime import datetime


def post_post(post):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved')
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

        for tag in post["tags"]:
            db_cursor.execute(
                """
            SELECT id FROM tags WHERE id = ?
            """,
                (tag,),
            )
            tag_id = db_cursor.fetchone()[0]

            db_cursor.execute(
                """
        INSERT INTO posttags ('post_id', 'tag_id') 
                              VALUES (?, ?)   
        """,
                (post_id, tag_id),
            )

        conn.commit()

        return json.dumps({"success": True})


# --- FUNCTION ADDED FOR STEP 3 (VIEW POST DETAILS #5) ---
def get_single_post(post_id):
    """Retrieve a single post with all details for Post Details page"""


def get_user_posts(post_data, user):
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
            u.username AS author
        FROM Posts p
        JOIN Users u ON u.id = p.user_id
        WHERE p.id = ?
        """,
            (post_id,),
        )

        post = db_cursor.fetchone()

        if post is None:
            return json.dumps({"error": "Post not found"})

        # Convert row to dict
        post_dict = {
            "id": post["id"],
            "title": post["title"],
            "content": post["content"],
            "publication_date": post["publication_date"],
            "image_url": post["image_url"],
            "author": post["author"],
        }

        return json.dumps(post_dict)
        if post_data:
            if user:
                db_cursor.execute(
                    """
                SELECT
                    p.id,
                    p.title,
                    p.publication_date,
                    p.image_url,
                    u.first_name,
                    u.last_name,
                    c.label
                FROM posts p
                JOIN users u ON p.user_id = u.id
                JOIN categories c ON p.category_id = c.id
                WHERE p.user_id = ?
                ORDER BY p.id DESC
                """,
                    (user,),
                )
                query_results = db_cursor.fetchall()
        else:
            pass

        posts = []
        for row in query_results:
            posts.append(dict(row))

        serialized_posts = json.dumps(posts)

    return serialized_posts


def get_posts(post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if post_data:
            db_cursor.execute(
                """
                SELECT
                    p.id,
                    p.title,
                    p.publication_date,
                    p.image_url,
                    u.first_name,
                    u.last_name,
                    c.label
                FROM posts p
                JOIN users u ON p.user_id = u.id
                JOIN categories c ON p.category_id = c.id
                ORDER BY p.id DESC
                """
            )
            query_results = db_cursor.fetchall()
        else:
            pass

        posts = []
        for row in query_results:
            posts.append(dict(row))

        serialized_posts = json.dumps(posts)

    return serialized_posts
