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
algebra professor explain matrix multiplication a year ago" and get
a useful answer. the tools that can search each silo don't understand
structure (which class, when written, what it links to). the tools
that could reason across everything (chatgpt, etc.) don't have access
to my notes and don't cite. noteql is the thing in the middle.

## who it's for

right now: me. one user, one machine, my own vault. this scoping
matters — it means i can make design decisions that assume a personal
corpus (thousands of notes, not billions of documents; single-user
ranking signals; local disk) instead of pretending to build web-scale
infrastructure.

later, maybe: other people with the same problem. but the v1 audience
is one, on purpose.

## the core bet

the interesting engineering in personal-knowledge tools is not the
llm layer — it's the retrieval layer underneath. everyone is calling
the same models. what differentiates a useful personal agent from a
generic chatbot is *what context gets retrieved and how*. most
projects in this space treat retrieval as "call a vector db, hope
for the best." noteql treats retrieval as a real systems problem:
custom storage, from-scratch inverted index, structure-aware
ranking, and a query layer richer than similarity search.

corollary: the llm is the last thing i build, not the first. the
retrieval has to be good enough to stand alone as search before an
llm ever touches it.

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

## open design questions (unresolved)

- storage format: own on-disk format vs sqlite vs json. leaning own
  format for depth of learning and resume story, but haven't
  committed. will decide when v1 forces it.
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

## why this project, honestly

i teach sql. i think about data through a relational lens. i've been
building a second brain across tools for years and consistently hit
the "i know i wrote this somewhere" problem. i'm interning on ai
tooling. the intersection of "databases and query engines" with
"retrieval systems for agents" is where i actually want to work, and
this project is the smallest honest thing i can build to demonstrate
i can work there.
