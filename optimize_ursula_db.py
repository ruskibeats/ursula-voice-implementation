import sqlite3

def optimize_database():
    conn = sqlite3.connect('ursula.db')
    cursor = conn.cursor()
    
    # Add indexes for frequently accessed columns
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_ssml_patterns_type_name 
        ON ssml_patterns(pattern_type, pattern_name)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_slang_terms_category 
        ON slang_terms(category)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_slang_terms_region 
        ON slang_terms(region)
    ''')
    
    # Add new tables for better organization
    
    # Required phrases table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS required_phrases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phrase_type TEXT NOT NULL,
            phrase_text TEXT NOT NULL,
            ssml_pattern_type TEXT NOT NULL,
            ssml_pattern_name TEXT NOT NULL,
            context TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(phrase_type, phrase_text)
        )
    ''')
    
    # Scene templates table with improved structure
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scene_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_name TEXT NOT NULL,
            template_type TEXT NOT NULL,
            base_emotion TEXT NOT NULL,
            structure TEXT NOT NULL,
            required_elements TEXT NOT NULL,
            optional_elements TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(template_name)
        )
    ''')
    
    # Character traits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS character_traits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trait_type TEXT NOT NULL,
            trait_value TEXT NOT NULL,
            ssml_impact TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(trait_type, trait_value)
        )
    ''')
    
    # Populate required phrases
    required_phrases = [
        ('greeting', 'Hey sugar!', 'emotion', 'happy_high', 'Standard greeting'),
        ('greeting', 'Hey sweetie!', 'emotion', 'happy_high', 'Alternative greeting'),
        ('transition', 'Now honey...', 'prosody', 'soft', 'Tough love transition'),
        ('reaction', 'Bless his heart', 'emotion', 'disappointed', 'Reaction to chaos'),
        ('closing', 'Your girl Ursula', 'prosody', 'emphasis', 'Standard sign-off')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO required_phrases 
        (phrase_type, phrase_text, ssml_pattern_type, ssml_pattern_name, context)
        VALUES (?, ?, ?, ?, ?)
    ''', required_phrases)
    
    # Populate scene templates
    scene_templates = [
        ('task_update', 'update', 'excited', 
         '[GREETING][TASKS][PERSONAL][CLOSING]',
         'greeting,tasks,closing',
         'personal_update'),
        ('gossip', 'social', 'whispered',
         '[GREETING][SECRET][DETAILS][REACTION][CLOSING]',
         'greeting,secret,closing',
         'personal_gossip')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO scene_templates 
        (template_name, template_type, base_emotion, structure, required_elements, optional_elements)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', scene_templates)
    
    # Populate character traits
    character_traits = [
        ('voice', 'smoker', 'prosody:rate=95%', 'Half-pack-a-day smoker voice'),
        ('personality', 'tough_love', 'emotion:disappointed+prosody:soft', 'Tough love approach'),
        ('background', 'boston', 'none', 'Boston finance background'),
        ('relationship', 'auntie', 'prosody:volume=+10%', 'Protective auntie figure')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO character_traits 
        (trait_type, trait_value, ssml_impact, description)
        VALUES (?, ?, ?, ?)
    ''', character_traits)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    optimize_database()
    print("Database optimization complete!") 