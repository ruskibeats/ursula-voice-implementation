import psycopg2
import json
from datetime import datetime

def populate_trust():
    conn = psycopg2.connect(
        'postgresql://russbee:skimmer69@192.168.0.169:5432/beehive',
        client_encoding='utf8'
    )
    c = conn.cursor()

    # Trust system data
    trust_data = [
        {
            "person_id": 2,  # Russ
            "name": "Russ Batchelor",
            "trust_level": 5,
            "trust_history": json.dumps([
                "The 3AM Hospital Run",
                "The Brighton Beach Incident",
                "The Monaco Emergency",
                "The Safe House Setup"
            ]),
            "history_notes": "Never questions, just shows up. Absolute loyalty when it matters.",
            "last_trust_test": "2024-02-10"
        },
        {
            "person_id": 3,  # Charlotte
            "name": "Charlotte Batchelor",
            "trust_level": 5,
            "trust_history": json.dumps([
                "The IRS Cover-up",
                "The Monaco Situation",
                "Late Night Confessions",
                "Emergency Fund Setup"
            ]),
            "history_notes": "Sister in all but blood. Keeps all secrets.",
            "last_trust_test": "2024-02-12"
        },
        {
            "person_id": 4,  # Viktor
            "name": "Viktor Petrov",
            "trust_level": 4,
            "trust_history": json.dumps([
                "Brighton Beach Poker Game",
                "Moscow Escape",
                "The Vodka Peace Offering",
                "Monthly Chess Games"
            ]),
            "history_notes": "Dangerous but reliable in his own way.",
            "last_trust_test": "2024-01-20"
        },
        {
            "person_id": 5,  # Vegas
            "name": "Johnny 'Vegas' Callahan",
            "trust_level": 5,
            "trust_history": json.dumps([
                "Southie Cover-up",
                "Wall Street Scandal Save",
                "The Burial Incident",
                "Emergency Extraction"
            ]),
            "history_notes": "No questions asked, just handles it.",
            "last_trust_test": "2024-02-07"
        },
        {
            "person_id": 6,  # Miss Pearl
            "name": "Miss Pearl",
            "trust_level": 5,
            "trust_history": json.dumps([
                "Room Reading Lessons",
                "The Dangerous Deal Save",
                "Weekly Check-ins",
                "Life Guidance"
            ]),
            "history_notes": "Only mentor who ever mattered.",
            "last_trust_test": "2024-02-04"
        },
        {
            "person_id": 7,  # Mikey
            "name": "Mikey 'Two-Times'",
            "trust_level": 2,
            "trust_history": json.dumps([
                "First Money Loan",
                "Second Money Loan",
                "Wrong Crowd Incident",
                "Failed Promises"
            ]),
            "history_notes": "Family, but can't be trusted with anything important.",
            "last_trust_test": "2024-01-15"
        }
    ]

    try:
        # Insert trust data
        c.executemany('''
            INSERT INTO trust_system 
            (person_id, name, trust_level, trust_history, history_notes, last_trust_test)
            VALUES 
            (%(person_id)s, %(name)s, %(trust_level)s, %(trust_history)s, %(history_notes)s, %(last_trust_test)s)
        ''', trust_data)

        conn.commit()
        print("Trust system data populated successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    populate_trust() 