-- Drop existing tables
DROP TABLE IF EXISTS family;
DROP TABLE IF EXISTS characters;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS personal_rules;
DROP TABLE IF EXISTS relationships;
DROP TABLE IF EXISTS character_profiles;
DROP TABLE IF EXISTS adhd_patterns;
DROP TABLE IF EXISTS escalation_triggers;
DROP TABLE IF EXISTS failure_stories;
DROP TABLE IF EXISTS data_sources;
DROP TABLE IF EXISTS processing_rules;
DROP TABLE IF EXISTS priority_matrix;
DROP TABLE IF EXISTS red_flags;
DROP TABLE IF EXISTS ai_commands;
DROP TABLE IF EXISTS peak_performance_tracking;
DROP TABLE IF EXISTS task_routing;
DROP TABLE IF EXISTS ai_agents;
DROP TABLE IF EXISTS ai_escalation_triggers;
DROP TABLE IF EXISTS decision_authority;
DROP TABLE IF EXISTS raw_data;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS tasks_subtasks;

-- Ursula's Universe Schema
CREATE TABLE IF NOT EXISTS family (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    relation TEXT NOT NULL,
    status TEXT,
    details TEXT,
    impact TEXT,
    last_referenced TIMESTAMP
);

CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    key_traits TEXT,
    relevance_to_ursula TEXT,
    last_interaction TIMESTAMP,
    trust_level FLOAT DEFAULT 0.5
);

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    significance TEXT,
    key_contacts TEXT,
    insider_tips TEXT
);

CREATE TABLE IF NOT EXISTS personal_rules (
    id INTEGER PRIMARY KEY,
    rule TEXT NOT NULL,
    origin_story TEXT,
    importance_rating INTEGER CHECK (importance_rating BETWEEN 1 AND 10)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT,
    complications TEXT,
    threat_level INTEGER CHECK (threat_level BETWEEN 1 AND 5)
);

-- Russ Management Schema
CREATE TABLE IF NOT EXISTS character_profiles (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    key_traits TEXT NOT NULL,
    relevance TEXT,
    trust_level FLOAT DEFAULT 0.5
);

CREATE TABLE IF NOT EXISTS adhd_patterns (
    id INTEGER PRIMARY KEY,
    task_type TEXT NOT NULL,
    russ_excuse TEXT NOT NULL,
    ursula_response TEXT NOT NULL,
    success_rate FLOAT DEFAULT 0.0,
    last_used TIMESTAMP
);

CREATE TABLE IF NOT EXISTS escalation_triggers (
    id INTEGER PRIMARY KEY,
    trigger TEXT NOT NULL,
    russ_response TEXT NOT NULL,
    ursula_note TEXT,
    effectiveness_rating FLOAT DEFAULT 1.0,
    last_used TIMESTAMP
);

CREATE TABLE IF NOT EXISTS failure_stories (
    id INTEGER PRIMARY KEY,
    story_name TEXT NOT NULL,
    what_happened TEXT NOT NULL,
    russ_lesson TEXT,
    ursula_quote TEXT NOT NULL,
    date_occurred TIMESTAMP,
    times_referenced INTEGER DEFAULT 0
);

-- AI Minion System
CREATE TABLE IF NOT EXISTS data_sources (
    id INTEGER PRIMARY KEY,
    source_type TEXT NOT NULL,
    source_name TEXT NOT NULL,
    data_type TEXT NOT NULL,
    collection_frequency TEXT NOT NULL,
    priority_level INTEGER CHECK (priority_level BETWEEN 1 AND 5),
    retention_period TEXT,
    last_collected TIMESTAMP,
    UNIQUE(source_type, source_name)
);

CREATE TABLE IF NOT EXISTS processing_rules (
    id INTEGER PRIMARY KEY,
    step_name TEXT NOT NULL,
    process_type TEXT NOT NULL,
    rules TEXT NOT NULL,
    priority_order INTEGER,
    success_criteria TEXT,
    failure_action TEXT,
    last_run TIMESTAMP,
    UNIQUE(step_name)
);

CREATE TABLE IF NOT EXISTS priority_matrix (
    id INTEGER PRIMARY KEY,
    level_name TEXT NOT NULL,
    urgency_score INTEGER CHECK (urgency_score BETWEEN 1 AND 5),
    response_time TEXT NOT NULL,
    notification_method TEXT NOT NULL,
    auto_actions TEXT,
    ursula_quote TEXT,
    UNIQUE(level_name)
);

