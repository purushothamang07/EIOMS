import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/reports.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS templates(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name TEXT NOT NULL,
    report_code TEXT,
    description TEXT,
    filename TEXT,
    uploaded_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active INTEGER DEFAULT 1
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_name TEXT,
    template_id INTEGER,
    consumer_name TEXT,
    letter_no TEXT,
    generated_file TEXT,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")