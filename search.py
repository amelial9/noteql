import sys
from pathlib import Path

VAULT = Path('/Users/ameliali/GitHub/milynotes/milynotes vault')

def search(query):
    for md_file in VAULT.rglob("*.md"):
        text = md_file.read_text(errors="ignore")
        if query.lower() in text.lower():
            print(md_file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Search: ").strip()
    if not query:
        sys.exit("No search term provided.")
    search(query)