CREATE TABLE IF NOT EXISTS red_flags (
    id INTEGER PRIMARY KEY,
    trigger_name TEXT NOT NULL,
    conditions TEXT NOT NULL,
    severity_level INTEGER CHECK (severity_level BETWEEN 1 AND 5),
    immediate_actions TEXT NOT NULL,
    notification_priority TEXT NOT NULL,
    cooldown_period TEXT,
    last_triggered TIMESTAMP,
    UNIQUE(trigger_name)
);

CREATE TABLE IF NOT EXISTS ai_commands (
    id INTEGER PRIMARY KEY,
    command_name TEXT NOT NULL,
    command_type TEXT NOT NULL,
    parameters TEXT,
    execution_steps TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    error_handling TEXT,
    last_used TIMESTAMP,
    UNIQUE(command_name)
);

CREATE TABLE IF NOT EXISTS peak_performance_tracking (
    id INTEGER PRIMARY KEY,
    time_of_day TEXT NOT NULL,
    energy_level INTEGER,
    focus_rating FLOAT,
    success_rate FLOAT,
    task_types TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS task_routing (
    id INTEGER PRIMARY KEY,
    task_type TEXT NOT NULL,
    handled_by_ursula BOOLEAN DEFAULT true,
    delegated_to TEXT,
    routing_logic TEXT NOT NULL,
    ursula_oversight TEXT,
    success_rate FLOAT DEFAULT 0.0,
    last_failure TIMESTAMP,
    UNIQUE(task_type)
);

CREATE TABLE IF NOT EXISTS ai_agents (
    id INTEGER PRIMARY KEY,
    agent_name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    trust_level FLOAT DEFAULT 0.5,
    oversight_required TEXT NOT NULL,
    failure_count INTEGER DEFAULT 0,
    last_success TIMESTAMP,
    UNIQUE(agent_name)
);

CREATE TABLE IF NOT EXISTS ai_escalation_triggers (
    id INTEGER PRIMARY KEY,
    trigger_condition TEXT NOT NULL,
    ai_agent TEXT NOT NULL,
    severity_level INTEGER CHECK (severity_level BETWEEN 1 AND 5),
    ursula_response TEXT NOT NULL,
    response_deadline TEXT,
    last_triggered TIMESTAMP,
    FOREIGN KEY(ai_agent) REFERENCES ai_agents(agent_name)
);

CREATE TABLE IF NOT EXISTS decision_authority (
    id INTEGER PRIMARY KEY,
    decision_type TEXT NOT NULL,
    authority_level TEXT CHECK (authority_level IN ('AI_ONLY', 'AI_SUPERVISED', 'URSULA_ONLY', 'HYBRID')),
    reasoning TEXT NOT NULL,
    risk_level INTEGER CHECK (risk_level BETWEEN 1 AND 5),
    review_required BOOLEAN DEFAULT true,
    UNIQUE(decision_type)
);

-- Raw Data Ingestion
CREATE TABLE IF NOT EXISTS raw_data (
    id INTEGER PRIMARY KEY,
    source TEXT NOT NULL,
    content TEXT NOT NULL,  -- JSON content
    metadata TEXT,  -- JSON metadata
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    context TEXT,
    priority TEXT,
    processed BOOLEAN DEFAULT FALSE,
    processing_status TEXT DEFAULT 'pending',
    last_processed TIMESTAMP,
    UNIQUE(source, timestamp)
);

CREATE INDEX IF NOT EXISTS idx_raw_data_source ON raw_data(source);
CREATE INDEX IF NOT EXISTS idx_raw_data_priority ON raw_data(priority);
CREATE INDEX IF NOT EXISTS idx_raw_data_processed ON raw_data(processed);

-- Tasks Table
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    labels TEXT,  -- JSON array
    docid TEXT,
    due_date TEXT,
    comments TEXT,
    task_order INTEGER,
    ursula_notes TEXT,
    priority_level TEXT CHECK (priority_level IN ('RED', 'ORANGE', 'YELLOW', 'GREEN')),
    voice_pattern TEXT,
    last_reviewed TIMESTAMP,
    charlotte_notified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority_level);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(is_completed);

-- Tasks Subtasks
CREATE TABLE IF NOT EXISTS tasks_subtasks (
    id INTEGER PRIMARY KEY,
    parent_task_id TEXT NOT NULL,
    content TEXT NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(parent_task_id) REFERENCES tasks(id)
);

