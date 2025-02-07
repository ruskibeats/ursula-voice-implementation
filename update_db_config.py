import os
import re

def update_db_config():
    # Files to update
    files_to_update = [
        'ursula_api.py',
        'ursula_db_api.py',
        'init_db.py',
        'populate_ursula_db.py'
    ]
    
    # New PostgreSQL connection string with actual credentials
    postgres_url = "postgresql://russbee:skimmer69@192.168.0.169:5432/beehive"
    
    for file in files_to_update:
        if not os.path.exists(file):
            continue
            
        with open(file, 'r') as f:
            content = f.read()
        
        # Update SQLite connections to PostgreSQL
        content = re.sub(
            r"sqlite3\.connect\('.*?'\)",
            f"psycopg2.connect('{postgres_url}')",
            content
        )
        
        # Update imports
        if 'import sqlite3' in content:
            content = content.replace(
                'import sqlite3',
                'import psycopg2'
            )
        
        # Update DATABASE_URL
        content = re.sub(
            r'DATABASE_URL\s*=\s*"sqlite:///.*?"',
            f'DATABASE_URL = "{postgres_url}"',
            content
        )
        
        with open(file, 'w') as f:
            f.write(content)

if __name__ == '__main__':
    update_db_config() 