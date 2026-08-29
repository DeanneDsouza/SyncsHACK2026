# app.py
#
# A simple signup/login app using Flask + SQLite (Python's built-in
# sqlite3 module) + Werkzeug's password hashing (already included with Flask).
# No JavaScript is used anywhere — every "step" is just a regular page load.

import sqlite3
import re
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Needed so Flask can use "session" (a small, secure place to temporarily
# store step-1 signup data before step 2 is submitted). In a real project
# keep this secret and out of source control — fine as-is for local testing.
app.secret_key = "dev-secret-key-change-this-later"

DB_PATH = "users.db"


def get_db():
    """Open a connection to the SQLite database file."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db():
    """Create the users table if it doesn't already exist."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            interests TEXT,
            country TEXT
        )
    """)
    conn.commit()
    conn.close()


# ---------- HOME / WELCOME PAGE ----------
@app.route("/")
def welcome():
    return render_template("welcome.html")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            # Login successful. In a bigger app you'd set up a proper
            # logged-in session here. For now, just send them somewhere.
            return redirect(url_for("welcome"))
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)


# ---------- SIGNUP STEP 1: account details ----------
@app.route("/signup", methods=["GET", "POST"])
def signup_step1():
    errors = {}

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # --- Validation ---
        email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if not re.match(email_pattern, email):
            errors["email"] = "Enter a valid email address."

        has_min_length = len(password) >= 8
        has_letter = re.search(r"[A-Za-z]", password) is not None
        has_number = re.search(r"[0-9]", password) is not None
        if not (has_min_length and has_letter and has_number):
            errors["password"] = (
                "Password must be at least 8 characters and include a letter and a number."
            )

        if password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."

        if not username:
            errors["username"] = "Username is required."
        else:
            conn = get_db()
            existing = conn.execute(
                "SELECT id FROM users WHERE username = ? OR email = ?",
                (username, email),
            ).fetchone()
            conn.close()
            if existing:
                errors["username"] = "Username or email is already taken."

        if not errors:
            # Save step-1 data temporarily in the session, then move to step 2.
            session["signup_username"] = username
            session["signup_email"] = email
            session["signup_password"] = password  # hashed later, in step 2
            return redirect(url_for("signup_step2"))

    return render_template("signup_step1.html", errors=errors)


# ---------- SIGNUP STEP 2: interests & country ----------
@app.route("/signup/profile", methods=["GET", "POST"])
def signup_step2():
    # If someone jumps straight to this URL without doing step 1 first,
    # send them back to step 1.
    if "signup_username" not in session:
        return redirect(url_for("signup_step1"))

    errors = {}

    if request.method == "POST":
        interests = request.form.get("interests", "")
        country = request.form.get("country", "")

        # Same rule you had in JavaScript, now enforced server-side too.
        if interests == "ai-arts":
            errors["interests"] = "AI Arts are not allowed here."

        if not errors:
            username = session["signup_username"]
            email = session["signup_email"]
            password = session["signup_password"]
            password_hash = generate_password_hash(password)

            conn = get_db()
            conn.execute(
                """
                INSERT INTO users (username, email, password_hash, interests, country)
                VALUES (?, ?, ?, ?, ?)
                """,
                (username, email, password_hash, interests, country),
            )
            conn.commit()
            conn.close()

            # Clear the temporary signup data now that the account is created.
            session.pop("signup_username", None)
            session.pop("signup_email", None)
            session.pop("signup_password", None)

            return redirect(url_for("login"))

    return render_template("signup_step2.html", errors=errors)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)