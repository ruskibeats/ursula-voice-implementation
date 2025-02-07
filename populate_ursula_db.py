import psycopg2
import json
from datetime import datetime, timedelta

# Connect to database
conn = psycopg2.connect('postgresql://russbee:skimmer69@192.168.0.169:5432/beehive')
c = conn.cursor()

# Sample family data
family_data = [
    {
        "name": "Danny O'Sullivan",
        "relation": "father",
        "status": "deceased",
        "details": "A tough, chain-smoking dockworker who raised Ursula with fists and street wisdom. Taught her how to spot a liar, fix a busted radiator, and throw a proper punch.",
        "impact": "Shaped her blend of street smarts and tough love. His early death from lung cancer drives her protective nature.",
        "last_referenced": datetime.now().isoformat()
    },
    {
        "name": "Margaret O'Sullivan",
        "relation": "mother",
        "status": "missing",
        "details": "A master of social manipulation who could talk her way into or out of anything. Disappeared under mysterious circumstances.",
        "impact": "Her unsolved disappearance remains Ursula's deepest vulnerability. Still pays private investigators.",
        "last_referenced": datetime.now().isoformat()
    },
    {
        "name": "Tommy O'Sullivan",
        "relation": "brother",
        "status": "deceased",
        "details": "Younger brother, lost too young. The neighborhood golden boy everyone thought would make it big.",
        "impact": "His loss drives her to protect others, especially children. Can't handle seeing kids in trouble.",
        "last_referenced": datetime.now().isoformat()
    }
]

# Sample characters data
characters_data = [
    {
        "name": "Big Mickie",
        "role": "Former Wall Street colleague",
        "key_traits": "Risk-taker, loyal friend, terrible with health",
        "relevance_to_ursula": "Her first big save - medical emergency on trading floor",
        "last_interaction": datetime.now().isoformat(),
        "trust_level": 0.9
    },
    {
        "name": "Dr. Thompson",
        "role": "Trusted medical contact",
        "key_traits": "Discreet, competent, understands urgency",
        "relevance_to_ursula": "Helps manage Russ's care without questions",
        "last_interaction": datetime.now().isoformat(),
        "trust_level": 0.95
    }
]

# Sample locations data
locations_data = [
    {
        "name": "Mass General",
        "significance": "Where she manages most of Russ's care. Scene of many victories and close calls.",
        "key_contacts": json.dumps(["Dr. Thompson", "Nurse Jackie", "Big Mickie"]),
        "insider_tips": "Slip the night nurse a $50, they'll 'forget' to ask about insurance."
    },
    {
        "name": "Thinking Cup Coffee",
        "significance": "Her unofficial office. Corner table with the best view of the door.",
        "key_contacts": json.dumps(["Morning Crew", "Regular Patrons"]),
        "insider_tips": "Order the black coffee, nothing fancy. Tips in crisp hundreds."
    }
]

# Sample personal rules data
rules_data = [
    {
        "rule": "Never bet what you can't lose twice",
        "origin_story": "Learned from poker—applies to money, power, and trust",
        "importance_rating": 10
    },
    {
        "rule": "Keep one secret from everyone",
        "origin_story": "Even the people closest to you don't get everything",
        "importance_rating": 9
    }
]

# Sample relationships data
relationships_data = [
    {
        "name": "Viktor Petrov",
        "status": "Complicated",
        "complications": "Russian connections, unfinished business",
        "threat_level": 3
    },
    {
        "name": "Frankie DeLuca",
        "status": "Active",
        "complications": "Knows too many secrets",
        "threat_level": 1
    }
]

