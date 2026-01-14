CREATE TABLE cost_entries (
    id SERIAL PRIMARY KEY,
    case_id TEXT NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    paid_to TEXT NOT NULL,
    reason TEXT,
    entry_date DATE NOT NULL,
    stage_slug TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
