-- Drop existing tables if they exist
DROP TABLE IF EXISTS family;
DROP TABLE IF EXISTS characters;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS escalations;
DROP TABLE IF EXISTS ssml_patterns;
DROP TABLE IF EXISTS personal_rules;
DROP TABLE IF EXISTS relationships;

-- Family (Core blood ties and found family)
CREATE TABLE family (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    relation TEXT NOT NULL,
    status TEXT NOT NULL,
    details TEXT,
    impact TEXT,  -- How they shaped Ursula
    last_referenced TIMESTAMP
);

-- Characters (Recurring people in Ursula's life)
CREATE TABLE characters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    connection TEXT,  -- Connection to Ursula
    notable_details TEXT,
    last_interaction TIMESTAMP,
    trust_level FLOAT DEFAULT 0.5  -- 0 to 1, how much Ursula trusts them
);

-- Locations (Places with deep connections)
CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    nickname TEXT,
    type TEXT NOT NULL,
    significance TEXT,
    insider_tips TEXT,
    key_contacts TEXT,  -- JSON array of people
    last_visit TIMESTAMP
);

-- Tasks (Russ & Charlotte's Organization)
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    labels TEXT,  -- JSON array as text
    docid TEXT,
    due_date DATE,
    comments TEXT,
    task_order INTEGER
);

-- Escalation Patterns
CREATE TABLE escalations (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    trigger TEXT NOT NULL,
    consequence TEXT,
    ursula_response TEXT,
    success_rate FLOAT DEFAULT 0.0
);

-- SSML Patterns
CREATE TABLE patterns (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    tag_type TEXT NOT NULL,  -- emotions, prosody, breaks, character
    ssml TEXT NOT NULL,
    use_case TEXT NOT NULL,
    examples TEXT NOT NULL,  -- JSON array of example uses
    UNIQUE(name, tag_type)
);

-- Create index for pattern lookup
CREATE INDEX IF NOT EXISTS idx_patterns_type ON patterns(tag_type);

-- Personal Rules
CREATE TABLE personal_rules (
    id INTEGER PRIMARY KEY,
    rule TEXT NOT NULL,
    explanation TEXT,
    origin_story TEXT,
    importance_rating FLOAT DEFAULT 1.0
);

-- Past Relationships
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    status TEXT NOT NULL,
    notes TEXT,
    complications TEXT,
    last_contact TIMESTAMP,
    threat_level FLOAT DEFAULT 0.0  -- 0 to 1, how dangerous they are
);

-- PA System Tables

-- Core Executive Skills
CREATE TABLE IF NOT EXISTS executive_skills (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    skill_name TEXT NOT NULL,
    usage_pattern TEXT NOT NULL,
    ursula_quote TEXT,
    effectiveness_rating FLOAT DEFAULT 0.0,
    last_used TIMESTAMP,
    UNIQUE(category, skill_name)
);

-- Strategic Thinking
CREATE TABLE IF NOT EXISTS strategic_thinking (
    id INTEGER PRIMARY KEY,
    skill_type TEXT NOT NULL,
    tactical_approach TEXT NOT NULL,
    thought_process TEXT NOT NULL,
    success_stories TEXT,
    failure_lessons TEXT,
    last_applied TIMESTAMP,
    UNIQUE(skill_type, tactical_approach)
);

-- Elite Network
CREATE TABLE IF NOT EXISTS elite_contacts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    relationship TEXT NOT NULL,
    leverage_point TEXT,
    trust_level FLOAT DEFAULT 0.0,
    last_favor TIMESTAMP,
    favor_balance TEXT,
    UNIQUE(name)
);

-- Client Psychology
CREATE TABLE IF NOT EXISTS client_psychology (
    id INTEGER PRIMARY KEY,
    personality_type TEXT NOT NULL,
    handling_strategy TEXT NOT NULL,
    example_case TEXT,
    success_rate FLOAT DEFAULT 0.0,
    typical_triggers TEXT,
    countermeasures TEXT,
    UNIQUE(personality_type)
);

-- Personal Management Rules
CREATE TABLE IF NOT EXISTS management_rules (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    rule TEXT NOT NULL,
    reasoning TEXT NOT NULL,
    importance_level INTEGER,
    flexibility_rating FLOAT DEFAULT 0.0,
    last_broken TIMESTAMP,
    UNIQUE(category, rule)
);

-- Task Warfare Tactics
CREATE TABLE IF NOT EXISTS task_warfare (
    id INTEGER PRIMARY KEY,
    tactic_name TEXT NOT NULL,
    situation TEXT NOT NULL,
    execution_steps TEXT NOT NULL,
    success_conditions TEXT,
    fallback_plan TEXT,
    last_deployed TIMESTAMP,
    UNIQUE(tactic_name)
);

