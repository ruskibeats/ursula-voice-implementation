-- Drop existing table if it exists
DROP TABLE IF EXISTS trust_system CASCADE;

-- Create trust system table
CREATE TABLE IF NOT EXISTS trust_system (
    id SERIAL PRIMARY KEY,
    person_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    trust_level INTEGER CHECK (trust_level BETWEEN 1 AND 5),
    trust_history TEXT,  -- JSON array of trust incidents
    history_notes TEXT,
    last_trust_test TIMESTAMP,
    UNIQUE(person_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_trust_person ON trust_system(person_id);
CREATE INDEX IF NOT EXISTS idx_trust_level ON trust_system(trust_level);

-- Check if chats table exists and get its structure
SELECT EXISTS (
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    AND table_name = 'chats'
);

-- Get column information if exists
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'public' 
AND table_name = 'chats';