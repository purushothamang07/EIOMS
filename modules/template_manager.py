import sqlite3
import os

DB = os.path.join("database", "reports.db")


def add_template(template_name, filename):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO templates(template_name,file_name)
        VALUES(?,?)
        """,
        (template_name, filename)
    )

    conn.commit()

    conn.close()


def get_templates():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("SELECT * FROM templates ORDER BY template_name")

    rows = cur.fetchall()

    conn.close()

    return rows