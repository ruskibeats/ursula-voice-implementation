from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
import databases
import sqlalchemy
from datetime import datetime, timezone
import sqlite3
import os
from fastapi import Path
import json
import httpx

# Constants
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN", "e0617c43571f8e13254c5b49c1e561715380461d")
TODOIST_API_BASE = "https://api.todoist.com/rest/v2"
DATABASE_URL = "sqlite:///./ursula.db"

# FastAPI app
app = FastAPI(
    title="Ursula's Task Management System",
    description="Task management and escalation system",
    version="1.0.0"
)

# Database
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Models
class Priority(str, Enum):
    RED = "🔥 RED"
    ORANGE = "🟠 ORANGE"
    YELLOW = "🟡 YELLOW"
    GREEN = "🟢 GREEN"

class FamilyMember(BaseModel):
    id: int
    name: str
    relation: str
    status: str
    details: Optional[str]
    impact: Optional[str]
    last_referenced: Optional[datetime]

class CharacterProfile(BaseModel):
    id: int
    name: str
    role: str
    key_traits: str
    relevance_to_ursula: Optional[str]
    last_interaction: Optional[datetime]
    trust_level: float = Field(default=0.5, ge=0.0, le=1.0)

class ADHDPattern(BaseModel):
    id: int
    task_type: str
    russ_excuse: str
    ursula_response: str
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    last_used: Optional[datetime]

class EscalationTrigger(BaseModel):
    id: int
    trigger: str
    russ_response: str
    ursula_note: Optional[str]
    effectiveness_rating: float = Field(default=1.0, ge=0.0, le=1.0)
    last_used: Optional[datetime]

class FailureStory(BaseModel):
    id: int
    story_name: str
    what_happened: str
    russ_lesson: Optional[str]
    ursula_quote: str
    date_occurred: Optional[datetime]
    times_referenced: int = Field(default=0, ge=0)

class VoicePattern(BaseModel):
    name: str
    ssml: str
    use_case: str
    examples: List[str]
    tag_type: str

class Task(BaseModel):
    id: str
    content: str
    description: Optional[str]
    is_completed: bool = False
    labels: List[str] = []
    docid: Optional[str]
    due_date: Optional[str]
    comments: Optional[str]
    task_order: Optional[int]
    ursula_notes: Optional[str]
    priority_level: Optional[str]
    voice_pattern: Optional[str]

class TaskEnrichment(BaseModel):
    description: str
    due_date: Optional[str]
    status: str
    is_urgent: bool
    comments: Optional[str]
    content: str
    ursula_voice_notes: Optional[str]
    voice_pattern: Optional[str]

class AIEnrichmentResponse(BaseModel):
    content: str
    context: Dict[str, Any]
    voice_pattern: str
    references: List[str]
    relationships: List[str]
    urgency_context: Dict[str, Any]

class TodoistTask(BaseModel):
    id: str
    content: str
    description: Optional[str]
    due: Optional[Dict[str, Any]]
    priority: int
    project_id: Optional[str]
    labels: List[str] = []
    parent_id: Optional[str]

class TodoistComment(BaseModel):
    id: str
    task_id: str
    content: str
    posted_at: datetime

# Initialize database
def init_db():
    conn = sqlite3.connect('ursula.db')
    c = conn.cursor()
    
    # Read schema files
    schema_files = [
        'ursula_universe_schema.sql',
        'russ_management_schema.sql',
        'ursula-db-schema.sql'
    ]
    
    for schema_file in schema_files:
        try:
            with open(schema_file, 'r') as f:
                schema = f.read()
                c.executescript(schema)
        except Exception as e:
            print(f"Error executing {schema_file}: {e}")
    
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup():
    if not os.path.exists('ursula.db'):
        init_db()
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Core Universe Endpoints
@app.get("/universe/family", response_model=List[FamilyMember], tags=["Universe"])
async def get_family():
    """
    Get Ursula's family members and their impact on her life.
    
    Returns a list of family members, including:
    * Core blood relations
    * Found family
    * Impact on Ursula's character
    """
    query = "SELECT * FROM family"
    return await database.fetch_all(query)

@app.get("/universe/characters", response_model=List[CharacterProfile], tags=["Universe"])
async def get_characters():
    """
    Get the recurring characters in Ursula's life.
    
    Returns profiles ordered by trust level, including:
    * Role in Ursula's world
    * Trust level and history
    * Last interaction details
    """
    query = "SELECT * FROM characters"
    return await database.fetch_all(query)

