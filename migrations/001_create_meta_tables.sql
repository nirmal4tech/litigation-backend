CREATE TABLE case_types (
    id SERIAL PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL
);

CREATE TABLE stages (
    id SERIAL PRIMARY KEY,
    case_type_slug TEXT NOT NULL,
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    short_desc TEXT NOT NULL,
    UNIQUE(case_type_slug, slug)
);
