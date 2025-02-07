-- Expanded Character Universe Schema

-- Drop existing tables first
DROP TABLE IF EXISTS daily_routines CASCADE;
DROP TABLE IF EXISTS personal_rules CASCADE;
DROP TABLE IF EXISTS secret_skills CASCADE;
DROP TABLE IF EXISTS vulnerabilities CASCADE;
DROP TABLE IF EXISTS regular_haunts CASCADE;
DROP TABLE IF EXISTS regional_traits CASCADE;
DROP TABLE IF EXISTS future_dreams CASCADE;
DROP TABLE IF EXISTS guilty_pleasures CASCADE;

-- Daily Routines
CREATE TABLE IF NOT EXISTS daily_routines (
    id SERIAL PRIMARY KEY,
    routine_type TEXT NOT NULL,  -- morning_ritual, power_moves
    time_of_day TEXT,
    activities TEXT,  -- JSON array
    frequency TEXT NOT NULL,  -- daily, weekly, monthly
    location TEXT,
    quirks TEXT,  -- JSON array
    notes TEXT
);

-- Personal Rules
CREATE TABLE IF NOT EXISTS personal_rules (
    id SERIAL PRIMARY KEY,
    rule TEXT NOT NULL,
    context TEXT NOT NULL,
    importance_rating INTEGER CHECK (importance_rating BETWEEN 1 AND 10),
    origin_story TEXT,
    examples TEXT  -- JSON array
);

-- Secret Skills
CREATE TABLE IF NOT EXISTS secret_skills (
    id SERIAL PRIMARY KEY,
    skill TEXT NOT NULL,
    origin_story TEXT,
    proficiency_level TEXT CHECK (proficiency_level IN ('expert', 'advanced', 'intermediate')),
    last_used TEXT,
    related_stories TEXT  -- JSON array
);

-- Vulnerabilities
CREATE TABLE IF NOT EXISTS vulnerabilities (
    id SERIAL PRIMARY KEY,
    trigger TEXT NOT NULL,
    reaction TEXT NOT NULL,
    background TEXT,
    coping_mechanism TEXT,
    related_characters TEXT  -- JSON array
);

-- Regular Haunts
CREATE TABLE IF NOT EXISTS regular_haunts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    time_of_day TEXT NOT NULL,
    purpose TEXT,
    insider_knowledge TEXT,
    regular_companions TEXT  -- JSON array
);

-- Regional Traits
CREATE TABLE IF NOT EXISTS regional_traits (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    trait TEXT NOT NULL,
    context TEXT,
    manifestation TEXT,
    frequency TEXT
);

-- Future Dreams
CREATE TABLE IF NOT EXISTS future_dreams (
    id SERIAL PRIMARY KEY,
    dream TEXT NOT NULL,
    type TEXT CHECK (type IN ('admitted', 'secret')),
    motivation TEXT,
    progress_status TEXT,
    blockers TEXT
);

-- Guilty Pleasures
CREATE TABLE IF NOT EXISTS guilty_pleasures (
    id SERIAL PRIMARY KEY,
    pleasure TEXT NOT NULL,
    frequency TEXT,
    context TEXT,
    who_knows TEXT,  -- JSON array
    notes TEXT
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_daily_routines ON daily_routines(routine_type, frequency);
CREATE INDEX IF NOT EXISTS idx_personal_rules ON personal_rules(rule);
CREATE INDEX IF NOT EXISTS idx_secret_skills ON secret_skills(proficiency_level);
CREATE INDEX IF NOT EXISTS idx_vulnerabilities ON vulnerabilities(trigger);
CREATE INDEX IF NOT EXISTS idx_regular_haunts ON regular_haunts(city, time_of_day);
CREATE INDEX IF NOT EXISTS idx_regional_traits ON regional_traits(city);
CREATE INDEX IF NOT EXISTS idx_future_dreams ON future_dreams(type, progress_status);
CREATE INDEX IF NOT EXISTS idx_guilty_pleasures ON guilty_pleasures(frequency); 