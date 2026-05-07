from fastapi import FastAPI, HTTPException, Query
import sqlite3
from deep_translator import GoogleTranslator
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel # Added for better data handling

app = FastAPI(title="Quotes API - Full CRUD & Translation", version="3.0")

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models (For POST and PUT) ---
class QuoteCreate(BaseModel):
    author: str
    text: str
    tags: str = "general"

# --- Database Connection ---
def get_conn():
    conn = sqlite3.connect("quotes.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- READ ENDPOINTS (You already have these) ---

@app.get("/quotes")
def get_all():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM quotes ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- WRITE ENDPOINTS (The "CRUD" parts you need to add) ---

@app.post("/quotes")
def create_quote(quote: QuoteCreate):
    """CREATE: Add a new quote to the database."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quotes (author, text, tags) VALUES (?, ?, ?)",
        (quote.author, quote.text, quote.tags)
    )
    conn.commit()
    new_id = cursor.lastrow_id
    conn.close()
    return {"message": "Quote created", "id": new_id}

@app.put("/quotes/{quote_id}")
def update_quote(quote_id: int, quote: QuoteCreate):
    """UPDATE: Edit an existing quote."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE quotes SET author = ?, text = ?, tags = ? WHERE id = ?",
        (quote.author, quote.text, quote.tags, quote_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Quote updated"}

@app.delete("/quotes/{quote_id}")
def delete_quote(quote_id: int):
    """DELETE: Remove a quote."""
    conn = get_conn()
    conn.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
    conn.commit()
    conn.close()
    return {"message": f"Quote {quote_id} deleted"}

# --- TRANSLATION ENDPOINT (Keep your original logic here) ---
@app.get("/quotes/{quote_id}/translate")
def translate_quote(quote_id: int, lang: str = Query(..., description="tl or ko")):
    # ... (Keep your original translation code here) ...
    pass