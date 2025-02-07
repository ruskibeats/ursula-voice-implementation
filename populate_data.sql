-- Populate task routing
INSERT INTO task_routing (task_type, handled_by_ursula, ai_agent, routing_rules) VALUES
('Financial_High_Value', true, 'Marcus_AI', 'Route high-value financial tasks'),
('Medical_Routine', false, 'Health_AI', 'Route routine medical tasks'),
('Legal_Documentation', false, 'Benny_AI', 'Route legal document processing'),
('PR_Crisis', true, 'Media_AI', 'Route PR crisis management'),
('Routine_Errands', false, 'Logistics_AI', 'Route daily errands')
ON CONFLICT (task_type) DO NOTHING;

-- Populate behavior patterns
INSERT INTO behavior_patterns (pattern_type, category, frequency, notes) VALUES
('Morning_Routine', 'Daily', 5, 'Regular morning activities pattern'),
('Work_Focus', 'Productivity', 3, 'Deep work concentration pattern'),
('Evening_Wind_Down', 'Daily', 4, 'Evening relaxation routine'),
('Exercise_Routine', 'Health', 2, 'Regular exercise pattern'),
('Social_Interaction', 'Communication', 3, 'Social engagement pattern')
ON CONFLICT DO NOTHING;

-- Populate decision authority
INSERT INTO decision_authority (category, authority_level, description, risk_level, review_required) VALUES
('Financial', 'High', 'High-value financial decisions', 3, true),
('Medical', 'Medium', 'Routine medical decisions', 2, true),
('Schedule', 'Low', 'Daily schedule management', 1, false),
('Communication', 'Medium', 'External communication decisions', 2, true),
('Task_Priority', 'High', 'Task prioritization decisions', 3, true)
ON CONFLICT DO NOTHING;

-- Populate ai_escalation_triggers
INSERT INTO ai_escalation_triggers (ai_agent, trigger_condition, action_required, threshold) VALUES
('Health_AI', 'Health metrics outside normal range', 'Alert medical team', 0.9),
('Marcus_AI', 'Unusual financial pattern detected', 'Freeze transactions and review', 0.95),
('Benny_AI', 'Legal risk identified', 'Escalate to legal team', 0.85),
('Media_AI', 'Negative PR sentiment detected', 'Initiate PR response protocol', 0.8),
('Logistics_AI', 'Schedule conflict detected', 'Reorganize priority tasks', 0.75)
ON CONFLICT DO NOTHING;

-- Populate family members
INSERT INTO family_members (name, role, preferences, active) VALUES
('Russell', 'Primary', '{"schedule_preference": "morning", "communication_style": "direct"}', true),
('Sarah', 'Partner', '{"schedule_preference": "flexible", "communication_style": "detailed"}', true),
('Max', 'Pet', '{"schedule_preference": "regular", "care_needs": "high"}', true)
ON CONFLICT (name) DO NOTHING;

-- Populate voice patterns
INSERT INTO voice_patterns (emotion, ssml_template, description, use_case) VALUES
('Calm', '<speak><prosody rate="slow" pitch="low">{{text}}</prosody></speak>', 'Calming voice pattern', 'Relaxation prompts'),
('Energetic', '<speak><prosody rate="fast" pitch="high">{{text}}</prosody></speak>', 'Energetic voice pattern', 'Motivation prompts'),
('Focused', '<speak><prosody rate="medium" pitch="medium">{{text}}</prosody></speak>', 'Focused voice pattern', 'Task instructions')
ON CONFLICT DO NOTHING;

-- Populate adhd patterns
INSERT INTO adhd_patterns (pattern_name, triggers, coping_strategies, severity) VALUES
('Task_Switching', '["interruptions", "notifications", "time pressure"]', '["pomodoro technique", "environment control"]', 3),
('Hyperfocus', '["interesting tasks", "deadlines", "creative work"]', '["time blocking", "regular breaks"]', 2),
('Executive_Function', '["complex tasks", "decision making", "planning"]', '["task breakdown", "external structure"]', 4)
ON CONFLICT DO NOTHING;

-- Populate failure stories
INSERT INTO failure_stories (title, description, lessons_learned, date_occurred, prevention_steps) VALUES
('Missed Deadline', 'Important project deadline was missed due to poor time management', 
'["Set earlier internal deadlines", "Break down large tasks", "Regular progress checks"]',
CURRENT_TIMESTAMP - INTERVAL '30 days',
'["Use time blocking", "Set reminders", "Daily progress review"]'),
('Communication Gap', 'Critical information was not properly communicated to team members',
'["Establish clear communication channels", "Regular status updates", "Confirmation of receipt"]',
CURRENT_TIMESTAMP - INTERVAL '15 days',
'["Use communication checklist", "Follow-up protocol", "Documentation system"]')
ON CONFLICT DO NOTHING; 