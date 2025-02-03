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

-- Background Stories
CREATE TABLE background_stories (
    id INTEGER PRIMARY KEY,
    era TEXT NOT NULL,  -- wall_street, boston_youth, philly_days
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    characters TEXT,  -- JSON array of character names
    location TEXT,
    mood TEXT,
    frequency_weight FLOAT DEFAULT 1.0,  -- How often to reference this story
    last_referenced TIMESTAMP,
    success_rating FLOAT DEFAULT 0.0,
    UNIQUE(title)
);

-- Character Backstories
CREATE TABLE character_backstories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    relationship TEXT,  -- connection to Ursula
    era TEXT,  -- when they met/knew each other
    background TEXT,  -- their story
    status TEXT,  -- current status (active/inactive)
    last_referenced TIMESTAMP,
    reference_count INTEGER DEFAULT 0,
    UNIQUE(name)
);

-- Story Locations
CREATE TABLE story_locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    era TEXT,  -- time period
    description TEXT,
    significance TEXT,  -- why it matters to Ursula
    stories TEXT,  -- JSON array of related story IDs
    last_referenced TIMESTAMP,
    UNIQUE(name, era)
);

-- SSML Patterns
CREATE TABLE IF NOT EXISTS ssml_patterns (
    id INTEGER PRIMARY KEY,
    pattern_type TEXT NOT NULL,
    pattern_name TEXT NOT NULL,
    ssml_pattern TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(pattern_type, pattern_name)
);

-- Create index for SSML patterns
CREATE INDEX IF NOT EXISTS idx_ssml_patterns_type_name ON ssml_patterns(pattern_type, pattern_name);

-- Response Templates
CREATE TABLE IF NOT EXISTS response_templates (
    id INTEGER PRIMARY KEY,
    template_type TEXT NOT NULL,  -- greeting, medical_update, task_update, personal, closing
    template_name TEXT NOT NULL,  -- standard, urgent, warning, etc.
    ssml_pattern TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(template_type, template_name)
);

-- Create index for response templates
CREATE INDEX IF NOT EXISTS idx_response_templates ON response_templates(template_type, template_name);

-- Voicemail Templates
CREATE TABLE IF NOT EXISTS voicemail_templates (
    id INTEGER PRIMARY KEY,
    template_type TEXT NOT NULL,  -- voicemail
    template_name TEXT NOT NULL,  -- medical_urgent, general_update, deadline_warning
    ssml_content TEXT NOT NULL,   -- Full SSML template with placeholders
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(template_type, template_name)
);

-- Create index for voicemail templates
CREATE INDEX IF NOT EXISTS idx_voicemail_templates ON voicemail_templates(template_type, template_name);

-- Slang Terms
CREATE TABLE IF NOT EXISTS slang_terms (
    id INTEGER PRIMARY KEY,
    term TEXT NOT NULL,
    meaning TEXT,
    usage_example TEXT,
    ssml_pattern_type TEXT,
    category TEXT,
    region TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(term)
);

-- Create index for slang terms
CREATE INDEX IF NOT EXISTS idx_slang_terms ON slang_terms(category, region);

-- Scenes
CREATE TABLE IF NOT EXISTS scenes (
    id INTEGER PRIMARY KEY,
    scene_name TEXT NOT NULL,
    scene_type TEXT NOT NULL,
    ssml_content TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(scene_name)
);

-- Create index for scenes
CREATE INDEX IF NOT EXISTS idx_scenes ON scenes(scene_type);

-- Character Traits
CREATE TABLE IF NOT EXISTS character_traits (
    id INTEGER PRIMARY KEY,
    trait_type TEXT NOT NULL,
    trait_value TEXT NOT NULL,
    ssml_impact TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(trait_type, trait_value)
);

-- Create index for character traits
CREATE INDEX IF NOT EXISTS idx_character_traits ON character_traits(trait_type);

-- Indexes
CREATE INDEX idx_stories_category ON stories(category);
CREATE INDEX idx_stories_mood ON stories(mood);
CREATE INDEX idx_locations_category ON locations(category);
CREATE INDEX idx_patterns_type ON interaction_patterns(pattern_type);
CREATE INDEX idx_memory_updates_category ON memory_updates(category);
CREATE INDEX idx_memory_updates_context ON memory_updates(context);
CREATE INDEX idx_background_era ON background_stories(era);
CREATE INDEX idx_background_mood ON background_stories(mood);
CREATE INDEX idx_character_era ON character_backstories(era);
CREATE INDEX idx_location_era ON story_locations(era);

-- Views
CREATE VIEW recent_successful_patterns AS
SELECT * FROM interaction_patterns
WHERE success_rating > 0.7
ORDER BY last_used DESC;

CREATE VIEW favorite_stories AS
SELECT * FROM stories
WHERE success_rating > 0.8
ORDER BY times_told DESC;

CREATE VIEW popular_backgrounds AS
SELECT * FROM background_stories
WHERE success_rating > 0.7
ORDER BY frequency_weight DESC; 
-- Romantic History
CREATE TABLE romantic_relationships (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    era TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    status TEXT NOT NULL,
    story TEXT NOT NULL,
    special_notes TEXT,
    locations TEXT,
    interaction_history TEXT,
    last_interaction TIMESTAMP,
    UNIQUE(name, era)
);

-- Romantic Stories
CREATE TABLE romantic_stories (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    location TEXT NOT NULL,
    characters TEXT,
    content TEXT NOT NULL,
    mood TEXT NOT NULL,
    times_told INTEGER DEFAULT 0,
    last_told TIMESTAMP,
    success_rating FLOAT,
    UNIQUE(title)
);