@app.get("/universe/locations", tags=["Universe"])
async def get_locations():
    """
    Get Ursula's significant locations and their stories.
    
    Returns locations with:
    * Significance in her life
    * Key contacts at each place
    * Insider tips and secrets
    """
    query = "SELECT * FROM locations"
    return await database.fetch_all(query)

@app.get("/universe/rules", tags=["Universe"])
async def get_rules():
    """
    Get Ursula's personal rules for survival.
    
    Returns rules ordered by importance, including:
    * The rule itself
    * Origin story
    * Importance rating
    """
    query = "SELECT * FROM personal_rules ORDER BY importance_rating DESC"
    return await database.fetch_all(query)

@app.get("/universe/relationships", tags=["Universe"])
async def get_relationships():
    """
    Get Ursula's past relationships and their complications.
    
    Returns relationships ordered by threat level, including:
    * Current status
    * Complications
    * Threat assessment
    """
    query = "SELECT * FROM relationships ORDER BY threat_level DESC"
    return await database.fetch_all(query)

@app.get("/universe/network", tags=["Universe"])
async def get_character_network():
    """
    Get the full network of character relationships and connections.
    
    Returns:
    * Direct relationships between characters
    * Shared locations
    * Connection history
    * Trust levels
    """
    query = """
    SELECT 
        c1.name as character1,
        c2.name as character2,
        rm.relationship_type,
        rm.trust_level,
        rm.shared_history,
        rm.complications,
        l.name as shared_location,
        lcl1.frequency as character1_frequency,
        lcl2.frequency as character2_frequency
    FROM relationship_metadata rm
    JOIN characters c1 ON rm.character1_id = c1.id
    JOIN characters c2 ON rm.character2_id = c2.id
    LEFT JOIN locations_characters_link lcl1 ON c1.id = lcl1.character_id
    LEFT JOIN locations_characters_link lcl2 ON c2.id = lcl2.character_id
    LEFT JOIN locations l ON lcl1.location_id = l.id AND lcl1.location_id = lcl2.location_id
    ORDER BY rm.trust_level DESC
    """
    return await database.fetch_all(query)

# Task Management Endpoints
@app.get("/tasks/{priority}", tags=["Tasks"])
async def get_tasks(priority: Priority):
    """
    Get tasks by priority level.
    
    Parameters:
    * priority: One of 🔥 RED, 🟠 ORANGE, 🟡 YELLOW, 🟢 GREEN
    
    Returns tasks ordered by deadline.
    """
    query = "SELECT * FROM tasks WHERE priority_level = :priority ORDER BY due_date"
    return await database.fetch_all(query, {"priority": priority.value})

@app.get("/tasks/escalations/{type}", tags=["Tasks"])
async def get_escalations(type: str):
    """
    Get escalation patterns for when things go wrong.
    
    Returns escalation strategies including:
    * Trigger conditions
    * Response steps
    * Success metrics
    """
    query = "SELECT * FROM escalations WHERE type = :type"
    return await database.fetch_all(query, {"type": type})

@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
async def get_all_tasks():
    """
    Get all tasks for Ursula's roll call voicenote to Charlotte.
    
    Returns tasks ordered by priority and due date, including:
    * Task details and deadlines
    * Ursula's notes for voice recording
    * Voice patterns to use
    """
    query = """
    SELECT *, 
        CASE 
            WHEN labels LIKE '%urgent%' THEN '🔥 RED'
            WHEN due_date <= date('now', '+7 days') THEN '🟠 ORANGE'
            WHEN due_date <= date('now', '+14 days') THEN '🟡 YELLOW'
            ELSE '🟢 GREEN'
        END as priority_level,
        CASE
            WHEN labels LIKE '%urgent%' THEN 'concerned'
            WHEN labels LIKE '%Newsletter%' THEN 'formal'
            ELSE 'casual'
        END as voice_pattern
    FROM tasks 
    ORDER BY priority_level ASC, due_date ASC, task_order ASC
    """
    return await database.fetch_all(query)

@app.get("/tasks/subtasks/{task_id}", tags=["Tasks"])
async def get_task_subtasks(task_id: str):
    """
    Get subtasks for a specific task.
    
    Returns:
    * Subtask details
    * Completion status
    * Related notes
    """
    query = "SELECT * FROM tasks_subtasks WHERE parent_task_id = :task_id"
    return await database.fetch_all(query, {"task_id": task_id})

