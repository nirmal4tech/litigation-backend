CREATE TABLE diary_entries (
    id SERIAL PRIMARY KEY,
    case_id TEXT NOT NULL,
    stage_slug TEXT NOT NULL,
    entry_date DATE NOT NULL,
    what_happened TEXT NOT NULL,
    personal_note TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
