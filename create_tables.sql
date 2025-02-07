-- Drop existing tables if they exist
DROP TABLE IF EXISTS family_members CASCADE;
DROP TABLE IF EXISTS characters CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS rules CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS subtasks CASCADE;
DROP TABLE IF EXISTS voice_patterns CASCADE;
DROP TABLE IF EXISTS adhd_patterns CASCADE;
DROP TABLE IF EXISTS failure_stories CASCADE;
DROP TABLE IF EXISTS raw_data CASCADE;
DROP TABLE IF EXISTS webhooks CASCADE;
DROP TABLE IF EXISTS ai_agents CASCADE;
DROP TABLE IF EXISTS task_routing CASCADE;
DROP TABLE IF EXISTS behavior_patterns CASCADE;
DROP TABLE IF EXISTS decision_authority CASCADE;
DROP TABLE IF EXISTS ai_escalation_triggers CASCADE;

-- Create tables
CREATE TABLE family_members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    preferences JSONB,
    active BOOLEAN DEFAULT true
);

CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    universe VARCHAR(100) NOT NULL,
    traits JSONB,
    relationships JSONB
);

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    universe VARCHAR(100) NOT NULL,
    description TEXT,
    coordinates JSONB
);

CREATE TABLE rules (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(20) NOT NULL,
    active BOOLEAN DEFAULT true
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    due_date TIMESTAMP,
    assigned_to VARCHAR(100),
    parent_task_id INTEGER REFERENCES tasks(id),
    notes TEXT
);

CREATE TABLE subtasks (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(20) NOT NULL,
    "order" INTEGER NOT NULL
);

CREATE TABLE voice_patterns (
    id SERIAL PRIMARY KEY,
    emotion VARCHAR(50) NOT NULL,
    ssml_template TEXT NOT NULL,
    description TEXT,
    use_case VARCHAR(100)
);

CREATE TABLE adhd_patterns (
    id SERIAL PRIMARY KEY,
    pattern_name VARCHAR(100) NOT NULL,
    triggers JSONB,
    coping_strategies JSONB,
    severity INTEGER NOT NULL
);

CREATE TABLE failure_stories (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    lessons_learned JSONB,
    date_occurred TIMESTAMP NOT NULL,
    prevention_steps JSONB
);

CREATE TABLE raw_data (
    id SERIAL PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    content JSONB NOT NULL,
    processed BOOLEAN DEFAULT false,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE TABLE webhooks (
    id SERIAL PRIMARY KEY,
    url VARCHAR(500) NOT NULL,
    source VARCHAR(100) NOT NULL,
    active BOOLEAN DEFAULT true,
    headers JSONB,
    retry_count INTEGER DEFAULT 0
);

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
    task_type VARCHAR(50) UNIQUE NOT NULL,
    handled_by_ursula BOOLEAN NOT NULL DEFAULT false,
    ai_agent VARCHAR(50) REFERENCES ai_agents(agent_name) ON DELETE CASCADE,
    routing_rules TEXT
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

CREATE TABLE ai_escalation_triggers (
    id SERIAL PRIMARY KEY,
    ai_agent VARCHAR(50) REFERENCES ai_agents(agent_name) ON DELETE CASCADE,
    trigger_condition TEXT NOT NULL,
    action_required TEXT NOT NULL,
    threshold FLOAT NOT NULL DEFAULT 0.8,
    last_triggered TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_assigned ON tasks(assigned_to);
CREATE INDEX idx_subtasks_task ON subtasks(task_id);
CREATE INDEX idx_voice_patterns_emotion ON voice_patterns(emotion);
CREATE INDEX idx_raw_data_processed ON raw_data(processed);
CREATE INDEX idx_webhooks_source ON webhooks(source);
CREATE INDEX idx_behavior_patterns_type ON behavior_patterns(pattern_type);
CREATE INDEX idx_decision_authority_category ON decision_authority(category); 