@app.put("/tasks/{task_id}/complete", tags=["Tasks"])
async def complete_task(task_id: str):
    """
    Mark a task as completed.
    
    Updates:
    * Completion status
    * Last modified timestamp
    * Triggers notification to Charlotte
    """
    query = """
    UPDATE tasks 
    SET is_completed = TRUE,
        comments = CASE 
            WHEN comments IS NULL THEN 'Completed by Ursula'
            ELSE comments || ' | Completed by Ursula'
        END
    WHERE id = :task_id
    """
    await database.execute(query, {"task_id": task_id})
    return {"message": "Task marked as completed"}

@app.put("/tasks/{task_id}/notes", tags=["Tasks"])
async def update_task_notes(task_id: str, notes: str):
    """
    Update Ursula's notes for the roll call voicenote.
    
    Updates:
    * Voice notes for Charlotte
    * Special instructions
    * Priority changes
    """
    query = """
    UPDATE tasks 
    SET ursula_notes = :notes
    WHERE id = :task_id
    """
    await database.execute(query, {"task_id": task_id, "notes": notes})
    return {"message": "Task notes updated"}

@app.post("/tasks/process", tags=["Tasks"])
async def process_tasks():
    """
    Process and enrich tasks with Ursula's voice patterns and urgency tracking.
    
    Adds:
    * Urgency tracking
    * Voice patterns for roll call
    * Ursula's notes for Charlotte
    """
    query = "SELECT * FROM tasks"
    tasks = await database.fetch_all(query)
    
    enriched_tasks = []
    for task in tasks:
        # Calculate urgency and status
        status = "No Due Date"
        is_urgent = False
        
        if task["due_date"]:
            try:
                due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
                days_until_due = (due_date - datetime.now()).days
                
                if days_until_due < -3:
                    status = "🔥 Overdue"
                    is_urgent = True
                elif days_until_due <= -1:
                    status = "⚠️ Critical"
                    is_urgent = True
                elif days_until_due == 0:
                    status = "❗ Due Today"
                    is_urgent = True
                elif days_until_due <= 3:
                    status = "⚡ Soon"
                elif days_until_due <= 7:
                    status = "📅 This Week"
                else:
                    status = "📆 Scheduled"
            except:
                status = "📋 No Valid Date"

        # Determine voice pattern
        voice_pattern = "casual"
        if is_urgent:
            voice_pattern = "urgent_reminder"
        elif "Newsletter" in (task["labels"] or ""):
            voice_pattern = "formal"
        elif days_until_due and days_until_due <= 7:
            voice_pattern = "deadline_warning"

        # Generate Ursula's notes
        notes = []
        if is_urgent:
            notes.append("Sugar, this needs immediate attention.")
        if task["description"]:
            notes.append(f"Context: {task['description'][:100]}...")
        if task["comments"]:
            notes.append(f"Note: {task['comments']}")

        enriched_task = TaskEnrichment(
            description=task["description"] or "",
            due_date=task["due_date"],
            status=status,
            is_urgent=is_urgent,
            comments=task["comments"],
            content=task["content"],
            ursula_voice_notes=" ".join(notes),
            voice_pattern=voice_pattern
        )
        enriched_tasks.append(enriched_task)

        # Update task in database
        await database.execute("""
            UPDATE tasks 
            SET ursula_notes = :notes,
                voice_pattern = :pattern,
                last_reviewed = CURRENT_TIMESTAMP
            WHERE id = :id
        """, {
            "id": task["id"],
            "notes": enriched_task.ursula_voice_notes,
            "pattern": enriched_task.voice_pattern
        })

    # Group by urgency
    urgent = [t for t in enriched_tasks if t.is_urgent]
    regular = [t for t in enriched_tasks if not t.is_urgent]

    return {
        "stats": {
            "total": len(enriched_tasks),
            "urgent": len(urgent),
            "regular": len(regular)
        },
        "urgent_tasks": urgent,
        "regular_tasks": regular
    }

