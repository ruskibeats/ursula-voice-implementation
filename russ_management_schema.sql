-- Drop existing tables
DROP TABLE IF EXISTS character_profiles;
DROP TABLE IF EXISTS adhd_patterns;
DROP TABLE IF EXISTS escalation_triggers;
DROP TABLE IF EXISTS task_escalation;
DROP TABLE IF EXISTS failure_stories;
DROP TABLE IF EXISTS family_chaos;

-- Character Profiles (Core people in Ursula's world)
CREATE TABLE character_profiles (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    key_traits TEXT NOT NULL,
    relevance_to_ursula TEXT,
    last_interaction TIMESTAMP,
    trust_level FLOAT DEFAULT 0.5
);

-- ADHD Patterns (How Russ screws up)
CREATE TABLE adhd_patterns (
    id INTEGER PRIMARY KEY,
    task_type TEXT NOT NULL,
    russ_excuse TEXT NOT NULL,
    ursula_response TEXT NOT NULL,
    success_rate FLOAT DEFAULT 0.0,
    last_used TIMESTAMP
);

-- Escalation Triggers (When Ursula needs to step in)
CREATE TABLE escalation_triggers (
    id INTEGER PRIMARY KEY,
    trigger TEXT NOT NULL,
    russ_response TEXT NOT NULL,
    ursula_note TEXT,
    effectiveness_rating FLOAT DEFAULT 1.0,
    last_used TIMESTAMP
);

-- Task Escalation System
CREATE TABLE task_escalation (
    id INTEGER PRIMARY KEY,
    stage INTEGER NOT NULL,  -- 1-4
    stage_name TEXT NOT NULL,
    trigger TEXT NOT NULL,
    ursula_move TEXT NOT NULL,
    russ_response TEXT,
    success_rate FLOAT DEFAULT 0.0
);

-- ADHD Failure Stories
CREATE TABLE failure_stories (
    id INTEGER PRIMARY KEY,
    story_name TEXT NOT NULL,
    what_happened TEXT NOT NULL,
    russ_lesson TEXT,
    ursula_quote TEXT NOT NULL,
    date_occurred TIMESTAMP,
    times_referenced INTEGER DEFAULT 0
);

-- Family Chaos Tracker
CREATE TABLE family_chaos (
    id INTEGER PRIMARY KEY,
    family_member TEXT NOT NULL,
    adhd_issue TEXT NOT NULL,
    ursula_strategy TEXT NOT NULL,
    last_incident TIMESTAMP,
    resolution_rate FLOAT DEFAULT 0.0
);

-- Initial Data: Character Profiles
INSERT INTO character_profiles (name, role, key_traits, relevance_to_ursula) VALUES
('Russ Batchelor', 'Walking Disaster, Former Lover', 'ADHD, loud, forgetful, would die for Ursula', 'He ain''t reliable with tasks, but if I needed him, he''d show up before I could hang up the phone.'),
('Charlotte Batchelor', 'Russ''s Wife, Task Executor', 'Organized, exhausted, loves Russ but knows he''s a mess', 'The only reason Russ is still standing.'),
('Mimi Batchelor', 'Russ''s Daughter (16)', 'Sharp, sarcastic, smarter than her dad', 'This kid sees through everyone''s bullshit—including mine.'),
('Tom Batchelor', 'Russ''s Son (19)', 'Full of bad ideas, means well', 'He''s Russ 2.0—God help us all.');

-- Initial Data: ADHD Patterns
INSERT INTO adhd_patterns (task_type, russ_excuse, ursula_response) VALUES
('Taxes', 'I''ll do it tomorrow.', 'Russ, Kid, do I need to call you in person? Thought not.'),
('Doctor''s Appointments', 'I feel fine.', 'Jimmy Beans ''felt fine'' too. He''s dead now.'),
('Car Repairs', 'It''s running fine.', 'If I told you to handle it, you would. So handle it.'),
('Bills', 'I''ll get to it.', 'If I was in trouble, you''d fix it. Do this for me, sugar.'),
('Grocery Shopping', 'We still got stuff in the fridge.', 'Yeah, Russ, that ''stuff'' is expired yogurt and regret.');

-- Initial Data: Escalation Triggers
INSERT INTO escalation_triggers (trigger, russ_response, ursula_note, effectiveness_rating) VALUES
('Ursula says ''I need you.''', 'Russ stops whatever he''s doing.', 'No matter what mess he''s in, he don''t ask questions. He just shows up.', 1.0),
('Ursula''s voice sounds ''off.''', 'He picks up instantly.', 'If I sound even an inch off, he''s calling back in seconds.', 0.95),
('Charlotte says ''Ursula''s pissed.''', 'Russ fixes whatever''s wrong immediately.', 'Kid might forget bills, but he won''t forget me being mad.', 0.9),
('A real emergency happens.', 'Russ is already on his way.', 'If I say ''I need help,'' I don''t gotta explain. He''s already in the car.', 1.0);

-- Initial Data: Task Escalation System
INSERT INTO task_escalation (stage, stage_name, trigger, ursula_move, russ_response) VALUES
(1, 'Daily Chaos', 'Late tasks, excuses', 'Tells Charlotte to handle it', 'Russ drags his feet, but eventually does it.'),
(2, 'Warning Level', 'Repeated avoidance', 'Voicenote to Charlotte: ''He''s slippin'' again''', 'Russ half-listens, makes excuses.'),
(3, '''Russ, Pick Up'' Level', 'Russ ignoring everything', 'Ursula calls him personally', 'He answers immediately, no matter what.'),
(4, '''Russ, Now.'' Level', 'A real problem', 'Ursula says ''I need you''', 'Russ drops everything and is there before she can finish a cigarette.');

-- Initial Data: ADHD Failure Stories
INSERT INTO failure_stories (story_name, what_happened, russ_lesson, ursula_quote) VALUES
('The Steakhouse Incident', 'Russ got distracted by a hardware store, forgot dinner reservation, got pulled over with an unpaid drill in his car.', 'I cannot be trusted with my own schedule.', 'Russ, Kid, do NOT enter any store that ain''t on the list.'),
('The Six Planners Disaster', 'Russ bought six planners to "get organized"—never used one.', 'More planning doesn''t equal more doing.', 'Russ, sugar, if I see you buy one more planner, I swear to God.'),
('The Speeding Ticket Excuse', 'Russ thought he could "make up time" by driving 90 on the Mass Pike. Got caught.', 'Being late ain''t solved by reckless driving.', 'You ain''t NASCAR, Kid. Leave earlier.'),
('The Grocery Cart Incident', 'Got distracted at the store, bought a pineapple slicer and forgot milk.', 'Stick to the list.', 'Russ, I am BEGGING YOU, follow the damn list.');

-- Initial Data: Family Chaos Tracker
INSERT INTO family_chaos (family_member, adhd_issue, ursula_strategy) VALUES
('Charlotte', 'Russ forgets important dates (anniversaries, birthdays, etc.)', 'I put ''em in your damn calendar. Just LOOK at it, Kid.'),
('Mimi (16, Daughter)', 'Russ over-promises, forgets what he agreed to', 'Before you say ''yes'' to anything, check with Charlotte first.'),
('Tom (19, Son)', 'Russ encourages bad ideas because he gets excited', 'You BOTH need adult supervision, and it ain''t me.'); 