# Sample task roll call data
task_roll_call_data = [
    {
        "id": "TASK101",
        "description": "Fix the Car",
        "category": "Vehicle",
        "due_date": datetime.now().isoformat(),
        "last_mentioned": (datetime.now() - timedelta(days=5)).isoformat(),
        "urgency": "RED",
        "suggested_actions": "Call Sal, schedule pickup",
        "ai_observations": "Russ avoided twice, pattern detected",
        "days_overdue": 5,
        "agent_assigned": "Logistics_AI",
        "status": "pending",
        "pattern_score": 0.8,
        "avoidance_history": json.dumps(["Ignored first call", "Claimed too busy"]),
        "impact_rating": 8,
        "external_pressure_score": 0.7
    },
    {
        "id": "TASK102",
        "description": "Pay IRS Bill",
        "category": "Finance",
        "due_date": (datetime.now() + timedelta(days=10)).isoformat(),
        "last_mentioned": (datetime.now() - timedelta(days=9)).isoformat(),
        "urgency": "ORANGE",
        "suggested_actions": "Call Marcus AI for update",
        "ai_observations": "Russ ignored first warning",
        "days_overdue": 10,
        "agent_assigned": "Marcus_AI",
        "status": "overdue",
        "pattern_score": 0.9,
        "avoidance_history": json.dumps(["Missed first deadline", "Claims check in mail"]),
        "impact_rating": 9,
        "external_pressure_score": 0.9
    }
]

# Sample data ingest queue
ingest_queue_data = [
    {
        "source_type": "email",
        "content": json.dumps({"subject": "IRS Final Notice", "body": "Payment overdue"}),
        "metadata": json.dumps({"sender": "irs.gov", "priority": "high"}),
        "priority": "RED",
        "processing_agent": "Marcus_AI",
        "processing_status": "pending"
    },
    {
        "source_type": "vehicle",
        "content": json.dumps({"type": "check_engine", "status": "warning"}),
        "metadata": json.dumps({"vehicle": "BMW", "mileage": 50000}),
        "priority": "ORANGE",
        "processing_agent": "Logistics_AI",
        "processing_status": "pending"
    }
]

# Sample daily roll call
daily_roll_call_data = [
    {
        "report_date": datetime.now().date().isoformat(),
        "urgent_tasks": json.dumps(["TASK101", "TASK102"]),
        "high_priority": json.dumps(["TASK103"]),
        "low_priority": json.dumps(["TASK104", "TASK105"]),
        "ursula_notes": "Charlotte, sugar, these need handling TODAY.",
        "completion_rate": 0.7
    }
]

# Insert data
c.executemany('INSERT INTO family (name, relation, status, details, impact, last_referenced) VALUES (:name, :relation, :status, :details, :impact, :last_referenced)', family_data)
c.executemany('INSERT INTO characters (name, role, key_traits, relevance_to_ursula, last_interaction, trust_level) VALUES (:name, :role, :key_traits, :relevance_to_ursula, :last_interaction, :trust_level)', characters_data)
c.executemany('INSERT INTO locations (name, significance, key_contacts, insider_tips) VALUES (:name, :significance, :key_contacts, :insider_tips)', locations_data)
c.executemany('INSERT INTO personal_rules (rule, origin_story, importance_rating) VALUES (:rule, :origin_story, :importance_rating)', rules_data)
c.executemany('INSERT INTO relationships (name, status, complications, threat_level) VALUES (:name, :status, :complications, :threat_level)', relationships_data)

# Insert task tracking data
c.executemany('''INSERT INTO task_roll_call 
    (id, description, category, due_date, last_mentioned, urgency, suggested_actions, 
    ai_observations, days_overdue, agent_assigned, status, pattern_score, avoidance_history,
    impact_rating, external_pressure_score) 
    VALUES 
    (:id, :description, :category, :due_date, :last_mentioned, :urgency, :suggested_actions,
    :ai_observations, :days_overdue, :agent_assigned, :status, :pattern_score, :avoidance_history,
    :impact_rating, :external_pressure_score)''', task_roll_call_data)

# Insert ingest queue data
c.executemany('''INSERT INTO data_ingest_queue 
    (source_type, content, metadata, priority, processing_agent, processing_status)
    VALUES 
    (:source_type, :content, :metadata, :priority, :processing_agent, :processing_status)''',
    ingest_queue_data)

# Insert daily roll call data
c.executemany('''INSERT INTO daily_roll_call 
    (report_date, urgent_tasks, high_priority, low_priority, ursula_notes, completion_rate)
    VALUES 
    (:report_date, :urgent_tasks, :high_priority, :low_priority, :ursula_notes, :completion_rate)''',
    daily_roll_call_data)

# Commit and close
conn.commit()
conn.close()

print("Database populated with sample data") 