@app.get("/tasks/rollcall", tags=["Tasks"])
async def get_rollcall_script():
    """
    Generate Ursula's roll call script for Charlotte.
    
    Returns:
    * Formatted script with voice patterns
    * Task summaries by priority
    * Special notes and warnings
    """
    query = """
    SELECT t.*, p.ssml 
    FROM tasks t
    LEFT JOIN patterns p ON t.voice_pattern = p.name
    ORDER BY 
        CASE 
            WHEN t.labels LIKE '%urgent%' THEN 1
            WHEN t.due_date <= date('now', '+3 days') THEN 2
            WHEN t.due_date <= date('now', '+7 days') THEN 3
            ELSE 4
        END,
        t.due_date
    """
    tasks = await database.fetch_all(query)
    
    script_sections = []
    
    # Intro
    script_sections.append({
        "pattern": "greeting",
        "text": "Hey Charlotte, here's our daily rundown."
    })
    
    # Urgent tasks
    urgent = [t for t in tasks if "urgent" in (t["labels"] or "").lower()]
    if urgent:
        script_sections.append({
            "pattern": "urgent_reminder",
            "text": f"First up, we've got {len(urgent)} urgent items that need attention."
        })
        for task in urgent:
            script_sections.append({
                "pattern": task["voice_pattern"],
                "text": task["ursula_notes"]
            })
    
    # Regular tasks
    regular = [t for t in tasks if t not in urgent]
    if regular:
        script_sections.append({
            "pattern": "routine_update",
            "text": "Now for our regular updates."
        })
        for task in regular:
            script_sections.append({
                "pattern": task["voice_pattern"],
                "text": task["ursula_notes"]
            })
    
    return {
        "sections": script_sections,
        "stats": {
            "total_tasks": len(tasks),
            "urgent_tasks": len(urgent),
            "regular_tasks": len(regular)
        }
    }

# Voice Pattern Endpoints
@app.get("/voice/patterns/{tag_type}", 
    response_model=List[VoicePattern],
    tags=["Voice"], 
    responses={
        200: {
            "description": "Successfully retrieved voice patterns",
            "content": {
                "application/json": {
                    "example": [{
                        "name": "excited",
                        "ssml": "<amazon:emotion name=\"excited\" intensity=\"high\"><prosody rate=\"+10%\" pitch=\"+20%\">$TEXT</prosody></amazon:emotion>",
                        "use_case": "Good news or urgent updates",
                        "examples": ["Hey sugar, you won't believe this!", "Drop everything, I got news!"],
                        "tag_type": "emotions"
                    }]
                }
            }
        }
    })
async def get_voice_patterns(
    tag_type: str = Path(
        ..., 
        description="Type of voice pattern to retrieve",
        example="emotions",
        enum=["emotions", "prosody", "breaks", "character"]
    )
):
    """
    Get SSML patterns for Ursula's voice.
    
    Available tag_types:
    * emotions - Happy, disappointed, excited patterns
    * prosody - Soft, loud, fast patterns
    * breaks - Pauses and timing patterns
    * character - Ursula-specific expressions
    
    Returns patterns including:
    * name: Pattern name (e.g., "excited", "whispered")
    * ssml: SSML markup pattern with $TEXT placeholder
    * use_case: When to use this pattern
    * examples: Example phrases using this pattern
    """
    query = "SELECT * FROM patterns WHERE tag_type = :tag_type"
    results = await database.fetch_all(query, {"tag_type": tag_type})
    
    # Parse examples JSON string into list
    patterns = []
    for row in results:
        pattern = dict(row)
        pattern['examples'] = json.loads(pattern['examples'])
        patterns.append(pattern)
    return patterns

# Russ Management Endpoints
@app.get("/russ/profiles", response_model=List[CharacterProfile], tags=["Russ Management"])
async def get_character_profiles():
    """
    Get profiles of Russ and his family members.
    
    Returns detailed profiles ordered by trust level, including:
    * Key traits and behaviors
    * Relevance to Ursula
    * Trust level (0.0 - 1.0)
    """
    query = "SELECT * FROM character_profiles ORDER BY trust_level DESC"
    return await database.fetch_all(query)

@app.get("/russ/patterns", response_model=List[ADHDPattern], tags=["Russ Management"])
async def get_adhd_patterns():
    """
    Get Russ's ADHD patterns and Ursula's responses.
    
    Returns patterns ordered by success rate, including:
    * Task types that cause issues
    * Russ's typical excuses
    * Ursula's proven responses
    * Success rate of each strategy
    """
    query = "SELECT * FROM adhd_patterns ORDER BY success_rate DESC"
    return await database.fetch_all(query)

@app.get("/russ/triggers", response_model=List[EscalationTrigger], tags=["Russ Management"])
async def get_escalation_triggers():
    """
    Get triggers that make Russ respond immediately.
    
    Returns triggers ordered by effectiveness, including:
    * What triggers immediate response
    * How Russ typically reacts
    * Ursula's notes on effectiveness
    * Effectiveness rating (0.0 - 1.0)
    """
    query = "SELECT * FROM escalation_triggers ORDER BY effectiveness_rating DESC"
    return await database.fetch_all(query)

