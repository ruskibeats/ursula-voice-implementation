-- Drop and recreate family members table
DROP TABLE IF EXISTS family_members CASCADE;

CREATE TABLE family_members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    preferences JSONB,
    active BOOLEAN DEFAULT true
);

-- Repopulate family members
INSERT INTO family_members (name, role, preferences, active) VALUES
('Russell', 'Primary', '{"schedule_preference": "morning", "communication_style": "direct"}'::jsonb, true),
('Sarah', 'Partner', '{"schedule_preference": "flexible", "communication_style": "detailed"}'::jsonb, true),
('Max', 'Pet', '{"schedule_preference": "regular", "care_needs": "high"}'::jsonb, true)
ON CONFLICT (name) DO NOTHING; 