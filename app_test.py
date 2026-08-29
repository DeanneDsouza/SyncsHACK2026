import sqlite3

db = sqlite3.connect("database.db")

db.execute("""
INSERT INTO arts
(name, country, category, description, history,
 how_it_is_made, why_it_matters, image_url, source_url)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Warli Painting",                                      # 1
    "India",                                               # 2
    "Art & Crafts",                                       # 3
    "A traditional painting style from Maharashtra.",     # 4
    "Warli painting has been practiced for generations.",  # 5
    "The paintings use simple geometric shapes.",         # 6
    "It helps preserve cultural traditions.",              # 7
    "",                                                    # 8
    "https://ich.unesco.org/"                             # 9
))

db.execute("""
INSERT INTO arts
(name, country, category, description, history,
 how_it_is_made, why_it_matters, image_url, source_url)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Indian Oral Storytelling",
    "India",
    "Literature",
    "Traditional stories passed between generations.",
    "Oral storytelling has long been used to preserve knowledge.",
    "Stories are passed from one generation to another.",
    "It preserves cultural memory.",
    "",
    "https://ich.unesco.org/"
))

db.execute("""
INSERT INTO arts
(name, country, category, description, history,
 how_it_is_made, why_it_matters, image_url, source_url)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Indian Folk Music",
    "India",
    "Music",
    "Traditional musical practices passed through generations.",
    "Indian folk music has developed across many communities.",
    "Music is traditionally passed from one generation to another.",
    "It preserves cultural stories and traditions.",
    "",
    "https://ich.unesco.org/"
))

db.commit()
db.close()

print("Test data added!")