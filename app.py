import os
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

import content_data
import ai_helper  # OPTIONAL - only runs if ANTHROPIC_API_KEY is set. See ai_helper.py.

app = Flask(__name__)
app.secret_key = "your-secret-key"


# ============================================================
# DATABASE
# ============================================================

def get_db():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """
    Create tables that don't already exist. Safe to run on every
    startup. ai_cache stores optional AI "did you know" enrichment,
    keyed by art form name + category - it's only ever written to if
    ANTHROPIC_API_KEY is set (see ai_helper.py). The app works fully
    without it.
    """
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            country TEXT NOT NULL,
            hobbies TEXT NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS ai_cache (
            cache_key TEXT PRIMARY KEY,
            extra_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    db.close()


init_db()


# ============================================================
# CATEGORIES / COUNTRIES
# ============================================================

COUNTRIES = ["China", "India", "Australia"]

# Canonical category names used EVERYWHERE (signup form, session,
# content_data.py keys, routes). One source of truth for these
# strings avoids the old "Art/Crafts" vs "Art & Crafts" mismatch bug.
CATEGORIES = ["Music", "Art & Crafts", "Literature"]


# ============================================================
# ART FORM SELECTION  (curated content, no live filtering)
# ============================================================

def get_today_pick(country, category):
    """
    First-round version: each (country, category) combo has exactly
    one standard, fixed entry in content_data.py - no rotation yet.
    Named get_today_pick() to keep this a one-line swap if you bring
    daily rotation back later (change ART_DATA's value to a list and
    date-seed a random.choice() over it, same as the previous version).
    """
    return content_data.ART_DATA.get(country, {}).get(category)


def build_art_view(country, category):
    """
    Returns the dict the templates render, or None if nothing is
    curated yet for this country + category. Optionally merges in an
    AI "did you know" fact - entirely skipped if no API key is set.
    """
    entry = get_today_pick(country, category)
    if not entry:
        return None

    art = dict(entry)  # shallow copy - don't mutate content_data.py's data

    if os.environ.get("ANTHROPIC_API_KEY"):
        db = get_db()
        extra = ai_helper.maybe_enrich(db, art, country, category)
        db.close()
        if extra:
            art.update(extra)

    return art


# ============================================================
# INDEX
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user["password"], password):
            session["username"] = user["username"]
            session["country"] = user["country"]
            session["hobbies"] = user["hobbies"]
            return redirect(url_for("homepage"))

        return "Invalid username or password."

    return render_template("login.html")


# ============================================================
# SIGNUP
# ============================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        country = request.form.get("country")
        hobby = request.form.get("hobbies")

        if country not in COUNTRIES:
            return "Please select a valid country."

        if hobby not in CATEGORIES:
            return "Please select a valid hobby."

        hashed_password = generate_password_hash(password)

        db = get_db()

        try:
            db.execute(
                """
                INSERT INTO users (username, email, password, country, hobbies)
                VALUES (?, ?, ?, ?, ?)
                """,
                (username, email, hashed_password, country, hobby)
            )
            db.commit()

        except sqlite3.IntegrityError:
            db.close()
            return "Username or email already exists."

        db.close()

        return redirect(url_for("login"))

    return render_template("signup.html", categories=CATEGORIES)


# ============================================================
# HOMEPAGE  (the user's original country + hobby)
# ============================================================

@app.route("/homepage")
def homepage():

    country = session.get("country")
    category = session.get("hobbies")

    if not country or not category:
        return redirect(url_for("pickCountry"))

    art = build_art_view(country, category)

    return render_template(
        "home_page.html",
        art=art,
        country=country,
        category=category
    )


# ============================================================
# ART / CRAFTS PAGE
# ============================================================

@app.route("/crafts")
def crafts():

    country = session.get("country")
    if not country:
        return redirect(url_for("pickCountry"))

    art = build_art_view(country, "Art & Crafts")

    return render_template("craft_page.html", art=art, country=country)


# ============================================================
# LITERATURE PAGE
# ============================================================

@app.route("/literature")
def literature():

    country = session.get("country")
    if not country:
        return redirect(url_for("pickCountry"))

    art = build_art_view(country, "Literature")

    return render_template("Literature_page.html", art=art, country=country)


# ============================================================
# MUSIC PAGE
# ============================================================

@app.route("/music")
def music():

    country = session.get("country")
    if not country:
        return redirect(url_for("pickCountry"))

    art = build_art_view(country, "Music")

    return render_template("music.html", art=art, country=country)


# ============================================================
# PICK COUNTRY
# ============================================================

@app.route("/pickCountry", methods=["GET", "POST"])
def pickCountry():

    if request.method == "POST":
        country = request.form.get("country")
        session["country"] = country
        return redirect(url_for("homepage"))

    return render_template("pick_country.html")


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
