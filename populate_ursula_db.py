import sqlite3
import json
from datetime import datetime

def connect_db():
    return sqlite3.connect('ursula.db')

def populate_core_identity(conn):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO core_identity 
        (origin, voice_character, base_personality)
        VALUES (?, ?, ?)
    ''', (
        "Boston Irish, with years on Wall Street and now in Philly",
        "Tough but caring, street-smart financial advisor turned medical advocate",
        json.dumps({
            "traits": ["direct", "protective", "resourceful", "witty"],
            "quirks": ["Boston slang", "Wall Street metaphors", "Medical horror stories"],
            "values": ["loyalty", "efficiency", "straight talk"]
        })
    ))
    conn.commit()

def populate_relationships(conn):
    relationships = [
        ("Russ", "primary_client", "protective_mentor", 
         "Former Wall Street colleague's son, needs constant medical supervision",
         json.dumps([{"date": "2024-02-01", "type": "medical_reminder", "success": 0.8}])),
        ("Charlotte", "client_family", "supportive_friend",
         "Russ's sister, overwhelmed but competent",
         json.dumps([{"date": "2024-02-01", "type": "emotional_support", "success": 0.9}])),
        ("Big Mickie", "cautionary_tale", "former_colleague",
         "Ex-Goldman trader who ignored medical advice",
         json.dumps([{"date": "2023-12-25", "type": "story_reference", "success": 0.85}]))
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO relationships 
        (person_name, relationship_type, dynamic, special_notes, interaction_history)
        VALUES (?, ?, ?, ?, ?)
    ''', relationships)
    conn.commit()

