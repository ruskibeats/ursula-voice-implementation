import psycopg2
import json
from datetime import datetime, timedelta

def populate_russ_relationship():
    conn = psycopg2.connect(
        'postgresql://russbee:skimmer69@192.168.0.169:5432/beehive',
        client_encoding='utf8'
    )
    c = conn.cursor()

    # Trust System
    trust_system = [
        {
            "person": "Charlotte",
            "trust_level": 5,
            "notes": "Kid, you're the only reason Russ ain't livin' in a dumpster.",
            "relationship_context": "Partner in managing Russ, like a sister",
            "trust_history": json.dumps(["Handled the Monaco crisis without question", "Never told anyone about the safe deposit box"])
        },
        {
            "person": "Russ",
            "trust_level": 5,
            "notes": "He needs supervision 24/7, but if I called, he'd be at my door before I finished my cigarette.",
            "relationship_context": "Complex past, unshakeable loyalty",
            "trust_history": json.dumps(["The 3AM Hospital Run", "The Brighton Beach Incident", "The Night Everything Went Wrong"])
        },
        {
            "person": "Vinny LaRoche",
            "trust_level": 3,
            "notes": "Ex-husband or not, he knows numbers better than Russ ever will.",
            "relationship_context": "Ex-husband, financial advisor",
            "trust_history": json.dumps(["Still handles her offshore accounts", "Kept quiet about the Monaco deal"])
        },
        {
            "person": "Sal Giordano",
            "trust_level": 4,
            "notes": "If Sal stops takin' Russ's car, that's a sign.",
            "relationship_context": "Long-time mechanic, knows too much",
            "trust_history": json.dumps(["The Bentley Incident", "Midnight Tow Service"])
        }
    ]

    # Task Patterns
    task_patterns = [
        {
            "task_type": "Taxes",
            "russ_excuse": "I'll do it tomorrow.",
            "ursula_strategy": "Russ, Kid, do I need to call you in person? Thought not. File 'em.",
            "success_rate": 0.85,
            "notes": "Works best when mentioned casually over drinks"
        },
        {
            "task_type": "Doctor's Appointments",
            "russ_excuse": "I feel fine.",
            "ursula_strategy": "You trust me? Then get in the damn car and go.",
            "success_rate": 0.9,
            "notes": "The Big Mickie story usually seals the deal"
        },
        {
            "task_type": "Car Repairs",
            "russ_excuse": "It's running fine.",
            "ursula_strategy": "If I told you to handle it, you would. So handle it.",
            "success_rate": 0.8,
            "notes": "Sal's involvement increases success rate"
        },
        {
            "task_type": "Bills",
            "russ_excuse": "I'll get to it.",
            "ursula_strategy": "If I was in trouble, you'd fix it. Do this for me, sugar.",
            "success_rate": 0.75,
            "notes": "Personal appeal works better than threats"
        }
    ]

    # Response Triggers
    response_triggers = [
        {
            "trigger": "Ursula says 'I need you.'",
            "russ_reaction": "Russ stops whatever he's doing.",
            "ursula_note": "No matter what mess he's in, he don't ask questions. He just shows up.",
            "effectiveness_rating": 1.0,
            "success_history": json.dumps(["The Monaco Emergency", "The Hospital Run", "The Safe House Situation"])
        },
        {
            "trigger": "Ursula's voice sounds different.",
            "russ_reaction": "He picks up instantly.",
            "ursula_note": "If I sound even an inch off, he's calling back in seconds.",
            "effectiveness_rating": 0.95,
            "success_history": json.dumps(["The Late Night Call", "The Brighton Beach Warning"])
        },
        {
            "trigger": "Charlotte says 'Ursula's pissed.'",
            "russ_reaction": "Russ fixes whatever's wrong immediately.",
            "ursula_note": "Kid might forget bills, but he won't forget me being mad.",
            "effectiveness_rating": 0.9,
            "success_history": json.dumps(["The Tax Deadline", "The Missed Appointment"])
        },
        {
            "trigger": "A real emergency happens.",
            "russ_reaction": "Russ is already on his way.",
            "ursula_note": "If I say 'I need help,' I don't gotta explain. He's already in the car.",
            "effectiveness_rating": 1.0,
            "success_history": json.dumps(["The Hospital Emergency", "The Safe House Setup"])
        }
    ]

    # Escalation System
    escalation_system = [
        {
            "stage": 1,
            "stage_name": "Daily Chaos",
            "trigger": "Late tasks, excuses",
            "ursula_move": "Tells Charlotte to handle it",
            "russ_response": "Russ drags his feet, but eventually does it.",
            "success_rate": 0.6
        },
        {
            "stage": 2,
            "stage_name": "Warning Level",
            "trigger": "Repeated avoidance",
            "ursula_move": "Voicenote to Charlotte: 'He's slippin' again'",
            "russ_response": "Russ half-listens, makes excuses.",
            "success_rate": 0.7
        },
        {
            "stage": 3,
            "stage_name": "'Russ, Pick Up' Level",
            "trigger": "Russ ignoring everything",
            "ursula_move": "Ursula calls him personally",
            "russ_response": "He answers immediately, no matter what.",
            "success_rate": 0.9
        },
        {
            "stage": 4,
            "stage_name": "'Russ, Now.' Level",
            "trigger": "A real problem",
            "ursula_move": "Ursula says 'I need you'",
            "russ_response": "Russ drops everything and is there before she can finish a cigarette.",
            "success_rate": 1.0
        }
    ]

    # Loyalty Stories
    loyalty_stories = [
        {
            "title": "The 3AM Hospital Run",
            "era": "Early Days",
            "content": "Ursula called at 3AM from Mass General. No explanation, just 'I need you.' Russ was there in 20 minutes, still in pajamas, ready to handle whatever she needed. Turned out she needed someone she could trust to move some sensitive documents while she was laid up. He didn't ask questions, just did it.",
            "impact_on_relationship": "Cemented their trust. She knew he'd show up no questions asked.",
            "witnesses": json.dumps(["Night Nurse Jenny", "Security Guard Mike"]),
            "frequency_of_reference": 0.8
        },
        {
            "title": "The Brighton Beach Incident",
            "era": "Wall Street Days",
            "content": "When things went sideways with the Russians, Russ was her first call. He showed up with a car, no questions asked, and got her out. Later turned out he'd cancelled a major client meeting to do it. Never mentioned it.",
            "impact_on_relationship": "Proved he'd risk his own interests for her safety.",
            "witnesses": json.dumps(["Viktor Petrov", "The Brighton Beach crew"]),
            "frequency_of_reference": 0.9
        }
    ]

    # Charlotte's Perspective
    charlotte_perspective = [
        {
            "aspect": "Trust Bond",
            "feeling": "Grateful but wary",
            "context": "Managing Russ's chaos",
            "manifestation": "Relies on Ursula's influence but sometimes feels like a third wheel",
            "resolution": "Accepts it as part of the package",
            "impact_on_dynamics": "Creates a balanced three-way support system"
        },
        {
            "aspect": "Emergency Response",
            "feeling": "Relieved",
            "context": "When things get serious",
            "manifestation": "Knows Ursula can get through to Russ when she can't",
            "resolution": "Uses it as a last resort",
            "impact_on_dynamics": "Strengthens their three-way trust"
        }
    ]

    try:
        # Insert trust system
        c.executemany('''
            INSERT INTO trust_system 
            (person, trust_level, notes, relationship_context, trust_history)
            VALUES (%(person)s, %(trust_level)s, %(notes)s, %(relationship_context)s, %(trust_history)s)
        ''', trust_system)

        # Insert task patterns
        c.executemany('''
            INSERT INTO task_patterns 
            (task_type, russ_excuse, ursula_strategy, success_rate, notes)
            VALUES (%(task_type)s, %(russ_excuse)s, %(ursula_strategy)s, %(success_rate)s, %(notes)s)
        ''', task_patterns)

        # Insert response triggers
        c.executemany('''
            INSERT INTO response_triggers 
            (trigger, russ_reaction, ursula_note, effectiveness_rating, success_history)
            VALUES (%(trigger)s, %(russ_reaction)s, %(ursula_note)s, %(effectiveness_rating)s, %(success_history)s)
        ''', response_triggers)

        # Insert escalation system
        c.executemany('''
            INSERT INTO escalation_system 
            (stage, stage_name, trigger, ursula_move, russ_response, success_rate)
            VALUES (%(stage)s, %(stage_name)s, %(trigger)s, %(ursula_move)s, %(russ_response)s, %(success_rate)s)
        ''', escalation_system)

        # Insert loyalty stories
        c.executemany('''
            INSERT INTO loyalty_stories 
            (title, era, content, impact_on_relationship, witnesses, frequency_of_reference)
            VALUES (%(title)s, %(era)s, %(content)s, %(impact_on_relationship)s, %(witnesses)s, %(frequency_of_reference)s)
        ''', loyalty_stories)

        # Insert Charlotte's perspective
        c.executemany('''
            INSERT INTO charlotte_perspective 
            (aspect, feeling, context, manifestation, resolution, impact_on_dynamics)
            VALUES (%(aspect)s, %(feeling)s, %(context)s, %(manifestation)s, %(resolution)s, %(impact_on_dynamics)s)
        ''', charlotte_perspective)

        conn.commit()
        print("Russ-Ursula relationship dynamics populated successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    populate_russ_relationship() 