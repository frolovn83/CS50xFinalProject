import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import datetime
import time

# Configure application

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

@app.route("/")
@login_required
def index():
    articles = db.execute("SELECT * FROM articles")
    return render_template("index.html", articles=articles)


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/<int:id>")
@login_required
def post(id):
    id_art=id
    articles=db.execute("SELECT * FROM articles where id=?", id_art)
    comments = db.execute("SELECT * FROM coment WHERE id_article=?", id_art)
    return render_template("post.html", articles=articles, comments=comments)


@app.route("/<int:id>/del")
@login_required
def delite(id):
    id_art=id
    user = db.execute("SELECT user_id FROM articles where id=?", id_art)[0]["user_id"]
    user_log = session["user_id"]
    if user_log == user:
        db.execute("DELETE FROM articles WHERE id = ?", id_art)
        return redirect("/")
    else:
        message = "You have'n permition to delite this article"
        return render_template('post.html', message=message)


@app.route("/<int:id>/comment", methods=["GET", "POST"])
@login_required
def comment(id):
    if request.method == "POST":
        id_art=id # id статьи
        comment = request.form.get("comment") # получаем коментарий
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]    #Имя пользователя
        user_id = session["user_id"]
        user = db.execute("SELECT user_id FROM articles where id=?", id_art)[0]["user_id"]
        db.execute("INSERT INTO coment (coment, username, id_article, date, user_id) VALUES (?, ?, ?, ?, ?)", comment, username, id_art, datetime.datetime.now().strftime(" %m/%d/%Y, %H:%M:%S"), user_id)
        return redirect("/")


@app.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    id_art=id
    edit = db.execute("SELECT * FROM articles WHERE id = ?", id_art) #Получаем данные статьи
    if request.method == "POST":
        category = request.form.get("category")
        title = request.form.get("title")
        textarticle = request.form.get("textarticle")
        db.execute("UPDATE articles SET category = ?, title=?, articletext=? WHERE id = ?", category, title, textarticle, id_art)
        return redirect("/")
    return render_template("edit.html", edit=edit, id_art=id_art)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        category=request.form.get("category")
        title=request.form.get("title")
        text=request.form.get("textarticle")
        if not category:
            message = "You forgot to specify the category of the article"
            return render_template('add.html', message=message)
        if not title:
            message = "You forgot to enter the title of the article"
            return render_template('add.html', message=message)
        if not text:
            message = "You forgot to enter the text of the article"
            return render_template('add.html', message=message)
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        db.execute("INSERT INTO articles (category, title, articletext, user_name, createdate, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                       category, title, text, username, datetime.datetime.now().strftime(" %m/%d/%Y, %H:%M:%S"), session["user_id"])
        return redirect("/")
    return render_template("add.html")


#Function @Logout from CS50 Week 9, Problem Set 9 "Finance"
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        mail = request.form.get("inputemail")
        login = request.form.get("inputname")
        pswd = request.form.get("inputPassword")
        pswd1 = request.form.get("inputPasswordConfirmation")

        # Check if the user enter "Username"
        if not login:
            message = "You forgot enter user name"
            return render_template('register.html', message=message)
        if pswd != pswd1:
            message = "Passwords are not equal"
            return render_template('register.html', message=message)
        if not pswd or not pswd1:
            message = "Please check your password"
            return render_template('register.html', message=message)
        # Check passwords equality

        if pswd == pswd1:
            hashpswd = generate_password_hash(pswd)
            check = db.execute("SELECT username FROM users WHERE username = ?", login)

        if not check:
            db.execute("INSERT INTO users (username, hash, mail) VALUES(?, ?, ?)", login, hashpswd, mail)
            return render_template("login.html")

    return render_template("register.html")

#In this function I used some code from CS50 Week 9, Problem Set 9 "Finance"
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("name"):
            message = "must provide username"
            return render_template('login.html', message=message)

        # Ensure password was submitted
        if not request.form.get("password"):
            message = "must provide password"
            return render_template('login.html', message=message)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("name"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            message = "invalid username and/or password"
            return render_template('login.html', message=message)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/change", methods=["GET", "POST"])
def change():
    if request.method == "POST":

        old = request.form.get("old")
        pswd = request.form.get("newpass")
        pswdconf = request.form.get("confpass")
        # Check if the user enter "Username"
        if not old:
            message = "You forgot enter old password"
            return render_template('change.html', message=message)
        if pswd != pswdconf:
            message = "New passwords are not equal"
            return render_template('change.html', message=message)
        if not pswd or not pswdconf:
            message = "You forgot enter new password"
            return render_template('change.html', message=message)

        user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        rows = db.execute("SELECT * FROM users WHERE username = ?", user)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("old")):
            message = "Invalid password"
            return render_template('change.html', message=message)
        if pswd == pswdconf:
            hashpswd = generate_password_hash(request.form.get("newpass"))

            db.execute("UPDATE users SET hash = ? WHERE id = ?", hashpswd, session["user_id"])
            return redirect('/')
    return render_template("change.html")

