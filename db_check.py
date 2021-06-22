from connect import get_connection


def get_tables_from_db():
    _, cursor = get_connection()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall() if "sqlite" not in table[0]]

    return tables