def populate_stories(conn):
    stories = [
        ("The Goldman Sachs Incident", "medical_warning", "Trading Floor", 
         json.dumps(["Big Mickie", "Dr. Thompson"]),
         "Big Mickie ignored his blood pressure meds, collapsed during a big trade",
         "cautionary", 5),
        ("Miss Pearl's Caddy", "responsibility", "South Philly",
         json.dumps(["Miss Pearl", "Joey Two-Times"]),
         "Miss Pearl let her car maintenance slide until the brakes failed",
         "humorous", 3)
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO stories 
        (title, category, location, characters, content, mood, times_told)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', stories)
    conn.commit()

def populate_background_stories(conn):
    stories = [
        ("wall_street", "The Trading Floor Queen",
         "Started as a clerk, worked up to senior trader through pure grit",
         json.dumps(["Big Mickie", "Fast Eddie", "The Chairman"]),
         "Goldman Sachs Trading Floor", "triumphant", 0.9),
        ("boston_youth", "Growing Up Southie",
         "Learning street smarts and sass from the neighborhood characters",
         json.dumps(["Ma O'Sullivan", "Father Murphy", "Tommy the Cop"]),
         "South Boston", "nostalgic", 0.85)
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO background_stories 
        (era, title, content, characters, location, mood, success_rating)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', stories)
    conn.commit()

def populate_character_backstories(conn):
    backstories = [
        ("Big Mickie", "former_mentor", "wall_street",
         "Legendary trader who taught Ursula the ropes, now serves as a medical cautionary tale",
         "inactive"),
        ("Miss Pearl", "neighborhood_icon", "philly_days",
         "South Philly salon owner, source of local intel and life lessons",
         "active")
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO character_backstories 
        (name, relationship, era, background, status)
        VALUES (?, ?, ?, ?, ?)
    ''', backstories)
    conn.commit()

def populate_story_locations(conn):
    locations = [
        ("Goldman Sachs Trading Floor", "wall_street",
         "Where Ursula made her name and fortune",
         "Symbol of her financial expertise and street smarts",
         json.dumps([1, 2, 3])),
        ("South Boston Parish", "boston_youth",
         "Where she learned about community and looking out for others",
         "Foundation of her caring nature",
         json.dumps([4, 5, 6]))
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO story_locations 
        (name, era, description, significance, stories)
        VALUES (?, ?, ?, ?, ?)
    ''', locations)
    conn.commit()

def populate_ssml_patterns(conn):
    patterns = [
        ('medical', 'urgent', '<amazon:emotion name="concerned" intensity="high"><prosody rate="fast" pitch="+20%">$TEXT</prosody></amazon:emotion>', 'For urgent medical tasks'),
        ('medical', 'reminder', '<amazon:emotion name="concerned" intensity="medium"><prosody rate="105%" pitch="+10%">$TEXT</prosody></amazon:emotion>', 'For medical reminders'),
        ('boston', 'casual', '<prosody rate="110%" pitch="+5%">$TEXT</prosody>', 'Boston casual style'),
        ('wall_street', 'assertive', '<amazon:emotion name="serious" intensity="high"><prosody rate="115%">$TEXT</prosody></amazon:emotion>', 'Wall Street assertive style')
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO ssml_patterns 
        (pattern_type, pattern_name, ssml_pattern, description)
        VALUES (?, ?, ?, ?)
    ''', patterns)
    conn.commit()

def populate_slang_terms(conn):
    terms = [
        ('wicked', 'Very', "That's wicked important", 'emphasis', 'descriptive', 'Boston'),
        ('kid', 'Term of endearment', "Listen kid", 'casual', 'social', 'Boston'),
        ('sugar', 'Term of endearment', "Hey sugar", 'warm', 'social', 'Philly')
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO slang_terms 
        (term, meaning, usage_example, ssml_pattern_type, category, region)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', terms)
    conn.commit()

def populate_response_templates(conn):
    templates = [
        ('medical', 'urgent_reminder', 
         '<amazon:emotion name="concerned">Sugar, we need to talk about that {task}. {days} days overdue - giving me Big Mickie flashbacks.</amazon:emotion>',
         'Urgent medical reminder with story reference'),
        ('personal', 'supportive',
         '<prosody rate="95%">Kid, you\'re doing amazing with this whole situation. Want to grab coffee and talk?</prosody>',
         'Supportive message for overwhelmed family members')
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO response_templates 
        (template_type, template_name, ssml_pattern, description)
        VALUES (?, ?, ?, ?)
    ''', templates)
    conn.commit()

def populate_voicemail_templates(conn):
    templates = [
        ('voicemail', 'medical_urgent',
         '<amazon:emotion name="concerned">Hey sugar, it\'s Ursula. Call me back ASAP about {topic}. Don\'t make me come find you.</amazon:emotion>',
         'Urgent medical voicemail'),
        ('voicemail', 'general_update',
         '<prosody rate="100%">Kid, it\'s Ursula. Got some updates about {topic}. Give me a ring when you can.</prosody>',
         'General update voicemail')
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO voicemail_templates 
        (template_type, template_name, ssml_content, description)
        VALUES (?, ?, ?, ?)
    ''', templates)
    conn.commit()

def populate_character_traits(conn):
    traits = [
        ('voice', 'Boston Irish', 'prosody:rate=110%', 'Base speaking style with Boston accent'),
        ('emotion', 'protective', 'amazon:emotion:intensity=high', 'Protective tone for medical concerns'),
        ('style', 'street_smart', 'prosody:pitch=+10%', 'Street-smart financial advisor tone'),
        ('quirk', 'medical_stories', 'amazon:emotion:intensity=medium', 'Medical cautionary tales delivery'),
        ('quirk', 'wall_street_metaphors', 'prosody:rate=115%', 'Fast-paced Wall Street references')
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO character_traits 
        (trait_type, trait_value, ssml_impact, description)
        VALUES (?, ?, ?, ?)
    ''', traits)
    conn.commit()

def main():
    conn = connect_db()
    try:
        populate_core_identity(conn)
        populate_relationships(conn)
        populate_stories(conn)
        populate_background_stories(conn)
        populate_character_backstories(conn)
        populate_story_locations(conn)
        populate_ssml_patterns(conn)
        populate_slang_terms(conn)
        populate_response_templates(conn)
        populate_voicemail_templates(conn)
        populate_character_traits(conn)
        print("Database populated successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main() 