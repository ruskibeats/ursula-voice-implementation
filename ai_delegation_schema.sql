-- AI Delegation System Schema

-- Task Routing System
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

-- AI Agents Configuration
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

-- Escalation Matrix
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

-- Decision Authority Matrix
CREATE TABLE IF NOT EXISTS decision_authority (
    id INTEGER PRIMARY KEY,
    decision_type TEXT NOT NULL,
    authority_level TEXT CHECK (authority_level IN ('AI_ONLY', 'AI_SUPERVISED', 'URSULA_ONLY', 'HYBRID')),
    reasoning TEXT NOT NULL,
    risk_level INTEGER CHECK (risk_level BETWEEN 1 AND 5),
    review_required BOOLEAN DEFAULT true,
    UNIQUE(decision_type)
);

-- Data Sources
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

-- Data Processing Rules
CREATE TABLE IF NOT EXISTS processing_rules (
    id INTEGER PRIMARY KEY,
    step_name TEXT NOT NULL,
    process_type TEXT NOT NULL,
    rules TEXT NOT NULL,  -- JSON array of processing rules
    priority_order INTEGER,
    success_criteria TEXT,
    failure_action TEXT,
    last_run TIMESTAMP,
    UNIQUE(step_name)
);

-- Priority Matrix
CREATE TABLE IF NOT EXISTS priority_matrix (
    id INTEGER PRIMARY KEY,
    level_name TEXT NOT NULL,
    urgency_score INTEGER CHECK (urgency_score BETWEEN 1 AND 5),
    response_time TEXT NOT NULL,
    notification_method TEXT NOT NULL,
    auto_actions TEXT,  -- JSON array of automatic actions
    ursula_quote TEXT,  -- Characteristic response
    UNIQUE(level_name)
);

-- Red Flag Triggers
CREATE TABLE IF NOT EXISTS red_flags (
    id INTEGER PRIMARY KEY,
    trigger_name TEXT NOT NULL,
    conditions TEXT NOT NULL,  -- JSON array of trigger conditions
    severity_level INTEGER CHECK (severity_level BETWEEN 1 AND 5),
    immediate_actions TEXT NOT NULL,
    notification_priority TEXT NOT NULL,
    cooldown_period TEXT,  -- How long before triggering again
    last_triggered TIMESTAMP,
    UNIQUE(trigger_name)
);

-- AI Commands
CREATE TABLE IF NOT EXISTS ai_commands (
    id INTEGER PRIMARY KEY,
    command_name TEXT NOT NULL,
    command_type TEXT NOT NULL,
    parameters TEXT,  -- JSON array of required parameters
    execution_steps TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    error_handling TEXT,
    last_used TIMESTAMP,
    UNIQUE(command_name)
);

-- Initial Data: AI Agents
INSERT INTO ai_agents (agent_name, specialty, trust_level, oversight_required) VALUES
('Marcus_AI', 'Financial Analysis & Tracking', 0.8, 'All transfers over $10k need Ursula''s approval'),
('Health_AI', 'Medical Scheduling & Monitoring', 0.7, 'Escalate after 3 missed appointments'),
('Benny_AI', 'Legal Document Processing', 0.6, 'All court documents need review'),
('Media_AI', 'Social Media & PR Monitoring', 0.5, 'Alert on any potential PR issues'),
('Logistics_AI', 'Routine Task Management', 0.9, 'Weekly completion rate review');

-- Initial Data: Task Routing
INSERT INTO task_routing (task_type, handled_by_ursula, delegated_to, routing_logic, ursula_oversight) VALUES
('Financial_High_Value', true, 'Marcus_AI', 'High-stakes financial decisions need human intuition', 'Final approval on all transactions over $10k'),
('Medical_Routine', false, 'Health_AI', 'Routine appointments can be AI-managed through Charlotte', 'Steps in after 3 missed appointments'),
('Legal_Documentation', false, 'Benny_AI', 'Standard legal docs can be AI-processed', 'Reviews all court-related documents'),
('PR_Crisis', true, 'Media_AI', 'Reputation management needs human touch', 'Personally handles all media responses'),
('Routine_Errands', false, 'Logistics_AI', 'Low-risk tasks suitable for AI', 'Only monitors completion rates');

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