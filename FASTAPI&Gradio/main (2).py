from fastapi import FastAPI, HTTPException, Query
import sqlite3
from deep_translator import GoogleTranslator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Quotes API - Translation Mode", version="3.0")

# --- Middleware ---
# This allows your frontend (Gradio, HTML, etc.) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Connection ---
def get_conn():
    conn = sqlite3.connect("quotes.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- Endpoints ---

@app.get("/")
def root():
    return {
        "message": "Quotes API is running (Translation Mode)",
        "endpoints": {
            "all_quotes": "/quotes",
            "search": "/quotes/search/{keyword}",
            "translate": "/quotes/{id}/translate?lang=tl"
        }
    }

@app.get("/quotes")
def get_all():
    """Returns all quotes in the database."""
    conn = get_conn()
    rows = conn.execute("SELECT * FROM quotes ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/quotes/search/{keyword}")
def search(keyword: str):
    """Search for quotes by text, author, or tags."""
    conn = get_conn()
    kw = f"%{keyword}%"
    rows = conn.execute(
        "SELECT * FROM quotes WHERE text LIKE ? OR author LIKE ? OR tags LIKE ?",
        (kw, kw, kw)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/quotes/{quote_id}")
def get_one(quote_id: int):
    """Returns a specific quote by its ID."""
    conn = get_conn()
    row = conn.execute("SELECT * FROM quotes WHERE id=?", (quote_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Quote not found")
    return dict(row)

@app.get("/quotes/{quote_id}/translate")
def translate_quote(quote_id: int, lang: str = Query(..., description="tl for Filipino, ko for Korean")):
    """Fetches a quote and translates it into the chosen language."""
    if lang not in ["tl", "ko"]:
        raise HTTPException(status_code=400, detail="Use 'tl' for Filipino or 'ko' for Korean")

    conn = get_conn()
    row = conn.execute("SELECT text, author FROM quotes WHERE id=?", (quote_id,)).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Quote not found")

    try:
        # Translates the quote text
        translated = GoogleTranslator(source='auto', target=lang).translate(row["text"])
        
        return {
            "quote_id": quote_id,
            "author": row["author"],
            "original_text": row["text"],
            "target_language": "Filipino" if lang == "tl" else "Korean",
            "translated_text": translated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.get("/stats")
def stats():
    """Returns basic database counts."""
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]
    authors = conn.execute("SELECT COUNT(DISTINCT author) FROM quotes").fetchone()[0]
    conn.close()
    return {
        "total_quotes": total,
        "unique_authors": authors
    }
