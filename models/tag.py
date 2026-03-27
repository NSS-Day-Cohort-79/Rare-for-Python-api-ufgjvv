import sqlite3
import json


def create_tag(tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Tags (label)
            VALUES (?)
        """,
            (tag["label"],),
        )

        conn.commit()

        return json.dumps({"id": db_cursor.lastrowid, "label": tag["label"]})
