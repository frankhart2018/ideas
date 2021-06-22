import sqlite3
from sqlite3.dbapi2 import Cursor


def get_connection():
    conn = sqlite3.connect(
        database="ideas.db"
    )

    cursor = conn.cursor()

    return conn, cursor