-- Core Task Tracking (Real-Time Roll Call System)
CREATE TABLE IF NOT EXISTS task_roll_call (
    id TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    due_date TIMESTAMP,
    last_mentioned TIMESTAMP,
    urgency TEXT CHECK (urgency IN ('RED', 'ORANGE', 'YELLOW', 'GREEN')),
    suggested_actions TEXT,
    ai_observations TEXT,
    days_overdue INTEGER,
    agent_assigned TEXT,
    status TEXT DEFAULT 'pending',
    pattern_score FLOAT DEFAULT 0.0,
    avoidance_history TEXT,  -- JSON array of past avoidance incidents
    impact_rating INTEGER CHECK (impact_rating BETWEEN 1 AND 10),
    external_pressure_score FLOAT DEFAULT 0.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(agent_assigned) REFERENCES ai_agents(agent_name)
);

-- Task Grading System
CREATE TABLE IF NOT EXISTS task_grading_factors (
    id INTEGER PRIMARY KEY,
    task_id TEXT NOT NULL,
    days_overdue_score FLOAT,
    avoidance_score FLOAT,
    impact_score FLOAT,
    pressure_score FLOAT,
    final_grade FLOAT,
    grading_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(task_id) REFERENCES task_roll_call(id)
);

-- Data Ingestion System
CREATE TABLE IF NOT EXISTS data_ingest_queue (
    id INTEGER PRIMARY KEY,
    source_type TEXT NOT NULL,  -- email, document, call, transaction, vehicle, health
    content TEXT NOT NULL,      -- JSON content
    metadata TEXT,             -- JSON metadata
    priority TEXT CHECK (priority IN ('RED', 'ORANGE', 'YELLOW', 'GREEN')),
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE,
    processing_agent TEXT,
    processing_status TEXT DEFAULT 'pending',
    FOREIGN KEY(processing_agent) REFERENCES ai_agents(agent_name)
);

-- Pattern Detection System
CREATE TABLE IF NOT EXISTS behavior_patterns (
    id INTEGER PRIMARY KEY,
    pattern_type TEXT NOT NULL,  -- avoidance, delay, excuse, success
    category TEXT NOT NULL,      -- health, finance, vehicle, etc.
    frequency INTEGER DEFAULT 0,
    last_observed TIMESTAMP,
    impact_level INTEGER CHECK (impact_level BETWEEN 1 AND 5),
    ai_analysis TEXT,
    mitigation_strategy TEXT
);

-- Task History & Analytics
CREATE TABLE IF NOT EXISTS task_analytics (
    id INTEGER PRIMARY KEY,
    task_id TEXT NOT NULL,
    completion_time INTEGER,  -- in hours
    delay_pattern TEXT,
    excuse_used TEXT,
    intervention_required BOOLEAN,
    intervention_type TEXT,
    success_rate FLOAT,
    notes TEXT,
    FOREIGN KEY(task_id) REFERENCES task_roll_call(id)
);

