-- Core Identity
CREATE TABLE core_identity (
    id INTEGER PRIMARY KEY,
    origin TEXT NOT NULL,
    voice_character TEXT,
    base_personality TEXT
);

-- Relationships
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_name TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    dynamic TEXT,
    special_notes TEXT,
    interaction_history TEXT,
    last_interaction TIMESTAMP,
    UNIQUE(person_name)
);

-- Stories
CREATE TABLE stories (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    location TEXT,
    characters TEXT,
    content TEXT,
    mood TEXT,
    times_told INTEGER DEFAULT 0,
    last_told TIMESTAMP,
    success_rating FLOAT,
    UNIQUE(title)
);

-- Story Categories
CREATE TABLE story_categories (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    context TEXT,
    appropriate_for TEXT,
    UNIQUE(category)
);

-- Locations
CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    nickname TEXT,
    category TEXT,
    stories TEXT,
    characters TEXT,
    refs TEXT,
    UNIQUE(name)
);

-- Characters
CREATE TABLE characters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    full_name TEXT,
    occupation TEXT,
    stories TEXT,
    catchphrases TEXT,
    relationship_dynamic TEXT,
    last_mentioned TIMESTAMP,
    UNIQUE(name)
);

-- Interaction Patterns
CREATE TABLE interaction_patterns (
    id INTEGER PRIMARY KEY,
    pattern_type TEXT NOT NULL,
    pattern TEXT NOT NULL,
    context TEXT,
    success_rating FLOAT,
    last_used TIMESTAMP,
    metadata TEXT
);

-- Memory Updates
CREATE TABLE memory_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    context TEXT NOT NULL,
    success_rating FLOAT DEFAULT 0.0
);

-- Indexes
CREATE INDEX idx_stories_category ON stories(category);
CREATE INDEX idx_stories_mood ON stories(mood);
CREATE INDEX idx_locations_category ON locations(category);
CREATE INDEX idx_patterns_type ON interaction_patterns(pattern_type);
CREATE INDEX idx_memory_updates_category ON memory_updates(category);
CREATE INDEX idx_memory_updates_context ON memory_updates(context);

-- Views
CREATE VIEW recent_successful_patterns AS
SELECT * FROM interaction_patterns
WHERE success_rating > 0.7
ORDER BY last_used DESC;

CREATE VIEW favorite_stories AS
SELECT * FROM stories
WHERE success_rating > 0.8
ORDER BY times_told DESC; 