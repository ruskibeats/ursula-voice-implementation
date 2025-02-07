-- Russ-Ursula Relationship Schema

-- Trust System
CREATE TABLE IF NOT EXISTS trust_system (
    id SERIAL PRIMARY KEY,
    person TEXT NOT NULL,
    trust_level INTEGER CHECK (trust_level BETWEEN 1 AND 5),
    notes TEXT,
    relationship_context TEXT,
    last_trust_test TIMESTAMP,
    trust_history TEXT  -- JSON array of incidents that proved/tested trust
);

-- Task Patterns
CREATE TABLE IF NOT EXISTS task_patterns (
    id SERIAL PRIMARY KEY,
    task_type TEXT NOT NULL,
    russ_excuse TEXT NOT NULL,
    ursula_strategy TEXT NOT NULL,
    success_rate FLOAT DEFAULT 0.0,
    last_used TIMESTAMP,
    notes TEXT
);

-- Response Triggers
CREATE TABLE IF NOT EXISTS response_triggers (
    id SERIAL PRIMARY KEY,
    trigger TEXT NOT NULL,
    russ_reaction TEXT NOT NULL,
    ursula_note TEXT,
    effectiveness_rating FLOAT DEFAULT 1.0,
    last_triggered TIMESTAMP,
    success_history TEXT  -- JSON array of times this trigger worked
);

-- Escalation System
CREATE TABLE IF NOT EXISTS escalation_system (
    id SERIAL PRIMARY KEY,
    stage INTEGER CHECK (stage BETWEEN 1 AND 4),
    stage_name TEXT NOT NULL,
    trigger TEXT NOT NULL,
    ursula_move TEXT NOT NULL,
    russ_response TEXT,
    success_rate FLOAT DEFAULT 0.0,
    last_used TIMESTAMP
);

-- Loyalty Proof Stories
CREATE TABLE IF NOT EXISTS loyalty_stories (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    era TEXT NOT NULL,
    content TEXT NOT NULL,
    impact_on_relationship TEXT,
    witnesses TEXT,  -- JSON array of who else was there
    frequency_of_reference FLOAT DEFAULT 0.0,
    last_referenced TIMESTAMP
);

-- Charlotte's Perspective
CREATE TABLE IF NOT EXISTS charlotte_perspective (
    id SERIAL PRIMARY KEY,
    aspect TEXT NOT NULL,
    feeling TEXT NOT NULL,
    context TEXT,
    manifestation TEXT,
    resolution TEXT,
    impact_on_dynamics TEXT
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_trust_level ON trust_system(trust_level);
CREATE INDEX IF NOT EXISTS idx_task_type ON task_patterns(task_type);
CREATE INDEX IF NOT EXISTS idx_trigger_effectiveness ON response_triggers(effectiveness_rating);
CREATE INDEX IF NOT EXISTS idx_escalation_stage ON escalation_system(stage);
CREATE INDEX IF NOT EXISTS idx_loyalty_era ON loyalty_stories(era);
CREATE INDEX IF NOT EXISTS idx_charlotte_aspect ON charlotte_perspective(aspect); 