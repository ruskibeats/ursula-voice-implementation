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
    pattern_type TEXT NOT NULL,  -- emotion, prosody, break, effect, character
    pattern_name TEXT NOT NULL,
    ssml_pattern TEXT NOT NULL,
    description TEXT,
    context TEXT,               -- When to use this pattern
    intensity TEXT,             -- low, medium, high
    success_rating FLOAT,
    last_used TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    UNIQUE(pattern_type, pattern_name)
);

-- Create index for pattern lookup
CREATE INDEX IF NOT EXISTS idx_patterns_type_name ON ssml_patterns(pattern_type, pattern_name);

-- Regional Slang
CREATE TABLE IF NOT EXISTS regional_slang (
    id INTEGER PRIMARY KEY,
    term TEXT NOT NULL,
    region TEXT NOT NULL,      -- boston, ny, philly
    context TEXT,              -- When to use this slang
    ssml_pattern TEXT,         -- Associated SSML pattern for pronunciation
    usage_frequency FLOAT,     -- How often to use this term
    examples TEXT,             -- Example usage
    UNIQUE(term, region)
);

-- Required Phrases
CREATE TABLE IF NOT EXISTS required_phrases (
    id INTEGER PRIMARY KEY,
    phrase_type TEXT NOT NULL,  -- opening, self_reference, situational
    phrase TEXT NOT NULL,
    context TEXT NOT NULL,      -- When to use this phrase
    ssml_pattern_id INTEGER,    -- Link to ssml_patterns
    success_rating FLOAT,
    usage_count INTEGER DEFAULT 0,
    FOREIGN KEY(ssml_pattern_id) REFERENCES ssml_patterns(id),
    UNIQUE(phrase_type, phrase)
);

-- HTML Formatting Rules
CREATE TABLE IF NOT EXISTS formatting_rules (
    id INTEGER PRIMARY KEY,
    element_type TEXT NOT NULL,  -- strong, em, ul, li, p
    context TEXT NOT NULL,       -- When to use this formatting
    example TEXT,
    description TEXT,
    UNIQUE(element_type, context)
);

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

-- Voice Characteristics
CREATE TABLE IF NOT EXISTS voice_characteristics (
    id INTEGER PRIMARY KEY,
    characteristic_type TEXT NOT NULL,  -- accent, habit, mannerism
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    ssml_impact TEXT,                  -- How it affects SSML
    frequency FLOAT,                   -- How often to use
    context TEXT,                      -- When to use
    examples TEXT,                     -- JSON array of example uses
    success_rating FLOAT DEFAULT 0.0,
    last_used TIMESTAMP,
    UNIQUE(characteristic_type, name)
);

-- Message Structure Templates
CREATE TABLE IF NOT EXISTS message_structures (
    id INTEGER PRIMARY KEY,
    structure_type TEXT NOT NULL,      -- medical_urgent, task_list, story_telling
    name TEXT NOT NULL,
    components TEXT NOT NULL,          -- JSON array of required components
    html_template TEXT NOT NULL,       -- Base HTML structure
    required_phrases TEXT,             -- JSON array of required phrase types
    context TEXT,                      -- When to use this structure
    success_rating FLOAT DEFAULT 0.0,
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    UNIQUE(structure_type, name)
);

-- Create indexes for new tables
CREATE INDEX IF NOT EXISTS idx_voice_char_type ON voice_characteristics(characteristic_type);
CREATE INDEX IF NOT EXISTS idx_message_struct_type ON message_structures(structure_type);

-- Task Locations
CREATE TABLE IF NOT EXISTS task_locations (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,      -- medical, vehicle, financial
    name TEXT NOT NULL,
    nickname TEXT,
    significance TEXT,
    key_contact TEXT,
    stories TEXT,               -- JSON array of related stories
    insider_tips TEXT,          -- JSON array of tips
    last_used TIMESTAMP,
    success_rating FLOAT DEFAULT 0.0,
    UNIQUE(category, name)
);

-- Task Characters
CREATE TABLE IF NOT EXISTS task_characters (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,      -- medical, vehicle, financial
    name TEXT NOT NULL,
    nickname TEXT,
    specialty TEXT,
    relationship TEXT,
    stories TEXT,               -- JSON array of related stories
    last_contact TIMESTAMP,
    reliability_rating FLOAT DEFAULT 0.0,
    UNIQUE(category, name)
);

-- Task Escalations
CREATE TABLE IF NOT EXISTS task_escalations (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,      -- medical, vehicle, financial
    level INTEGER NOT NULL,      -- 1-5 escalation level
    action TEXT NOT NULL,
    trigger TEXT,
    intervention TEXT,
    success_rate FLOAT DEFAULT 0.0,
    last_used TIMESTAMP,
    UNIQUE(category, level, action)
);

