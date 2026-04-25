import os
import sqlite3
from datetime import timedelta

from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = "change_this_secret_key"
app.permanent_session_lifetime = timedelta(minutes=10)


def get_db_connection():
    database_path = os.path.join(BASE_DIR, "users_new.db")
    connection = sqlite3.connect(database_path, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if username == "" or password == "":
            message = "Username and password are required."
            return render_template("register.html", message=message)

        hashed_password = generate_password_hash(password)

        try:
            connection = get_db_connection()
            connection.execute(
                "INSERT INTO users (username, password, failed_attempts) VALUES (?, ?, ?)",
                (username, hashed_password, 0)
            )
            connection.commit()
            connection.close()

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            message = "Username already exists."

    return render_template("register.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if user:
            if user["failed_attempts"] >= 3:
                connection.close()
                message = "Account temporarily locked due to too many failed attempts."
                return render_template("login.html", message=message)

            if check_password_hash(user["password"], password):
                connection.execute(
                    "UPDATE users SET failed_attempts = 0 WHERE username = ?",
                    (username,)
                )
                connection.commit()
                connection.close()

                session.permanent = True
                session["username"] = username

                return redirect(url_for("dashboard"))

            else:
                connection.execute(
                    "UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = ?",
                    (username,)
                )
                connection.commit()
                connection.close()

                message = "Invalid username or password."

        else:
            connection.close()
            message = "Invalid username or password."

    return render_template("login.html", message=message)


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session["username"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)