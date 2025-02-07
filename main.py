from fastapi import FastAPI, HTTPException, BackgroundTasks
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean, DateTime, Text, select, JSON, Enum
import os, psutil, shutil
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
import enum

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://russbee:skimmer69@192.168.0.169:5432/beehive")

# FastAPI app
app = FastAPI(
    title="Beehive API",
    description="API for managing AI agents and task routing",
    version="1.0.0"
)

# Database
database = Database(DATABASE_URL)
metadata = MetaData()

# Models
class AIAgentBase(BaseModel):
    agent_name: str
    agent_type: str
    description: Optional[str] = None
    confidence_threshold: float = 0.8

class AIAgent(AIAgentBase):
    id: int
    failure_count: int = 0

class TaskRoutingBase(BaseModel):
    task_type: str
    handled_by_ursula: bool = False
    ai_agent: str
    routing_rules: Optional[str] = None

class TaskRouting(TaskRoutingBase):
    id: int

class BehaviorPatternBase(BaseModel):
    pattern_type: str
    category: str
    frequency: int = 0
    notes: Optional[str] = None

class BehaviorPattern(BehaviorPatternBase):
    id: int
    last_observed: Optional[datetime] = None

class DecisionAuthorityBase(BaseModel):
    category: str
    authority_level: str
    description: Optional[str] = None
    risk_level: int = 1
    review_required: bool = True

class DecisionAuthority(DecisionAuthorityBase):
    id: int

class EscalationTriggerBase(BaseModel):
    ai_agent: str
    trigger_condition: str
    action_required: str
    threshold: float = 0.8

class EscalationTrigger(EscalationTriggerBase):
    id: int
    last_triggered: Optional[datetime] = None

# New Enums
class TaskPriority(str, enum.Enum):
    RED = "RED"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

# New Models
class SystemHealth(BaseModel):
    status: str
    database: str
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    last_checked: datetime

class FamilyMember(BaseModel):
    id: int
    name: str
    role: str
    preferences: Dict[str, Any]
    active: bool = True

class Character(BaseModel):
    id: int
    name: str
    universe: str
    traits: List[str]
    relationships: Dict[str, str]

class Location(BaseModel):
    id: int
    name: str
    universe: str
    description: str
    coordinates: Optional[Dict[str, float]]

class Rule(BaseModel):
    id: int
    category: str
    description: str
    priority: TaskPriority
    active: bool = True

class Task(BaseModel):
    id: int
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    due_date: Optional[datetime]
    assigned_to: Optional[str]
    parent_task_id: Optional[int]
    notes: Optional[str]

class Subtask(BaseModel):
    id: int
    task_id: int
    title: str
    status: TaskStatus
    order: int

class VoicePattern(BaseModel):
    id: int
    emotion: str
    ssml_template: str
    description: str
    use_case: str

class ADHDPattern(BaseModel):
    id: int
    pattern_name: str
    triggers: List[str]
    coping_strategies: List[str]
    severity: int

class FailureStory(BaseModel):
    id: int
    title: str
    description: str
    lessons_learned: List[str]
    date_occurred: datetime
    prevention_steps: List[str]

class RawData(BaseModel):
    id: int
    source: str
    content: Dict[str, Any]
    processed: bool
    timestamp: datetime
    metadata: Optional[Dict[str, Any]]

class Webhook(BaseModel):
    id: int
    url: HttpUrl
    source: str
    active: bool
    headers: Optional[Dict[str, str]]
    retry_count: int = 0

# Database tables
ai_agents = Table(
    "ai_agents",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("agent_name", String, unique=True),
    Column("agent_type", String),
    Column("description", String),
    Column("confidence_threshold", Float),
    Column("failure_count", Integer)
)

task_routing = Table(
    "task_routing",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("task_type", String, unique=True),
    Column("handled_by_ursula", Boolean),
    Column("ai_agent", String),
    Column("routing_rules", Text)
)

behavior_patterns = Table(
    "behavior_patterns",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pattern_type", String),
    Column("category", String),
    Column("frequency", Integer),
    Column("last_observed", DateTime),
    Column("notes", Text)
)

decision_authority = Table(
    "decision_authority",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("category", String),
    Column("authority_level", String),
    Column("description", Text),
    Column("risk_level", Integer),
    Column("review_required", Boolean)
)

