from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Union, Any
import uvicorn
from ursula_db_api import UrsulaDB
from datetime import datetime
import json
import databases
import sqlalchemy
from sqlalchemy import create_engine

# Database setup
DATABASE_URL = "sqlite:///./ursula.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Create tables
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI(
    title="Ursula API",
    description="API for Ursula's voice, memory, and personality",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

db = UrsulaDB()

# Request Models
class SSMLRequest(BaseModel):
    text: str
    pattern_type: str
    pattern_name: str

class SlangRequest(BaseModel):
    term: str

class SceneRequest(BaseModel):
    template_name: str
    content: Dict[str, str]

class MemoryRequest(BaseModel):
    category: str
    content: Dict[str, Any]
    context: str

# Additional Request Models
class PatternUpdateRequest(BaseModel):
    pattern_id: int
    success_rating: float

class StoryUpdateRequest(BaseModel):
    story_id: int
    times_told: int
    success_rating: Optional[float] = None

class RelationshipUpdateRequest(BaseModel):
    person_name: str
    interaction_type: str
    success_rating: float
    notes: Optional[str] = None

class PatternResponseRequest(BaseModel):
    pattern_id: int
    response_type: str

# API Routes
@app.get("/api/ursula/memory/relationships/{person_name}")
async def get_relationship(person_name: str):
    """Get relationship data for a person"""
    relationship = db.get_relationship(person_name)
    if not relationship:
        raise HTTPException(status_code=404, detail=f"No relationship found with: {person_name}")
    return relationship

@app.get("/api/ursula/memory/stories/{category}")
async def get_stories(category: str, mood: Optional[str] = None):
    """Get stories by category and optional mood"""
    stories = db.get_stories(category, mood)
    if not stories:
        raise HTTPException(status_code=404, detail=f"No stories found for category: {category}")
    return stories

@app.get("/api/ursula/patterns/{pattern_type}")
async def get_patterns(pattern_type: str):
    """Get voice patterns by type"""
    patterns = db.get_patterns_by_type(pattern_type)
    if not patterns:
        raise HTTPException(status_code=404, detail=f"No patterns found for type: {pattern_type}")
    return patterns

@app.post("/api/ursula/memory/store")
async def store_memory(request: MemoryRequest):
    """Store a new memory"""
    success = db.store_memory(request.category, request.content, request.context)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to store memory")
    return {"status": "success"}

@app.post("/api/ursula/ssml/build")
async def build_ssml(request: SSMLRequest):
    """Build SSML markup for text"""
    ssml = db.build_ssml(request.text, request.pattern_type, request.pattern_name)
    if not ssml:
        raise HTTPException(status_code=404, detail="Could not build SSML with given parameters")
    return {"ssml": ssml}

@app.post("/api/ursula/slang/build")
async def build_slang_ssml(request: SlangRequest):
    """Build SSML markup for slang term"""
    ssml = db.build_slang_ssml(request.term)
    if not ssml:
        raise HTTPException(status_code=404, detail=f"Could not build SSML for slang term: {request.term}")
    return {"ssml": ssml}

@app.post("/api/ursula/scene/build")
async def build_scene(request: SceneRequest):
    """Build a complete scene"""
    scene = db.build_scene(request.template_name, request.content)
    if not scene:
        raise HTTPException(status_code=404, detail=f"Could not build scene with template: {request.template_name}")
    return {"ssml": scene}

@app.get("/api/ursula/character/traits/{trait_type}")
async def get_character_traits(trait_type: Optional[str] = None):
    """Get character traits"""
    traits = db.get_character_trait(trait_type)
    if not traits:
        raise HTTPException(status_code=404, detail=f"No traits found for type: {trait_type}")
    return traits

@app.get("/api/ursula/phrases/{phrase_type}")
async def get_required_phrases(phrase_type: str):
    """Get required phrases of a specific type"""
    phrases = db.get_required_phrase(phrase_type)
    if not phrases:
        raise HTTPException(status_code=404, detail=f"No phrases found for type: {phrase_type}")
    return phrases

# Additional API Routes
@app.get("/api/ursula/memory/recent/{category}")
async def get_recent_memories(category: str, limit: int = 5):
    """Get recent memories by category"""
    memories = db.get_recent_memories(category, limit)
    if not memories:
        raise HTTPException(status_code=404, detail=f"No recent memories found for category: {category}")
    return memories

@app.get("/api/ursula/patterns/successful/{pattern_type}")
async def get_successful_patterns(pattern_type: str, min_success_rate: float = 0.7):
    """Get patterns with success rate above threshold"""
    patterns = db.get_successful_patterns(pattern_type, min_success_rate)
    if not patterns:
        raise HTTPException(status_code=404, detail=f"No successful patterns found for type: {pattern_type}")
    return patterns

@app.post("/api/ursula/patterns/update")
async def update_pattern_success(request: PatternUpdateRequest):
    """Update pattern success rating"""
    success = db.update_pattern_success(request.pattern_id, request.success_rating)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update pattern")
    return {"status": "success"}

@app.post("/api/ursula/stories/update")
async def update_story_stats(request: StoryUpdateRequest):
    """Update story usage statistics"""
    success = db.update_story_stats(request.story_id, request.times_told, request.success_rating)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update story stats")
    return {"status": "success"}

@app.post("/api/ursula/relationships/update")
async def update_relationship(request: RelationshipUpdateRequest):
    """Update relationship interaction history"""
    success = db.update_relationship_interaction(
        request.person_name,
        request.interaction_type,
        request.success_rating,
        request.notes
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update relationship")
    return {"status": "success"}

@app.get("/api/ursula/stories/favorite")
async def get_favorite_stories(min_success_rate: float = 0.8, limit: int = 5):
    """Get most successful stories"""
    stories = db.get_favorite_stories(min_success_rate, limit)
    if not stories:
        raise HTTPException(status_code=404, detail="No favorite stories found")
    return stories

@app.get("/api/ursula/memory/interactions/{person_name}")
async def get_interaction_history(person_name: str, limit: int = 10):
    """Get recent interactions with a person"""
    history = db.get_interaction_history(person_name, limit)
    if not history:
        raise HTTPException(status_code=404, detail=f"No interaction history found for: {person_name}")
    return history

@app.get("/api/ursula/stats/patterns")
async def get_pattern_stats(min_success_rate: float = 0.0):
    """Get pattern usage statistics"""
    stats = db.get_pattern_stats(min_success_rate)
    if not stats:
        raise HTTPException(status_code=404, detail="No pattern statistics found")
    return stats

@app.post("/api/ursula/patterns/response")
async def track_pattern_response(request: PatternResponseRequest):
    """Track response to a pattern"""
    if request.response_type not in ['positive', 'negative', 'neutral']:
        raise HTTPException(status_code=400, detail="Invalid response type")
    success = db.track_pattern_response(request.pattern_id, request.response_type)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to track pattern response")
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("ursula_api:app", host="0.0.0.0", port=8080, reload=True) 