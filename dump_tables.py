import sqlite3
import json

def dump_all_tables():
    conn = sqlite3.connect('ursula.db')
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    universe_data = {}
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        table_data = []
        for row in rows:
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[col] = row[i]
            table_data.append(row_dict)
            
        universe_data[table_name] = table_data

    conn.close()

    # Write to file with nice formatting
    with open('ursula_universe_complete.json', 'w') as f:
        json.dump({
            "ursula_universe": {
                "core_identity": {
                    "family": universe_data.get('family', []),
                    "characters": universe_data.get('characters', []),
                    "relationships": universe_data.get('relationships', [])
                },
                "locations_and_networks": {
                    "locations": universe_data.get('locations', []),
                    "elite_contacts": universe_data.get('elite_contacts', [])
                },
                "skills_and_tactics": {
                    "executive_skills": universe_data.get('executive_skills', []),
                    "task_warfare": universe_data.get('task_warfare', []),
                    "strategic_thinking": universe_data.get('strategic_thinking', [])
                },
                "psychology_and_rules": {
                    "client_psychology": universe_data.get('client_psychology', []),
                    "personal_rules": universe_data.get('personal_rules', []),
                    "management_rules": universe_data.get('management_rules', [])
                },
                "task_management": {
                    "tasks": universe_data.get('tasks', []),
                    "escalations": universe_data.get('escalations', [])
                },
                "voice_patterns": {
                    "patterns": universe_data.get('patterns', []),
                    "ssml_patterns": universe_data.get('ssml_patterns', [])
                },
                "russ_management": {
                    "character_profiles": universe_data.get('character_profiles', []),
                    "adhd_patterns": universe_data.get('adhd_patterns', []),
                    "escalation_triggers": universe_data.get('escalation_triggers', []),
                    "task_escalation": universe_data.get('task_escalation', []),
                    "failure_stories": universe_data.get('failure_stories', []),
                    "family_chaos": universe_data.get('family_chaos', [])
                }
            }
        }, f, indent=2)

if __name__ == '__main__':
    dump_all_tables() 