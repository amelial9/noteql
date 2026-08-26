## 2026-08-21
- v0.5 DONE. full pipeline runs on real vault.
  - db.py: sqlite storage, notes table (id/path/title/body/content_hash),
    insert_note + search_notes (dumb LIKE scan). ids = hash(path),
    content_hash = hash(body). INSERT OR REPLACE = idempotent.
  - ingest.py: walks vault, reads each .md, inserts. 86 notes ingested.
  - confirmed: re-running ingest doesn't duplicate (idempotent).
- decided: sqlite stores actual note body (option A), not just pointers.
- decided: all cols TEXT (sqlite type affinity — no real varchar/nvarchar).
- images: stored as text refs (![[x.png]]) in body, not touched otherwise.
- formatting cleanup (frontmatter stripping, image-ref tokens) = deferred to v1.

## next
- [ ] v1: tokenizer — text -> terms. `re.findall(r"[a-z0-9]+", text.lower())`
- [ ] v1: build inverted index in memory (dict[term, set[note_id]]) during ingest
- [ ] v1: search via index instead of LIKE scan
- [ ] v1: persist index to disk (custom on-disk format — the from-scratch part)