ai_escalation_triggers = Table(
    "ai_escalation_triggers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("ai_agent", String),
    Column("trigger_condition", Text),
    Column("action_required", Text),
    Column("threshold", Float),
    Column("last_triggered", DateTime)
)

family_members = Table(
    "family_members",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
    Column("role", String),
    Column("preferences", JSON),
    Column("active", Boolean, default=True)
)

characters = Table(
    "characters",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("universe", String),
    Column("traits", JSON),
    Column("relationships", JSON)
)

locations = Table(
    "locations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("universe", String),
    Column("description", Text),
    Column("coordinates", JSON)
)

rules = Table(
    "rules",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("category", String),
    Column("description", Text),
    Column("priority", String),
    Column("active", Boolean, default=True)
)

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", Text),
    Column("priority", String),
    Column("status", String),
    Column("due_date", DateTime),
    Column("assigned_to", String),
    Column("parent_task_id", Integer),
    Column("notes", Text)
)

subtasks = Table(
    "subtasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("task_id", Integer),
    Column("title", String),
    Column("status", String),
    Column("order", Integer)
)

voice_patterns = Table(
    "voice_patterns",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("emotion", String),
    Column("ssml_template", Text),
    Column("description", Text),
    Column("use_case", String)
)

adhd_patterns = Table(
    "adhd_patterns",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pattern_name", String),
    Column("triggers", JSON),
    Column("coping_strategies", JSON),
    Column("severity", Integer)
)

failure_stories = Table(
    "failure_stories",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", Text),
    Column("lessons_learned", JSON),
    Column("date_occurred", DateTime),
    Column("prevention_steps", JSON)
)

raw_data = Table(
    "raw_data",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("source", String),
    Column("content", JSON),
    Column("processed", Boolean, default=False),
    Column("timestamp", DateTime),
    Column("metadata", JSON)
)

webhooks = Table(
    "webhooks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("url", String),
    Column("source", String),
    Column("active", Boolean, default=True),
    Column("headers", JSON),
    Column("retry_count", Integer, default=0)
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "Welcome to Beehive API"}

@app.get("/health", response_model=SystemHealth)
async def get_system_health():
    try:
        # Check database
        await database.fetch_one("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "last_checked": datetime.utcnow()
    }

@app.get("/agents", response_model=List[AIAgent])
async def get_agents():
    query = select([ai_agents])
    return await database.fetch_all(query)

@app.get("/agents/{agent_name}", response_model=AIAgent)
async def get_agent(agent_name: str):
    query = select([ai_agents]).where(ai_agents.c.agent_name == agent_name)
    agent = await database.fetch_one(query)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.post("/agents", response_model=AIAgent)
async def create_agent(agent: AIAgentBase):
    query = ai_agents.insert().values(
        agent_name=agent.agent_name,
        agent_type=agent.agent_type,
        description=agent.description,
        confidence_threshold=agent.confidence_threshold,
        failure_count=0
    )
    try:
        agent_id = await database.execute(query)
        return {**agent.dict(), "id": agent_id, "failure_count": 0}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/agents/{agent_name}", response_model=AIAgent)
async def update_agent(agent_name: str, agent: AIAgentBase):
    query = ai_agents.update().where(ai_agents.c.agent_name == agent_name).values(
        agent_type=agent.agent_type,
        description=agent.description,
        confidence_threshold=agent.confidence_threshold
    )
    await database.execute(query)
    return await get_agent(agent_name)

@app.delete("/agents/{agent_name}")
async def delete_agent(agent_name: str):
    query = ai_agents.delete().where(ai_agents.c.agent_name == agent_name)
    await database.execute(query)
    return {"message": f"Agent {agent_name} deleted"}

@app.get("/task-routing", response_model=List[TaskRouting])
async def get_task_routes():
    query = select([task_routing])
    return await database.fetch_all(query)

@app.get("/task-routing/{task_type}", response_model=TaskRouting)
async def get_task_route(task_type: str):
    query = select([task_routing]).where(task_routing.c.task_type == task_type)
    route = await database.fetch_one(query)
    if not route:
        raise HTTPException(status_code=404, detail="Task route not found")
    return route

