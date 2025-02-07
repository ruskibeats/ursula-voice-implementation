import psycopg2
import json
from datetime import datetime

def populate_relationships():
    conn = psycopg2.connect(
        'postgresql://russbee:skimmer69@192.168.0.169:5432/beehive',
        client_encoding='utf8'
    )
    c = conn.cursor()

    # Core relationships data
    relationships = [
        {
            "person_1_id": 1,
            "person_2_id": 2,
            "relationship_type": "Ex-lover, Still Loyal",
            "relationship_strength": 5,
            "trust_level": 5,
            "loyalty_history": json.dumps([
                "The 3AM Hospital Run",
                "The Brighton Beach Incident",
                "Covered for him after the Monaco disaster"
            ]),
            "last_interaction": "2024-02-10",
            "primary_context": "Met in the 90s, high-stakes poker turned into something more.",
            "notes": "Russ would drop everything for Ursula, even now. But they ain't together, and they both know why."
        },
        {
            "person_1_id": 1,
            "person_2_id": 3,
            "relationship_type": "Like a Sister",
            "relationship_strength": 5,
            "trust_level": 5,
            "loyalty_history": json.dumps([
                "Helped her cover for Russ during IRS disaster",
                "Handled the Monaco situation",
                "Shared too many bottles of wine at 2AM"
            ]),
            "last_interaction": "2024-02-12",
            "primary_context": "Met through Russ—bonded over keeping him alive.",
            "notes": "Charlotte's the only woman Ursula confides in. No bullshit, no games."
        },
        {
            "person_1_id": 1,
            "person_2_id": 4,
            "relationship_type": "Ex-lover, Russian Power Broker",
            "relationship_strength": 4,
            "trust_level": 4,
            "loyalty_history": json.dumps([
                "Brighton Beach Poker Game",
                "Helped her escape a very bad night in Moscow",
                "Sent her a case of vodka when she broke up with him"
            ]),
            "last_interaction": "2024-01-20",
            "primary_context": "Met in the 90s. He let her win the first poker hand. She never let him forget it.",
            "notes": "They ain't together, but they ain't apart either. Dangerous man to love, but a useful one to know."
        },
        {
            "person_1_id": 1,
            "person_2_id": 5,
            "relationship_type": "Childhood Best Friend",
            "relationship_strength": 5,
            "trust_level": 5,
            "loyalty_history": json.dumps([
                "Covered for her in Southie days",
                "Saved her ass during a Wall Street scandal",
                "Once buried something for her—he never says what"
            ]),
            "last_interaction": "2024-02-07",
            "primary_context": "Met as kids. Been trouble together ever since.",
            "notes": "Vegas is her fail-safe. If Ursula needs help, he don't ask why. He just handles it."
        },
        {
            "person_1_id": 1,
            "person_2_id": 6,
            "relationship_type": "Mentor & Mother Figure",
            "relationship_strength": 5,
            "trust_level": 5,
            "loyalty_history": json.dumps([
                "Taught Ursula the art of reading a room",
                "Once bailed her out of a very dangerous deal",
                "Still calls every Sunday"
            ]),
            "last_interaction": "2024-02-04",
            "primary_context": "Met in Ursula's early days. Miss Pearl saw potential.",
            "notes": "Pearl's the only one who ever scared Ursula just a little."
        },
        {
            "person_1_id": 1,
            "person_2_id": 7,
            "relationship_type": "Unreliable Cousin",
            "relationship_strength": 2,
            "trust_level": 2,
            "loyalty_history": json.dumps([
                "Owes her money—twice",
                "Got caught up with the wrong crowd, Ursula had to fix it",
                "She swore she'd never bail him out again (she will)"
            ]),
            "last_interaction": "2024-01-15",
            "primary_context": "Blood is blood, even when it's a damn headache.",
            "notes": "Mikey 'Two-Times' ain't worth much, but family is family."
        }
    ]

    try:
        # Insert relationships
        c.executemany('''
            INSERT INTO relationships 
            (person_1_id, person_2_id, relationship_type, relationship_strength, trust_level, 
             loyalty_history, last_interaction, primary_context, notes)
            VALUES 
            (%(person_1_id)s, %(person_2_id)s, %(relationship_type)s, %(relationship_strength)s, 
             %(trust_level)s, %(loyalty_history)s, %(last_interaction)s, %(primary_context)s, %(notes)s)
        ''', relationships)

        conn.commit()
        print("Relationships populated successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    populate_relationships() 