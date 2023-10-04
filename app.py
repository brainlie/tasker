import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

#Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///tasker.db")

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        return render_template("home.html")

    else:
        #Name of person logged in
        name = db.execute("SELECT name FROM users WHERE user_id = ?", session["user_id"])[0]["name"]

        #Selecting all tasks from database
        tasks = db.execute("SELECT * FROM tasks WHERE recipient = ? ORDER BY due ASC", name)

        #Selecting all tasks given by user
        tasks_given = db.execute("SELECT * FROM tasks WHERE sender = ? ORDER BY due ASC", name)

        return render_template('home.html', name=name, tasks=tasks, tasks_given=tasks_given)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        #Assign username and password
        username = request.form.get("username")
        password = request.form.get("password")

        #Error Checking
        if not username or not password:
            return render_template('error.html', error="Missing username/password")

        password_check = db.execute("SELECT password FROM users WHERE username = ?", username)
        if len(password_check) == 0 or not check_password_hash(password_check[0]["password"], password):
            return render_template('error.html', error="Invalid username/password")

        #Remember user id
        else:
            user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
            session["user_id"] = user_id
            return redirect('/')

    #If get request, show login page
    else:
        return render_template('login.html')

@app.route("/changepw", methods=["GET", "POST"])
def changepw():
    #Assign Values
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        cfm_password = request.form.get("cfm_password")

        #Error Checking
        if not username or not password or not name or not cfm_password:
            return render_template('error.html', error="Missing field(s)")

        check_username = db.execute("SELECT username FROM users WHERE name = ?", name.title())
        print(check_username)
        if len(check_username) == 0 or username != check_username[0]["username"]:
            return render_template('error.html', error="Invalid username/name")

        elif password != cfm_password:
            return render_template('error.html', error="Passwords do not match")

        else:
            db.execute("UPDATE users SET password = ? WHERE username = ?", generate_password_hash(password), username)

        return render_template("login.html")

    else:
        return render_template('changepw.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #Assign information to respective variables
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        #Error Checking
        if not name or not username or not password or not password2:
            return render_template("error.html", error="missing field(s)")

        username_check = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(username_check) > 0:
            return render_template("error.html", error="username has been taken")

        elif password != password2:
            return render_template("error.html", error="passwords do not match")

        #Insert all inputs by user into database
        else:
            password = generate_password_hash(password)
            db.execute("INSERT INTO users(name, username, password) VALUES(?, ?, ?)", name.title(), username, password)
            user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
            session["user_id"] = user_id
            return render_template("home.html", name=name.title())

    #If GET request, display register page
    else:
        return render_template('register.html')

@app.route("/view", methods=["GET", "POST"])
@login_required
def view():
    #If method is POST, get all tasks for that user
    if request.method == "POST":
        #Name of person logged in
        name = db.execute("SELECT name FROM users WHERE user_id = ?", session["user_id"])[0]["name"]

        #Name of user searched
        named = request.form.get("name")
        #Selecting all tasks that were given to user searched
        received = db.execute("SELECT * FROM tasks WHERE recipient = ?", named)
        #Selecting all tasks that were given by user searched
        given = db.execute("SELECT * FROM tasks WHERE sender = ?", named)
        return render_template('view.html', name=name, received=received, given=given, named=named)

    else:
        return redirect('/')

@app.route("/manage", methods=["GET", "POST"])
@login_required
def manage():
    if request.method == "POST":
        return render_template('layout.html')

    else:
        #Name of person logged in
        name = db.execute("SELECT name FROM users WHERE user_id = ?", session["user_id"])[0]["name"]

        #Select all results from tasks database ordered by name
        tasks = db.execute("SELECT * FROM tasks ORDER BY recipient, sender ASC")

        names = db.execute("SELECT name FROM users ORDER BY name ASC")

        return render_template('manage.html', name=name, tasks=tasks, names=names)

@app.route("/logout")
def logout():
    #Forget user_id
    session.clear()
    #Redirect to login form
    return redirect("/")

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    #Name of person logged in
    name = db.execute("SELECT name FROM users WHERE user_id = ?", session["user_id"])[0]["name"]
    if request.method == "POST" and request.form.get("order") == "first":
        #Getting task id to edit the requested task
        task_id = request.form.get("id")
        task = request.form.get("task")
        date = request.form.get("date")
        recipient = request.form.get("recipient")
        importance = request.form.get("importance")

        #Select all users names excluding self
        names = db.execute("SELECT name FROM users WHERE NOT name = ? ORDER BY name ASC", name)

        return render_template("edit.html", name=name, task=task, names=names, task_id=task_id, date=date, recipient=recipient, action="Edit", importance=importance)

    elif request.method == "POST":
        #Assigning new values to variables
        task_id = request.form.get("task_id")
        new_task = request.form.get("new_task")
        new_date = request.form.get("new_date")
        new_status = request.form.get("new_status")
        new_importance = request.form.get("new_importance")
        new_recipient = request.form.get("new_recipient")
        order = request.form.get("order")

        #Error Checking
        if not new_task or not new_date or not new_status or not new_importance:
            return render_template("error.html", error="missing field(s)")

        if order == "second":
            #Updating task
            db.execute("UPDATE tasks SET task = ?, due = ?, status = ?, importance = ?, recipient = ? WHERE id = ?", new_task, new_date, new_status, new_importance, new_recipient, task_id)

            return redirect("/")

        elif order == "fourth":
            #Updating task
            db.execute("UPDATE tasks SET task = ?, due = ?, status = ?, importance = ? WHERE id = ?", new_task, new_date, new_status, new_importance, task_id)

            return redirect("/")

        elif order == "third":
            #Adding task
            db.execute("INSERT INTO tasks(task, due, status, importance, recipient, sender) VALUES(?, ?, ?, ?, ?, ?)", new_task, new_date, new_status, new_importance, new_recipient, name)

            return redirect("/")

    else:
        #Select all users names excluding self
        names = db.execute("SELECT name FROM users WHERE NOT name = ? ORDER BY name ASC", name)

        #Add new task created
        return render_template("edit.html", name=name, names=names, action="Add")

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    if request.method == "POST":
        db.execute("DELETE FROM tasks WHERE id = ?", request.form.get("id"))

    return redirect("/")