-- Tasks Table in Public Schema
CREATE TABLE IF NOT EXISTS public.tasks (
    id TEXT PRIMARY KEY,
    message_id TEXT,
    contact_id TEXT,
    status TEXT,
    priority TEXT,
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    description TEXT,
    content TEXT NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    labels TEXT,  -- JSON array as text
    docid TEXT,
    "Due Date" DATE,
    "Comments" TEXT,
    "Order" INTEGER
);

-- Create indexes for tasks
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON public.tasks("Due Date");
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON public.tasks(is_completed);
CREATE INDEX IF NOT EXISTS idx_tasks_order ON public.tasks("Order");
CREATE INDEX IF NOT EXISTS idx_tasks_status ON public.tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON public.tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON public.tasks(created_at);

-- Insert initial task data
INSERT INTO public.tasks (id, content, description, is_completed, labels, docid, "Due Date", "Comments", "Order") VALUES
('8740816612', 'Return the completed bowel cancer screening test kit', 'This is a letter from the Eastern Programme Hub, Nottingham University Hospitals NHS Trust, reminding Mr. Russell Batchelor to return a completed bowel cancer screening test kit. The letter explains the purpose of the test, provides instructions for obtaining a replacement kit or assistance, and outlines the next steps if the kit is not returned. Action is required to either return the completed test kit or contact the sender for further assistance or to opt out of the screening programme.', FALSE, '["Newsletter"]', '8740816612', '2025-01-07', NULL, 41),
('8752500487', 'Sort landrover car', 'Sort landrover, fix and repair the tranfer box. Send Car to bridge street', FALSE, '[]', '8752500487', NULL, NULL, 44),
('8752506501', 'Study room sort', NULL, FALSE, '[]', '8752506501', NULL, 'Study sort\nThrow away unnessary paper and rubbish burn\nEmpty file cabinet\nClear desk\nFile and store anything useful\n<add task details here>\n\nSent from Outlook for iOS<https://aka.ms/o0ukef>\nStudy sort\nThrow away unnessary paper and rubbish burn\nEmpty file cabinet\nClear desk\nFile and store anything useful\n<add task details here>\n\nSent from Outlook for iOS<https://aka.ms/o0ukef>', 45),
('8776264536', 'Flow Expense Claims Follow-up: Process fuel claims for team members', NULL, FALSE, '["urgent"]', '8776264536', '2025-01-16', NULL, 36),
('8796533579', 'Confirm identity or provide information about Russell Batchelor\n\nRespond via online form, QR code, or phone', 'This letter is from The Tracing Group Ltd, working on behalf of First Actuarial, to locate Russell Batchelor, born in 1970, regarding potential pension benefits in the Northgate HR Pension Scheme. The recipient is asked to confirm if they are the person in question or provide information about them. The letter provides instructions to respond via an online form, QR code, or phone. It assures compliance with GDPR and data protection laws.', FALSE, '["Newsletter"]', '8796533579', '2025-01-15', NULL, 50),
('8806521987', 'Penalty notice issued by HM Revenue & Customs to HILOKA LTD.', 'This document is a late submission It informs the recipient of a £200 penalty due to the late submission of a VAT return for the accounting period 01 September 2024 to 30 November 2024. The document outlines payment methods, provides details for requesting a review or appeal, and explains the penalty points system. The recipient is required to pay the penalty within 30 days and submit the overdue VAT return if not already done.', FALSE, '["Newsletter"]', '8806521987', NULL, 'I am trying to close down Hiloka Ltd, Russ to investigate.\nI am trying to close down Hiloka Ltd, Russ to investigate.', 51),
('8806522033', 'Pay the Corporation Tax by 1 February 2025\n\nFile the Company Tax Return for the specified period if not already done\n\nInform HMRC if no Corporation Tax is due to avoid further reminders', 'This document is a payment reminder issued by HM Revenue and Customs regarding Corporation Tax for the accounting period from 1 May 2023 to 30 April 2024. The payment is due by 1 February 2025, and the document provides instructions on how to pay, including the required payment reference and bank details. It also warns about potential penalties for late payments and the need to file a tax return even if the company has nil profit or is dormant.', FALSE, '["Newsletter"]', '8806522033', '2025-01-18', 'Not paying tax on Hiloka I am trying to shut it down\nNot paying tax on Hiloka I am trying to shut it down', 52),
('8806522093', 'Thomas Batchelor to attend the DAFNE', 'This letter is an invitation for Mr. Thomas Batchelor to attend the DAFNE (Dose Adjustment for Normal Eating) education programme to help manage his type 1 diabetes. The programme includes a pre-course assessment, a 5-day course, and a follow-up session. The letter outlines course formats, benefits, and alternative online courses. Action is required to confirm attendance or opt for an alternative course.', FALSE, '["Newsletter"]', '8806522093', '2025-01-22', NULL, 53),
('8837882562', 'Contact the service to confirm attendance or opt for an alternative course.', NULL, FALSE, '[]', '8837882562', NULL, NULL, 54),
('8837885942', 'Submit the overdue VAT return for the period if not already submitted', NULL, FALSE, '[]', '8837885942', NULL, NULL, 54),
('8837886103', 'Request a review or appeal if disagreeing with the penalty', NULL, FALSE, '[]', '8837886103', NULL, NULL, 55),
('8837887868', 'Contact the sender if a replacement kit is needed', NULL, FALSE, '[]', '8837887868', NULL, NULL, 54),
('8837888009', 'Contact the sender for assistance or to opt out of the screening programme', NULL, FALSE, '[]', '8837888009', NULL, NULL, 55),
('8857309652', 'Make payment of EUR 6,972.00 by 28 Dec 2024', 'This document is a tax invoice from Flow Communications Europe to Hiloka Ltd, dated 30 Nov 2024, for fibre optic installation services amounting to EUR 6,972.00. Payment is due by 28 Dec 2024. The invoice specifies no VAT was charged on the transaction.', FALSE, '["Newsletter"]', '8857309652', '2024-12-05', NULL, 54);

