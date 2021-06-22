from flask import Flask, json, request, render_template, jsonify, session, redirect

from setup import create_db_and_tables
from db_check import get_tables_from_db
from db_ops import register_user, user_exits, login_user, get_users, update_user_status_db
from db_ops import get_all_ideas, add_idea_db, get_idea_by_id_db, get_comments_for_idea
from db_ops import add_comment_db, delete_idea_db


# Instantiate flask app
app = Flask(__name__)

# Basic config for flask app
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = "my-secret-key"
app.config["SESSION_TYPE"] = "filesystem"

@app.route("/", methods=['GET'])
def index():

    if request.method == "GET":
        if session.get('logged_in'):
            account_type = session.get('account_type')

            if account_type == "admin":
                return redirect("/user")
            elif account_type == "user":
                return redirect("/admin")

        return render_template("index.html")

@app.route("/setup", methods=['GET'])
def setup():

    if request.method == "GET":
        try:
            create_db_and_tables()
            return jsonify({"status": "Setup success"})
        except Exception as e:
            return jsonify({"status": str(e)})

@app.route("/get-tables", methods=['GET'])
def get_tables():

    if request.method == "GET":
        return jsonify({"tables": get_tables_from_db()})

@app.route("/register", methods=['POST'])
def register():

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if user_exits(email=email):
            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "Account with this email already exists!",
                "url": "/",
            })

        register_user(name=name, email=email, password=password)

        return jsonify({
            "icon": "success",
            "title": "Success",
            "text": "User registered successfully!",
            "url": "/",
        })

@app.route("/login", methods=['POST'])
def login():

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if not user_exits(email=email):
            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "Account doesn't exist, register first!",
                "url": "/",
            })

        user_id, status = login_user(email=email, password=password)

        if user_id == None:
            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "Incorrect credentials!",
                "url": "/",
            })
        elif type(user_id) == int and status == -1:
            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "Account rejected by admin!",
                "url": "/",
            })
        elif type(user_id) == int and status == 0:
            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "Account is yet to be approved by admin!",
                "url": "/",
            })    

        session['user_id'] = user_id
        session['account_type'] = "user" if user_id != "admin" else "admin"
        session['logged_in'] = True

        if session.get('account_type') == 'admin':
            return jsonify({
                "icon": "success",
                "title": "Success",
                "text": "Welcome admin!",
                "url": "/admin",
            })

        return jsonify({
            "icon": "success",
            "title": "Success",
            "text": "Logged in successfully!",
            "url": "/user",
        })

@app.route("/logout", methods=['GET'])
def logout():

    if request.method == "GET":
        session['user_id'] = None
        session['account_type'] = None
        session['logged_in'] = False

        return redirect("/")

@app.route("/user", methods=['GET'])
def user():

    if request.method == "GET":
        own_uid = session.get('user_id')
        ideas = get_all_ideas(own_uid=own_uid)

        return render_template("user.html", ideas=ideas)

@app.route("/admin", methods=['GET'])
def admin():

    if request.method == "GET":
        users_data = get_users()
        ideas = get_all_ideas(own_uid=-1)

        return render_template("admin.html", users_data=users_data, ideas=ideas)

@app.route("/update-user-status", methods=['POST'])
def update_user_status():

    if request.method == "POST":
        uid = int(request.form['uid'])
        status = int(request.form['status'])

        update_user_status_db(uid=uid, status=status)

        return jsonify({
            "icon": "success",
            "title": "Success",
            "text": "Updated user status!",
            "url": "/admin",
        })     

@app.route("/add-idea", methods=['POST'])
def add_idea():

    if request.method == "POST":
        uid = int(session.get('user_id'))
        idea = request.form['idea']

        add_idea_db(uid=uid, idea=idea)

        return jsonify({
            "icon": "success",
            "title": "Success",
            "text": "Idea added successfully!",
            "url": "/user",
        })

@app.route("/get-idea/<idea_id>", methods=['GET'])
def get_idea(idea_id):

    if request.method == "GET":
        own_uid = session.get('user_id')
        idea = get_idea_by_id_db(own_uid=own_uid, iid=idea_id)
        comments = get_comments_for_idea(own_uid=own_uid, iid=idea_id)

        return render_template("idea.html", idea=idea, comments=comments)

@app.route("/add-comment", methods=['POST'])
def add_comment():

    if request.method == "POST":
        uid = int(session.get('user_id'))
        iid = int(request.form['iid'])
        comment = request.form['comment']

        add_comment_db(uid=uid, iid=iid, comment=comment)

        return jsonify({
            "icon": "success",
            "title": "Success",
            "text": "Comment added successfully!",
            "url": f"/get-idea/{iid}",
        })

@app.route("/delete-idea", methods=['POST'])
def delete_idea():

    if request.method == "POST":
        iid = int(request.form['iid'])

        delete_idea_db(iid=iid)

        return jsonify({
            "icon": "success",
            "title": "Success",
            "text": "Idea and all comments deleted successfully!",
            "url": "/admin",
        })

if __name__ == "__main__":
    app.run(debug=True)