from pathlib import Path
from db import init_db, insert_note

VAULT = Path('/Users/ameliali/GitHub/milynotes/milynotes vault')

def ingest():
    init_db()
    count = 0

    for md_file in VAULT.rglob("*.md"):
        body = md_file.read_text(errors="ignore")
        title = md_file.stem
        insert_note(str(md_file), title, body)
        count += 1

    print(f"ingested {count} notes")

if __name__ == "__main__":
    ingest()
