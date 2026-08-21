import sqlite3
import hashlib
from pathlib import Path

DB_PATH = "noteql.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            path TEXT NOT NULL,
            title TEXT,
            body TEXT,
            content_hash TEXT
            )
    """)
    conn.commit()
    conn.close()

def insert_note(path, title, body):
    note_id = hashlib.sha256(path.encode()).hexdigest()[:16]
    content_hash = hashlib.sha256(body.encode()).hexdigest()[:16]
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO notes (id, path, title, body, content_hash) VALUES (?, ?, ?, ?, ?)",
        (note_id, path, title, body, content_hash)
    )
    conn.commit()
    conn.close()

def search_notes(query):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT path, title FROM notes WHERE body LIKE ?",
        (f"%{query}%",)
    ).fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    insert_note("/fake/path/test.md", "Test Note", "maybe note about matrix multiplication")
    print(search_notes("matrix"))
