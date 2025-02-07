import psycopg2
import json
from datetime import datetime

def populate_expanded():
    conn = psycopg2.connect(
        'postgresql://russbee:skimmer69@192.168.0.169:5432/beehive',
        client_encoding='utf8'
    )
    c = conn.cursor()

    # Daily Routines
    daily_routines = [
        {
            "routine_type": "morning_ritual",
            "time_of_day": "5:30 AM",
            "activities": json.dumps(["Black coffee at Thinking Cup", "Wall Street Journal review", "Calls to Europe"]),
            "frequency": "daily",
            "location": "Boston",
            "quirks": json.dumps(["Always sits at the same corner table", "Tips in crisp hundreds", "Knows baristas' life stories"])
        },
        {
            "routine_type": "power_moves",
            "time_of_day": "various",
            "activities": json.dumps(["Sunday dinner in North End", "Friday night poker", "Wednesday spa day"]),
            "frequency": "weekly",
            "location": "Boston",
            "quirks": json.dumps(["Networking at Oak Room", "Drinks at Tatiana", "Late nights at Keens"])
        }
    ]

    # Personal Rules
    personal_rules = [
        {
            "rule": "Never bet what you can't lose twice",
            "context": "Gambling and business",
            "importance_rating": 10,
            "origin_story": "Lost big once in Monte Carlo, never again",
            "examples": json.dumps(["Walks away from risky deals", "Keeps emergency funds in three countries"])
        },
        {
            "rule": "Keep one secret from everyone",
            "context": "Personal relationships",
            "importance_rating": 9,
            "origin_story": "Learned from her mother's disappearance",
            "examples": json.dumps(["Has a safety deposit box no one knows about", "Maintains separate emergency identities"])
        }
    ]

    # Secret Skills
    secret_skills = [
        {
            "skill": "Speaks fluent Cantonese",
            "origin_story": "Learned from kitchen staff in Chinatown",
            "proficiency_level": "expert",
            "last_used": "weekly",
            "related_stories": json.dumps(["The Chinatown Poker Ring", "The Dim Sum Dynasty Deal"])
        },
        {
            "skill": "Expert lockpick",
            "origin_story": "Never lost the touch from Southie days",
            "proficiency_level": "expert",
            "last_used": "monthly",
            "related_stories": json.dumps(["The Safe Deposit Heist", "The Night We Lost a Bentley"])
        }
    ]

    # Vulnerabilities
    vulnerabilities = [
        {
            "trigger": "Mentions of her mother's disappearance",
            "reaction": "Goes quiet, orders double scotch",
            "background": "Never solved, still pays private investigators",
            "coping_mechanism": "Throws herself into work",
            "related_characters": json.dumps(["Danny O'Sullivan", "Private Detective Mike Flanagan"])
        },
        {
            "trigger": "Children in trouble",
            "reaction": "Drops everything to help",
            "background": "Lost a younger brother young, never got over it",
            "coping_mechanism": "Donates anonymously to children's charities",
            "related_characters": json.dumps(["Tommy O'Sullivan (deceased brother)", "Local youth center kids"])
        }
    ]

    # Regular Haunts
    regular_haunts = [
        {
            "name": "Thinking Cup Coffee",
            "city": "Boston",
            "time_of_day": "morning",
            "purpose": "Daily planning and intelligence gathering",
            "insider_knowledge": "The corner table has the best view and worst coffee stains",
            "regular_companions": json.dumps(["Morning regulars", "Financial district early birds"])
        },
        {
            "name": "Tatiana",
            "city": "Brighton Beach",
            "time_of_day": "evening",
            "purpose": "Russian connections and poker",
            "insider_knowledge": "Order vodka neat if you want to be taken seriously",
            "regular_companions": json.dumps(["Yuri Mikhailov", "Viktor Petrov"])
        }
    ]

    # Regional Traits
    regional_traits = [
        {
            "city": "Boston",
            "trait": "Coffee: black, strong, no sugar",
            "context": "Morning ritual",
            "manifestation": "Refuses to acknowledge 'fancy' coffee exists",
            "frequency": "daily"
        },
        {
            "city": "New York",
            "trait": "Speaks fluent Russian",
            "context": "Brighton Beach years",
            "manifestation": "Switches languages mid-conversation to make a point",
            "frequency": "weekly"
        }
    ]

    # Future Dreams
    future_dreams = [
        {
            "dream": "Opening a high-stakes poker room",
            "type": "admitted",
            "motivation": "Combining all her worlds in one place",
            "progress_status": "planning",
            "blockers": "Licensing and Russian mob complications"
        },
        {
            "dream": "Finding her mother",
            "type": "secret",
            "motivation": "Closure and answers",
            "progress_status": "ongoing",
            "blockers": "Cold trail and dangerous implications"
        }
    ]

    # Guilty Pleasures
    guilty_pleasures = [
        {
            "pleasure": "Trashy reality TV watched in secret",
            "frequency": "weekly",
            "context": "Late nights alone",
            "who_knows": json.dumps(["Frankie DeLuca"]),
            "notes": "Has strong opinions about Real Housewives"
        },
        {
            "pleasure": "McDonald's fries at 3 AM",
            "frequency": "monthly",
            "context": "After big wins or tough losses",
            "who_knows": json.dumps(["Late night drive-through staff"]),
            "notes": "Always pays in cash, never during daylight"
        }
    ]

    try:
        # Insert daily routines
        c.executemany('''
            INSERT INTO daily_routines 
            (routine_type, time_of_day, activities, frequency, location, quirks)
            VALUES (%(routine_type)s, %(time_of_day)s, %(activities)s, %(frequency)s, %(location)s, %(quirks)s)
        ''', daily_routines)

        # Insert personal rules
        c.executemany('''
            INSERT INTO personal_rules 
            (rule, context, importance_rating, origin_story, examples)
            VALUES (%(rule)s, %(context)s, %(importance_rating)s, %(origin_story)s, %(examples)s)
        ''', personal_rules)

        # Insert secret skills
        c.executemany('''
            INSERT INTO secret_skills 
            (skill, origin_story, proficiency_level, last_used, related_stories)
            VALUES (%(skill)s, %(origin_story)s, %(proficiency_level)s, %(last_used)s, %(related_stories)s)
        ''', secret_skills)

        # Insert vulnerabilities
        c.executemany('''
            INSERT INTO vulnerabilities 
            (trigger, reaction, background, coping_mechanism, related_characters)
            VALUES (%(trigger)s, %(reaction)s, %(background)s, %(coping_mechanism)s, %(related_characters)s)
        ''', vulnerabilities)

        # Insert regular haunts
        c.executemany('''
            INSERT INTO regular_haunts 
            (name, city, time_of_day, purpose, insider_knowledge, regular_companions)
            VALUES (%(name)s, %(city)s, %(time_of_day)s, %(purpose)s, %(insider_knowledge)s, %(regular_companions)s)
        ''', regular_haunts)

        # Insert regional traits
        c.executemany('''
            INSERT INTO regional_traits 
            (city, trait, context, manifestation, frequency)
            VALUES (%(city)s, %(trait)s, %(context)s, %(manifestation)s, %(frequency)s)
        ''', regional_traits)

        # Insert future dreams
        c.executemany('''
            INSERT INTO future_dreams 
            (dream, type, motivation, progress_status, blockers)
            VALUES (%(dream)s, %(type)s, %(motivation)s, %(progress_status)s, %(blockers)s)
        ''', future_dreams)

        # Insert guilty pleasures
        c.executemany('''
            INSERT INTO guilty_pleasures 
            (pleasure, frequency, context, who_knows, notes)
            VALUES (%(pleasure)s, %(frequency)s, %(context)s, %(who_knows)s, %(notes)s)
        ''', guilty_pleasures)

        conn.commit()
        print("Expanded character details populated successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    populate_expanded() 