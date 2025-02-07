from fastapi import FastAPI, HTTPException, Query, Path, Body, Depends
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Literal
from datetime import datetime, timedelta
import databases
import json

# Database setup
DATABASE_URL = "postgresql://russbee:skimmer69@192.168.0.169:5432/beehive"
database = databases.Database(DATABASE_URL)

app = FastAPI(title="Ursula's Universe API")

# Basic Models
class Task(BaseModel):
    title: str
    description: Optional[str]
    status: str
    priority: str

class TaskPriority(BaseModel):
    task_id: int
    priority_score: int
    escalation_level: str

# Models
class FamilyMember(BaseModel):
    id: int
    name: str
    relationship_to_russ: str
    role: str
    status: str
    traits: List[str]
    active_in_task_system: bool

class EscalationTrigger(BaseModel):
    id: int
    trigger_event: str
    task_name: str
    threshold: int
    escalation_action: str
    last_triggered: str

class TaskRollCall(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    due_date: str
    assigned_to: str

class TaskAnalytics(BaseModel):
    task_id: int
    title: str
    times_ignored: int
    completion_rate: int
    pattern_analysis: str

class DailyRollCall(BaseModel):
    task_id: int
    title: str
    priority: str
    notes: str

class TrustSystem(BaseModel):
    person_id: int
    name: str
    trust_level: int
    history_notes: str

class TaskPattern(BaseModel):
    pattern_name: str
    frequency: int
    last_observed: str
    notes: str

# Startup and shutdown
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Basic Task Endpoints
@app.get("/tasks")
async def get_tasks():
    query = "SELECT * FROM tasks"
    return await database.fetch_all(query)

@app.get("/tasks/priority")
async def get_task_priorities():
    query = "SELECT * FROM task_prioritization"
    return await database.fetch_all(query)

@app.get("/tasks/priority/critical")
async def get_critical_tasks():
    query = """
    SELECT * FROM task_prioritization 
    WHERE escalation_level = 'CRITICAL'
    """
    return await database.fetch_all(query)

@app.get("/tasks/priority/by-level/{level}")
async def get_tasks_by_priority(level: str):
    query = """
    SELECT * FROM task_prioritization 
    WHERE escalation_level = :level
    """
    return await database.fetch_all(query, {"level": level})

# Recurring Tasks
@app.get("/tasks/recurring")
async def get_recurring_tasks():
    query = "SELECT * FROM recurring_tasks"
    return await database.fetch_all(query)

@app.get("/tasks/recurring/overdue")
async def get_overdue_tasks():
    query = """
    SELECT * FROM recurring_tasks 
    WHERE next_due < CURRENT_TIMESTAMP
    """
    return await database.fetch_all(query)

@app.get("/tasks/recurring/next-24h")
async def get_upcoming_tasks():
    query = """
    SELECT * FROM recurring_tasks 
    WHERE next_due < CURRENT_TIMESTAMP + interval '24 hours'
    """
    return await database.fetch_all(query)

# Russ-specific endpoints
@app.get("/russ/tasks/avoided")
async def get_avoided_tasks():
    query = """
    SELECT * FROM task_history 
    WHERE times_avoided > 0
    """
    return await database.fetch_all(query)

@app.get("/russ/patterns/adhd")
async def get_adhd_patterns():
    query = "SELECT * FROM adhd_patterns"
    return await database.fetch_all(query)

# Family and Circle
@app.get("/family", response_model=List[FamilyMember])
async def get_family():
    query = """
    SELECT id, name, relationship_to_russ, role, status, traits, active_in_task_system 
    FROM family_members;
    """
    family_members = await database.fetch_all(query)
    return family_members

@app.get("/inner-circle")
async def get_inner_circle():
    query = "SELECT * FROM inner_circle"
    return await database.fetch_all(query)

# Communication
@app.get("/communication/breakdowns")
async def get_breakdowns():
    query = "SELECT * FROM communication_breakdowns"
    return await database.fetch_all(query)

# Task History
@app.get("/tasks/history/{task_id}")
async def get_task_history(task_id: int):
    query = "SELECT * FROM task_history WHERE task_id = :task_id"
    return await database.fetch_all(query, {"task_id": task_id})

@app.get("/tasks/performance")
async def get_performance():
    query = "SELECT * FROM task_history"
    return await database.fetch_all(query)

# External Triggers
@app.get("/triggers/external")
async def get_triggers():
    query = "SELECT * FROM external_triggers"
    return await database.fetch_all(query)

# Task Delegation
@app.get("/tasks/delegation")
async def get_delegations():
    query = "SELECT * FROM task_delegation"
    return await database.fetch_all(query)

# Dashboard
@app.get("/dashboard/summary")
async def get_summary():
    query = """
    SELECT 
        (SELECT COUNT(*) FROM tasks) as total_tasks,
        (SELECT COUNT(*) FROM tasks WHERE status = 'PENDING') as pending_tasks,
        (SELECT COUNT(*) FROM recurring_tasks WHERE next_due < CURRENT_TIMESTAMP) as overdue_tasks
    """
    return await database.fetch_one(query)

# POST Endpoints
@app.post("/tasks/priority/update")
async def update_priority(priority: TaskPriority):
    query = """
    INSERT INTO task_prioritization (task_id, priority_score, escalation_level)
    VALUES (:task_id, :priority_score, :escalation_level)
    ON CONFLICT (task_id) DO UPDATE 
    SET priority_score = EXCLUDED.priority_score,
        escalation_level = EXCLUDED.escalation_level
    RETURNING *
    """
    return await database.fetch_one(query, priority.dict())

@app.post("/tasks/recurring/create")
async def create_recurring(task: dict):
    query = """
    INSERT INTO recurring_tasks (description, frequency, next_due)
    VALUES (:description, :frequency, :next_due)
    RETURNING *
    """
    return await database.fetch_one(query, task)

@app.post("/communication/breakdown/report")
async def report_breakdown(breakdown: dict):
    query = """
    INSERT INTO communication_breakdowns (task_id, description)
    VALUES (:task_id, :description)
    RETURNING *
    """
    return await database.fetch_one(query, breakdown)

@app.post("/tasks/delegate")
async def delegate_task(delegation: dict):
    query = """
    INSERT INTO task_delegation (task_id, delegated_to)
    VALUES (:task_id, :delegated_to)
    RETURNING *
    """
    return await database.fetch_one(query, delegation)

# Endpoint for Escalation Triggers
@app.get("/escalation-triggers", response_model=List[EscalationTrigger])
async def get_escalation_triggers():
    query = """
    SELECT e.id, e.trigger_event, t.title AS task_name, e.threshold, e.escalation_action, e.last_triggered
    FROM escalation_triggers e
    JOIN tasks t ON e.task_id = t.id
    WHERE e.last_triggered >= NOW() - INTERVAL '30 days';
    """
    triggers = await database.fetch_all(query)
    return triggers

# Endpoint for Task Roll Call
@app.get("/task-roll-call/today", response_model=List[TaskRollCall])
async def get_task_roll_call():
    query = """
    SELECT tr.id, t.title, t.description, t.priority, t.status, t.due_date, fm.name AS assigned_to
    FROM task_roll_call tr
    JOIN tasks t ON tr.task_id = t.id
    JOIN family_members fm ON tr.assigned_to = fm.id
    WHERE t.due_date = CURRENT_DATE
    ORDER BY t.priority DESC;
    """
    tasks = await database.fetch_all(query)
    return tasks

# Endpoint for Task Analytics
@app.get("/task-analytics", response_model=List[TaskAnalytics])
async def get_task_analytics():
    query = """
    SELECT ta.task_id, t.title, ta.times_ignored, ta.completion_rate, ta.pattern_analysis
    FROM task_analytics ta
    JOIN tasks t ON ta.task_id = t.id
    ORDER BY ta.completion_rate ASC;
    """
    analytics = await database.fetch_all(query)
    return analytics

# Endpoint for Daily Roll Call
@app.get("/daily-roll-call", response_model=List[DailyRollCall])
async def get_daily_roll_call():
    query = """
    SELECT dr.task_id, t.title, t.priority, dr.notes
    FROM daily_roll_call dr
    JOIN tasks t ON dr.task_id = t.id
    WHERE dr.date = CURRENT_DATE;
    """
    roll_call = await database.fetch_all(query)
    return roll_call

# Endpoint for Trust System
@app.get("/trust-system", response_model=List[TrustSystem])
async def get_trust_system():
    query = """
    SELECT ts.person_id, fm.name, ts.trust_level, ts.history_notes
    FROM trust_system ts
    JOIN family_members fm ON ts.person_id = fm.id
    ORDER BY ts.trust_level DESC;
    """
    trust_data = await database.fetch_all(query)
    return trust_data

# Endpoint for Task Patterns
@app.get("/task-patterns", response_model=List[TaskPattern])
async def get_task_patterns():
    query = """
    SELECT tp.pattern_name, tp.frequency, tp.last_observed, tp.notes
    FROM task_patterns tp
    ORDER BY tp.frequency DESC;
    """
    patterns = await database.fetch_all(query)
    return patterns

# Models for Family Members
class FamilyMember(BaseModel):
    id: int
    name: str
    relationship: str
    role: str
    traits: List[str]
    status: str
    notes: str

# Family Structure
class UrsulaFamily(BaseModel):
    batchelor_family: List[FamilyMember]
    ursula_blood_family: List[FamilyMember]
    close_as_family: List[FamilyMember]

# Sample Data
ursula_family_data = {
    "family": {
        "batchelor_family": [
            {
                "id": 1,
                "name": "Russ Batchelor",
                "relationship": "Ex-Lover, Chaos Generator",
                "role": "ADHD Disaster, Needs Full Management",
                "traits": ["Loyal", "Forgetful", "Spontaneous", "Talks Too Much"],
                "status": "Active",
                "notes": "Russ would walk through fire for Ursula, but he also forgets to file his taxes."
            },
            {
                "id": 2,
                "name": "Charlotte Batchelor",
                "relationship": "Russ's Wife",
                "role": "Co-Manager of Russ's Life, Ursula's Sister in All But Blood",
                "traits": ["Patient", "Sharp-Tongued", "Exhausted"],
                "status": "Active",
                "notes": "The only person besides Ursula who can keep Russ from completely self-destructing."
            },
            {
                "id": 3,
                "name": "Mimi Batchelor",
                "relationship": "Russ & Charlotte's Daughter (16)",
                "role": "Teenager, Sarcastic Eye-Roller",
                "traits": ["Smart", "Sassy", "Social Media Addict"],
                "status": "Active",
                "notes": "Thinks Russ is a total mess, thinks Ursula is 'kinda badass.'"
            },
            {
                "id": 4,
                "name": "Tom Batchelor",
                "relationship": "Russ & Charlotte's Son (19)",
                "role": "College Student, Generally Useless",
                "traits": ["Lazy", "Charming", "Mostly Unhelpful"],
                "status": "Active",
                "notes": "Russ babies him too much. Ursula keeps him in check."
            },
            {
                "id": 5,
                "name": "Ted, Bella, Riva",
                "relationship": "Russ's Dogs",
                "role": "Chaos on Four Legs",
                "traits": ["Loud", "Messy", "Overly Attached to Russ"],
                "status": "Active",
                "notes": "The reason Russ never leaves the house on time."
            }
        ],
        "ursula_blood_family": [
            {
                "id": 6,
                "name": "Danny O'Sullivan",
                "relationship": "Father",
                "role": "Dockworker, Southie Legend",
                "traits": ["Hardworking", "Tough as Nails", "Drank Too Much"],
                "status": "Deceased (Lung Cancer, 1995)",
                "notes": "Taught Ursula how to fight, gamble, and never back down."
            },
            {
                "id": 7,
                "name": "Linda 'Linnie' Moretti O'Sullivan",
                "relationship": "Mother",
                "role": "Gangster's Daughter, Disappeared in 1986",
                "traits": ["Mysterious", "Cunning", "Vanished Without a Trace"],
                "status": "Missing",
                "notes": "Ursula still hires private investigators to find out what happened to her."
            },
            {
                "id": 8,
                "name": "Richie O'Sullivan",
                "relationship": "Younger Brother",
                "role": "The One She Couldn't Save",
                "traits": ["Funny", "Hot-Tempered", "Loved Too Hard"],
                "status": "Deceased (Overdose, 1999)",
                "notes": "Died from heroin sold by a mobster's kid. Ursula still carries his poker chip."
            }
        ],
        "close_as_family": [
            {
                "id": 9,
                "name": "Johnny 'Vegas' Callahan",
                "relationship": "Childhood Best Friend",
                "role": "Bar Owner, Former Street Hustler",
                "traits": ["Loyal", "Smooth Talker", "Has Connections Everywhere"],
                "status": "Active",
                "notes": "Runs a bar in Southie, knows every cop, bookie, and bouncer in the city."
            },
            {
                "id": 10,
                "name": "Cha Cha Moretti",
                "relationship": "Tattoo Artist & Confidante",
                "role": "Ex-CIA Wet Worker, Now Runs a Tattoo Shop",
                "traits": ["Deadly", "Mysterious", "Speaks Five Languages"],
                "status": "Active",
                "notes": "Only person Ursula lets near her with a needle."
            },
            {
                "id": 11,
                "name": "Miss Pearl",
                "relationship": "Mentor & Mother Figure",
                "role": "Former Madam, Knows Everybody's Secrets",
                "traits": ["Elegant", "Savvy", "Cutthroat"],
                "status": "Active",
                "notes": "Calls Ursula 'Kid.' Still gives the best advice."
            }
        ]
    }
}

# Endpoint for Family
@app.get("/family", response_model=Dict[str, UrsulaFamily])
async def get_family():
    return ursula_family_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
