from fastapi import FastAPI, HTTPException, Path, Header, Request, Body, Response
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
import databases
import sqlalchemy
from datetime import datetime, timezone
import psycopg2
import os
from fastapi import Path
import json
import httpx
import uvicorn
import logging
import structlog
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_client import Counter, Histogram, CollectorRegistry
from contextlib import asynccontextmanager
import time
from fastapi.responses import JSONResponse

# Constants
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN", "e0617c43571f8e13254c5b49c1e561715380461d")
TODOIST_API_BASE = "https://api.todoist.com/rest/v2"
DATABASE_URL = "postgresql://russbee:skimmer69@192.168.0.169:5432/beehive"

# Metrics
METRICS_REGISTRY = CollectorRegistry()
REQUEST_COUNT = Counter('ursula_http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'], registry=METRICS_REGISTRY)
REQUEST_LATENCY = Histogram('ursula_http_request_duration_seconds', 'HTTP request duration in seconds', ['method', 'endpoint'], registry=METRICS_REGISTRY)

# Structured logging setup
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

# Sentry setup (if SENTRY_DSN is provided)
if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
        environment=os.getenv("ENVIRONMENT", "production")
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Ursula's Task Management System...")
    if not os.path.exists('ursula.db'):
        init_db()
    await database.connect()
    logger.info("Database initialized!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await database.disconnect()

# FastAPI app
app = FastAPI(
    title="Ursula's Task Management System",
    description="Production API for Ursula's task management and AI delegation system",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["192.168.0.63", "localhost", "127.0.0.1"]
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    method = request.method
    path = request.url.path
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        duration = time.time() - start_time
        
        # Update metrics
        REQUEST_COUNT.labels(method=method, endpoint=path, status=status_code).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=path).observe(duration)
        
        # Structured logging
        logger.info(
            "request_processed",
            method=method,
            path=path,
            status_code=status_code,
            duration=duration
        )
        
        return response
    except Exception as e:
        logger.error(
            "request_failed",
            method=method,
            path=path,
            error=str(e),
            duration=time.time() - start_time
        )
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        await check_db_connection()
        memory = get_memory_usage()
        disk = get_disk_space()
        return {
            "status": "healthy",
            "database": "connected",
            "memory": memory,
            "disk": disk,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/metrics")
async def metrics():
    from prometheus_client import generate_latest
    return Response(
        content=generate_latest(METRICS_REGISTRY),
        media_type="text/plain"
    )

# Database
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Models
class Priority(str, Enum):
    RED = "RED"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

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

# Raw Data Ingestion Models
class RawDataIngestion(BaseModel):
    source: str  # email, document, chat, note, etc.
    content: Dict[str, Any]  # flexible JSON content
    metadata: Optional[Dict[str, Any]]
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    context: Optional[str]
    priority: Optional[str]

# Webhook Models
class WebhookPayload(BaseModel):
    event_type: str  # email, todoist, calendar, etc.
    data: Dict[str, Any]  # raw webhook data
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    signature: Optional[str]  # webhook signature for verification

# Initialize database
def init_db():
    try:
        # Initialize database with retries
        for attempt in range(3):
            try:
                conn = psycopg2.connect('postgresql://russbee:skimmer69@192.168.0.169:5432/beehive')
                c = conn.cursor()
                
                # Read and execute schema
                with open('combined_schema.sql', 'r') as f:
                    schema = f.read()
                c.executescript(schema)
                
                # Initialize task roll call with sample data
                c.execute('''
                    INSERT INTO task_roll_call (
                        id, description, category, due_date, last_mentioned,
                        urgency, suggested_actions, ai_observations, days_overdue,
                        agent_assigned, status, pattern_score, avoidance_history,
                        impact_rating, external_pressure_score
                    ) VALUES (
                        'TASK101', 'Fix the Car', 'Vehicle', CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP, 'RED', 'Call Sal, schedule pickup',
                        'Russ avoided twice, pattern detected', 5, 'Logistics_AI',
                        'pending', 0.8, '["Ignored first call", "Claimed too busy"]',
                        8, 0.7
                    )
                ''')
                
                # Initialize daily roll call
                c.execute('''
                    INSERT INTO daily_roll_call (
                        report_date, urgent_tasks, high_priority, low_priority,
                        ursula_notes, completion_rate
                    ) VALUES (
                        DATE('now'),
                        '["TASK101", "TASK102"]',
                        '["TASK103"]',
                        '["TASK104", "TASK105"]',
                        'Charlotte, sugar, these need handling TODAY.',
                        0.7
                    )
                ''')
                
                conn.commit()
                conn.close()
                logger.info("Database initialized successfully")
                break
            except Exception as e:
                logger.error(f"Database initialization attempt {attempt + 1} failed", error=str(e))
                if attempt == 2:
                    raise
                time.sleep(1)
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        raise

async def check_db_connection():
    try:
        conn = psycopg2.connect('postgresql://russbee:skimmer69@192.168.0.169:5432/beehive')
        c = conn.cursor()
        c.execute("SELECT 1")
        conn.close()
        return True
    except Exception as e:
        logger.error("Database connection check failed", error=str(e))
        return False

def get_memory_usage():
    import psutil
    return psutil.virtual_memory().percent

def get_disk_space():
    import psutil
    return psutil.disk_usage('/').free / (1024 * 1024 * 1024)  # Convert to GB

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
    * priority: One of RED, ORANGE, YELLOW, GREEN
    
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
    Get all tasks ordered by priority and due date
    """
    try:
        query = """
        SELECT 
            id,
            content,
            description,
            is_completed,
            labels,
            docid,
            due_date,
            comments,
            task_order,
            ursula_notes,
            voice_pattern,
            last_reviewed,
            charlotte_notified,
            priority_level
        FROM tasks 
        ORDER BY 
            CASE priority_level 
                WHEN 'RED' THEN 1 
                WHEN 'ORANGE' THEN 2 
                WHEN 'YELLOW' THEN 3 
                WHEN 'GREEN' THEN 4 
                ELSE 5 
            END,
            due_date
        """
        tasks = await database.fetch_all(query)
        return [
            Task(
                id=str(task['id']),
                content=task['content'],
                description=task['description'],
                is_completed=bool(task['is_completed']),
                labels=json.loads(task['labels']) if task['labels'] else [],
                docid=task['docid'],
                due_date=task['due_date'],
                comments=task['comments'],
                task_order=task['task_order'],
                ursula_notes=task['ursula_notes'],
                voice_pattern=task['voice_pattern'],
                priority_level=task['priority_level']
            )
            for task in tasks
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
async def update_task_notes(task_id: str, notes: str = Body(..., embed=True)):
    """
    Update Ursula's notes for the roll call voicenote.
    
    Updates:
    * Voice notes for Charlotte
    * Special instructions
    * Priority changes
    """
    query = """
    UPDATE tasks 
    SET ursula_notes = :notes,
        last_reviewed = CURRENT_TIMESTAMP
    WHERE id = :task_id
    RETURNING id
    """
    result = await database.execute(query, {"task_id": task_id, "notes": notes})
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
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
                    status = "RED Overdue"
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
                    "examples": {
                        "excited": {
                            "value": {
                                "name": "excited",
                                "ssml": "<amazon:emotion name=\"excited\" intensity=\"high\"><prosody rate=\"+10%\" pitch=\"+20%\">$TEXT</prosody></amazon:emotion>",
                                "use_case": "Good news or urgent updates",
                                "examples": ["Hey sugar, you won't believe this!", "Drop everything, I got news!"],
                                "tag_type": "emotions"
                            }
                        }
                    }
                }
            }
        }
    })
async def get_voice_patterns(
    tag_type: str = Path(
        ..., 
        description="Type of voice pattern to retrieve",
        examples=["emotions", "prosody", "breaks", "character"]
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
    try:
        async with httpx.AsyncClient() as client:
            # Get tasks
            tasks_response = await client.get(
                f"{TODOIST_API_BASE}/tasks",
                headers={"Authorization": f"Bearer {TODOIST_API_TOKEN}"}
            )
            if tasks_response.status_code != 200:
                raise HTTPException(status_code=tasks_response.status_code, detail="Failed to fetch tasks from Todoist")
            
            tasks = tasks_response.json()
            
            imported_count = 0
            for task in tasks:
                try:
                    # Get comments for task
                    comments_response = await client.get(
                        f"{TODOIST_API_BASE}/comments",
                        params={"task_id": task["id"]},
                        headers={"Authorization": f"Bearer {TODOIST_API_TOKEN}"}
                    )
                    comments = comments_response.json() if comments_response.status_code == 200 else []
                    
                    # Convert to our format
                    priority_map = {
                        4: Priority.RED.value,
                        3: Priority.ORANGE.value,
                        2: Priority.YELLOW.value,
                        1: Priority.GREEN.value
                    }
                    
                    db_task = {
                        "id": str(task["id"]),
                        "content": task["content"],
                        "description": task.get("description", ""),
                        "is_completed": False,
                        "labels": json.dumps(task.get("labels", [])),
                        "docid": task.get("project_id"),
                        "due_date": task.get("due", {}).get("date"),
                        "comments": "\n".join([c["content"] for c in comments]),
                        "task_order": task.get("order", 1),
                        "priority_level": priority_map.get(task.get("priority", 1), Priority.GREEN.value)
                    }
                    
                    # Insert task
                    query = """
                    INSERT INTO tasks 
                    (id, content, description, is_completed, labels, docid, due_date, comments, task_order, priority_level)
                    VALUES (:id, :content, :description, :is_completed, :labels, :docid, :due_date, :comments, :task_order, :priority_level)
                    ON CONFLICT (id) DO UPDATE SET
                        content = :content,
                        description = :description,
                        labels = :labels,
                        docid = :docid,
                        due_date = :due_date,
                        comments = :comments,
                        task_order = :task_order,
                        priority_level = :priority_level
                    """
                    await database.execute(query, db_task)
                    imported_count += 1
                except Exception as task_error:
                    print(f"Error importing task {task.get('id')}: {str(task_error)}")
                    continue
            
            return {
                "status": "success",
                "imported_count": imported_count,
                "last_sync": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

@app.post("/ingest/raw", tags=["Data Ingestion"])
async def ingest_raw_data(data: RawDataIngestion):
    """
    Ingest raw data into the system for AI processing.
    Data will be stored in raw form and processed asynchronously.
    """
    try:
        query = """
        INSERT INTO raw_data 
        (source, content, metadata, timestamp, context, priority)
        VALUES (:source, :content, :metadata, :timestamp, :context, :priority)
        RETURNING id
        """
        
        values = {
            "source": data.source,
            "content": json.dumps(data.content),
            "metadata": json.dumps(data.metadata) if data.metadata else None,
            "timestamp": data.timestamp,
            "context": data.context,
            "priority": data.priority
        }
        
        result = await database.execute(query, values)
        
        # Trigger async processing if needed
        if data.priority == "urgent":
            await process_urgent_data(result)
        
        return {
            "status": "success",
            "message": "Data ingested successfully",
            "id": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ingest/status/{ingest_id}", tags=["Data Ingestion"])
async def get_ingestion_status(ingest_id: int):
    """
    Check the status of ingested data processing
    """
    query = """
    SELECT 
        id,
        source,
        timestamp,
        context,
        priority,
        processed,
        processing_status,
        last_processed
    FROM raw_data 
    WHERE id = :id
    """
    result = await database.fetch_one(query, {"id": ingest_id})
    if not result:
        raise HTTPException(status_code=404, detail="Ingestion record not found")
    return result

@app.get("/ingest/pending", tags=["Data Ingestion"])
async def get_pending_ingestions(
    source: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = 10
):
    """
    Get pending data ingestions for processing
    """
    query = """
    SELECT 
        id,
        source,
        timestamp,
        context,
        priority
    FROM raw_data 
    WHERE processed = FALSE
    """
    if source:
        query += " AND source = :source"
    if priority:
        query += " AND priority = :priority"
    query += " ORDER BY timestamp DESC LIMIT :limit"
    
    params = {"source": source, "priority": priority, "limit": limit}
    return await database.fetch_all(query, params)

async def process_urgent_data(ingest_id: int):
    """
    Process urgent data immediately
    """
    query = """
    SELECT * FROM raw_data WHERE id = :id
    """
    data = await database.fetch_one(query, {"id": ingest_id})
    if not data:
        return
    
    content = json.loads(data["content"])
    
    # Check for tasks
    if "tasks" in content:
        for task in content["tasks"]:
            task_query = """
            INSERT INTO tasks 
            (content, description, priority_level, due_date)
            VALUES (:content, :description, :priority_level, :due_date)
            """
            await database.execute(task_query, {
                "content": task.get("content"),
                "description": task.get("description"),
                "priority_level": "RED" if task.get("urgent") else "YELLOW",
                "due_date": task.get("due_date")
            })
    
    # Update processing status
    update_query = """
    UPDATE raw_data 
    SET processed = TRUE,
        processing_status = 'completed',
        last_processed = CURRENT_TIMESTAMP
    WHERE id = :id
    """
    await database.execute(update_query, {"id": ingest_id})

@app.post("/webhook/{source}", tags=["Webhooks"])
async def handle_webhook(
    source: str,
    payload: WebhookPayload,
    x_signature: Optional[str] = Header(None)
):
    """
    Handle incoming webhooks from various sources.
    Supports: Todoist, Email, Calendar, etc.
    """
    try:
        # Verify webhook signature if provided
        if x_signature and not verify_webhook_signature(source, x_signature, payload):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
        
        # Store raw webhook data
        query = """
        INSERT INTO raw_data 
        (source, content, metadata, timestamp, context, priority)
        VALUES (:source, :content, :metadata, :timestamp, :context, :priority)
        RETURNING id
        """
        
        # Extract priority and context based on source and event type
        priority = determine_priority(source, payload.event_type, payload.data)
        context = determine_context(source, payload.event_type)
        
        values = {
            "source": source,
            "content": json.dumps(payload.data),
            "metadata": json.dumps({
                "event_type": payload.event_type,
                "signature": payload.signature
            }),
            "timestamp": payload.timestamp,
            "context": context,
            "priority": priority
        }
        
        ingest_id = await database.execute(query, values)
        
        # Process urgent webhooks immediately
        if priority == "urgent":
            await process_urgent_data(ingest_id)
        
        return {
            "status": "success",
            "message": f"Webhook from {source} processed",
            "id": ingest_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def verify_webhook_signature(source: str, signature: str, payload: WebhookPayload) -> bool:
    """Verify webhook signature based on source"""
    # Add signature verification logic per source
    if source == "todoist":
        # Todoist signature verification
        return True
    return True  # Default to True for now

def determine_priority(source: str, event_type: str, data: Dict[str, Any]) -> str:
    """Determine priority based on source and event data"""
    if source == "todoist":
        if "due" in data and data.get("priority", 1) >= 3:
            return "urgent"
    elif source == "email" and "urgent" in data.get("subject", "").lower():
        return "urgent"
    return "normal"

def determine_context(source: str, event_type: str) -> str:
    """Determine context based on source and event type"""
    contexts = {
        "todoist": "task_management",
        "email": "communication",
        "calendar": "scheduling"
    }
    return contexts.get(source, "general")

@app.get("/webhook/config/{source}", tags=["Webhooks"])
async def get_webhook_config(source: str):
    """
    Get webhook configuration for a specific source
    """
    configs = {
        "todoist": {
            "url": f"http://192.168.0.63:8080/webhook/todoist",
            "headers": {
                "Content-Type": "application/json",
                "X-Signature": "YOUR_SIGNATURE"
            },
            "events": ["item:added", "item:completed", "item:updated"],
            "example": {
                "event_type": "item:added",
                "data": {
                    "content": "New task",
                    "priority": 4
                }
            }
        },
        "email": {
            "url": f"http://192.168.0.63:8080/webhook/email",
            "headers": {
                "Content-Type": "application/json"
            },
            "example": {
                "event_type": "new_email",
                "data": {
                    "subject": "Urgent: Medical Appointment",
                    "body": "Reminder for tomorrow"
                }
            }
        }
    }
    
    if source not in configs:
        raise HTTPException(status_code=404, detail=f"No config for source: {source}")
    
    return configs[source]

@app.get("/tasks/roll_call/daily", response_model=List[Dict], tags=["Task Roll Call"])
async def get_daily_roll_call():
    """
    Get today's task roll call report
    """
    query = """
        SELECT * FROM daily_roll_call 
        WHERE DATE(report_date) = DATE('now')
        ORDER BY generated_timestamp DESC 
        LIMIT 1
    """
    return await database.fetch_all(query)

@app.get("/tasks/roll_call/urgent", response_model=List[Dict], tags=["Task Roll Call"])
async def get_urgent_tasks():
    """
    Get all urgent (RED) tasks
    """
    query = """
        SELECT * FROM task_roll_call 
        WHERE urgency = 'RED' 
        AND status != 'completed'
        ORDER BY days_overdue DESC
    """
    return await database.fetch_all(query)

@app.get("/tasks/roll_call/high", response_model=List[Dict], tags=["Task Roll Call"])
async def get_high_priority_tasks():
    """
    Get all high priority (ORANGE) tasks
    """
    query = """
        SELECT * FROM task_roll_call 
        WHERE urgency = 'ORANGE' 
        AND status != 'completed'
        ORDER BY days_overdue DESC
    """
    return await database.fetch_all(query)

@app.get("/tasks/roll_call/patterns/{category}", response_model=List[Dict], tags=["Task Roll Call"])
async def get_behavior_patterns(category: str):
    """
    Get behavior patterns for a specific category
    """
    query = """
        SELECT * FROM behavior_patterns 
        WHERE category = :category
        ORDER BY frequency DESC
    """
    return await database.fetch_all(query, {"category": category})

@app.post("/tasks/roll_call/ingest", response_model=Dict, tags=["Task Roll Call"])
async def ingest_new_task(task: Dict = Body(...)):
    """
    Ingest a new task into the system
    """
    query = """
        INSERT INTO data_ingest_queue (
            source_type, content, metadata, priority, 
            processing_agent, processing_status
        ) VALUES (
            :source_type, :content, :metadata, :priority,
            :processing_agent, 'pending'
        ) RETURNING id
    """
    return await database.fetch_one(query, task)

@app.put("/tasks/roll_call/{task_id}/status", response_model=Dict, tags=["Task Roll Call"])
async def update_task_status(
    task_id: str,
    status: str = Body(..., embed=True),
    notes: Optional[str] = Body(None, embed=True)
):
    """
    Update task status and add notes
    """
    query = """
        UPDATE task_roll_call 
        SET status = :status,
        last_updated = CURRENT_TIMESTAMP,
        ai_observations = CASE 
            WHEN ai_observations IS NULL THEN :notes
            ELSE ai_observations || ' | ' || :notes
        END
        WHERE id = :task_id
        RETURNING *
    """
    return await database.fetch_one(query, {
        "task_id": task_id,
        "status": status,
        "notes": notes
    })

@app.get("/tasks/roll_call/analytics/{task_id}", response_model=Dict, tags=["Task Roll Call"])
async def get_task_analytics(task_id: str):
    """
    Get analytics for a specific task
    """
    query = """
        SELECT * FROM task_analytics 
        WHERE task_id = :task_id
    """
    return await database.fetch_one(query, {"task_id": task_id})

if __name__ == "__main__":
    # Initialize database
    if not os.path.exists('ursula.db'):
        init_db()
    
    # Start server
    print("Starting Ursula's Task Management System...")
    print("Starting server at http://0.0.0.0:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
