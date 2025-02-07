
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

-- Post-migration fixes
UPDATE task_routing SET handled_by_ursula = FALSE WHERE handled_by_ursula IS NULL;
UPDATE decision_authority SET review_required = TRUE WHERE review_required IS NULL;
UPDATE raw_data SET processed = FALSE WHERE processed IS NULL;
UPDATE behavior_patterns SET frequency = 0 WHERE frequency IS NULL;

-- Create missing indexes
CREATE INDEX IF NOT EXISTS idx_ai_agents_name ON ai_agents(agent_name);
CREATE INDEX IF NOT EXISTS idx_task_routing_agent ON task_routing(ai_agent);
