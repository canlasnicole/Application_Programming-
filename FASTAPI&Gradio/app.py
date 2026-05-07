import gradio as gr
import sqlite3
import requests
import os
from collections import Counter

# ── API Key & Config ──────────────────────────────────────────────────────────
_raw_key = os.environ.get("GROQ_API_KEY", "")
GROQ_API_KEY = _raw_key.strip() if _raw_key else ""
BACKEND_URL = "http://127.0.0.1:8000"

# ── DB Setup ───────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT NOT NULL,
            tags TEXT DEFAULT ''
        )
    """)
    try:
        c.execute("ALTER TABLE quotes ADD COLUMN tags TEXT DEFAULT ''")
    except:
        pass 
    conn.commit()
    conn.close()

init_db()

def get_all_quotes():
    """Fetches quotes in chronological order (1-30)."""
    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()
    # Dito natin sinisigurado na sunod-sunod ang ID
    c.execute("SELECT id, text, author, tags FROM quotes ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    return rows

def refresh_table():
    rows = get_all_quotes()
    return [[r[0], r[2], r[1][:60] + ("..." if len(r[1]) > 60 else ""), r[3]] for r in rows]

# ── Groq AI Logic ──────────────────────────────────────────────────────────────
def ask_groq(prompt):
    if not GROQ_API_KEY:
        return "ERROR: Groq API Key is missing."
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "max_tokens": 800},
            timeout=20
        )
        result = response.json()
        return result["choices"][0]["message"]["content"] if "choices" in result else "AI Error"
    except Exception as e:
        return f"Connection Error: {str(e)}"

# ── All Your Features (Preserved) ─────────────────────────────────────────────
def translate_single_quote(quote_id, language):
    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()
    c.execute("SELECT text FROM quotes WHERE id = ?", (quote_id,))
    row = c.fetchone()
    conn.close()
    if not row: return "Quote not found."
    return ask_groq(f"Translate this to {language}: {row[0]}")

def get_references():
    rows = get_all_quotes()[:3]
    output = "📚 AUTHOR REFERENCES\n" + "="*30 + "\n\n"
    for _, t, a, _ in rows:
        ref = ask_groq(f"Tell me 2 famous books written by {a} and one fun fact.")
        output += f"AUTHOR: {a}\n{ref}\n\n" + "-"*30 + "\n"
    return output

def get_mood_quotes(mood, language):
    rows = get_all_quotes()[:10]
    text_blob = "\n".join([f"{t} - {a}" for _, t, a, _ in rows])
    return ask_groq(f"Pick 2 quotes for mood '{mood}' and translate to {language}:\n{text_blob}")

def word_count_analysis():
    rows = get_all_quotes()
    output = "ID | Words | Author\n" + "-"*30 + "\n"
    for qid, text, author, _ in rows:
        output += f"{qid} | {len(text.split())} | {author}\n"
    return output

def search_quotes(keyword):
    rows = get_all_quotes()
    matches = [f"{t} - {a}" for _, t, a, tg in rows if keyword.lower() in t.lower() or keyword.lower() in a.lower()]
    return "\n\n".join(matches) if matches else "No matches found."

def deep_dive(quote_id, language):
    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()
    c.execute("SELECT text, author FROM quotes WHERE id = ?", (quote_id,))
    row = c.fetchone()
    conn.close()
    if not row: return "Quote ID not found."
    return ask_groq(f"Deep dive into: '{row[0]}' by {row[1]}. Explain meaning and translate to {language}.")

def show_stats():
    rows = get_all_quotes()
    authors = Counter(a for _, _, a, _ in rows)
    return f"Total Quotes: {len(rows)}\nUnique Authors: {len(authors)}"

# ── UI Layout ──────────────────────────────────────────────────────────────────
with gr.Blocks(theme=gr.themes.Soft(primary_hue="teal")) as app:
    gr.Markdown("# 📜 Quotes Explorer (Sequential Edition)")

    with gr.Tab("Browse Quotes"):
        table = gr.Dataframe(headers=["ID", "Author", "Text (preview)", "Tags"], value=refresh_table())
        gr.Button("Refresh List").click(refresh_table, outputs=table)

    with gr.Tab("Translate"):
        with gr.Row():
            tr_id = gr.Number(label="Quote ID", value=1, precision=0)
            tr_lang = gr.Dropdown(choices=["Filipino (Tagalog)", "Korean (한국어)"], value="Filipino (Tagalog)", label="Language")
        tr_out = gr.Textbox(label="Result", lines=5)
        gr.Button("Translate").click(translate_single_quote, inputs=[tr_id, tr_lang], outputs=tr_out)

    with gr.Tab("Author References"):
        ref_out = gr.Textbox(label="Famous Works & Facts", lines=15)
        gr.Button("Load References", variant="primary").click(get_references, outputs=ref_out)

    with gr.Tab("Mood Picker"):
        with gr.Row():
            m_in = gr.Dropdown(choices=["inspirational", "motivational", "reflective"], label="Mood")
            ml_in = gr.Dropdown(choices=["Filipino (Tagalog)", "Korean (한국어)"], label="Language")
        m_out = gr.Textbox(label="Quotes for your mood", lines=10)
        gr.Button("Find Mood").click(get_mood_quotes, inputs=[m_in, ml_in], outputs=m_out)

    with gr.Tab("Deep Dive"):
        with gr.Row():
            dd_id = gr.Number(label="Quote ID", value=1, precision=0)
            dd_lang = gr.Dropdown(choices=["Filipino (Tagalog)", "Korean (한국어)"], label="Language")
        dd_out = gr.Textbox(label="Full Analysis", lines=15)
        gr.Button("Analyze").click(deep_dive, inputs=[dd_id, dd_lang], outputs=dd_out)

    with gr.Tab("Search & Word Count"):
        with gr.Row():
            with gr.Column():
                s_in = gr.Textbox(label="Search keyword")
                s_out = gr.Textbox(label="Results", lines=10)
                gr.Button("Search").click(search_quotes, inputs=s_in, outputs=s_out)
            with gr.Column():
                wc_out = gr.Textbox(label="Word Count Report", lines=10)
                gr.Button("Run Analysis").click(word_count_analysis, outputs=wc_out)

    with gr.Tab("Statistics"):
        st_out = gr.Textbox(label="Database Stats")
        gr.Button("Show Stats").click(show_stats, outputs=st_out)

app.launch()