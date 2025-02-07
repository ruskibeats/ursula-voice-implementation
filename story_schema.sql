-- Story-related tables schema

-- Background Stories
CREATE TABLE IF NOT EXISTS background_stories (
    id SERIAL PRIMARY KEY,
    era TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    characters TEXT,  -- JSON array
    location TEXT,
    mood TEXT,
    frequency_weight FLOAT DEFAULT 1.0
);

-- Character Backstories
CREATE TABLE IF NOT EXISTS character_backstories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    relationship TEXT NOT NULL,
    era TEXT NOT NULL,
    background TEXT NOT NULL,
    status TEXT NOT NULL
);

-- Story Locations
CREATE TABLE IF NOT EXISTS story_locations (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    era TEXT NOT NULL,
    description TEXT NOT NULL,
    significance TEXT,
    regular_characters TEXT,  -- JSON array
    stories TEXT  -- JSON array
);

-- Life Philosophies
CREATE TABLE IF NOT EXISTS life_philosophies (
    id SERIAL PRIMARY KEY,
    quote TEXT NOT NULL,
    context TEXT NOT NULL,
    origin_story TEXT NOT NULL,
    usage_scenarios TEXT,  -- JSON array
    related_characters TEXT  -- JSON array
);

-- Character Traits
CREATE TABLE IF NOT EXISTS character_traits (
    id SERIAL PRIMARY KEY,
    trait TEXT NOT NULL,
    manifestation TEXT NOT NULL,
    origin_story TEXT NOT NULL,
    examples TEXT,  -- JSON array
    related_stories TEXT  -- JSON array
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_background_stories_era ON background_stories(era);
CREATE INDEX IF NOT EXISTS idx_character_backstories_name ON character_backstories(name);
CREATE INDEX IF NOT EXISTS idx_story_locations_name ON story_locations(name);
CREATE INDEX IF NOT EXISTS idx_life_philosophies_quote ON life_philosophies(quote);
CREATE INDEX IF NOT EXISTS idx_character_traits_trait ON character_traits(trait); 