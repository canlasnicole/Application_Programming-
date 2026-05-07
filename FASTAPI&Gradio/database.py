import sqlite3

def create_table():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        author TEXT,
        tags TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_quotes(quotes):
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    for q in quotes:
        cursor.execute("""
        INSERT INTO quotes (text, author, tags)
        VALUES (?, ?, ?)
        """, (q["text"], q["author"], ", ".join(q["tags"])))

    conn.commit()
    conn.close()