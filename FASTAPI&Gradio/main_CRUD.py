import sqlite3

DB_FILE = "quotes.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    # This allows us to access columns by name (like row['author'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the table if it doesn't exist."""
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# CRUD Operations
def create_quote(author, text):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO quotes (author, text) VALUES (?, ?)', (author, text))
    conn.commit()
    new_id = cursor.lastrow_id
    conn.close()
    return new_id

def read_all_quotes():
    conn = get_connection()
    rows = conn.execute('SELECT * FROM quotes').fetchall()
    conn.close()
    # Convert Row objects to a list of dictionaries for the API
    return [dict(row) for row in rows]

def update_quote(quote_id, author, text):
    conn = get_connection()
    conn.execute('UPDATE quotes SET author = ?, text = ? WHERE id = ?', (author, text, quote_id))
    conn.commit()
    conn.close()

def delete_quote(quote_id):
    conn = get_connection()
    conn.execute('DELETE FROM quotes WHERE id = ?', (quote_id,))
    conn.commit()
    conn.close()

# Initialize the DB immediately when this script is imported
init_db()