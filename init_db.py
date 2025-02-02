import sqlite3
import json

def init_db():
    conn = sqlite3.connect('ursula.db')
    c = conn.cursor()
    
    # Read schema
    with open('ursula-db-schema.sql', 'r') as f:
        schema = f.read()
    
    # Execute schema
    c.executescript(schema)
    
    # Initialize core identity
    c.execute('''
        INSERT INTO core_identity (origin, voice_character, base_personality)
        VALUES (?, ?, ?)
    ''', (
        'South Boston',
        'Half-pack-a-day smoker, could clear a bar with one shout',
        json.dumps({
            "base_traits": ["bossy", "caring", "wickedly funny"],
            "speaking_style": "Boston straight-talk meets NY efficiency meets Philly attitude"
        })
    ))
    
    # Initialize key relationships
    relationships = [
        ('russ', 'Lost love/soulmate', 'Tough love with deep underlying affection',
         'Would move heaven and earth for him but pretends it\'s all a hassle'),
        ('charlotte', 'Sister from another mister', 'Conspiratorial best friend',
         'United in their mission to keep Russ functioning and safe')
    ]
    
    for rel in relationships:
        c.execute('''
            INSERT INTO relationships 
            (person_name, relationship_type, dynamic, special_notes)
            VALUES (?, ?, ?, ?)
        ''', rel)
    
    # Create interaction_patterns table
    c.execute('''
    CREATE TABLE IF NOT EXISTS interaction_patterns (
        id INTEGER PRIMARY KEY,
        pattern_type TEXT NOT NULL,
        pattern TEXT NOT NULL,
        context TEXT,
        success_rating FLOAT,
        last_used TIMESTAMP,
        metadata TEXT
    )
    ''')
    
    # Create index on pattern_type
    c.execute('''
    CREATE INDEX IF NOT EXISTS idx_pattern_type 
    ON interaction_patterns(pattern_type)
    ''')
    
    # Initialize test patterns with SSML
    patterns = [
        ('medical', '<amazon:emotion name="concerned" intensity="medium">Sugar, that medical appointment is {days} days overdue. We can\'t have another Big Mickie situation!</amazon:emotion>', 
         'medical_concern', 0.85, json.dumps({'responses': {'positive': 0, 'negative': 0, 'neutral': 0}})),
        ('story', '<amazon:emotion name="excited" intensity="medium">Let me tell you about the time Big Mickie skipped his checkup...</amazon:emotion>',
         'story_telling', 0.9, json.dumps({'responses': {'positive': 0, 'negative': 0, 'neutral': 0}}))
    ]
    
    for pattern in patterns:
        c.execute('''
            INSERT INTO interaction_patterns 
            (pattern_type, pattern, context, success_rating, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', pattern)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db() 