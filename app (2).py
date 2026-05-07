import gradio as gr
import sqlite3
import requests
import os
from collections import Counter

# ── API Key ────────────────────────────────────────────────────────────────────
# Make sure you have "GROQ_API_KEY" in your Hugging Face Space Settings > Secrets!
_raw_key = os.environ.get("GROQ_API_KEY", "")
GROQ_API_KEY = _raw_key.strip() if _raw_key else ""

# ── Bundled Quotes ─────────────────────────────────────────────────────────────
BUNDLED_QUOTES = [
    ("“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”", "Albert Einstein", "change, thinking, world"),
    ("“It is our choices that show what we truly are, far more than our abilities.”", "J.K. Rowling", "choices, abilities, character"),
    ("“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”", "Albert Einstein", "inspirational, life, miracle"),
    ("“The person who has not pleasure in a good novel must be intolerably stupid.”", "Jane Austen", "books, humor, classic"),
    ("“Imperfection is beauty, madness is genius and it is better to be absolutely ridiculous than absolutely boring.”", "Marilyn Monroe", "be-yourself, inspirational"),
    ("“Try not to become a man of success. Rather become a man of value.”", "Albert Einstein", "success, value"),
    ("“It is better to be hated for what you are than to be loved for what you are not.”", "Andre Gide", "life, love, authenticity"),
    ("“I have not failed. I have just found 10,000 ways that will not work.”", "Thomas A. Edison", "failure, inspirational, persistence"),
    ("“A woman is like a tea bag; you never know how strong it is until it is in hot water.”", "Eleanor Roosevelt", "strength, women"),
    ("“In the middle of every difficulty lies opportunity.”", "Albert Einstein", "difficulty, opportunity, motivational"),
    ("“Life is what happens when you are busy making other plans.”", "John Lennon", "life, plans, reflective"),
    ("“The future belongs to those who believe in the beauty of their dreams.”", "Eleanor Roosevelt", "future, dreams, inspirational"),
    ("“It does not matter how slowly you go as long as you do not stop.”", "Confucius", "perseverance, motivational"),
    ("“Everything you have ever wanted is on the other side of fear.”", "George Addair", "fear, courage, motivational"),
    ("“Success is not final, failure is not fatal: it is the courage to continue that counts.”", "Winston Churchill", "success, failure, courage"),
    ("“Happiness is not something ready-made. It comes from your own actions.”", "Dalai Lama", "happiness, actions"),
    ("“If you tell the truth, you do not have to remember anything.”", "Mark Twain", "truth, humor, wisdom"),
    ("“The only way to do great work is to love what you do.”", "Steve Jobs", "work, love, passion"),
    ("“Not all those who wander are lost.”", "J.R.R. Tolkien", "adventure, wandering, fantasy"),
    ("“You only live once, but if you do it right, once is enough.”", "Mae West", "life, humor, inspirational"),
    ("“In three words I can sum up everything I have learned about life: it goes on.”", "Robert Frost", "life, wisdom"),
    ("“To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.”", "Ralph Waldo Emerson", "authenticity, self, inspirational"),
    ("“Be yourself; everyone else is already taken.”", "Oscar Wilde", "humor, authenticity, identity"),
    ("“Two things are infinite: the universe and human stupidity; and I am not sure about the universe.”", "Albert Einstein", "humor, science, wisdom"),
    ("“A reader lives a thousand lives before he dies. The man who never reads lives only one.”", "George R.R. Martin", "reading, books, life"),
    ("“You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose.”", "Dr. Seuss", "inspirational, children, choices"),
    ("“Do one thing every day that scares you.”", "Eleanor Roosevelt", "courage, fear, daily"),
    ("“The secret of getting ahead is getting started.”", "Mark Twain", "motivation, action, success"),
    ("“It always seems impossible until it is done.”", "Nelson Mandela", "motivation, perseverance, achievement"),
    ("“Believe you can and you are halfway there.”", "Theodore Roosevelt", "belief, motivation, confidence"),
]

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
    c.execute("SELECT COUNT(*) FROM quotes")
    if c.fetchone()[0] == 0:
        for text, author, tags in BUNDLED_QUOTES:
            c.execute("INSERT INTO quotes (text, author, tags) VALUES (?, ?, ?)", (text, author, tags))
    conn.commit()
    conn.close()