@app.get("/russ/escalation/{stage}")
async def get_escalation_stage(stage: int):
    """Get details of a specific escalation stage (1-4)"""
    query = "SELECT * FROM task_escalation WHERE stage = :stage"
    return await database.fetch_one(query, {"stage": stage})

@app.get("/russ/stories", response_model=List[FailureStory], tags=["Russ Management"])
async def get_failure_stories():
    """
    Get Russ's ADHD failure stories and lessons learned.
    
    Returns stories ordered by reference frequency, including:
    * What went wrong
    * Lessons learned
    * Ursula's memorable quotes
    * How often the story is referenced
    """
    query = "SELECT * FROM failure_stories ORDER BY times_referenced DESC"
    return await database.fetch_all(query)

@app.get("/russ/family", response_model=List[dict], tags=["Russ Management"])
async def get_family_chaos():
    """
    Get details of family chaos patterns and Ursula's solutions.
    
    Returns patterns ordered by success rate, including:
    * Family member involved
    * Type of chaos
    * Description of the situation
    * Ursula's proven solution
    * Success rate of the intervention
    """
    query = "SELECT * FROM family_chaos ORDER BY success_rate DESC"
    return await database.fetch_all(query)

@app.post("/tasks/ai_enrich", response_model=AIEnrichmentResponse, tags=["Tasks"])
async def enrich_task_for_ai(task_id: str):
    """
    Provide rich context for AI agents to generate Ursula's responses.
    
    Returns:
    * Task content with metadata
    * Relevant relationships and history
    * Past interactions and stories
    * Voice pattern suggestions
    * Urgency context
    """
    # Get task details
    task = await database.fetch_one(
        "SELECT * FROM tasks WHERE id = :id",
        {"id": task_id}
    )
    
    # Get relevant relationships
    relationships = await database.fetch_all("""
        SELECT r.* 
        FROM relationships r
        WHERE r.name IN (
            SELECT DISTINCT name 
            FROM batchelor_family 
            WHERE name LIKE '%' || :search || '%'
        )
    """, {"search": task["content"]})
    
    # Get relevant stories
    stories = await database.fetch_all("""
        SELECT * FROM failure_stories 
        WHERE what_happened LIKE '%' || :search || '%'
        OR russ_lesson LIKE '%' || :search || '%'
    """, {"search": task["content"]})
    
    # Get family chaos patterns
    chaos = await database.fetch_all("""
        SELECT * FROM family_chaos
        WHERE description LIKE '%' || :search || '%'
    """, {"search": task["content"]})
    
    # Calculate urgency context
    urgency = {
        "is_urgent": "urgent" in (task["labels"] or "").lower(),
        "due_soon": False,
        "has_dependencies": False,
        "involves_family": False
    }
    
    if task["due_date"]:
        try:
            due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
            days_until_due = (due_date - datetime.now()).days
            urgency["due_soon"] = days_until_due <= 3
        except:
            pass
    
    # Check for family involvement
    for member in await database.fetch_all("SELECT name FROM batchelor_family"):
        if member["name"].lower() in task["content"].lower():
            urgency["involves_family"] = True
            break
    
    # Determine voice pattern
    voice_pattern = "casual"
    if urgency["is_urgent"]:
        voice_pattern = "urgent_reminder"
    elif urgency["involves_family"]:
        voice_pattern = "family_concerned"
    elif "Newsletter" in (task["labels"] or ""):
        voice_pattern = "formal"
    
    return AIEnrichmentResponse(
        content=task["content"],
        context={
            "description": task["description"],
            "comments": task["comments"],
            "related_stories": [dict(s) for s in stories],
            "chaos_patterns": [dict(c) for c in chaos]
        },
        voice_pattern=voice_pattern,
        references=[s["story_name"] for s in stories],
        relationships=[dict(r) for r in relationships],
        urgency_context=urgency
    )

