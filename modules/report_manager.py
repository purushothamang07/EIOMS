import sqlite3
import os

DB = os.path.join("database", "reports.db")


def add_report(report_name, template_name, generated_file):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO reports(
            report_name,
            template_name,
            generated_file
        )
        VALUES(?,?,?)
        """,
        (
            report_name,
            template_name,
            generated_file
        )
    )

    conn.commit()

    conn.close()


def get_reports():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("SELECT * FROM reports ORDER BY id DESC")

    rows = cur.fetchall()

    conn.close()

    return rows