init_db()

def get_all_quotes():
    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()
    c.execute("SELECT id, text, author, tags FROM quotes ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows

def refresh_table():
    rows = get_all_quotes()
    return [[r[0], r[2], r[1][:60] + ("..." if len(r[1]) > 60 else ""), r[3]] for r in rows]

# ── Groq AI Logic ──────────────────────────────────────────────────────────────
def ask_groq(prompt):
    if not GROQ_API_KEY:
        return "ERROR: Groq API Key is missing. Go to Settings > Secrets in Hugging Face."
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "max_tokens": 800},
            timeout=20
        )
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"AI Error: {result.get('error', {}).get('message', 'Unknown error')}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

# ── Features ──────────────────────────────────────────────────────────────────
def translate_single_quote(quote_id, language):
    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()
    c.execute("SELECT text FROM quotes WHERE id = ?", (quote_id,))
    row = c.fetchone()
    conn.close()
    if not row: return "Quote not found."
    target = "Filipino" if "Filipino" in language else "Korean"
    return ask_groq(f"Translate this to {target}. Return only the translation: {row[0]}")

def get_references():
    rows = get_all_quotes()[:3] # Limit to 3 authors to prevent timeouts
    output = "📚 AUTHOR REFERENCES\n" + "="*30 + "\n\n"
    for _, t, a, _ in rows:
        ref = ask_groq(f"Tell me 2 famous books written by {a} and one fun fact.")
        output += f"AUTHOR: {a}\n{ref}\n\n" + "-"*30 + "\n"
    return output

def get_mood_quotes(mood, language):
    rows = get_all_quotes()[:10]
    text_blob = "\n".join([f"{t} - {a}" for _, t, a, _ in rows])
    return ask_groq(f"Pick 2 quotes from this list for mood '{mood}' and translate to {language}:\n{text_blob}")

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
    return ask_groq(f"Deep dive into this quote: '{row[0]}' by {row[1]}. Explain the meaning and provide a {language} translation.")

def show_stats():
    rows = get_all_quotes()
    authors = Counter(a for _, _, a, _ in rows)
    return f"Total Quotes: {len(rows)}\nUnique Authors: {len(authors)}"

# ── UI ─────────────────────────────────────────────────────────────────────────
LANG_CHOICES = ["Filipino (Tagalog)", "Korean (한국어)"]
MOOD_CHOICES = ["inspirational", "motivational", "philosophical", "humorous", "reflective"]

with gr.Blocks(theme=gr.themes.Soft(primary_hue="teal")) as app:
    gr.Markdown("# 📜 Quotes Explorer (International Edition)")

    with gr.Tab("Browse Quotes"):
        table = gr.Dataframe(headers=["ID", "Author", "Text (preview)", "Tags"], value=refresh_table())
        gr.Button("Refresh List").click(refresh_table, outputs=table)

    with gr.Tab("Translate"):
        with gr.Row():
            tr_id = gr.Number(label="Quote ID", value=1, precision=0)
            tr_lang = gr.Dropdown(choices=LANG_CHOICES, value="Filipino (Tagalog)", label="Language")
        tr_out = gr.Textbox(label="Result", lines=5)
        gr.Button("Translate").click(translate_single_quote, inputs=[tr_id, tr_lang], outputs=tr_out)

    with gr.Tab("Author References"):
        ref_out = gr.Textbox(label="Famous Works & Facts", lines=15)
        gr.Button("Load References", variant="primary").click(get_references, outputs=ref_out)

    with gr.Tab("Mood Picker"):
        with gr.Row():
            m_in = gr.Dropdown(choices=MOOD_CHOICES, label="Mood")
            ml_in = gr.Dropdown(choices=LANG_CHOICES, label="Language")
        m_out = gr.Textbox(label="Quotes for your mood", lines=10)
        gr.Button("Find Mood").click(get_mood_quotes, inputs=[m_in, ml_in], outputs=m_out)

    with gr.Tab("Deep Dive"):
        with gr.Row():
            dd_id = gr.Number(label="Quote ID", value=1, precision=0)
            dd_lang = gr.Dropdown(choices=LANG_CHOICES, label="Language")
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