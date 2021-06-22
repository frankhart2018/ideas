import hashlib
from sqlite3.dbapi2 import Cursor

from connect import get_connection


def user_exits(email):
    _, cursor = get_connection()

    cursor.execute(f"SELECT * FROM users WHERE email='{email}'")
    data = cursor.fetchall()

    if len(data) > 0:
        return True

    return False

def register_user(name, email, password):
    encoded_password = hashlib.sha512(password.encode()).hexdigest()

    conn, cursor = get_connection()

    cursor.execute(f"INSERT INTO users(name, email, password, status) VALUES('{name}', '{email}', '{encoded_password}', 0)")
    conn.commit()

def login_user(email, password):
    _, cursor = get_connection()

    encoded_password = hashlib.sha512(password.encode()).hexdigest()

    cursor.execute(f"SELECT id, password, status FROM users WHERE email='{email}'")
    data = cursor.fetchone()
    
    cursor.execute(f"SELECT * FROM admin WHERE password='{password}'")
    data_admin = cursor.fetchone()

    if data_admin != None:
        return "admin", -1

    if data[-2] != encoded_password:
        return None, data[-1]

    return data[0], data[-1]

def get_users():
    _, cursor = get_connection()

    cursor.execute("SELECT id, name, email FROM users WHERE status=0")
    users_data = cursor.fetchall()

    return users_data

def update_user_status_db(uid, status):
    conn, cursor = get_connection()

    cursor.execute(f"UPDATE users SET status={status} WHERE id={uid}")
    conn.commit()

def get_username_by_id(own_uid, uid):
    _, cursor = get_connection()

    cursor.execute(f"SELECT name FROM users WHERE id={uid}")
    name = cursor.fetchone()[0]

    return name if uid != own_uid else "Me"

def get_all_ideas(own_uid):
    _, cursor = get_connection()

    cursor.execute("SELECT * FROM ideas")
    ideas = cursor.fetchall()

    unique_uids = set([idea[1] for idea in ideas])
    uids_to_names = {uid: get_username_by_id(own_uid=own_uid, uid=uid) for uid in unique_uids}

    for i in range(len(ideas)):
        ideas[i] = list(ideas[i])
        ideas[i][1] = uids_to_names[ideas[i][1]]
        ideas[i][2] = ideas[i][2][:30] + "..."

    return ideas

def get_idea_by_id_db(own_uid, iid):
    _, cursor = get_connection()

    cursor.execute(f"SELECT * FROM ideas WHERE id={iid}")
    idea = cursor.fetchone()

    idea = list(idea)
    idea[1] = get_username_by_id(own_uid=own_uid, uid=idea[1])

    return idea

def add_idea_db(uid, idea):
    conn, cursor = get_connection()

    cursor.execute(f"INSERT INTO ideas(uid, idea) VALUES({uid}, '{idea}')")
    conn.commit()

def get_comments_for_idea(own_uid, iid):
    _, cursor = get_connection()

    cursor.execute(f"SELECT * FROM comments WHERE iid={iid} ORDER by id DESC")
    comments = cursor.fetchall()

    print(comments)

    unique_uids = set([comment[2] for comment in comments])
    uids_to_names = {uid: get_username_by_id(own_uid=own_uid, uid=uid) for uid in unique_uids}

    print(uids_to_names)

    for i in range(len(comments)):
        comments[i] = list(comments[i])
        comments[i][2] = uids_to_names[comments[i][2]]

    

    return comments

def add_comment_db(iid, uid, comment):
    conn, cursor = get_connection()

    cursor.execute(f"INSERT INTO comments(iid, uid, comment) VALUES({iid}, {uid}, '{comment}')")
    conn.commit()

def delete_idea_db(iid):
    conn, cursor = get_connection()

    cursor.execute(f"DELETE FROM ideas WHERE id={iid}")
    conn.commit()

    cursor.execute(f"DELETE FROM comments WHERE iid={iid}")
    conn.commit()