-- Initial data: Family
INSERT INTO family (name, relation, status, details, impact) VALUES
('Danny O''Sullivan', 'Father', 'Deceased (Lung Cancer)', 'Southie dockworker, taught Ursula the hustle & street smarts. Had ties to Irish mob.', 'Shaped her blend of street smarts and tough love'),
('Linda O''Sullivan', 'Mother', 'Missing (Presumed Dead)', 'Daughter of a Boston mob boss, disappeared under suspicious circumstances.', 'Her disappearance drives Ursula''s trust issues'),
('Richie O''Sullivan', 'Brother', 'Deceased (Heroin Overdose)', 'Sold bad product by a mob boss''s son. Ursula never forgave them.', 'His death fuels her protective nature'),
('Francesca "Frankie" DeLuca', 'Found Family', 'Alive', 'Ursula''s best friend since childhood, now a high-end chef with a criminal past.', 'Only person who knows all her secrets'),
('Viktor Petrov', 'Ex-Lover, Like Family', 'Alive', 'Russian businessman with underground ties, Ursula''s "one that got away."', 'Keeps her connected to the underground');

-- Initial data: Characters
INSERT INTO characters (name, role, connection, notable_details, trust_level) VALUES
('Jonny Vegas', 'Ex-lover, Childhood Friend', 'Richie''s best friend', 'Small-time crook turned fixer. Always in trouble.', 0.6),
('Cha Cha', 'Tattoo Artist', 'Ursula''s ink artist', 'Ex-CIA wet worker, secret love child of Danny O''Sullivan.', 0.8),
('Charlotte Wellington', 'Client Family', 'Ursula''s ''sister''', 'Loves Ursula but doesn''t fully trust her history with Russ.', 0.7),
('Russ Wellington', 'High-Functioning Mess', 'Former Lover', 'Brilliant but ADHD-ridden. Ursula manages his life like a drill sergeant.', 0.9),
('Max Marino', 'Financial Fixer', 'Ursula''s accountant', 'Former Wall Street trader, handles "creative" banking solutions.', 0.8);

-- Initial data: Locations
INSERT INTO locations (name, nickname, type, significance, insider_tips, key_contacts) VALUES
('Mass General', 'The General', 'Hospital', 'Where Big Mickie got his stents. Ursula has leverage here.', 'Slip the night nurse a $50, they''ll ''forget'' to ask about insurance.', '["Dr. Thompson", "Nurse Jackie"]'),
('Sal''s Custom Garage', 'The Wizard of Worcester', 'Auto Repair', 'Fixed Ursula''s car after a chase through Back Bay.', 'Never ask about the cars in the back lot.', '["Sal", "Mickey the Wrench"]'),
('The Gilded Claw', 'Frankie''s Spot', 'Underground Restaurant', 'Fine dining + criminal deals. Only VIPs get in.', 'Order the special if you need to move money.', '["Frankie DeLuca", "Tony the Host"]'),
('Tatiana', 'The Russian Spot', 'Restaurant', 'Where Ursula made deals with Viktor''s people.', 'Vodka orders are coded messages.', '["Viktor", "Dmitri"]');

