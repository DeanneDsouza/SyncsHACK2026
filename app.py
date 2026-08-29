from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import requests
import random
import hashlib
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import ai_helper

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
    startup - CREATE TABLE IF NOT EXISTS is a no-op once the table
    is there. ai_cache stores AI-generated wiki sections keyed by a
    hash of the record's name + description (see ai_helper.py).
    """
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS ai_cache (
            cache_key TEXT PRIMARY KEY,
            sections_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    db.close()


init_db()


# ============================================================
# COUNTRY CODES
# ============================================================

COUNTRY_CODES = {
    "Australia": "AU",
    "China": "CN",
    "India": "IN"
}

# Canonical category names used EVERYWHERE in the app (signup form,
# session, filtering logic, routes). Keeping one single source of
# truth for these strings is what was breaking things before -
# the signup form said "Art/Crafts" while the filter checked for
# "Art & Crafts", so nothing ever matched.
CATEGORIES = ["Music", "Art & Crafts", "Literature"]


# ============================================================
# UNESCO API
# ============================================================

UNESCO_URL = (
    "https://data.unesco.org/api/explore/v2.1/"
    "catalog/datasets/ich001/records"
)


def get_unesco_records(country_code):
    """
    Get UNESCO Intangible Cultural Heritage records
    for one country.
    """

    params = {
        "where": f"countries='{country_code}'",
        "limit": 100
    }

    try:
        response = requests.get(
            UNESCO_URL,
            params=params,
            timeout=10
        )

        print("UNESCO status:", response.status_code)

        if response.status_code != 200:
            print("UNESCO API error:", response.text)
            return []

        data = response.json()

        return data.get("results", [])

    except requests.RequestException as e:
        print("UNESCO connection error:", e)
        return []


# ============================================================
# CATEGORY FILTERING
# ============================================================

ART_KEYWORDS = {
    "handicrafts", "craft", "crafts", "carving", "wood carving",
    "weaving", "textile", "embroidery", "pottery", "ceramics",
    "metalworking", "decorative arts", "architecture", "painting",
    "traditional tools", "craft workers", "artisans", "artisan"
}

MUSIC_KEYWORDS = {
    "music", "vocal music", "instrumental music", "singing",
    "polyphonic singing", "song", "songs", "dance",
    "performing arts", "musical"
}

LITERATURE_KEYWORDS = {
    "oral tradition", "oral culture", "storytelling", "stories",
    "poetry", "literature", "epic", "legend", "legends",
    "ballad", "ballads", "folklore", "narrative"
}


def get_concepts(record):
    """Extract UNESCO concepts from a record (primary + secondary)."""
    concepts = []
    primary = record.get("concepts_primary_names", [])
    secondary = record.get("concepts_secondary_names", [])

    if isinstance(primary, list):
        concepts.extend(primary)
    if isinstance(secondary, list):
        concepts.extend(secondary)

    return [str(x).lower().strip() for x in concepts]


def record_matches_category(record, category):
    """Decide whether a UNESCO record belongs to Art & Crafts, Music or Literature."""

    concepts = get_concepts(record)
    title = str(record.get("title_en", "")).lower()
    description = str(record.get("description_en", "")).lower()

    if category == "Art & Crafts":
        for concept in concepts:
            if concept in ART_KEYWORDS:
                return True
            for keyword in ART_KEYWORDS:
                if keyword in concept:
                    return True

        art_words = [
            "craft", "carving", "weaving", "embroidery", "pottery",
            "ceramic", "woodwork", "handicraft", "traditional craft"
        ]
        for word in art_words:
            if word in title or word in description:
                return True
        return False

    if category == "Music":
        for concept in concepts:
            if concept in MUSIC_KEYWORDS:
                return True
            for keyword in MUSIC_KEYWORDS:
                if keyword in concept:
                    return True

        music_words = [
            "music", "song", "singing", "singer", "choir",
            "musical", "instrument"
        ]
        for word in music_words:
            if word in title or word in description:
                return True
        return False

    if category == "Literature":
        for concept in concepts:
            if concept in LITERATURE_KEYWORDS:
                return True
            for keyword in LITERATURE_KEYWORDS:
                if keyword in concept:
                    return True

        literature_words = [
            "oral tradition", "oral culture", "storytelling", "poetry",
            "poem", "legend", "epic", "ballad", "folklore", "story"
        ]
        for word in literature_words:
            if word in title or word in description:
                return True
        return False

    return False


def filter_records_by_category(records, category):
    """Filter UNESCO records according to a category."""
    return [r for r in records if record_matches_category(r, category)]


# ============================================================
# RECORD NORMALIZATION
# ============================================================
#
# The UNESCO API returns raw fields like title_en / description_en /
# http_url_en / main_image_url. Every template in this app should
# read from ONE consistent shape instead of raw API field names, so
# if UNESCO changes their schema we only fix it in one place.
#
# NOTE: the UNESCO ich001 dataset does not provide separate
# "history" / "how it's made" / "why it matters" fields - only a
# single description. So those sections are left out of the
# normalized record rather than being invented.

def normalize_record(record):
    if not record:
        return None

    return {
        "name": record.get("title_en"),
        "description": record.get("description_en"),
        "source_url": record.get("http_url_en"),
        "image_url": record.get("main_image_url"),
        "inscription_year": record.get("inscription_year"),
        "concepts": record.get("concepts_secondary_names") or record.get("concepts_primary_names"),
    }


def get_single_record(country, category):
    """
    Get exactly ONE UNESCO record for a country + category,
    seeded by today's date so it stays the same "art form of the
    day" all day and only changes once per day, instead of
    re-randomizing on every page refresh.
    """

    country_code = COUNTRY_CODES.get(country)
    if not country_code:
        return None

    records = get_unesco_records(country_code)
    if not records:
        return None

    filtered_records = filter_records_by_category(records, category)

    print("--------------------------------")
    print("Country:", country)
    print("Category:", category)
    print("UNESCO records:", len(records))
    print("Filtered records:", len(filtered_records))
    print("--------------------------------")

    if not filtered_records:
        return None

    seed_str = f"{country}-{category}-{datetime.date.today().isoformat()}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    rng = random.Random(seed)

    return rng.choice(filtered_records)


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

            print("Logged in user:", username)
            print("Country:", user["country"])
            print("Hobby:", user["hobbies"])

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

        # Guard against garbage/forged values - only accept the
        # exact category strings the rest of the app expects.
        if country not in COUNTRY_CODES:
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

    if not country:
        return redirect(url_for("pickCountry"))

    if not category:
        return redirect(url_for("pickCountry"))

    record = get_single_record(country, category)
    art = normalize_record(record)

    if art:
        db = get_db()
        art["sections"] = ai_helper.generate_sections(
            db, art["name"], art["description"], country, category
        )
        db.close()

    return render_template(
        "home_page.html",
        art=art,
        country=country,
        category=category
    )


# ============================================================
# ART / CRAFTS PAGE  (one record, fixed category)
# ============================================================

@app.route("/crafts")
def crafts():

    country = session.get("country")
    if not country:
        return redirect(url_for("pickCountry"))

    record = get_single_record(country, "Art & Crafts")
    art = normalize_record(record)

    if art:
        db = get_db()
        art["sections"] = ai_helper.generate_sections(
            db, art["name"], art["description"], country, "Art & Crafts"
        )
        db.close()

    return render_template(
        "craft_page.html",
        art=art,
        country=country
    )


# ============================================================
# LITERATURE PAGE  (one record, fixed category)
# ============================================================

@app.route("/literature")
def literature():

    country = session.get("country")
    if not country:
        return redirect(url_for("pickCountry"))

    record = get_single_record(country, "Literature")
    art = normalize_record(record)

    if art:
        db = get_db()
        art["sections"] = ai_helper.generate_sections(
            db, art["name"], art["description"], country, "Literature"
        )
        db.close()

    return render_template(
        "Literature_page.html",
        art=art,
        country=country
    )


# ============================================================
# MUSIC PAGE  (one record, fixed category)
# ============================================================

@app.route("/music")
def music():

    country = session.get("country")
    if not country:
        return redirect(url_for("pickCountry"))

    record = get_single_record(country, "Music")
    art = normalize_record(record)

    if art:
        db = get_db()
        art["sections"] = ai_helper.generate_sections(
            db, art["name"], art["description"], country, "Music"
        )
        db.close()

    return render_template(
        "music.html",
        art=art,
        country=country
    )


# ============================================================
# PICK COUNTRY
# ============================================================

@app.route("/pickCountry", methods=["GET", "POST"])
def pickCountry():

    if request.method == "POST":
        country = request.form.get("country")
        session["country"] = country
        print("Selected country:", country)
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
