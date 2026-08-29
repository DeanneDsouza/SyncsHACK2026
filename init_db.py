import sqlite3

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    country TEXT NOT NULL,
    hobbies TEXT NOT NULL
)
""")

# Arts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS arts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    history TEXT,
    how_it_is_made TEXT,
    why_it_matters TEXT,
    image_url TEXT,
    source_url TEXT
)
""")

connection.commit()
connection.close()

print("Database created!")