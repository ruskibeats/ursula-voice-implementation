-- Drop and recreate problematic tables
DROP TABLE IF EXISTS ai_agents CASCADE;
DROP TABLE IF EXISTS ai_escalation_triggers CASCADE;
DROP TABLE IF EXISTS task_routing CASCADE;
DROP TABLE IF EXISTS behavior_patterns CASCADE;
DROP TABLE IF EXISTS decision_authority CASCADE;

-- Create tables with correct data types
CREATE TABLE ai_agents (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) UNIQUE NOT NULL,
    agent_type VARCHAR(50) NOT NULL,
    description TEXT,
    confidence_threshold FLOAT NOT NULL DEFAULT 0.8,
    failure_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE task_routing (
    id SERIAL PRIMARY KEY,
    task_type VARCHAR(50) NOT NULL,
    handled_by_ursula BOOLEAN NOT NULL DEFAULT false,
    ai_agent VARCHAR(50) REFERENCES ai_agents(agent_name),
    routing_rules TEXT,
    UNIQUE(task_type)
);

CREATE TABLE ai_escalation_triggers (
    id SERIAL PRIMARY KEY,
    ai_agent VARCHAR(50) REFERENCES ai_agents(agent_name),
    trigger_condition TEXT NOT NULL,
    action_required TEXT NOT NULL,
    threshold FLOAT DEFAULT 0.8,
    last_triggered TIMESTAMP
);

CREATE TABLE behavior_patterns (
    id SERIAL PRIMARY KEY,
    pattern_type VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    frequency INTEGER NOT NULL DEFAULT 0,
    last_observed TIMESTAMP,
    notes TEXT
);

CREATE TABLE decision_authority (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    authority_level VARCHAR(50) NOT NULL,
    description TEXT,
    risk_level INTEGER NOT NULL DEFAULT 1,
    review_required BOOLEAN NOT NULL DEFAULT true
);

-- Insert AI agents
INSERT INTO ai_agents (agent_name, agent_type, description, confidence_threshold) VALUES 
('Health_AI', 'MEDICAL', 'Medical task processing agent', 0.85),
('Marcus_AI', 'FINANCIAL', 'Financial task processing agent', 0.95),
('Benny_AI', 'LEGAL', 'Legal document processing agent', 0.90),
('Media_AI', 'PR', 'Public relations management agent', 0.80),
('Logistics_AI', 'OPERATIONS', 'Day-to-day operations agent', 0.75)
ON CONFLICT (agent_name) DO NOTHING;

-- Insert task routing
INSERT INTO task_routing (task_type, handled_by_ursula, ai_agent, routing_rules) VALUES
('Financial_High_Value', true, 'Marcus_AI', 'Route high-value financial tasks'),
('Medical_Routine', false, 'Health_AI', 'Route routine medical tasks'),
('Legal_Documentation', false, 'Benny_AI', 'Route legal document processing'),
('PR_Crisis', true, 'Media_AI', 'Route PR crisis management'),
('Routine_Errands', false, 'Logistics_AI', 'Route daily errands')
ON CONFLICT (task_type) DO NOTHING;

-- Create indexes
CREATE INDEX idx_ai_agents_name ON ai_agents(agent_name);
CREATE INDEX idx_task_routing_agent ON task_routing(ai_agent);
CREATE INDEX idx_behavior_patterns_type ON behavior_patterns(pattern_type);
CREATE INDEX idx_decision_authority_level ON decision_authority(authority_level); 