-- Daily Roll Call Reports
CREATE TABLE IF NOT EXISTS daily_roll_call (
    id INTEGER PRIMARY KEY,
    report_date DATE UNIQUE,
    urgent_tasks TEXT,       -- JSON array
    high_priority TEXT,      -- JSON array
    low_priority TEXT,       -- JSON array
    ursula_notes TEXT,
    charlotte_feedback TEXT,
    completion_rate FLOAT,
    generated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_roll_call_urgency ON task_roll_call(urgency);
CREATE INDEX IF NOT EXISTS idx_roll_call_due_date ON task_roll_call(due_date);
CREATE INDEX IF NOT EXISTS idx_roll_call_status ON task_roll_call(status);
CREATE INDEX IF NOT EXISTS idx_ingest_priority ON data_ingest_queue(priority);
CREATE INDEX IF NOT EXISTS idx_ingest_processed ON data_ingest_queue(processed);
CREATE INDEX IF NOT EXISTS idx_patterns_type ON behavior_patterns(pattern_type, category);
CREATE INDEX IF NOT EXISTS idx_analytics_task ON task_analytics(task_id);
CREATE INDEX IF NOT EXISTS idx_roll_call_date ON daily_roll_call(report_date);

-- Initial AI Agents
INSERT INTO ai_agents (agent_name, specialty, trust_level, oversight_required) 
SELECT 'Marcus_AI', 'Finance & Taxes', 0.8, 'Transactions over $10k need Ursula review'
WHERE NOT EXISTS (SELECT 1 FROM ai_agents WHERE agent_name = 'Marcus_AI');

INSERT INTO ai_agents (agent_name, specialty, trust_level, oversight_required) 
SELECT 'Health_AI', 'Medical & Appointments', 0.7, 'All new diagnoses need review'
WHERE NOT EXISTS (SELECT 1 FROM ai_agents WHERE agent_name = 'Health_AI');

INSERT INTO ai_agents (agent_name, specialty, trust_level, oversight_required) 
SELECT 'Logistics_AI', 'Errands & Vehicles', 0.9, 'Major repairs need approval'
WHERE NOT EXISTS (SELECT 1 FROM ai_agents WHERE agent_name = 'Logistics_AI');

INSERT INTO ai_agents (agent_name, specialty, trust_level, oversight_required) 
SELECT 'Pattern_AI', 'Behavioral Analysis', 0.6, 'All pattern changes need review'
WHERE NOT EXISTS (SELECT 1 FROM ai_agents WHERE agent_name = 'Pattern_AI');

INSERT INTO ai_agents (agent_name, specialty, trust_level, oversight_required) 
SELECT 'Crisis_AI', 'Emergency Detection', 0.5, 'All red flags need immediate review'
WHERE NOT EXISTS (SELECT 1 FROM ai_agents WHERE agent_name = 'Crisis_AI');

-- Initial Behavior Patterns
INSERT OR REPLACE INTO behavior_patterns (pattern_type, category, frequency, impact_level, mitigation_strategy) VALUES
('avoidance', 'health', 0, 4, 'Have Charlotte schedule and physically take him'),
('delay', 'finance', 0, 5, 'Set up auto-payments where possible'),
('excuse', 'vehicle', 0, 3, 'Pre-schedule maintenance, no discussion needed'),
('success', 'groceries', 0, 2, 'Auto-delivery for essentials');

-- Initial Data: Task Routing
INSERT INTO task_routing (task_type, handled_by_ursula, delegated_to, routing_logic, ursula_oversight) VALUES
('Financial_High_Value', true, 'Marcus_AI', 'High-stakes financial decisions need human intuition', 'Final approval on all transactions over $10k'),
('Medical_Routine', false, 'Health_AI', 'Routine appointments can be AI-managed through Charlotte', 'Steps in after 3 missed appointments'),
('Legal_Documentation', false, 'Benny_AI', 'Standard legal docs can be AI-processed', 'Reviews all court-related documents'),
('PR_Crisis', true, 'Media_AI', 'Reputation management needs human touch', 'Personally handles all media responses'),
('Routine_Errands', false, 'Logistics_AI', 'Low-risk tasks suitable for AI', 'Only monitors completion rates');

-- Initial Data: AI Agents
INSERT INTO ai_agents (agent_name, specialty, trust_level, oversight_required) VALUES
('Marcus_AI', 'Financial Analysis & Tracking', 0.8, 'All transfers over $10k need Ursula''s approval'),
('Health_AI', 'Medical Scheduling & Monitoring', 0.7, 'Escalate after 3 missed appointments'),
('Benny_AI', 'Legal Document Processing', 0.6, 'All court documents need review'),
('Media_AI', 'Social Media & PR Monitoring', 0.5, 'Alert on any potential PR issues'),
('Logistics_AI', 'Routine Task Management', 0.9, 'Weekly completion rate review');

-- Initial Data: Escalation Triggers
INSERT INTO ai_escalation_triggers (trigger_condition, ai_agent, severity_level, ursula_response, response_deadline) VALUES
('3+ missed health appointments', 'Health_AI', 4, 'Direct intervention with Russ', '24 hours'),
('Suspicious financial activity', 'Marcus_AI', 5, 'Account freeze and personal review', '1 hour'),
('Legal deadline risk', 'Benny_AI', 5, 'Immediate legal team activation', '2 hours'),
('Negative press mention', 'Media_AI', 3, 'PR strategy review', '4 hours');

-- Initial Data: Decision Authority
INSERT INTO decision_authority (decision_type, authority_level, reasoning, risk_level, review_required) VALUES
('Routine_Scheduling', 'AI_ONLY', 'Low-risk, repetitive tasks suitable for automation', 1, false),
('Financial_Transactions', 'AI_SUPERVISED', 'Needs human oversight for security', 4, true),
('Legal_Strategy', 'URSULA_ONLY', 'Requires street smarts and human intuition', 5, true),
('Crisis_Management', 'HYBRID', 'AI monitors, Ursula decides response', 4, true),
('Emotional_Support', 'URSULA_ONLY', 'Pure human domain - no AI involvement', 5, true);

-- Initial Data: Data Sources
INSERT INTO data_sources (source_type, source_name, data_type, collection_frequency, priority_level, retention_period) VALUES
('paperwork', 'Bills & Contracts', 'document', 'daily', 5, '7 years'),
('communication', 'Phone Calls', 'audio', 'realtime', 4, '30 days'),
('communication', 'Voice Notes', 'audio', 'hourly', 3, '90 days'),
('calendar', 'Appointments', 'event', 'hourly', 5, '1 year'),
('financial', 'Bank Statements', 'document', 'daily', 5, '7 years'),
('communication', 'Text Messages', 'text', 'realtime', 4, '90 days'),
('vehicle', 'Car Alerts', 'notification', 'realtime', 4, '1 year');

-- Initial Data: Processing Rules
INSERT INTO processing_rules (step_name, process_type, rules, priority_order, success_criteria, failure_action) VALUES
('data_collection', 'ingestion', '["validate_source", "check_completeness", "verify_format"]', 1, 'All sources checked', 'Retry 3 times'),
('noise_reduction', 'filtering', '["remove_duplicates", "filter_spam", "check_relevance"]', 2, 'Clean data set', 'Log and proceed'),
('priority_sorting', 'analysis', '["check_urgency", "verify_importance", "assign_priority"]', 3, 'All items categorized', 'Manual review'),
('pattern_recognition', 'analysis', '["identify_recurring", "flag_anomalies", "track_frequency"]', 4, 'Patterns identified', 'Alert Ursula'),
('red_flag_detection', 'monitoring', '["check_triggers", "verify_severity", "initiate_alerts"]', 5, 'All flags processed', 'Immediate alert');

-- Initial Data: Priority Matrix
INSERT INTO priority_matrix (level_name, urgency_score, response_time, notification_method, auto_actions, ursula_quote) VALUES
('CRITICAL', 5, '1 hour', 'call,text,email', '["freeze_accounts", "alert_charlotte", "schedule_intervention"]', 'Drop everything, sugar. We got a situation.'),
('HIGH', 4, '4 hours', 'text,email', '["prepare_report", "alert_relevant_contacts"]', 'This better be handled by end of day.'),
('MEDIUM', 3, '24 hours', 'email', '["log_details", "schedule_followup"]', 'Keep an eye on this one.'),
('LOW', 2, '1 week', 'weekly_report', '["archive", "add_to_summary"]', 'File it away, might need it later.');

-- Initial Data: Red Flags
INSERT INTO red_flags (trigger_name, conditions, severity_level, immediate_actions, notification_priority, cooldown_period) VALUES
('irs_contact', '["multiple_calls", "official_notices", "deadline_warnings"]', 5, 'Alert Ursula and freeze any related accounts', 'CRITICAL', '1 hour'),
('medical_avoidance', '["missed_appointments", "ignored_reminders", "health_warnings"]', 4, 'Contact Charlotte and schedule intervention', 'HIGH', '24 hours'),
('legal_notice', '["court_documents", "lawyer_contact", "official_summons"]', 5, 'Forward to legal team and alert Ursula', 'CRITICAL', '1 hour'),
('suspicious_payments', '["unknown_vendors", "unusual_amounts", "irregular_timing"]', 4, 'Freeze transactions and prepare report', 'HIGH', '6 hours');

-- Initial Data: AI Commands
INSERT INTO ai_commands (command_name, command_type, parameters, execution_steps, expected_output, error_handling) VALUES
('daily_summary', 'report', '["date_range", "priority_threshold"]', 'Collect, filter, summarize daily activities', 'Prioritized activity report', 'Generate partial report'),
('pattern_analysis', 'analysis', '["data_type", "time_range", "pattern_type"]', 'Analyze historical data for patterns', 'Pattern report with recommendations', 'Use available data'),
('contact_verification', 'security', '["contact_info", "verification_depth"]', 'Run background check and verify legitimacy', 'Verification report', 'Flag as unverified'),
('schedule_audit', 'calendar', '["date_range", "conflict_types"]', 'Cross-reference calendar items', 'Conflict report', 'List potential issues'); 