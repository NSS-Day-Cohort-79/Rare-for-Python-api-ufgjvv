import sqlite3
import json
from datetime import datetime


def create_comment(comment):
    """Create a new comment"""

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Comments (post_id, author_id, content, created_on)
        VALUES (?, ?, ?, ?)
        """,
            (
                comment["post_id"],
                comment["author_id"],
                comment["content"],
                datetime.now(),
            ),
        )

        new_id = db_cursor.lastrowid

        return json.dumps(
            {
                "id": new_id,
                "post_id": comment["post_id"],
                "author_id": comment["author_id"],
                "content": comment["content"],
                "created_on": datetime.now().isoformat(),
            }
        )
