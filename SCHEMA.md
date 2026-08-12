```mermaid
erDiagram
    NOTES ||--o{ TAGS : "tagged with"
    NOTES ||--o{ LINKS : "links out"
    NOTES ||--o{ LINKS : "linked from"
    NOTES {
        string id PK
        string path
        string title
        text body
        string source
        string folder_path
        datetime created_at
        datetime modified_at
        string content_hash
    }
    TAGS {
        string note_id PK, FK
        string tag PK
    }
    LINKS {
        string from_note_id PK, FK
        string to_note_id PK, FK
    }
```
