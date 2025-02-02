import sqlite3
import json
from datetime import datetime

def connect_db():
    return sqlite3.connect('ursula.db')

def populate_ssml_patterns(conn):
    patterns = [
        ('emotion', 'happy_high', '<amazon:emotion name="happy" intensity="high"><prosody pitch="+15%">TEXT</prosody></amazon:emotion>', 'High intensity happy emotion'),
        ('emotion', 'excited', '<amazon:emotion name="excited" intensity="medium"><prosody rate="110%" pitch="+10%">TEXT</prosody></amazon:emotion>', 'Medium intensity excited emotion'),
        ('emotion', 'disappointed', '<amazon:emotion name="disappointed" intensity="medium"><prosody rate="95%">TEXT</prosody></amazon:emotion>', 'Medium intensity disappointed emotion'),
        ('emotion', 'whispered', '<prosody volume="soft" rate="90%"><amazon:effect name="whispered">TEXT</amazon:effect></prosody>', 'Whispered effect with soft volume'),
        ('prosody', 'soft', '<prosody volume="soft" rate="95%" pitch="-5%">TEXT</prosody>', 'Soft speaking voice'),
        ('prosody', 'loud', '<prosody volume="+20%" rate="105%" pitch="+10%">TEXT</prosody>', 'Loud speaking voice'),
        ('prosody', 'fast_excited', '<prosody rate="fast" pitch="+2st">TEXT</prosody>', 'Fast and excited speaking'),
        ('prosody', 'emphasis', '<prosody volume="+10%" rate="105%">TEXT</prosody>', 'Emphasized speaking')
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
        ('wicked', 'Very', "That's wicked cool.", 'emphasis', 'descriptive', 'Boston'),
        ('packie', 'Liquor store', "Run to the packie", 'casual', 'location', 'Boston'),
        ('bubbler', 'Water fountain', "Get water at the bubbler", 'casual', 'location', 'Boston'),
        ('masshole', 'Massachusetts resident', "Proud to be a Masshole", 'excited', 'social', 'Boston'),
        ('frappe', 'Milkshake', "Get me a chocolate frappe", 'casual', 'food', 'Boston'),
        ('grinder', 'Sub sandwich', "Italian grinder", 'casual', 'food', 'Boston'),
        ('tonic', 'Soda', "Grab a tonic", 'casual', 'food', 'Boston'),
        ('kid', 'Friend/person', "Listen, kid", 'emphasis', 'social', 'Boston'),
        ('sugar', 'Term of endearment', "Hey sugar!", 'emphasis', 'social', 'Boston')
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO slang_terms 
        (term, meaning, usage_example, ssml_pattern_type, category, region)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', terms)
    conn.commit()

def populate_scenes(conn):
    scenes = [
        ('salon_gossip', 'gossip', '''
            <speak>
                ${getPhraseSsml('greetings', 'generalOpener')}
                ${getPhraseSsml('transitions', 'sharingSecret')}
                That ${getSlangSsml('biddy')} from ${getSlangSsml('upTheCorner')} is ${getSlangSsml('wicked')} upset.
                ${getPhraseSsml('transitions', 'addingDetail')}
                She got ${getSlangSsml('bagged')} at the ${getSlangSsml('packie')}.
                ${getPhraseSsml('closings', 'standard')}
            </speak>
        ''', 'Salon gossip scene with Boston slang'),
        ('weather_warning', 'weather', '''
            <speak>
                ${getPhraseSsml('greetings', 'bigNews')}
                We're getting a ${getSlangSsml('wicked')} bad ${getSlangSsml('norEaster')}.
                Better head to the ${getSlangSsml('packie')} before the ${getSlangSsml('flurries')} start.
                ${getPhraseSsml('closings', 'lightHearted')}
            </speak>
        ''', 'Weather warning scene with Boston slang')
    ]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO scenes 
        (scene_name, scene_type, ssml_content, description)
        VALUES (?, ?, ?, ?)
    ''', scenes)
    conn.commit()

def main():
    conn = connect_db()
    try:
        populate_ssml_patterns(conn)
        populate_slang_terms(conn)
        populate_scenes(conn)
        print("Database populated successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main() 