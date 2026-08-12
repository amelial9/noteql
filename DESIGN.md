# noteql — design doc

## what it is

noteql is a local-first retrieval and query engine for personal notes.
it reads notes from wherever i keep them (starting with an obsidian
vault of markdown files), builds its own storage and index, and lets
me ask questions about my own past thinking — across sources, across
time, across courses — and get back either a ranked list of relevant
notes or an llm-generated answer grounded in those notes with
citations.

it exists because my notes are fragmented across obsidian, notion,
and onenote, and no existing tool lets me ask "how did my linear
algebra professor explain matrix multiplication years ago" and get
a useful answer. the tools that can search each silo don't understand
structure (which class, when written, what it links to). the tools
that could reason across everything (chatgpt, etc.) don't have access
to my notes and don't cite. noteql is the thing in the middle.

## the core

the interesting engineering in personal-knowledge tools is not the
llm layer — it's the retrieval layer underneath. everyone is calling
the same models. what differentiates a useful personal agent from a
generic chatbot is *what context gets retrieved and how*. most
projects in this space treat retrieval as "call a vector db, hope
for the best." noteql treats retrieval as a real systems problem:
custom storage, from-scratch inverted index, structure-aware
ranking, and a query layer richer than similarity search.

## final product shape

two thin interfaces on top of one real engine:

1. a search interface: type a query, get a ranked list of matching
   notes with snippets. for browsing and reading.
2. a question-answering interface: ask a natural-language question,
   get an llm-generated answer grounded in retrieved notes, with
   citations back to the sources. for synthesis.

the retrieval engine underneath is the actual product. the two
interfaces are how i demonstrate that good retrieval infrastructure
serves both traditional search and agentic use cases.

the engine is ui-agnostic. cli and web ui are thin clients over the
same engine api — same functions, different frontends. sequencing:

- v0–v2 (engine era): cli only. no ui work while retrieval is
  being built.
- v3–v4 (interfaces era): local web ui served on localhost —
  search results view and qa view — over the same engine api.

explicitly not a hosted webpage: the whole point is local-first,
notes never leave the machine.

## build order

strict sequence, no jumping ahead:

- v0: substring search over one folder. done.
- v0.x: snippets, line numbers, case handling, tokenization.
- v1: real inverted index on disk. own storage format for notes +
  index. search across the whole vault, fast.
- v2: structure-aware ranking. use metadata (folder, tags, links,
  recency) as first-class ranking signals, not just text similarity.
- v3: add semantic search alongside keyword (hybrid retrieval).
  embeddings for notes, combined ranking.
- v4: add the qa interface. retrieved notes + question → llm →
  answer with citations. small layer on top of an already-good engine.
- later: more sources beyond obsidian, query language, whatever
  comes up.

each version has to work end-to-end and be useful to me before i
start the next one.

## design decisions

**storage: hybrid sqlite + custom index format.** metadata lives in
a single `notes` table in sqlite. the inverted index (posting
lists) lives in a custom on-disk format i write myself.

metadata is small, structured, relationally shaped (notes↔tags,
notes↔links), and accessed transactionally — point lookups and
small filtered scans. that's sqlite's design center: embedded,
row-oriented, oltp, b-tree indexed, crash-safe. no reason to
rebuild it.

the posting-list index is custom because that's where the actual
retrieval engineering lives, and it mirrors how real systems
(lucene, postgres) separate metadata storage from index storage for
different access patterns.

alternatives considered:

- duckdb: embedded but columnar/olap. wrong workload — we do
  transactional row lookups, not analytical scans.
- rocksdb / lmdb: embedded kv, but metadata is relational and
  benefits from secondary indexes and sql. no sql either.
- own row store for metadata: low-return work. the interesting
  from-scratch layer is the posting-list index, not metadata
  storage.
- pure sqlite for everything (index via fts5): outsources the exact
  layer this project exists to build from scratch.

**incremental indexing is a v1 requirement.** the index must
support incremental updates, not just bulk rebuild. notes get added
and edited; unchanged notes should be skipped on re-import. this
constrains the on-disk format from the start even if the first
implementation is bulk-rebuild only.

- change detection: content hash per note (see schema below).
- deletions: tombstones — a deleted-id set filtered at query time,
  plus periodic compaction / full rebuild — rather than in-place
  edits to posting lists. lucene-style.
- full rebuild is acceptable for v1. incremental is the design
  target the format must not preclude.

**note schema (v1, rough):**

- id: stable identifier
- path: relative path in the vault
- title
- tags
- links (outbound wikilinks / md links)
- created / modified timestamps
- content_hash: for incremental-index change detection
- body: raw text (or a pointer to it)

## open design questions (unresolved)

- record granularity: whole notes vs paragraph chunks. leaning whole
  notes for v1 — chunking is easier to add later than to remove.
- which metadata to index in v1: title, tags, links, path, created
  date, modified date. probably all of these. tbd on frontmatter.
- ranking function for v2: bm25 base + structural boosts, but the
  weights are a real design problem.
- language: python for now. from-scratch boundaries include
  storage, index, query, ranking. off-limits to build myself: the
  llm, embedding models, and (probably) the tokenizer.

## non-goals

- multi-user support
- distributed anything
- web-scale
- real-time indexing (batch is fine)
- being a note-taking tool (obsidian is the note-taking tool)
- being a general search engine (this is for personal knowledge
  specifically, and design decisions assume that)