@app.post("/task-routing", response_model=TaskRouting)
async def create_task_route(route: TaskRoutingBase):
    query = task_routing.insert().values(**route.dict())
    try:
        route_id = await database.execute(query)
        return {**route.dict(), "id": route_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/task-routing/{task_type}", response_model=TaskRouting)
async def update_task_route(task_type: str, route: TaskRoutingBase):
    query = task_routing.update().where(task_routing.c.task_type == task_type).values(**route.dict())
    await database.execute(query)
    return await get_task_route(task_type)

@app.delete("/task-routing/{task_type}")
async def delete_task_route(task_type: str):
    query = task_routing.delete().where(task_routing.c.task_type == task_type)
    await database.execute(query)
    return {"message": f"Task route {task_type} deleted"}

@app.get("/behavior-patterns", response_model=List[BehaviorPattern])
async def get_behavior_patterns():
    query = select([behavior_patterns])
    return await database.fetch_all(query)

@app.get("/behavior-patterns/{pattern_type}", response_model=BehaviorPattern)
async def get_behavior_pattern(pattern_type: str):
    query = select([behavior_patterns]).where(behavior_patterns.c.pattern_type == pattern_type)
    pattern = await database.fetch_one(query)
    if not pattern:
        raise HTTPException(status_code=404, detail="Behavior pattern not found")
    return pattern

@app.post("/behavior-patterns", response_model=BehaviorPattern)
async def create_behavior_pattern(pattern: BehaviorPatternBase):
    query = behavior_patterns.insert().values(**pattern.dict(), last_observed=datetime.utcnow())
    try:
        pattern_id = await database.execute(query)
        return {**pattern.dict(), "id": pattern_id, "last_observed": datetime.utcnow()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/behavior-patterns/{pattern_type}", response_model=BehaviorPattern)
async def update_behavior_pattern(pattern_type: str, pattern: BehaviorPatternBase):
    query = behavior_patterns.update().where(behavior_patterns.c.pattern_type == pattern_type).values(
        **pattern.dict(),
        last_observed=datetime.utcnow()
    )
    await database.execute(query)
    return await get_behavior_pattern(pattern_type)

@app.delete("/behavior-patterns/{pattern_type}")
async def delete_behavior_pattern(pattern_type: str):
    query = behavior_patterns.delete().where(behavior_patterns.c.pattern_type == pattern_type)
    await database.execute(query)
    return {"message": f"Behavior pattern {pattern_type} deleted"}

@app.get("/decision-authority", response_model=List[DecisionAuthority])
async def get_decision_authorities():
    query = select([decision_authority])
    return await database.fetch_all(query)

@app.get("/decision-authority/{category}", response_model=DecisionAuthority)
async def get_decision_authority(category: str):
    query = select([decision_authority]).where(decision_authority.c.category == category)
    authority = await database.fetch_one(query)
    if not authority:
        raise HTTPException(status_code=404, detail="Decision authority not found")
    return authority

@app.post("/decision-authority", response_model=DecisionAuthority)
async def create_decision_authority(authority: DecisionAuthorityBase):
    query = decision_authority.insert().values(**authority.dict())
    try:
        authority_id = await database.execute(query)
        return {**authority.dict(), "id": authority_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/decision-authority/{category}", response_model=DecisionAuthority)
async def update_decision_authority(category: str, authority: DecisionAuthorityBase):
    query = decision_authority.update().where(decision_authority.c.category == category).values(**authority.dict())
    await database.execute(query)
    return await get_decision_authority(category)

@app.delete("/decision-authority/{category}")
async def delete_decision_authority(category: str):
    query = decision_authority.delete().where(decision_authority.c.category == category)
    await database.execute(query)
    return {"message": f"Decision authority {category} deleted"}

@app.get("/escalation-triggers", response_model=List[EscalationTrigger])
async def get_escalation_triggers():
    query = select([ai_escalation_triggers])
    return await database.fetch_all(query)

@app.get("/escalation-triggers/{ai_agent}", response_model=List[EscalationTrigger])
async def get_agent_escalation_triggers(ai_agent: str):
    query = select([ai_escalation_triggers]).where(ai_escalation_triggers.c.ai_agent == ai_agent)
    triggers = await database.fetch_all(query)
    if not triggers:
        raise HTTPException(status_code=404, detail="No escalation triggers found for agent")
    return triggers

@app.post("/escalation-triggers", response_model=EscalationTrigger)
async def create_escalation_trigger(trigger: EscalationTriggerBase):
    query = ai_escalation_triggers.insert().values(**trigger.dict())
    try:
        trigger_id = await database.execute(query)
        return {**trigger.dict(), "id": trigger_id, "last_triggered": None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/escalation-triggers/{trigger_id}", response_model=EscalationTrigger)
async def update_escalation_trigger(trigger_id: int, trigger: EscalationTriggerBase):
    query = ai_escalation_triggers.update().where(ai_escalation_triggers.c.id == trigger_id).values(**trigger.dict())
    await database.execute(query)
    updated = await database.fetch_one(
        select([ai_escalation_triggers]).where(ai_escalation_triggers.c.id == trigger_id)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Escalation trigger not found")
    return updated

@app.delete("/escalation-triggers/{trigger_id}")
async def delete_escalation_trigger(trigger_id: int):
    query = ai_escalation_triggers.delete().where(ai_escalation_triggers.c.id == trigger_id)
    await database.execute(query)
    return {"message": f"Escalation trigger {trigger_id} deleted"}

@app.get("/family", response_model=List[FamilyMember])
async def get_family_members():
    query = select([family_members])
    result = await database.fetch_all(query)
    if not result:
        return []
    return result

@app.post("/family", response_model=FamilyMember)
async def create_family_member(member: FamilyMember):
    query = family_members.insert().values(**member.dict())
    member_id = await database.execute(query)
    return {**member.dict(), "id": member_id}

@app.get("/characters", response_model=List[Character])
async def get_characters():
    query = select([characters])
    return await database.fetch_all(query)

@app.post("/characters", response_model=Character)
async def create_character(character: Character):
    query = characters.insert().values(**character.dict())
    char_id = await database.execute(query)
    return {**character.dict(), "id": char_id}

@app.get("/locations", response_model=List[Location])
async def get_locations():
    query = select([locations])
    return await database.fetch_all(query)

@app.post("/locations", response_model=Location)
async def create_location(location: Location):
    query = locations.insert().values(**location.dict())
    loc_id = await database.execute(query)
    return {**location.dict(), "id": loc_id}

@app.get("/tasks", response_model=List[Task])
async def get_tasks(priority: Optional[TaskPriority] = None):
    query = select([tasks])
    if priority:
        query = query.where(tasks.c.priority == priority)
    return await database.fetch_all(query)

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    query = tasks.insert().values(**task.dict())
    task_id = await database.execute(query)
    return {**task.dict(), "id": task_id}

@app.get("/tasks/{task_id}/subtasks", response_model=List[Subtask])
async def get_subtasks(task_id: int):
    query = select([subtasks]).where(subtasks.c.task_id == task_id)
    return await database.fetch_all(query)

@app.get("/voice/patterns/{emotion}", response_model=List[VoicePattern])
async def get_voice_patterns(emotion: str):
    query = select([voice_patterns]).where(voice_patterns.c.emotion == emotion)
    return await database.fetch_all(query)

@app.get("/adhd/patterns", response_model=List[ADHDPattern])
async def get_adhd_patterns():
    query = select([adhd_patterns])
    return await database.fetch_all(query)

@app.get("/failure-stories", response_model=List[FailureStory])
async def get_failure_stories():
    query = select([failure_stories])
    return await database.fetch_all(query)

@app.post("/data/raw", response_model=RawData)
async def ingest_raw_data(data: RawData, background_tasks: BackgroundTasks):
    query = raw_data.insert().values(**data.dict())
    data_id = await database.execute(query)
    background_tasks.add_task(process_raw_data, data_id)
    return {**data.dict(), "id": data_id}

@app.get("/data/queue", response_model=List[RawData])
async def get_pending_data():
    query = select([raw_data]).where(raw_data.c.processed == False)
    return await database.fetch_all(query)

@app.post("/webhooks", response_model=Webhook)
async def register_webhook(webhook: Webhook):
    query = webhooks.insert().values(**webhook.dict())
    webhook_id = await database.execute(query)
    return {**webhook.dict(), "id": webhook_id}

@app.get("/webhooks", response_model=List[Webhook])
async def get_webhooks(source: Optional[str] = None):
    query = select([webhooks])
    if source:
        query = query.where(webhooks.c.source == source)
    return await database.fetch_all(query)

async def process_raw_data(data_id: int):
    # Background task to process raw data
    # Implementation details would go here
    pass 