@app.post("/tasks/ai_rollcall", tags=["Tasks"])
async def generate_ai_rollcall():
    """
    Generate enriched context for AI to create Ursula's roll call.
    
    Returns:
    * Tasks grouped by priority
    * Relevant relationships and history
    * Suggested transitions and tone shifts
    * Voice pattern recommendations
    """
    tasks = await database.fetch_all("SELECT * FROM tasks ORDER BY task_order")
    
    # Group tasks by urgency
    urgent = []
    family = []
    regular = []
    
    for task in tasks:
        enriched = await enrich_task_for_ai(task["id"])
        if enriched.urgency_context["is_urgent"]:
            urgent.append(enriched)
        elif enriched.urgency_context["involves_family"]:
            family.append(enriched)
        else:
            regular.append(enriched)
    
    return {
        "structure": {
            "intro": {
                "pattern": "greeting",
                "context": "Daily roll call to Charlotte"
            },
            "sections": [
                {
                    "type": "urgent",
                    "tasks": urgent,
                    "transition": "First up, urgent matters"
                },
                {
                    "type": "family",
                    "tasks": family,
                    "transition": "Now, family updates"
                },
                {
                    "type": "regular",
                    "tasks": regular,
                    "transition": "And our regular items"
                }
            ],
            "closing": {
                "pattern": "sign_off",
                "context": "Summary and next steps"
            }
        },
        "stats": {
            "urgent_count": len(urgent),
            "family_count": len(family),
            "regular_count": len(regular)
        }
    }

@app.post("/tasks/todoist/import/full", tags=["Task Import"])
async def import_from_todoist_with_comments():
    """
    Import tasks and comments from Todoist API directly
    """
    async with httpx.AsyncClient() as client:
        # Get tasks
        tasks_response = await client.get(
            f"{TODOIST_API_BASE}/tasks",
            headers={"Authorization": f"Bearer {TODOIST_API_TOKEN}"}
        )
        tasks = tasks_response.json()
        
        imported_count = 0
        for task in tasks:
            # Get comments for task
            comments_response = await client.get(
                f"{TODOIST_API_BASE}/comments",
                params={"task_id": task["id"]},
                headers={"Authorization": f"Bearer {TODOIST_API_TOKEN}"}
            )
            comments = comments_response.json()
            
            # Convert to our format
            todoist_task = TodoistTask(
                id=task["id"],
                content=task["content"],
                description=task.get("description", ""),
                due=task.get("due"),
                priority=task.get("priority", 1),
                project_id=task.get("project_id"),
                labels=task.get("labels", []),
                parent_id=task.get("parent_id")
            )
            
            # Store task
            db_task = {
                "id": todoist_task.id,
                "content": todoist_task.content,
                "description": todoist_task.description,
                "is_completed": False,
                "labels": json.dumps(todoist_task.labels),
                "due_date": todoist_task.due.get("date") if todoist_task.due else None,
                "priority_level": {
                    4: Priority.RED,
                    3: Priority.ORANGE,
                    2: Priority.YELLOW,
                    1: Priority.GREEN
                }.get(todoist_task.priority, Priority.GREEN),
                "task_order": todoist_task.priority * 10,
                "comments": "\n".join([c["content"] for c in comments])
            }
            
            # Insert task
            query = """
            INSERT INTO tasks (id, content, description, is_completed, labels, due_date, priority_level, task_order, comments)
            VALUES (:id, :content, :description, :is_completed, :labels, :due_date, :priority_level, :task_order, :comments)
            ON CONFLICT (id) DO UPDATE SET
                content = :content,
                description = :description,
                labels = :labels,
                due_date = :due_date,
                priority_level = :priority_level,
                task_order = :task_order,
                comments = :comments
            """
            await database.execute(query, db_task)
            
            # Enrich with Ursula's context
            enriched = await enrich_task_for_ai(todoist_task.id)
            
            # Update with enriched data
            await database.execute("""
                UPDATE tasks 
                SET ursula_notes = :notes,
                    voice_pattern = :pattern,
                    last_reviewed = CURRENT_TIMESTAMP
                WHERE id = :id
            """, {
                "id": todoist_task.id,
                "notes": enriched.context.get("description"),
                "pattern": enriched.voice_pattern
            })
            
            imported_count += 1
        
        return {
            "status": "success",
            "imported_count": imported_count,
            "last_sync": datetime.now(timezone.utc).isoformat()
        }

@app.get("/tasks/todoist/sync", tags=["Task Import"])
async def get_todoist_sync_status():
    """
    Get status of Todoist sync and last import
    """
    query = """
    SELECT 
        COUNT(*) as total_tasks,
        SUM(CASE WHEN last_reviewed IS NOT NULL THEN 1 ELSE 0 END) as enriched_tasks,
        MAX(last_reviewed) as last_sync
    FROM tasks
    """
    return await database.fetch_one(query)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ursula_api:app", host="0.0.0.0", port=8080, reload=True)