-- Task Priorities
CREATE TABLE IF NOT EXISTS task_priorities (
    id INTEGER PRIMARY KEY,
    level TEXT NOT NULL,         -- RED, ORANGE, YELLOW, GREEN
    emoji TEXT NOT NULL,         -- 🔥, 🟠, 🟡, 🟢
    description TEXT NOT NULL,
    example_tasks TEXT,          -- JSON array of examples
    tone TEXT NOT NULL,
    urgency_multiplier FLOAT DEFAULT 1.0,
    UNIQUE(level)
);

-- Task Templates
CREATE TABLE IF NOT EXISTS task_templates (
    id INTEGER PRIMARY KEY,
    template_type TEXT NOT NULL,  -- voicemail, newsletter
    recipient TEXT NOT NULL,
    tone TEXT NOT NULL,
    subject TEXT,
    content_template TEXT NOT NULL,
    required_components TEXT,     -- JSON array of required sections
    success_rating FLOAT DEFAULT 0.0,
    last_used TIMESTAMP,
    UNIQUE(template_type, recipient)
);

-- Create indexes for task system
CREATE INDEX IF NOT EXISTS idx_task_locations ON task_locations(category);
CREATE INDEX IF NOT EXISTS idx_task_characters ON task_characters(category);
CREATE INDEX IF NOT EXISTS idx_task_escalations ON task_escalations(category, level);
CREATE INDEX IF NOT EXISTS idx_task_priorities ON task_priorities(level);

-- Category Aliases
CREATE TABLE IF NOT EXISTS category_aliases (
    id INTEGER PRIMARY KEY,
    alias TEXT NOT NULL,
    canonical_category TEXT NOT NULL,
    table_name TEXT NOT NULL,  -- stories, task_locations, etc.
    description TEXT,
    UNIQUE(alias, table_name)
);

-- Create index for category aliases
CREATE INDEX IF NOT EXISTS idx_category_aliases ON category_aliases(alias, table_name);

-- Insert common aliases
INSERT OR REPLACE INTO category_aliases (alias, canonical_category, table_name, description) VALUES
    ('medical', 'medical_warning', 'stories', 'Medical warning stories alias'),
    ('health', 'medical_warning', 'stories', 'Medical warning stories alias'),
    ('warning', 'medical_warning', 'stories', 'Medical warning stories alias'),
    ('hospital', 'medical', 'task_locations', 'Medical locations alias'),
    ('doctor', 'medical', 'task_locations', 'Medical locations alias'),
    ('car', 'vehicle', 'task_locations', 'Vehicle locations alias'),
    ('auto', 'vehicle', 'task_locations', 'Vehicle locations alias'),
    ('bank', 'financial', 'task_locations', 'Financial locations alias'),
    ('money', 'financial', 'task_locations', 'Financial locations alias'),
    ('urgent', 'RED', 'task_priorities', 'Red priority alias'),
    ('emergency', 'RED', 'task_priorities', 'Red priority alias'),
    ('important', 'ORANGE', 'task_priorities', 'Orange priority alias'),
    ('soon', 'ORANGE', 'task_priorities', 'Orange priority alias'),
    ('normal', 'YELLOW', 'task_priorities', 'Yellow priority alias'),
    ('routine', 'GREEN', 'task_priorities', 'Green priority alias');

-- Ursula's Universe Tables

-- Life Eras
CREATE TABLE IF NOT EXISTS life_eras (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,              -- e.g., "Wall Street Wild Years (1990s)"
    description TEXT,
    significance TEXT,
    themes TEXT,                     -- JSON array of themes
    key_locations TEXT,              -- JSON array of locations
    key_characters TEXT,             -- JSON array of character names
    UNIQUE(name)
);

-- Power Network
CREATE TABLE IF NOT EXISTS power_network (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    nickname TEXT,
    network_type TEXT NOT NULL,      -- finance, food, medical, legal
    relationship TEXT NOT NULL,
    era TEXT NOT NULL,
    status TEXT,
    influence_rating FLOAT,          -- 0-1 scale of how much influence they have
    favor_balance TEXT,              -- owes/owed/even
    last_interaction TIMESTAMP,
    locations TEXT,                  -- JSON array of their usual spots
    stories TEXT,                    -- JSON array of related stories
    special_notes TEXT,
    UNIQUE(name, network_type)
);

