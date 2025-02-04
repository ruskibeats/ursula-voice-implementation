-- Core Universe Tables

-- Family & Relationships
CREATE TABLE family (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    relation TEXT NOT NULL,  -- father, mother, brother
    status TEXT,  -- alive, deceased, missing
    background TEXT,  -- their story
    impact TEXT,  -- how they shaped Ursula
    last_referenced TIMESTAMP
);

-- Character Stories
CREATE TABLE stories (
    id INTEGER PRIMARY KEY,
    era TEXT NOT NULL,  -- Southie, Wall Street, Present
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    characters TEXT,  -- JSON array of people involved
    location TEXT,
    impact TEXT,  -- how this shaped her character
    frequency_weight FLOAT DEFAULT 1.0  -- how often to reference
);

-- Locations
CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,  -- Boston, NY, Philly
    type TEXT,  -- medical, business, personal
    significance TEXT,
    insider_tips TEXT,  -- her local knowledge
    characters TEXT  -- JSON array of regulars
);

-- Voice Patterns
CREATE TABLE patterns (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,  -- excited, concerned, whispered
    ssml TEXT NOT NULL,  -- SSML pattern
    use_case TEXT,  -- when to use this pattern
    examples TEXT  -- example phrases
);

-- Character Traits
CREATE TABLE traits (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,  -- personality, skills, vulnerabilities
    trait TEXT NOT NULL,
    origin TEXT,  -- where this came from
    manifestation TEXT  -- how it shows up
);

-- Catchphrases
CREATE TABLE phrases (
    id INTEGER PRIMARY KEY,
    phrase TEXT NOT NULL,
    context TEXT,  -- when to use it
    city_influence TEXT,  -- Boston/NY/Philly style
    frequency FLOAT DEFAULT 1.0
); 