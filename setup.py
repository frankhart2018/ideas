import sqlite3
from sqlite3.dbapi2 import Cursor

from connect import get_connection


def create_db_and_tables():
    conn, cursor = get_connection()

    cursor.execute(
        "CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, status INT NOT NULL)"
    )

    cursor.execute("CREATE TABLE admin(password TEXT NOT NULL)")

    cursor.execute(
        "CREATE TABLE ideas(id INTEGER PRIMARY KEY AUTOINCREMENT, uid INTEGER NOT NULL, idea TEXT NOT NULL)"
    )

    cursor.execute(
        "CREATE TABLE comments(id INTEGER PRIMARY KEY AUTOINCREMENT, iid INTEGER NOT NULL, uid INTEGER NOT NULL, comment TEXT NOT NULL)"
    )

    cursor.execute("INSERT INTO admin(password) VALUES('adminideas2021@')")

    conn.commit()
