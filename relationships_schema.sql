-- Drop existing table if it exists
DROP TABLE IF EXISTS relationships CASCADE;

-- Create relationships table
CREATE TABLE IF NOT EXISTS relationships (
    id SERIAL PRIMARY KEY,
    person_1_id INTEGER NOT NULL,
    person_2_id INTEGER NOT NULL,
    relationship_type TEXT NOT NULL,
    relationship_strength INTEGER CHECK (relationship_strength BETWEEN 1 AND 5),
    trust_level INTEGER CHECK (trust_level BETWEEN 1 AND 5),
    loyalty_history TEXT,  -- JSON array of significant events
    last_interaction DATE,
    primary_context TEXT,
    notes TEXT
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_relationships_person1 ON relationships(person_1_id);
CREATE INDEX IF NOT EXISTS idx_relationships_person2 ON relationships(person_2_id);
CREATE INDEX IF NOT EXISTS idx_relationships_trust ON relationships(trust_level);
CREATE INDEX IF NOT EXISTS idx_relationships_strength ON relationships(relationship_strength); 