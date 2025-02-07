-- Fix data types and constraints
ALTER TABLE IF EXISTS task_routing 
    ALTER COLUMN handled_by_ursula TYPE boolean USING (handled_by_ursula::integer)::boolean,
    ALTER COLUMN handled_by_ursula SET DEFAULT false;

ALTER TABLE IF EXISTS decision_authority 
    ALTER COLUMN risk_level TYPE integer USING CASE WHEN risk_level THEN 1 ELSE 0 END,
    ALTER COLUMN review_required TYPE boolean USING (review_required::integer)::boolean;

ALTER TABLE IF EXISTS raw_data 
    ALTER COLUMN processed TYPE boolean USING (processed::integer)::boolean,
    ALTER COLUMN processed SET DEFAULT false;

ALTER TABLE IF EXISTS behavior_patterns 
    ALTER COLUMN frequency TYPE integer USING COALESCE(frequency::integer, 0),
    ALTER COLUMN frequency SET DEFAULT 0;

ALTER TABLE IF EXISTS ai_agents 
    ALTER COLUMN failure_count TYPE integer USING COALESCE(failure_count::integer, 0),
    ALTER COLUMN failure_count SET DEFAULT 0;

-- Create AI agents first
INSERT INTO ai_agents (name, type, description, confidence_threshold, failure_count) VALUES 
('Health_AI', 'MEDICAL', 'Medical task processing agent', 0.85, 0),
('Marcus_AI', 'FINANCIAL', 'Financial task processing agent', 0.95, 0),
('Benny_AI', 'LEGAL', 'Legal document processing agent', 0.90, 0),
('Media_AI', 'PR', 'Public relations management agent', 0.80, 0),
('Logistics_AI', 'OPERATIONS', 'Day-to-day operations agent', 0.75, 0)
ON CONFLICT (name) DO NOTHING;

-- Fix foreign key references
ALTER TABLE IF EXISTS ai_escalation_triggers
    DROP CONSTRAINT IF EXISTS ai_escalation_triggers_ai_agent_fkey,
    ADD CONSTRAINT ai_escalation_triggers_ai_agent_fkey 
    FOREIGN KEY (ai_agent) REFERENCES ai_agents(name) ON DELETE CASCADE;

-- Create missing indexes
CREATE INDEX IF NOT EXISTS idx_ai_agents_name ON ai_agents(name);
CREATE INDEX IF NOT EXISTS idx_task_routing_agent ON task_routing(ai_agent);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);

-- Set default values for nullable columns
UPDATE task_routing SET handled_by_ursula = false WHERE handled_by_ursula IS NULL;
UPDATE decision_authority SET review_required = true WHERE review_required IS NULL;
UPDATE raw_data SET processed = false WHERE processed IS NULL;
UPDATE behavior_patterns SET frequency = 0 WHERE frequency IS NULL;
UPDATE ai_agents SET failure_count = 0 WHERE failure_count IS NULL; 