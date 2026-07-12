import sqlite3
import os

DB_PATH = os.path.join("database", "reports.db")


def connect():
    return sqlite3.connect(DB_PATH)