-- Life Philosophies
CREATE TABLE IF NOT EXISTS life_philosophies (
    id INTEGER PRIMARY KEY,
    quote TEXT NOT NULL,
    context TEXT,
    origin_story TEXT,
    usage_scenarios TEXT,            -- JSON array
    related_characters TEXT,         -- JSON array
    tags TEXT,                       -- JSON array
    success_rating FLOAT DEFAULT 0.0,
    last_used TIMESTAMP,
    UNIQUE(quote)
);

-- Rich Stories
CREATE TABLE IF NOT EXISTS rich_stories (
    id INTEGER PRIMARY KEY,
    era TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    characters TEXT,                 -- JSON array
    location TEXT,
    mood TEXT,
    frequency_weight FLOAT,
    tags TEXT,                       -- JSON array
    connected_stories TEXT,          -- JSON array
    last_told TIMESTAMP,
    success_rating FLOAT DEFAULT 0.0,
    UNIQUE(title)
);

-- Elite Locations
CREATE TABLE IF NOT EXISTS elite_locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    era TEXT NOT NULL,
    description TEXT,
    significance TEXT,
    regular_characters TEXT,         -- JSON array
    stories TEXT,                    -- JSON array
    tags TEXT,                       -- JSON array
    connected_locations TEXT,        -- JSON array
    insider_tips TEXT,              -- JSON array
    last_visit TIMESTAMP,
    UNIQUE(name, era)
);

-- Create indexes for Ursula's universe
CREATE INDEX IF NOT EXISTS idx_power_network_type ON power_network(network_type);
CREATE INDEX IF NOT EXISTS idx_rich_stories_era ON rich_stories(era);
CREATE INDEX IF NOT EXISTS idx_elite_locations_era ON elite_locations(era);

-- Personal Universe Tables

-- Daily Routines
CREATE TABLE IF NOT EXISTS daily_routines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    routine_type TEXT NOT NULL,
    time TEXT NOT NULL,
    activity TEXT NOT NULL,
    location TEXT NOT NULL,
    quirks TEXT NOT NULL,
    frequency TEXT NOT NULL,
    importance_rating REAL NOT NULL,
    UNIQUE(routine_type, time, activity)
);

-- Personal Rules
CREATE TABLE IF NOT EXISTS personal_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule TEXT NOT NULL UNIQUE,
    context TEXT NOT NULL,
    origin_story TEXT NOT NULL,
    importance_rating REAL NOT NULL
);

-- Secret Skills
CREATE TABLE IF NOT EXISTS secret_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill TEXT NOT NULL UNIQUE,
    origin_story TEXT NOT NULL,
    proficiency_level TEXT NOT NULL,
    reveal_frequency REAL NOT NULL
);

-- Vulnerabilities
CREATE TABLE IF NOT EXISTS vulnerabilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trigger TEXT NOT NULL UNIQUE,
    reaction TEXT NOT NULL,
    background TEXT NOT NULL,
    coping_mechanism TEXT NOT NULL
);

-- Regular Haunts
CREATE TABLE IF NOT EXISTS regular_haunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    time_of_day TEXT NOT NULL,
    location TEXT NOT NULL,
    purpose TEXT NOT NULL,
    frequency TEXT NOT NULL,
    special_notes TEXT NOT NULL,
    UNIQUE(city, location)
);

-- Regional Traits
CREATE TABLE IF NOT EXISTS regional_traits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    trait TEXT NOT NULL,
    context TEXT NOT NULL,
    manifestation TEXT NOT NULL,
    frequency REAL NOT NULL,
    UNIQUE(city, trait)
);

-- Future Dreams
CREATE TABLE IF NOT EXISTS future_dreams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dream TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    progress_status TEXT NOT NULL,
    related_actions TEXT NOT NULL
);

-- Guilty Pleasures
CREATE TABLE IF NOT EXISTS guilty_pleasures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pleasure TEXT NOT NULL UNIQUE,
    frequency TEXT NOT NULL,
    secrecy_level INTEGER NOT NULL
);

-- Create indexes for personal universe
CREATE INDEX IF NOT EXISTS idx_daily_routines ON daily_routines(routine_type, frequency);
CREATE INDEX IF NOT EXISTS idx_personal_rules ON personal_rules(context);
CREATE INDEX IF NOT EXISTS idx_secret_skills ON secret_skills(proficiency_level);
CREATE INDEX IF NOT EXISTS idx_vulnerabilities ON vulnerabilities(trigger);
CREATE INDEX IF NOT EXISTS idx_regular_haunts ON regular_haunts(city, time_of_day);
CREATE INDEX IF NOT EXISTS idx_regional_traits ON regional_traits(city, context);
CREATE INDEX IF NOT EXISTS idx_future_dreams ON future_dreams(type, progress_status);
CREATE INDEX IF NOT EXISTS idx_guilty_pleasures ON guilty_pleasures(frequency);