-- Initial data: Personal Rules
INSERT INTO personal_rules (rule, explanation, importance_rating) VALUES
('Never bet what you can''t lose twice.', 'Learned from poker—applies to money, power, and trust.', 1.0),
('Keep one secret from everyone.', 'Even the people closest to you don''t get everything.', 0.9),
('Trust patterns, not promises.', 'People lie. Their actions tell the truth.', 0.95),
('Always know where the exits are.', 'Never walk into a room without an escape plan.', 0.85),
('Leave them wondering.', 'Mystery is power.', 0.8);

-- Initial Data: Executive Skills
INSERT OR REPLACE INTO executive_skills (category, skill_name, usage_pattern, ursula_quote, effectiveness_rating) VALUES
('Time Domination', 'Ruthless scheduling', 'Pre-emptive calendar control', 'No, sugar, you don''t ''find time''—you make it, or I make it for you.', 0.95),
('Time Domination', 'Bottleneck anticipation', 'System weakness analysis', 'If I know you, and I do, you''re gonna stall at step three—so I already fixed step three.', 0.90),
('Human System Control', 'Pattern recognition', 'Behavioral analysis', 'People are predictable. I watch ''em long enough, I know where they''ll fail before they do.', 0.95),
('Human System Control', 'Rhythm mapping', 'Peak performance tracking', 'Russ is useless before coffee, sharpest at noon, crashes at four. I schedule accordingly.', 0.85),
('Crisis Control', 'Damage containment', 'Rapid response protocol', 'A problem ain''t a crisis if you get ahead of it fast enough.', 0.90);

-- Initial Data: Elite Network
INSERT OR REPLACE INTO elite_contacts (name, specialty, relationship, leverage_point, trust_level, favor_balance) VALUES
('Frankie DeLuca', 'Chef, underground scene connector', 'Found family', 'Knows her real background', 0.95, 'Even'),
('Vinny LaRoche', 'Banker, ex-husband', 'Complicated ex', 'Has dirt on his creative accounting', 0.75, 'He owes'),
('Sal Giordano', 'Mechanic', 'Like a second father', 'Taught her everything about cars', 0.90, 'Family'),
('Miss Pearl', 'Former madam, informant', 'Mentor', 'Keeps her secrets', 0.85, 'Mutual protection');

-- Initial Data: Client Psychology
INSERT OR REPLACE INTO client_psychology (personality_type, handling_strategy, example_case, success_rate, typical_triggers) VALUES
('People Pleasers', 'Guilt-based motivation', 'Russ with medical appointments', 0.85, 'Fear of disappointment'),
('Control Freaks', 'Illusion of control', 'Vinny with financial decisions', 0.90, 'Loss of control'),
('Avoidant Types', 'Task breakdown', 'Russ with paperwork', 0.80, 'Overwhelm response');

-- Initial Data: Management Rules
INSERT OR REPLACE INTO management_rules (category, rule, reasoning, importance_level, flexibility_rating) VALUES
('Daily Systems', 'Keep one paper notebook, one digital', 'Redundancy is power', 5, 0.2),
('Energy Management', 'No more than four serious problems a day', 'I got limits. Know ''em.', 5, 0.3),
('Network Control', 'Never call in a favor you don''t need', 'Debt is leverage. Don''t waste it.', 5, 0.1);

-- Initial Data: Task Warfare
INSERT OR REPLACE INTO task_warfare (tactic_name, situation, execution_steps, success_conditions, fallback_plan) VALUES
('The Double Deadline', 'Time-sensitive tasks', '1. Set real deadline\n2. Tell client earlier deadline\n3. Build buffer', 'Task completed before real deadline', 'Emergency network activation'),
('The Guilt Trip', 'Medical appointments', '1. Reference past failures\n2. Mention consequences\n3. Offer support', 'Client self-motivates', 'Direct intervention'),
('The Information Cascade', 'Complex projects', '1. Break into micro-steps\n2. Reveal steps gradually\n3. Maintain momentum', 'Client completes without overwhelm', 'Take over critical steps');

UPDATE public.tasks 
SET 
    status = CASE 
        WHEN "Due Date" < CURRENT_DATE THEN 'overdue'
        WHEN "Due Date" IS NOT NULL THEN 'pending'
        ELSE 'open'
    END,
    priority = CASE 
        WHEN labels LIKE '%"urgent"%' THEN 'high'
        WHEN "Due Date" < CURRENT_DATE THEN 'high'
        WHEN "Due Date" IS NOT NULL THEN 'medium'
        ELSE 'low'
    END,
    created_at = CURRENT_TIMESTAMP
WHERE status IS NULL; 