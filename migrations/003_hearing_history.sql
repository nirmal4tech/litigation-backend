CREATE TABLE hearing_entries (
    id SERIAL PRIMARY KEY,
    case_id TEXT NOT NULL,
    raw_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE hearing_stage_selection (
    id SERIAL PRIMARY KEY,
    hearing_entry_id INTEGER REFERENCES hearing_entries(id) ON DELETE CASCADE,
    stage_slug TEXT NOT NULL,
    selected_at TIMESTAMP DEFAULT NOW()
);
