import re

def convert_sqlite_to_postgres():
    with open('sqlite_dump.sql', 'r') as sqlite_file:
        with open('postgres_dump.sql', 'w') as postgres_file:
            # Write schema modifications first
            postgres_file.write("""
-- Schema modifications for proper data types
ALTER TABLE IF EXISTS task_routing ALTER COLUMN handled_by_ursula TYPE boolean USING CASE WHEN handled_by_ursula::text = '1' THEN true ELSE false END;
ALTER TABLE IF EXISTS decision_authority ALTER COLUMN review_required TYPE boolean USING CASE WHEN review_required::text = '1' THEN true ELSE false END;
ALTER TABLE IF EXISTS raw_data ALTER COLUMN processed TYPE boolean USING CASE WHEN processed::text = '1' THEN true ELSE false END;
ALTER TABLE IF EXISTS behavior_patterns ALTER COLUMN frequency TYPE integer USING COALESCE(frequency::integer, 0);

-- Ensure AI agents exist before foreign key constraints
INSERT INTO ai_agents (agent_name, agent_type, description, confidence_threshold, failure_count) VALUES 
('Health_AI', 'MEDICAL', 'Medical task processing agent', 0.85, 0),
('Marcus_AI', 'FINANCIAL', 'Financial task processing agent', 0.95, 0),
('Benny_AI', 'LEGAL', 'Legal document processing agent', 0.90, 0),
('Media_AI', 'PR', 'Public relations management agent', 0.80, 0),
('Logistics_AI', 'OPERATIONS', 'Day-to-day operations agent', 0.75, 0)
ON CONFLICT (agent_name) DO NOTHING;
""")

            for line in sqlite_file:
                # Convert AUTOINCREMENT to SERIAL
                line = re.sub(r'INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY', line)
                
                # Convert sqlite datetime functions
                line = re.sub(r'CURRENT_TIMESTAMP', 'CURRENT_TIMESTAMP', line)
                line = re.sub(r'DATETIME', 'TIMESTAMP', line)
                
                # Handle boolean values properly
                line = re.sub(r"'t'", 'TRUE', line)
                line = re.sub(r"'f'", 'FALSE', line)
                line = re.sub(r',\s*0\s*,', ',FALSE,', line)
                line = re.sub(r',\s*1\s*,', ',TRUE,', line)
                line = re.sub(r',\s*0\s*\)', ',FALSE)', line)
                line = re.sub(r',\s*1\s*\)', ',TRUE)', line)
                
                # Convert sqlite specific types
                line = re.sub(r'NUMERIC', 'DECIMAL', line)
                
                # Fix column names
                line = re.sub(r'name,', 'agent_name,', line)
                line = re.sub(r'type,', 'agent_type,', line)
                
                # Fix foreign key types
                line = re.sub(r'REFERENCES tasks \(id\)', 'REFERENCES tasks (id)', line)
                
                # Skip sqlite specific commands
                if any(cmd in line for cmd in ['PRAGMA', 'BEGIN TRANSACTION', 'COMMIT']):
                    continue
                
                # Handle duplicate inserts
                if line.startswith('INSERT'):
                    line = line.replace('INSERT INTO', 'INSERT INTO').replace(');', ') ON CONFLICT DO NOTHING;')
                    # Fix column names in INSERT statements
                    line = re.sub(r'INSERT INTO ai_agents \(name,', 'INSERT INTO ai_agents (agent_name,', line)
                    line = re.sub(r'INSERT INTO ai_agents \(type,', 'INSERT INTO ai_agents (agent_type,', line)
                
                postgres_file.write(line)

            # Write post-migration fixes
            postgres_file.write("""
-- Post-migration fixes
UPDATE task_routing SET handled_by_ursula = FALSE WHERE handled_by_ursula IS NULL;
UPDATE decision_authority SET review_required = TRUE WHERE review_required IS NULL;
UPDATE raw_data SET processed = FALSE WHERE processed IS NULL;
UPDATE behavior_patterns SET frequency = 0 WHERE frequency IS NULL;

-- Create missing indexes
CREATE INDEX IF NOT EXISTS idx_ai_agents_name ON ai_agents(agent_name);
CREATE INDEX IF NOT EXISTS idx_task_routing_agent ON task_routing(ai_agent);
""")

if __name__ == '__main__':
    convert_sqlite_to_postgres() 